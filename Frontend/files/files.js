const FILES_DIR = backendUrl + '/static/';
let currFolder = '';
let folders;
let deleteMode = false;
let prevColors = [];

function goBackFunc() {
	if (currFolder.length == 0 && getPermission() == 1) {
		redirect('../home/home.html');
	} else {
		removeAllChildNodes(document.querySelector('.container'));
		currFolder = '';
		showFiles(folders);
		if (getPermission() != 1) {
			let goBack = Array.from(document.querySelectorAll('h3.h3')).find((el) => el.textContent === 'Go Back');
			goBack.remove();
		}
	}
}

function getFolders() {
	fetch(backendUrl + '/download_files', { method: 'POST' })
		.then((res) => res.json())
		.then((data) => {
			folders = data;
			showFiles(folders);
		});
}

function showFiles(folder_info) {
	removeAllChildNodes(document.querySelector('.container'));
	let h2 = document.createElement('h2');
	h2.className = 'h2';
	h2.textContent = currFolder.split('/').at(1);
	document.querySelector('.container').appendChild(h2);

	let prettyBoxesList = [];
	Object.keys(folder_info).forEach((key) => {
		if (key == 'files') {
			for (const i in folder_info['files']) {
				let file = folder_info['files'][i];
				prettyBoxesList.push({
					image_url: '../assets/view.png',
					title: file,
					clickHandler: () => {
						if (deleteMode) {
							deleteFile('.' + currFolder, file);
						} else {
							window.open(FILES_DIR + currFolder + '/' + file, '_blank');
						}
					},
					style: {
						backgroundColor: 'var(--pretty-box-secondary)',
					},
				});
			}
		} else {
			prettyBoxesList.push({
				image_url: '../assets/folder.png',
				title: key,
				clickHandler: () => {
					currFolder += '/' + key;
					if (deleteMode) {
						deleteFile('.' + currFolder, '');
					} else {
						showFiles(folder_info[key]);
						makeHeader('../', true, goBackFunc);
					}
				},
			});
		}

		if (prettyBoxesList.length === 4) {
			makeRowBoxes(prettyBoxesList);
			prettyBoxesList = [];
		}
	});

	let prettyBoxes = document.querySelectorAll('.pretty-box');
	prevColors = [];
	prettyBoxes.forEach((el) => {
		prevColors.push(getComputedStyle(el).backgroundColor);
	});
}

function uploadBtnRedirect() {
	let uploadBtn = document.getElementById('new-folder');
	uploadBtn.addEventListener('click', (event) => {
		event.preventDefault();
		const parentFolderParam = 'parentFolder=' + encrypt(currFolder);
		redirect('./upload/upload.html', ['user', 'permission'], parentFolderParam);
	});
}

function deleteBtnClick() {
	let deleteBtn = document.getElementById('delete-file');
	deleteBtn.addEventListener('click', (event) => {
		event.preventDefault();
		deleteMode = !deleteMode;
		let prettyBoxes = document.querySelectorAll('.pretty-box');
		for (let i = 0; i < prettyBoxes.length; i++) {
			if (deleteMode) {
				prettyBoxes[i].style.backgroundColor = 'var(--danger-color)';
			} else {
				prettyBoxes[i].style.backgroundColor = prevColors[i];
			}
		}
	});
}

function deleteFile(folder, file) {
	let fileFolderStr = file.length > 0 ? 'file' : 'folder';
	if (confirm(`Are you sure you want to delete this ${fileFolderStr}?`)) {
		const formData = new FormData();
		formData.append('folder', folder);
		formData.append('file', file);
		fetch(backendUrl + '/delete_file', { method: 'POST', body: formData })
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS != 'SUCCESS') {
					alert('Error: ' + data.ERROR);
				}
			});
		window.location.reload();
	}
}

function showEditBtns() {
	if (getPermission() != 1) {
		let fileBtns = document.querySelector('.floating-btn');
		fileBtns.style.display = 'none';
	}
}

if (getPermission() == 1 || getPermission() == 2) {
	getFolders();
	uploadBtnRedirect();
	deleteBtnClick();
	showEditBtns();
	makeHeader('../', true, getPermission() == 1 ? goBackFunc : false);
} else {
	redirect('../index.html', false);
}
