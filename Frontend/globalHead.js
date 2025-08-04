const backendUrl = 'https://dev.toothmanager.com';
let key = new Date().getDay().toString();
let lastMouseDown = 0;
let timeout;

function toTitleCase(str) {
	return str
		.toLowerCase()
		.split(' ')
		.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
		.join(' ');
}

function getParam(paramTxt = 'user') {
	const params = window.location.search.substring(1).split('&');
	for (let i = 0; i < params.length; i++) {
		if (params[i].includes(paramTxt)) {
			const encryptedStr = params[i].substring(params[i].search(paramTxt + '=') + paramTxt.length + 1);
			return encryptedStr;
		}
	}
	return '';
}

function redirect(toUrl, paramSearchIndices = ['user', 'permission'], additionalParams = false) {
	if (paramSearchIndices.length > 0) {
		toUrl += '?';
		for (let i = 0; i < paramSearchIndices.length; i++) {
			toUrl += paramSearchIndices[i] + '=' + getParam(paramSearchIndices[i]) + '&';
		}
	}
	if (additionalParams) {
		toUrl += additionalParams + '&';
	}
	window.location.href = toUrl;
}

function encrypt(strToEncrypt) {
	return CryptoJS.AES.encrypt(strToEncrypt.toString(), key).toString();
}

function decrypt(strToDecrypt) {
	return CryptoJS.AES.decrypt(strToDecrypt, key).toString(CryptoJS.enc.Utf8);
}

function getUserName() {
	return decrypt(getParam('user'));
}

function getPermission() {
	return parseInt(decrypt(getParam('permission')));
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
