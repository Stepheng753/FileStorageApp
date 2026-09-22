/**
 * Tooth Manager - API Client & Session Manager
 */

const API_BASE = (function () {
	if (window.location.origin.includes('toothmanager.com')) {
		return 'https://dev.toothmanager.com/api';
	}
	// Fallback to local dev API
	return 'http://localhost:3001/api';
})();

const STATIC_BASE = (function () {
	if (window.location.origin.includes('toothmanager.com')) {
		return 'https://dev.toothmanager.com/static';
	}
	return 'http://localhost:3001/static';
})();


const api = {
	// --- Session Management ---
	setSession(token, user) {
		localStorage.setItem('tm_token', token);
		localStorage.setItem('tm_user', JSON.stringify(user));
	},

	clearSession() {
		localStorage.removeItem('tm_token');
		localStorage.removeItem('tm_user');
	},

	getToken() {
		return localStorage.getItem('tm_token');
	},

	getUser() {
		try {
			const u = localStorage.getItem('tm_user');
			return u ? JSON.parse(u) : null;
		} catch (e) {
			return null;
		}
	},

	getTier() {
		const u = this.getUser();
		return u ? parseInt(u.permission_tier || 3) : 3;
	},

	isAuthenticated() {
		return !!this.getToken();
	},

	requireAuth(allowedTiers = [1, 2]) {
		if (!this.isAuthenticated()) {
			window.location.href = this.getRelativePath('login/login.html');
			return false;
		}
		const tier = this.getTier();
		if (!allowedTiers.includes(tier)) {
			this.toast('Your account is pending administrator approval.', 'error');
			// If not allowed, redirect to home or login
			if (tier === 3 && !window.location.pathname.includes('home.html')) {
				window.location.href = this.getRelativePath('home/home.html');
			}
			return false;
		}
		return true;
	},

	getRelativePath(target) {
		// Calculate relative path to root Frontend folder
		const path = window.location.pathname;
		if (path.includes('/login/') || path.includes('/register/') || path.includes('/home/') || path.includes('/files/') || path.includes('/manage-users/')) {
			return '../' + target;
		}
		return './' + target;
	},

	// --- HTTP Request Core ---
	async request(endpoint, options = {}) {
		const headers = options.headers || {};
		const token = this.getToken();
		if (token) {
			headers['Authorization'] = `Bearer ${token}`;
		}

		if (options.body && !(options.body instanceof FormData) && typeof options.body === 'object') {
			headers['Content-Type'] = 'application/json';
			options.body = JSON.stringify(options.body);
		}

		options.headers = headers;

		try {
			const res = await fetch(`${API_BASE}${endpoint}`, options);

			// Handle unauthorized token expiration
			if (res.status === 401) {
				this.clearSession();
				this.toast('Session expired. Please log in again.', 'error');
				setTimeout(() => {
					window.location.href = this.getRelativePath('login/login.html');
				}, 1200);
				throw new Error('Session expired');
			}

			let data;
			const contentType = res.headers.get('content-type') || '';
			if (contentType.includes('application/json')) {
				data = await res.json();
			} else {
				const text = await res.text();
				data = { error: `Server error (${res.status}): ${text.substring(0, 100)}` };
			}

			if (!res.ok) {
				const errMsg = data.error || data.message || `Request failed (${res.status})`;
				throw new Error(errMsg);
			}
			return data;
		} catch (err) {
			if (err.message !== 'Session expired') {
				this.toast(err.message, 'error');
			}
			throw err;
		}
	},

	// --- Authentication Endpoints ---
	async login(username, password) {
		const data = await this.request('/auth/login', {
			method: 'POST',
			body: { username, password },
		});
		if (data.token && data.user) {
			this.setSession(data.token, data.user);
		}
		return data;
	},

	async register(firstname, lastname, username, password) {
		return await this.request('/auth/register', {
			method: 'POST',
			body: { firstname, lastname, username, password },
		});
	},

	async getMe() {
		return await this.request('/auth/me');
	},

	async changePassword(old_password, new_password) {
		return await this.request('/auth/change-password', {
			method: 'POST',
			body: { old_password, new_password },
		});
	},

	// --- File & Folder Endpoints ---
	async getFiles(folder = '') {
		const param = folder ? `?folder=${encodeURIComponent(folder)}` : '';
		return await this.request(`/files${param}`);
	},

	async createFolder(parentFolder, folderName) {
		return await this.request('/files/folder', {
			method: 'POST',
			body: {
				parent_folder: parentFolder,
				folder_name: folderName,
			},
		});
	},

	async uploadFiles(folder, filesList) {
		const formData = new FormData();
		formData.append('folder', folder);
		for (const file of filesList) {
			formData.append('file', file);
		}
		return await this.request('/files/upload', {
			method: 'POST',
			body: formData,
		});
	},

	async deleteItem(path) {
		return await this.request('/files', {
			method: 'DELETE',
			body: { path },
		});
	},

	getFileDownloadUrl(path, download = false) {
		return `${STATIC_BASE}/${path.replace(/^\/+/, '')}`;
	},

	// --- User Administration Endpoints ---
	async getUsers() {
		return await this.request('/users');
	},

	async updateUserTier(username, permissionTier) {
		return await this.request(`/users/${encodeURIComponent(username)}/tier`, {
			method: 'PATCH',
			body: { permission_tier: permissionTier },
		});
	},

	async resetUserPassword(username, newPassword) {
		return await this.request(`/users/${encodeURIComponent(username)}/password`, {
			method: 'PATCH',
			body: { new_password: newPassword },
		});
	},

	async deleteUser(username) {
		return await this.request(`/users/${encodeURIComponent(username)}`, {
			method: 'DELETE',
		});
	},

	// --- Toast Notifications ---
	toast(message, type = 'info') {
		let container = document.querySelector('.toast-container');
		if (!container) {
			container = document.createElement('div');
			container.className = 'toast-container';
			document.body.appendChild(container);
		}

		const toast = document.createElement('div');
		toast.className = `toast ${type}`;
		const icon = type === 'success' ? '✅' : type === 'error' ? '⚠️' : 'ℹ️';
		toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
		container.appendChild(toast);

		setTimeout(() => {
			toast.style.opacity = '0';
			toast.style.transform = 'translateY(-10px)';
			toast.style.transition = 'all 0.3s ease';
			setTimeout(() => toast.remove(), 300);
		}, 3500);
	},
};
