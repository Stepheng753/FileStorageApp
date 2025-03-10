function redirectButtonHandle(btnType) {
	const button = document.getElementById(btnType + '-btn');
	button.addEventListener('click', (event) => {
		event.preventDefault();
		console.log(btnType);
		if (btnType == 'logout') {
			window.location.href = '../';
		} else if (getParam('permission').length > 0) {
			window.location.href =
				'../' + btnType + '/' + btnType + '.html?user=' + getParam() + '&permission=' + getParam('permission');
		} else {
			window.location.href = '../' + btnType + '/' + btnType + '.html?user=' + getParam();
		}
	});
}

function filterButtons() {
	const permissionVal = parseInt(decryptUserName(getParam('permission')));
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
}

redirectButtonHandle('logout');
redirectButtonHandle('upload');
redirectButtonHandle('view');
redirectButtonHandle('manage');
filterButtons();
