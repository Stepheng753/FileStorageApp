// const backendUrl = 'http://127.0.0.1:5000';
const backendUrl = 'http://69.62.71.85:5000';
// const backendUrl = 'http://toothmanager.com:5000';
let key = '03022000';
let lastMouseDown = 0;
let timeout;

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
	return CryptoJS.AES.encrypt(username.toString(), key).toString();
}

function decryptUserName(encodedMsg) {
	return CryptoJS.AES.decrypt(encodedMsg, key).toString(CryptoJS.enc.Utf8);
}

document.addEventListener('mousedown', function (event) {
	lastMouseDown = new Date().getTime();
	resetTimeout();
});

function resetTimeout() {
	clearTimeout(timeout);
	timeout = setTimeout(() => (window.location.href = window.location.origin + '/Frontend/login/login.html'), 300_000);
}

resetTimeout();
