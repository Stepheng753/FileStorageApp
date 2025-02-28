function redirectButtonHandle(btnType) {
	const button = document.getElementById(btnType + '-btn');
	button.addEventListener('click', (event) => {
		event.preventDefault();

		if (btnType == 'login') {
			window.location.href = '../' + btnType + '/' + btnType + '.html';
		} else {
			window.location.href = '../' + btnType + '/' + btnType + '.html?user=' + getUserParam();
		}
	});
}

redirectButtonHandle('login');
redirectButtonHandle('upload');
redirectButtonHandle('view');
