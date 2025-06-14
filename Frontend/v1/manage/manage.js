const userContainer = document.querySelector('div.user-list');

function getAllUsers() {
	fetch(backendUrl + '/get_all_users', { method: 'GET' })
		.then((res) => res.json())
		.then((users) => {
			users.forEach((user) => {
				const firstname = user[1];
				const lastname = user[2];
				const username = user[3];
				const password = user[4];
				const permissionTier = user[5];
				makeUserItem(firstname, lastname, username, password, permissionTier);
			});
		});
}

function makeUserItem(firstname, lastname, username, password, permissionTier) {
	const userItem = document.createElement('div');
	userItem.className = 'user-item';

	const userInfo = document.createElement('div');
	userInfo.className = 'user-info';

	const nameSpan = document.createElement('span');
	nameSpan.className = 'name';
	nameSpan.innerText = `${firstname} ${lastname}`;

	const usernameSpan = document.createElement('span');
	usernameSpan.className = 'username';
	usernameSpan.innerText = username;

	const passwordSpan = document.createElement('span');
	passwordSpan.className = 'password';
	passwordSpan.innerText = password;

	const permissionTierSpan = document.createElement('span');
	permissionTierSpan.className = 'permission-tier';
	permissionTierSpan.innerText = permissionTier;

	userInfo.appendChild(nameSpan);
	userInfo.appendChild(usernameSpan);
	userInfo.appendChild(passwordSpan);
	userInfo.appendChild(permissionTierSpan);

	const editButton = document.createElement('button');
	editButton.className = 'edit-btn';
	editButton.innerText = 'Edit';
	editButtonEventHandler(editButton, username);

	userItem.appendChild(userInfo);
	userItem.appendChild(editButton);

	userContainer.appendChild(userItem);
}

function editButtonEventHandler(editButton, username) {
	editButton.addEventListener('click', (event) => {
		event.preventDefault();

		const userFromParam = 'userFrom=' + getParam();
		const userToParam = 'userTo=' + encryptUserName(username);
		const permissionParam = 'permission=' + getParam('permission');
		window.location.href = '../edit/edit.html?' + userFromParam + '&' + userToParam + '&' + permissionParam;
	});
}

getAllUsers();
