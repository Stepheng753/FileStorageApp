function changePassEventHandler() {
	const passwordForm = document.getElementById('update-password-form');

	passwordForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const formData = new FormData(passwordForm);
		formData.append('username', decrypt(getParam('userTo')));

		fetch(backendUrl + '/update_password', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					redirect('../../home/home.html');
				} else {
					alert('Error: ' + data.ERROR);
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
		formData.append('username', decrypt(getParam('userTo')));

		fetch(backendUrl + '/update_permission_tier', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					redirect('../../home/home.html');
				} else {
					alert('Error: ' + data.ERROR);
				}
			})
			.catch((error) => console.log('Error: ', error));
	});
}

function deleteUser() {
	const deleteButton = document.getElementById('delete-btn');

	deleteButton.addEventListener('click', (event) => {
		event.preventDefault();
		if (confirm(`Are you sure you want to delete this User?`)) {
			const formData = new FormData();
			formData.append('username', decrypt(getParam('userTo')));

			fetch(backendUrl + '/delete_user', {
				method: 'POST',
				body: formData,
			})
				.then((res) => res.json())
				.then((data) => {
					if (data.STATUS == 'SUCCESS') {
						redirect('../../home/home.html');
					} else {
						alert('Error: ' + data.ERROR);
					}
				})
				.catch((error) => console.log('Error: ', error));
		}
	});
}

function setDefaultPermissionVal() {
	const formData = new FormData();
	formData.append('username', decrypt(getParam('userTo')));

	fetch(backendUrl + '/get_user', { method: 'POST', body: formData })
		.then((res) => res.json())
		.then((users) => {
			const user = users[0];
			const permissionInput = document.getElementById('permission-input');
			permissionInput.setAttribute('value', user[5]);
		})
		.catch((error) => console.log('Error: ', error));
}

function changeEditTitles() {
	const editPassTitle = document.getElementById('pass-change-title');
	const editPermissionTitle = document.getElementById('permission-change-title');
	editPassTitle.innerText = 'Change Password for User: ' + decrypt(getParam('userTo'));
	editPermissionTitle.innerText = 'Change Permission for User: ' + decrypt(getParam('userTo'));
}

if (getPermission() != 1) {
	redirect('../../index.html', false);
} else {
	changePassEventHandler();
	changePermissionEventHandler();
	deleteUser();
	setDefaultPermissionVal();
	changeEditTitles();
	makeHeader(
		() => redirect('../../index.html'),
		() => redirect('../manage-users.html')
	);
}
