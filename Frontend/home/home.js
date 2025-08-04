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
	} else {
		let h2 = document.createElement('h2');
		h2.textContent = 'Please wait for approval to access files ⏰';
		h2.style.textAlign = 'center';
		document.querySelector('.container').appendChild(h2);
	}
}

makeHeader('../', true, false, false);
showOptions();
