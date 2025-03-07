function loginFormEventHandler() {
	const loginForm = document.getElementById('login-form');

	loginForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const formData = new FormData(loginForm);

		fetch('http://127.0.0.1:5000/login', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					const userParam = 'user=' + encryptUserName(formData.get('username'));
					window.location.href = '../home/home.html?' + userParam;
				} else {
					console.log(data);
				}
			})
			.catch((error) => console.log('Error: ', error));
	});
}

loginFormEventHandler();
