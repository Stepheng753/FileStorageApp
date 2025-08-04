function makeHeader(mainDir = './', signoutFunc = false, goBackFunc = false, registerFunc = false) {
	let bodyContainer = document.querySelector('.body-container');
	let backClicks;
	if (signoutFunc || goBackFunc || registerFunc) {
		backClicks = document.createElement('div');
		backClicks.className = 'back-clicks';
		if (signoutFunc) {
			if (signoutFunc === true) {
				signoutFunc = () => redirect('../index.html', []);
			}
			let h3 = document.createElement('h3');
			h3.className = 'h3';
			h3.onclick = signoutFunc;
			h3.textContent = 'Sign Out';
			backClicks.appendChild(h3);
		}
		if (goBackFunc) {
			if (goBackFunc === true) {
				goBackFunc = () => redirect('../home/home.html');
			}
			let h3 = document.createElement('h3');
			h3.className = 'h3';
			h3.onclick = goBackFunc;
			h3.textContent = 'Go Back';
			backClicks.appendChild(h3);
		}
		if (registerFunc) {
			if (registerFunc === true) {
				registerFunc = () => redirect('./register/register.html', []);
			}
			let h3 = document.createElement('h3');
			h3.className = 'h3';
			h3.onclick = registerFunc;
			h3.textContent = 'Register';
			backClicks.appendChild(h3);
		}
	}

	removeHeader();

	let section = document.createElement('section');
	section.className = 'header';
	let titleContainer = document.createElement('div');
	titleContainer.className = 'title-container';
	let h1 = document.createElement('h1');
	h1.classList.add('h1');
	h1.classList.add('darker');
	h1.classList.add('header-title');
	h1.textContent = 'Tooth Manager';
	titleContainer.appendChild(h1);
	if (backClicks) {
		section.appendChild(backClicks);
	}
	section.appendChild(titleContainer);

	bodyContainer.insertBefore(section, bodyContainer.firstChild);
}

function removeHeader() {
	let header = document.querySelector('.header');
	if (header) {
		header.remove();
	}
}

function makeRowBoxes(prettyBoxesList) {
	let rowBoxes = document.createElement('div');
	rowBoxes.className = 'row-boxes';

	for (let i = 0; i < prettyBoxesList.length; i++) {
		let prettyBox = makePrettyBox(
			prettyBoxesList[i].image_url,
			prettyBoxesList[i].title,
			prettyBoxesList[i].clickHandler,
			prettyBoxesList[i].style ? prettyBoxesList[i].style : false
		);
		rowBoxes.appendChild(prettyBox);
	}

	let container = document.querySelector('.container');
	container.appendChild(rowBoxes);
}

function makePrettyBox(image_url, title, clickHandler, style = false) {
	let prettyBox = document.createElement('div');
	prettyBox.className = 'pretty-box';

	prettyBox.addEventListener('click', () => clickHandler());

	let icon_container = document.createElement('div');
	icon_container.className = 'icon-container';

	let icon = document.createElement('img');
	icon.className = 'image';
	icon.src = image_url;
	icon.alt = title;
	icon.loading = 'lazy';

	let boxTitle = document.createElement('div');
	boxTitle.className = 'box-title';

	let titleElmt = document.createElement('h2');
	titleElmt.className = 'h2';
	titleElmt.textContent = title;

	icon_container.appendChild(icon);
	boxTitle.appendChild(titleElmt);

	prettyBox.appendChild(icon_container);
	prettyBox.appendChild(boxTitle);

	if (style) {
		Object.assign(prettyBox.style, style);
	}

	return prettyBox;
}

function removeAllChildNodes(parent) {
	while (parent.firstChild) {
		parent.removeChild(parent.firstChild);
	}
}
