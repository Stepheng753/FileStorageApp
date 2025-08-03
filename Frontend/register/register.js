function registerFormEventHandler() {
	const registerForm = document.getElementById('register-form');

	registerForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const formData = new FormData(registerForm);

		fetch(backendUrl + '/register', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					window.location.href = '../login/login.html';
				} else {
					alert('Error: ' + data.ERROR);
				}
			})
			.catch((error) => console.log('Error: ', error));
	});
}

registerFormEventHandler();
makeHeader('../', false, () => redirect('../login/login.html', []), false);
