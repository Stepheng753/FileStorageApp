function uploadFormEventHandler() {
	const uploadForm = document.getElementById('upload-form');

	uploadForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const formData = new FormData(uploadForm);

		fetch('http://127.0.0.1:5000/upload_file', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					const userParam = 'user=' + getParam();
					window.location.href = '../home/home.html?' + userParam;
				} else {
					console.log(data);
				}
			});
	});
}

uploadFormEventHandler();
