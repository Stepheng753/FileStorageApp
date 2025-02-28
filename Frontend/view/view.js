const FILES_DIR = '../../Backend/files/';
const form_container = document.querySelector('div.form-container');
console.log(form_container);

function getAllFiles() {
	fetch('http://127.0.0.1:5000/download_files', { method: 'POST' })
		.then((res) => res.json())
		.then((files) => {
			files = files.files;
			files.forEach((file) => {
				const a = document.createElement('a');
				a.href = FILES_DIR + file;
				a.innerText = file;
				a.setAttribute('target', '_blank');
				form_container.appendChild(a);
			});
		});
}

getAllFiles();
