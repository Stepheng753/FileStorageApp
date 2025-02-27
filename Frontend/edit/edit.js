function changePassEventHandler() {
	const passwordForm = document.getElementById('update-password-form');

	passwordForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const formData = new FormData(passwordForm);
		formData.append('username', getUserParam());

		fetch('http://127.0.0.1:5000/update_password', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					const userParam = 'user=' + formData.get('username');
					window.location.href = '../home/home.html?' + userParam;
				} else {
					console.log(data);
				}
			})
			.catch((error) => console.log('Error: ', error));
	});
}

function changePermissionEventHandler() {
	const permissionForm = document.getElementById('update-permission-form');

	permissionForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const formData = new FormData(permissionForm);
		formData.append('username', getUserParam());

		fetch('http://127.0.0.1:5000/update_permission_tier', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					const userParam = 'user=' + formData.get('username');
					window.location.href = '../home/home.html?' + userParam;
				} else {
					console.log(data);
				}
			})
			.catch((error) => console.log('Error: ', error));
	});
}

function deleteUser() {
	const deleteButton = document.getElementById('delete-btn');

	deleteButton.addEventListener('click', (event) => {
		event.preventDefault();

		const formData = new FormData();
		formData.append('username', getUserParam());

		fetch('http://127.0.0.1:5000/delete_user', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					const userParam = 'user=' + formData.get('username');
					window.location.href = '../home/home.html?' + userParam;
				} else {
					console.log(data);
				}
				console.log(data);
			})
			.catch((error) => console.log('Error: ', error));
	});
}

function setDefaultPermissionVal() {
	const formData = new FormData();
	formData.append('username', getUserParam());

	fetch('http://127.0.0.1:5000/get_user', { method: 'POST', body: formData })
		.then((res) => res.json())
		.then((users) => {
			const user = users[0];
			const permissionInput = document.getElementById('permission-input');
			permissionInput.setAttribute('value', user[3]);
		})
		.catch((error) => console.log('Error: ', error));
}

function changeEditTitles() {
	const editPassTitle = document.getElementById('pass-change-title');
	const editPermissionTitle = document.getElementById('permission-change-title');
	editPassTitle.innerText = 'Change Password for USER: ' + getUserParam();
	editPermissionTitle.innerText = 'Change Permission for USER: ' + getUserParam();
}

changePassEventHandler();
changePermissionEventHandler();
deleteUser();
setDefaultPermissionVal();
changeEditTitles();
