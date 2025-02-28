function registerFormEventHandler() {
	const registerForm = document.getElementById('register-form');

	registerForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const formData = new FormData(registerForm);

		fetch('http://127.0.0.1:5000/register', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					window.location.href = '../login/login.html';
				} else {
					console.log(data);
				}
			})
			.catch((error) => console.log('Error: ', error));
	});
}

registerFormEventHandler();
