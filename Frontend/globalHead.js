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

function encryptUserName(username) {
	return username;
}

function decryptUserName(encodedMsg) {
	return encodedMsg;
}

let key = '2025-03-06';
