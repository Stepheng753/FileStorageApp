const userContainer = document.querySelector('div.user-list');

function getAllUsers() {
	fetch('http://127.0.0.1:5000/get_all_users', { method: 'GET' })
		.then((res) => res.json())
		.then((users) => {
			users.forEach((user) => {
				const username = user[1];
				const password = user[2];
				const permissionTier = user[3];
				makeUserItem(username, password, permissionTier);
			});
		});
}

function makeUserItem(username, password, permissionTier) {
	const userItem = document.createElement('div');
	userItem.className = 'user-item';

	const userInfo = document.createElement('div');
	userInfo.className = 'user-info';

	const usernameSpan = document.createElement('span');
	usernameSpan.className = 'username';
	usernameSpan.innerText = username;

	const passwordSpan = document.createElement('span');
	passwordSpan.className = 'password';
	passwordSpan.innerText = password;

	const permissionTierSpan = document.createElement('span');
	permissionTierSpan.className = 'permission-tier';
	permissionTierSpan.innerText = permissionTier;

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
		const userToParam = 'userTo=' + username;
		window.location.href = '../edit/edit.html?' + userFromParam + '&' + userToParam;
	});
}

getAllUsers();
