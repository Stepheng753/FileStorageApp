document.addEventListener('DOMContentLoaded', () => {
	const form = document.getElementById('register-form');
	const btn = document.getElementById('register-btn');
	const card = document.getElementById('register-card');

	form.addEventListener('submit', async (e) => {
		e.preventDefault();
		const firstname = form.firstname.value.trim();
		const lastname = form.lastname.value.trim();
		const username = form.username.value.trim();
		const password = form.password.value;
		const confirm = form.confirm_password.value;

		if (password !== confirm) {
			api.toast('Passwords do not match.', 'error');
			return;
		}

		if (password.length < 6) {
			api.toast('Password must be at least 6 characters long.', 'error');
			return;
		}

		btn.disabled = true;
		btn.innerHTML = 'Submitting Request...';

		try {
			const res = await api.register(firstname, lastname, username, password);
			card.innerHTML = `
				<div style="text-align: center; padding: 1rem 0;">
					<div style="font-size: 3.5rem; margin-bottom: 1rem;">🎉</div>
					<h2 class="auth-title" style="font-size: 2.1rem; margin-bottom: 0.75rem;">Account Requested!</h2>
					<p style="color: var(--text-secondary); margin-bottom: 2rem; font-size: 0.95rem; line-height: 1.5;">
						Your account <strong>${escapeHtml(res.user.username)}</strong> has been registered.
						An administrator has been notified to activate your document access privileges.
					</p>
					<a href="../login/login.html" class="btn btn-primary btn-block">Return to Sign In</a>
				</div>
			`;
		} catch (err) {
			btn.disabled = false;
			btn.innerHTML = 'Submit Request';
		}
	});
});

function escapeHtml(str) {
	if (!str) return '';
	return str.replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m]));
}
