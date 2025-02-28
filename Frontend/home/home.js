function redirectButtonHandle(btnType) {
	const button = document.getElementById(btnType + '-btn');
	button.addEventListener('click', (event) => {
		event.preventDefault();

		if (btnType == 'logout') {
			window.location.href = '../';
		} else {
			window.location.href = '../' + btnType + '/' + btnType + '.html?user=' + getUserParam();
		}
	});
}

redirectButtonHandle('logout');
redirectButtonHandle('upload');
redirectButtonHandle('view');
redirectButtonHandle('manage');
