document.addEventListener('DOMContentLoaded', async () => {
	if (!api.isAuthenticated()) {
		window.location.replace('../login/login.html');
		return;
	}

	renderNavbar('home');

	const user = api.getUser();
	const tier = api.getTier();

	const greeting = document.getElementById('greeting-title');
	if (greeting && user) {
		greeting.textContent = `Welcome, ${user.firstname || user.username}`;
	}

	const grid = document.getElementById('hub-grid');

	if (tier === 1) {
		// Administrator Hub
		grid.innerHTML = `
			<a class="item-card folder" href="../files/files.html">
				<div class="card-top">
					<img src="../assets/view.png" alt="Files" class="card-icon" />
					<span class="card-meta-badge">All Folders</span>
				</div>
				<div class="card-bottom">
					<div class="card-title">Manage Files</div>
					<div class="card-subtitle">
						<span>Practice Documents & Forms</span>
						<span>➔</span>
					</div>
				</div>
			</a>

			<a class="item-card file" href="../manage-users/manage-users.html">
				<div class="card-top">
					<img src="../assets/manage-users.png" alt="Users" class="card-icon" />
					<span class="card-meta-badge">Access Control</span>
				</div>
				<div class="card-bottom">
					<div class="card-title">Manage Users</div>
					<div class="card-subtitle">
						<span>Roles, Approvals & Passwords</span>
						<span>➔</span>
					</div>
				</div>
			</a>
		`;
	} else if (tier === 2) {
		// Staff Hub
		grid.innerHTML = `
			<a class="item-card folder" href="../files/files.html">
				<div class="card-top">
					<img src="../assets/view.png" alt="Files" class="card-icon" />
					<span class="card-meta-badge">Read / Download</span>
				</div>
				<div class="card-bottom">
					<div class="card-title">Practice Files</div>
					<div class="card-subtitle">
						<span>View & Download Documents</span>
						<span>➔</span>
					</div>
				</div>
			</a>
		`;
	} else {
		// Pending Approval Tier 3
		grid.innerHTML = `
			<div class="empty-state" style="background: var(--surface-glass); border-radius: var(--radius-lg); padding: 3.5rem 2rem; border: 1px solid var(--border-light);">
				<div class="empty-icon">⏳</div>
				<h3 class="empty-title">Access Pending Approval</h3>
				<p class="empty-text" style="max-width: 480px; margin: 0 auto 1.5rem;">
					Your account is registered but requires practice administrator authorization before accessing dental documents and patient records.
				</p>
				<button class="btn btn-primary" onclick="window.location.reload()">
					Check Approval Status
				</button>
			</div>
		`;
	}
});
