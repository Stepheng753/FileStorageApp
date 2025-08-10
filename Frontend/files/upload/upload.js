function uploadFormEventHandler() {
	const uploadForm = document.getElementById('upload-form');

	uploadForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const uploadBtn = document.getElementById('upload-btn');
		uploadBtn.innerText = 'Uploading...';
		uploadBtn.disabled = true;

		const formData = new FormData();
		const folderInput = uploadForm.querySelector('input[name="folder"]');
		formData.set('folder', '.' + decrypt(getParam('parentFolder')) + '/' + folderInput.value);

		const fileInput = uploadForm.querySelector('input[type="file"]');
		for (const file of fileInput.files) {
			formData.append('file', file);
		}

		fetch(backendUrl + '/upload_file', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					redirect('../../files/files.html');
				} else {
					alert('Error:' + data.ERROR);
				}
			});
	});
}

if (getPermission() != 1) {
	redirect('../../index.html', false);
} else {
	uploadFormEventHandler();
	makeHeader(
		() => redirect('../../index.html'),
		() => redirect('../files.html')
	);
}
