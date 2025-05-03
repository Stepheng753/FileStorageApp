function loginFormEventHandler() {
	const loginForm = document.getElementById('login-form');

	loginForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const formData = new FormData(loginForm);

		fetch(backendUrl + '/login', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					const userParam = 'user=' + encryptUserName(formData.get('username'));
					const permissionParam = 'permission=' + encryptUserName(data.PERMISSION_TIER);
					window.location.href = '../home/home.html?' + userParam + '&' + permissionParam;
				} else {
					alert('Login failed. Please check your username and password.');
					loginForm.reset();
				}
			})
			.catch((error) => console.log('Error: ', error));
	});
}

loginFormEventHandler();
