const FILES_DIR = backendUrl + '/static/';
let folders;

function getFolders() {
	fetch(backendUrl + '/download_files', { method: 'POST' })
		.then((res) => res.json())
		.then((data) => {
			folders = data;
			showFolders();
		});
}

function showFolders() {
	let prettyBoxesList = [];
	for (const folder in folders) {
		if (folder.length > 0) {
			prettyBoxesList.push({
				image_url: '../assets/view.png',
				title: toTitleCase(folder),
				clickHandler: () => showFiles(folder, folders[folder]),
			});
			if (prettyBoxesList.length === 4) {
				makeRowBoxes(prettyBoxesList);
				prettyBoxesList = [];
			}
		}
	}
	if (prettyBoxesList.length > 0) {
		makeRowBoxes(prettyBoxesList);
	}
	makeHeader('../', true, false);
}

function showFiles(folder, file_list) {
	removeAllChildNodes(document.querySelector('.container'));
	let prettyBoxesList = [];
	for (const file of file_list) {
		console.log(file_list);
		prettyBoxesList.push({
			image_url: '../assets/view.png',
			title: toTitleCase(file),
			clickHandler: () => {
				window.open(FILES_DIR + folder + '/' + file, '_blank');
			},
		});
		if (prettyBoxesList.length === 4) {
			makeRowBoxes(prettyBoxesList);
			prettyBoxesList = [];
		}
	}
	if (prettyBoxesList.length > 0) {
		makeRowBoxes(prettyBoxesList);
	}

	let goBackFunc = () => {
		removeAllChildNodes(document.querySelector('.container'));
		showFolders();
	};
	makeHeader('../', true, goBackFunc);
}

getFolders();
