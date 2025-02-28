const FILES_DIR = '../../Backend/files/';
const filesContainer = document.querySelector('div.file-links');

function getAllFiles() {
	fetch('http://127.0.0.1:5000/download_files', { method: 'POST' })
		.then((res) => res.json())
		.then((files) => {
			files = files;
			files.forEach((file) => {
				const a = document.createElement('a');
				a.href = FILES_DIR + file;
				a.innerText = file;
				a.classList.add('file-link');
				a.setAttribute('target', '_blank');
				filesContainer.appendChild(a);
			});
		});
}

getAllFiles();
