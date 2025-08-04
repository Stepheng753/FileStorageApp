const FILES_DIR = backendUrl + '/static/';
let currFolder = '';
let folders;
let deleteMode = false;

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
	let prettyBoxesList = [];
	Object.keys(folder_info).forEach((key) => {
		if (key == 'files') {
			for (const i in folder_info['files']) {
				let file = folder_info['files'][i];
				prettyBoxesList.push({
					image_url: '../assets/view.png',
					title: toTitleCase(file),
					clickHandler: () => {
						if (deleteMode) {
							deleteFile('.' + currFolder, file);
						} else {
							window.open(FILES_DIR + currFolder + '/' + file, '_blank');
						}
					},
				});
			}
		} else {
			prettyBoxesList.push({
				image_url: '../assets/view.png',
				title: toTitleCase(key),
				clickHandler: () => {
					currFolder += '/' + key;
					showFiles(folder_info[key]);
					makeHeader('../', true, goBackFunc);
				},
			});
		}
		if (prettyBoxesList.length === 4) {
			makeRowBoxes(prettyBoxesList);
			prettyBoxesList = [];
		}
	});

	if (prettyBoxesList.length > 0) {
		makeRowBoxes(prettyBoxesList);
	}
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
	});
}

function deleteFile(folder, file) {
	if (confirm('Are you sure you want to delete this file?')) {
		const formData = new FormData();
		formData.append('folder', folder);
		formData.append('file', file);
		fetch(backendUrl + '/delete_file', { method: 'POST', body: formData })
			.then((res) => res.json())
			.then((data) => {
				if (data.STATUS === 'SUCCESS') {
					goBackFunc();
				} else {
					alert('Error: ' + data.ERROR);
				}
			});
	}
}

getFolders();
uploadBtnRedirect();
deleteBtnClick();
makeHeader('../', true, getPermission() == 1 ? goBackFunc : false);
