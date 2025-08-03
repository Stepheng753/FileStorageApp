uploadBox = {
	image_url: '../assets/upload.png',
	title: 'Upload Files',
	clickHandler: () => {
		redirect('../upload/upload.html');
	},
};

manageFilesBox = {
	image_url: '../assets/manage-files.png',
	title: 'Delete Files',
	clickHandler: () => {
		redirect('../manage-files/manage-files.html');
	},
};

manageUsersBox = {
	image_url: '../assets/manage-users.png',
	title: 'Manage Users',
	clickHandler: () => {
		redirect('../manage-users/manage-users.html');
	},
};

viewBox = {
	image_url: '../assets/view.png',
	title: 'View Files',
	clickHandler: () => {
		redirect('../view/view.html');
	},
};

function showOptions() {
	if (getPermission() == 1) {
		makeRowBoxes([uploadBox, manageFilesBox]);
		makeRowBoxes([manageUsersBox, viewBox]);
	} else if (getPermission() == 2) {
		makeRowBoxes([viewBox]);
	}
}

makeHeader('../', true, false, false);
showOptions();
