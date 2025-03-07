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

let key = '2025-03-06';

// window.addEventListener('load', () => {
// 	fetch('http://127.0.0.1:5000/get_key', {
// 		method: 'POST',
// 	})
// 		.then((res) => res.json())
// 		.then((data) => {
// 			key = data.key;
// 		})
// 		.catch((error) => console.log('Error: ', error));
// });
