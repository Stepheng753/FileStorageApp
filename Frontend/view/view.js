const FILES_DIR = backendUrl + '/static/';
const folderContainer = document.querySelector('div.container');

function getAllFiles() {
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
						const a = document.createElement('a');
						a.href = FILES_DIR + folderName + '/' + file;
						a.innerText = file;
						a.classList.add('file-link');
						a.setAttribute('target', '_blank');
						filesContainer.appendChild(a);
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
		const a = document.createElement('a');
		a.href = FILES_DIR + folderName + '/' + file;
		a.innerText = file;
		a.classList.add('file-link');
		a.setAttribute('target', '_blank');
		filesContainer.appendChild(a);
	});

	while (folderContainer.firstChild) {
		folderContainer.removeChild(folderContainer.firstChild);
	}
	makeH2();
	folderContainer.appendChild(filesContainer);

	const backBtn = document.createElement('button');
	backBtn.innerText = 'Back';
	backBtn.addEventListener('click', () => {
		while (folderContainer.firstChild) {
			folderContainer.removeChild(folderContainer.firstChild);
		}
		getAllFiles();
	});
	folderContainer.appendChild(backBtn);
}

function makeH2() {
	const h2 = document.createElement('h2');
	h2.innerText = 'View Files';
	folderContainer.appendChild(h2);
}

getAllFiles();
