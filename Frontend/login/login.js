function loginFormEventHandler() {
	const loginForm = document.getElementById('login-form');

	loginForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const formData = new FormData(loginForm);

		fetch('http://127.0.0.1:5000/get_user_pass', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				const userParam = 'user=' + formData.get('username');
				window.location.href = '../home/home.html?' + userParam;
			})
			.catch((error) => console.log('Error: ', error));
	});
}

loginFormEventHandler();
