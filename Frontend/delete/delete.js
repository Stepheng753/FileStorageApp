const FILES_DIR = '../files/';
const folderContainer = document.querySelector('div.container');

function getAllFiles() {
	while (folderContainer.firstChild) {
		folderContainer.removeChild(folderContainer.firstChild);
	}
	makeH2();
	fetch(backendUrl + '/download_files', { method: 'POST' })
		.then((res) => res.json())
		.then((files) => {
			let looseFiles = [];
			let folders = [];
			for (const folderName in files) {
				files[folderName].sort();
				if (folderName.length === 0) {
					const filesContainer = document.createElement('div');
					filesContainer.classList.add('file-links');
					files[folderName].forEach((file) => {
						const fileLink = document.createElement('div');
						fileLink.innerText = file;
						fileLink.classList.add('file-link');
						fileLink.addEventListener('click', () => {
							if (confirm('Are you sure you want to delete this file?')) {
								deleteFile(folderName, file);
							} else {
								return;
							}
						});
						filesContainer.appendChild(fileLink);
					});
					looseFiles.push(filesContainer);
				} else {
					const btn = document.createElement('button');
					btn.innerText = folderName;

					btn.addEventListener('click', () => {
						showFilesInFolder(folderName, files[folderName]);
					});
					folders.push(btn);
				}
			}
			folders.forEach((folder) => {
				folderContainer.appendChild(folder);
			});
			looseFiles.forEach((file) => {
				folderContainer.appendChild(file);
			});
		});
}

function showFilesInFolder(folderName, filesArr) {
	const filesContainer = document.createElement('div');
	filesContainer.classList.add('file-links');

	filesArr.forEach((file) => {
		const fileLink = document.createElement('div');
		fileLink.innerText = file;
		fileLink.classList.add('file-link');
		fileLink.addEventListener('click', () => {
			if (confirm('Are you sure you want to delete this file?')) {
				deleteFile(folderName, file);
			} else {
				return;
			}
		});
		filesContainer.appendChild(fileLink);
	});

	while (folderContainer.firstChild) {
		folderContainer.removeChild(folderContainer.firstChild);
	}
	makeH2();
	folderContainer.appendChild(filesContainer);

	const backBtn = document.createElement('button');
	backBtn.innerText = 'Back';
	backBtn.addEventListener('click', () => {
		getAllFiles();
	});
	folderContainer.appendChild(backBtn);
}

function makeH2() {
	const h2 = document.createElement('h2');
	h2.innerText = 'Delete Files';
	folderContainer.appendChild(h2);
}

function deleteFile(folder, file) {
	const formData = new FormData();
	formData.append('folder', folder);
	formData.append('file', file);
	fetch(backendUrl + '/delete_file', { method: 'POST', body: formData })
		.then((res) => res.json())
		.then((data) => {
			if (data.STATUS === 'SUCCESS') {
				getAllFiles();
			} else {
				alert('Error: ' + data.ERROR);
			}
		});
}

getAllFiles();
