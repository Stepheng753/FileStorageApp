function goBackToMain() {
	const imgContainer = document.querySelector('.img-container');
	console.log(imgContainer);

	imgContainer.addEventListener('click', (event) => {
		event.preventDefault();
		if (window.location.href == window.location.origin + '/Frontend/' || window.location.href.includes('login')) {
			window.location.href = window.location.origin + '/Frontend/';
		} else {
			window.location.href = window.location.origin + '/Frontend/home/home.html?user=' + getUserParam();
		}
	});
}

function getUserParam() {
	const params = window.location.search.substring(1).split('&');
	if (params.length > 0) {
		const username = params[0].substring(params[0].search('user=') + 5);
		return username;
	}
	return '';
}

goBackToMain();
