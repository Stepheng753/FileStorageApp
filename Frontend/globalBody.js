function makeRowBoxes(prettyBoxesList) {
	let rowBoxes = document.createElement('div');
	rowBoxes.className = 'row-boxes';

	for (let i = 0; i < prettyBoxesList.length; i++) {
		let prettyBox = makePrettyBox(
			prettyBoxesList[i].image_url,
			prettyBoxesList[i].title,
			prettyBoxesList[i].clickHandler
		);
		rowBoxes.appendChild(prettyBox);
	}

	let container = document.querySelector('.container');
	container.appendChild(rowBoxes);
}

function makePrettyBox(image_url, title, clickHandler) {
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

	return prettyBox;
}
