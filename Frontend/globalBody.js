function goBackToMain(userParam = 'user') {
	const imgContainer = document.querySelector('.img-container');

	imgContainer.addEventListener('click', (event) => {
		event.preventDefault();
		if (
			window.location.href == window.location.origin + '/Frontend/' ||
			window.location.href.includes('login') ||
			window.location.href.includes('register')
		) {
			window.location.href = window.location.origin + '/Frontend/';
		} else {
			window.location.href = window.location.origin + '/Frontend/home/home.html?user=' + getParam(userParam);
		}
	});
}

function getParam(paramTxt = 'user') {
	const params = window.location.search.substring(1).split('&');
	for (let i = 0; i < params.length; i++) {
		if (params[i].includes(paramTxt)) {
			const encryptedUsername = params[i].substring(params[i].search(paramTxt + '=') + paramTxt.length + 1);
			return encryptedUsername;
		}
	}
	return '';
}

// function encryptUserName(username) {
// 	return CryptoJS.AES.encrypt(username, key).toString();
// }

// function decryptUserName(encodedMsg) {
// 	return CryptoJS.AES.decrypt(encodedMsg, key).toString(CryptoJS.enc.Utf8);
// }

goBackToMain();
