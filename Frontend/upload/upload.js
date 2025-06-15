function uploadFormEventHandler() {
	const uploadForm = document.getElementById('upload-form');

	uploadForm.addEventListener('submit', (event) => {
		event.preventDefault();

		const uploadBtn = document.getElementById('upload-btn');
		uploadBtn.innerText = 'Uploading...';
		uploadBtn.disabled = true;

		const formData = new FormData(uploadForm);

		fetch(backendUrl + '/upload_file', {
			method: 'POST',
			body: formData,
		})
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS == 'SUCCESS') {
					const userParam = 'user=' + getParam();
					const permissionParam = 'permission=' + getParam('permission');
					window.location.href = '../home/home.html?' + userParam + '&' + permissionParam;
				} else {
					alert('Error:' + data.ERROR);
				}
			});
	});
}

function getFolders() {
	fetch(backendUrl + '/download_files', { method: 'POST' })
		.then((res) => res.json())
		.then((files) => {
			let folders = [];
			for (const folderName in files) {
				if (folderName.length > 0) {
					folders.push(folderName);
				}
			}
			const folderSelect = document.getElementById('folder-select');
			folders.forEach((folder) => {
				const option = document.createElement('option');
				option.value = folder;
				option.innerText = folder;
				folderSelect.appendChild(option);
			});
			const newFolder = document.createElement('option');
			newFolder.innerText = 'New Folder';
			folderSelect.appendChild(newFolder);
			folderSelect.addEventListener('change', () => {
				if (folderSelect.value === 'New Folder') {
					const newFolderInput = document.createElement('input');
					newFolderInput.type = 'text';
					newFolderInput.placeholder = 'Enter new folder name';
					newFolderInput.name = 'folder';
					folderSelect.parentNode.replaceChild(newFolderInput, folderSelect);
				}
			});
		});
}

getFolders();
uploadFormEventHandler();
