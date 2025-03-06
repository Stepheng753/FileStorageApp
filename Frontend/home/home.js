function redirectButtonHandle(btnType) {
	const button = document.getElementById(btnType + '-btn');
	button.addEventListener('click', (event) => {
		event.preventDefault();

		if (btnType == 'logout') {
			window.location.href = '../';
		} else {
			window.location.href = '../' + btnType + '/' + btnType + '.html?user=' + getParam();
		}
	});
}

function filterButtons() {
	const formData = new FormData();
	formData.append('username', getParam());

	fetch('http://127.0.0.1:5000/get_user', { method: 'POST', body: formData })
		.then((res) => res.json())
		.then((users) => {
			const user = users[0];
			const permissionVal = user[3];
			if (permissionVal == 3) {
				const uploadBtn = document.getElementById('upload-btn');
				uploadBtn.style.display = 'none';

				const manageBtn = document.getElementById('manage-btn');
				manageBtn.style.display = 'none';
			}
			if (permissionVal == 2) {
				const manageBtn = document.getElementById('manage-btn');
				manageBtn.style.display = 'none';
			}
		})
		.catch((error) => console.log('Error: ', error));
}

redirectButtonHandle('logout');
redirectButtonHandle('upload');
redirectButtonHandle('view');
redirectButtonHandle('manage');
filterButtons();
