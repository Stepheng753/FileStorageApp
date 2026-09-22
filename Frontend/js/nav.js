/**
 * Tooth Manager - Shared Navigation Component
 */

function renderNavbar(activePage = '') {
	const user = api.getUser();
	const tier = api.getTier();

	// Calculate asset paths relative to current directory
	const isSubDir = window.location.pathname.includes('/login/') ||
		window.location.pathname.includes('/register/') ||
		window.location.pathname.includes('/home/') ||
		window.location.pathname.includes('/files/') ||
		window.location.pathname.includes('/manage-users/');

	const rootPath = isSubDir ? '../' : './';
	const logoPath = rootPath + 'assets/tooth.png';

	let navHtml = `
	<header class="app-header">
		<div class="header-container">
			<a class="brand-section" href="${rootPath}files/files.html">
				<img src="${logoPath}" alt="Tooth Manager Logo" class="brand-logo" />
				<h1 class="brand-title">Tooth Manager</h1>
			</a>

			<div class="header-actions">
	`;

	if (user && api.isAuthenticated()) {
		const tierLabel = tier === 1 ? 'ADMIN' : tier === 2 ? 'STAFF' : 'PENDING';
		const tierClass = tier === 1 ? 'admin' : tier === 2 ? 'staff' : 'pending';
		const displayName = `${user.firstname || ''} ${user.lastname || ''}`.trim() || user.username;

		// Navigation links based on permissions
		if (tier === 1 || tier === 2) {
			navHtml += `
				<a href="${rootPath}files/files.html" class="btn-header-link ${activePage === 'files' ? 'active' : ''}">
					📁 Files
				</a>
			`;
		}

		if (tier === 1) {
			navHtml += `
				<a href="${rootPath}manage-users/manage-users.html" class="btn-header-link ${activePage === 'users' ? 'active' : ''}">
					👥 Users
				</a>
			`;
		}

		navHtml += `
				<div class="user-pill">
					<span>👤 ${escapeHtml(displayName)}</span>
					<span class="role-badge ${tierClass}">${tierLabel}</span>
				</div>
				<button class="btn-header-link btn-header-signout" id="nav-signout-btn">
					Sign Out
				</button>
		`;
	} else {
		navHtml += `
			<a href="${rootPath}login/login.html" class="btn-header-link">Log In</a>
			<a href="${rootPath}register/register.html" class="btn btn-primary" style="padding: 0.4rem 0.9rem; font-size: 0.85rem;">Register</a>
		`;
	}

	navHtml += `
			</div>
		</div>
	</header>
	`;

	// Insert header at top of body
	const existingHeader = document.querySelector('.app-header');
	if (existingHeader) existingHeader.remove();

	document.body.insertAdjacentHTML('afterbegin', navHtml);

	// Attach Signout Handler
	const signoutBtn = document.getElementById('nav-signout-btn');
	if (signoutBtn) {
		signoutBtn.addEventListener('click', () => {
			api.clearSession();
			api.toast('Signed out successfully', 'info');
			setTimeout(() => {
				window.location.href = rootPath + 'login/login.html';
			}, 300);
		});
	}
}

function escapeHtml(str) {
	if (!str) return '';
	return str.replace(/[&<>"']/g, function (m) {
		return {
			'&': '&amp;',
			'<': '&lt;',
			'>': '&gt;',
			'"': '&quot;',
			"'": '&#039;',
		}[m];
	});
}
