/**
 * Tooth Manager - User Management Administration
 */

let allUsers = [];
let targetUsernameForEdit = '';

document.addEventListener('DOMContentLoaded', () => {
	// Require Tier 1 (Admin)
	if (!api.requireAuth([1])) return;

	renderNavbar('users');
	initSearch();
	initModals();
	loadUsers();
});

async function loadUsers() {
	const tbody = document.getElementById('users-table-body');
	try {
		const res = await api.getUsers();
		allUsers = res.users || [];
		renderTable(allUsers);
	} catch (err) {
		tbody.innerHTML = `
			<tr>
				<td colspan="5" style="text-align: center; color: var(--danger); padding: 2rem;">
					⚠️ Failed to load users: ${escapeHtml(err.message)}
				</td>
			</tr>
		`;
	}
}

function renderTable(users = []) {
	const tbody = document.getElementById('users-table-body');
	tbody.innerHTML = '';

	if (users.length === 0) {
		tbody.innerHTML = `
			<tr>
				<td colspan="5" style="text-align: center; color: var(--text-muted); padding: 2rem;">
					No users found matching your search.
				</td>
			</tr>
		`;
		return;
	}

	const currentUser = api.getUser();
	const currentUsername = currentUser ? currentUser.username.toUpperCase() : '';

	users.forEach((user) => {
		const tr = document.createElement('tr');
		const tier = parseInt(user.permission_tier || 3);
		const tierClass = tier === 1 ? 'admin' : tier === 2 ? 'staff' : 'pending';
		const tierLabel = tier === 1 ? 'Tier 1: Admin' : tier === 2 ? 'Tier 2: Staff' : 'Tier 3: Pending';

		const isSelf = user.username.toUpperCase() === currentUsername;
		const createdDate = user.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A';

		tr.innerHTML = `
			<td>
				<div style="font-weight: 700; color: var(--text-primary);">
					${escapeHtml(user.firstname)} ${escapeHtml(user.lastname)}
					${isSelf ? '<span style="font-size: 0.75rem; color: var(--primary-dark); font-weight: normal;">(You)</span>' : ''}
				</div>
			</td>
			<td>
				<code style="background: rgba(0,0,0,0.04); padding: 0.2rem 0.45rem; border-radius: 4px; font-size: 0.85rem;">
					${escapeHtml(user.username)}
				</code>
			</td>
			<td>
				<span class="role-badge ${tierClass}">${tierLabel}</span>
			</td>
			<td style="color: var(--text-muted); font-size: 0.85rem;">
				${createdDate}
			</td>
			<td style="text-align: right;">
				<div class="table-actions" style="justify-content: flex-end;">
					<button class="btn btn-secondary action-btn-sm" onclick="openTierModal('${escapeHtml(user.username)}', ${tier})">
						Role
					</button>
					<button class="btn btn-secondary action-btn-sm" onclick="openPasswordModal('${escapeHtml(user.username)}')">
						Reset Pass
					</button>
					${
						!isSelf
							? `<button class="btn btn-danger action-btn-sm" onclick="confirmDeleteUser('${escapeHtml(user.username)}')">Delete</button>`
							: ''
					}
				</div>
			</td>
		`;

		tbody.appendChild(tr);
	});
}

function initSearch() {
	const input = document.getElementById('user-search-input');
	if (!input) return;

	input.addEventListener('input', (e) => {
		const query = e.target.value.toLowerCase().trim();
		if (!query) {
			renderTable(allUsers);
			return;
		}

		const filtered = allUsers.filter(
			(u) =>
				(u.firstname && u.firstname.toLowerCase().includes(query)) ||
				(u.lastname && u.lastname.toLowerCase().includes(query)) ||
				(u.username && u.username.toLowerCase().includes(query))
		);
		renderTable(filtered);
	});
}

function initModals() {
	// Tier modal
	const tierClose = document.getElementById('tier-modal-close');
	const tierCancel = document.getElementById('tier-cancel-btn');
	const tierForm = document.getElementById('tier-form');

	if (tierClose) tierClose.onclick = () => modal.close('tier-modal');
	if (tierCancel) tierCancel.onclick = () => modal.close('tier-modal');

	if (tierForm) {
		tierForm.onsubmit = async (e) => {
			e.preventDefault();
			const select = document.getElementById('tier-select');
			const newTier = parseInt(select.value);

			try {
				await api.updateUserTier(targetUsernameForEdit, newTier);
				api.toast(`Updated permission tier for '${targetUsernameForEdit}'`, 'success');
				modal.close('tier-modal');
				loadUsers();
			} catch (err) {}
		};
	}

	// Password modal
	const passClose = document.getElementById('password-modal-close');
	const passCancel = document.getElementById('password-cancel-btn');
	const passForm = document.getElementById('password-form');

	if (passClose) passClose.onclick = () => modal.close('password-modal');
	if (passCancel) passCancel.onclick = () => modal.close('password-modal');

	if (passForm) {
		passForm.onsubmit = async (e) => {
			e.preventDefault();
			const newPassInput = document.getElementById('new-password-input');
			const newPass = newPassInput.value;

			if (newPass.length < 6) {
				api.toast('Password must be at least 6 characters long.', 'error');
				return;
			}

			try {
				await api.resetUserPassword(targetUsernameForEdit, newPass);
				api.toast(`Password successfully reset for '${targetUsernameForEdit}'`, 'success');
				modal.close('password-modal');
				newPassInput.value = '';
			} catch (err) {}
		};
	}
}

window.openTierModal = function (username, currentTier) {
	targetUsernameForEdit = username;
	const subtitle = document.getElementById('tier-modal-subtitle');
	if (subtitle) subtitle.textContent = `Set permission tier for: ${username}`;

	const select = document.getElementById('tier-select');
	if (select) select.value = currentTier.toString();

	modal.open('tier-modal');
};

window.openPasswordModal = function (username) {
	targetUsernameForEdit = username;
	const subtitle = document.getElementById('password-modal-subtitle');
	if (subtitle) subtitle.textContent = `Set a new password for: ${username}`;

	const input = document.getElementById('new-password-input');
	if (input) input.value = '';

	modal.open('password-modal');
};

window.confirmDeleteUser = async function (username) {
	const confirmed = await modal.confirm({
		title: `Delete User '${username}'?`,
		message: `Are you sure you want to permanently delete user account '${username}'? This cannot be undone.`,
		confirmText: 'Delete User',
		danger: true,
	});

	if (confirmed) {
		try {
			await api.deleteUser(username);
			api.toast(`Deleted user '${username}'`, 'success');
			loadUsers();
		} catch (err) {}
	}
};

function escapeHtml(str) {
	if (!str) return '';
	return str.replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m]));
}
