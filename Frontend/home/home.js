manageUsersBox = {
	image_url: '../assets/manage-users.png',
	title: 'Manage Users',
	clickHandler: () => {
		redirect('../manage-users/manage-users.html');
	},
};

filesBox = {
	image_url: '../assets/view.png',
	title: 'Manage Files',
	clickHandler: () => {
		redirect('../files/files.html');
	},
};

function showOptions() {
	if (getPermission() == 1) {
		makeRowBoxes([manageUsersBox, filesBox]);
	} else if (getPermission() == 2) {
		makeRowBoxes([filesBox]);
	}
}

makeHeader('../', true, false, false);
showOptions();
