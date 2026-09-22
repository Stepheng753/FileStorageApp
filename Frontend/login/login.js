document.addEventListener('DOMContentLoaded', () => {
	// If already authenticated, redirect immediately
	if (api.isAuthenticated()) {
		const tier = api.getTier();
		if (tier === 1 || tier === 2) {
			window.location.replace('../files/files.html');
			return;
		} else {
			window.location.replace('../home/home.html');
			return;
		}
	}

	const form = document.getElementById('login-form');
	const btn = document.getElementById('login-btn');

	form.addEventListener('submit', async (e) => {
		e.preventDefault();
		const username = form.username.value.trim();
		const password = form.password.value;

		btn.disabled = true;
		btn.innerHTML = 'Signing In...';

		try {
			const res = await api.login(username, password);
			api.toast(`Welcome back, ${res.user.firstname || res.user.username}!`, 'success');

			setTimeout(() => {
				const tier = parseInt(res.user.permission_tier);
				if (tier === 1 || tier === 2) {
					window.location.href = '../files/files.html';
				} else {
					window.location.href = '../home/home.html';
				}
			}, 500);
		} catch (err) {
			btn.disabled = false;
			btn.innerHTML = 'Sign In';
		}
	});
});
