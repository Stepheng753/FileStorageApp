/**
 * Tooth Manager - File & Folder Management
 */

let currentFolder = '';
let currentFolderData = { folders: [], files: [], breadcrumbs: [] };
let deleteMode = false;
let selectedFilesForUpload = [];

document.addEventListener('DOMContentLoaded', () => {
	// Require Tier 1 (Admin) or Tier 2 (Staff)
	if (!api.requireAuth([1, 2])) return;

	renderNavbar('files');

	const tier = api.getTier();
	if (tier === 1) {
		const dock = document.getElementById('admin-action-dock');
		if (dock) dock.style.display = 'flex';
		initAdminActions();
	}

	initSearch();
	initUploadModal();

	// Check if URL specifies an initial folder
	const urlParams = new URLSearchParams(window.location.search);
	const initialFolder = urlParams.get('folder') || '';
	loadFolder(initialFolder);
});

async function loadFolder(folderPath = '') {
	currentFolder = folderPath.trim();
	const grid = document.getElementById('items-grid');
	grid.innerHTML = `
		<div class="empty-state">
			<div class="empty-icon">📂</div>
			<h3 class="empty-title">Loading...</h3>
		</div>
	`;

	try {
		const res = await api.getFiles(currentFolder);
		currentFolderData = res.data;
		renderBreadcrumbs(currentFolderData.breadcrumbs);
		renderGrid(currentFolderData.folders, currentFolderData.files);

		// Update URL without page reload
		const newUrl = currentFolder
			? `${window.location.pathname}?folder=${encodeURIComponent(currentFolder)}`
			: window.location.pathname;
		window.history.pushState({ folder: currentFolder }, '', newUrl);
	} catch (err) {
		grid.innerHTML = `
			<div class="empty-state">
				<div class="empty-icon">⚠️</div>
				<h3 class="empty-title">Folder Not Found</h3>
				<p class="empty-text">${escapeHtml(err.message)}</p>
				<button class="btn btn-primary" onclick="loadFolder('')" style="margin-top: 1rem;">
					Return to Root
				</button>
			</div>
		`;
	}
}

// Handle Browser Back / Forward Buttons
window.addEventListener('popstate', (e) => {
	const folder = e.state ? e.state.folder : '';
	loadFolder(folder);
});

function renderBreadcrumbs(breadcrumbs = []) {
	const nav = document.getElementById('breadcrumbs-nav');
	if (!nav) return;

	nav.innerHTML = '';
	breadcrumbs.forEach((crumb, idx) => {
		const isLast = idx === breadcrumbs.length - 1;
		const a = document.createElement('a');
		a.href = '#';
		a.className = `breadcrumb-item ${isLast ? 'active' : ''}`;
		a.innerHTML = idx === 0 ? '🏠 Practice Root' : `📁 ${escapeHtml(crumb.name)}`;
		a.onclick = (e) => {
			e.preventDefault();
			loadFolder(crumb.path);
		};
		nav.appendChild(a);

		if (!isLast) {
			const sep = document.createElement('span');
			sep.className = 'breadcrumb-separator';
			sep.textContent = '/';
			nav.appendChild(sep);
		}
	});
}

function renderGrid(folders = [], files = []) {
	const grid = document.getElementById('items-grid');
	grid.innerHTML = '';

	const hasItems = folders.length > 0 || files.length > 0;
	if (!hasItems) {
		grid.innerHTML = `
			<div class="empty-state">
				<div class="empty-icon">📂</div>
				<h3 class="empty-title">This folder is empty</h3>
				<p class="empty-text">No documents or subfolders found here.</p>
			</div>
		`;
		return;
	}

	// 1. Render Folders
	folders.forEach((folder) => {
		const card = document.createElement('div');
		card.className = `item-card folder ${deleteMode ? 'delete-candidate' : ''}`;
		card.title = folder.name;

		card.innerHTML = `
			<div class="card-top">
				<img src="../assets/folder.png" alt="Folder" class="card-icon" />
				<span class="card-meta-badge">${folder.item_count} items</span>
			</div>
			<div class="card-bottom">
				<div class="card-title">${escapeHtml(folder.name)}</div>
				<div class="card-subtitle">
					<span>Folder</span>
					<span>${deleteMode ? '🗑️ Click to delete' : 'Open ➔'}</span>
				</div>
			</div>
		`;

		card.onclick = async () => {
			if (deleteMode) {
				const confirmed = await modal.confirm({
					title: `Delete Folder '${folder.name}'?`,
					message: 'Deleting this folder will permanently erase all documents and subfolders inside it.',
					confirmText: 'Delete Folder',
					danger: true,
				});
				if (confirmed) {
					try {
						await api.deleteItem(folder.path);
						api.toast(`Deleted folder '${folder.name}'`, 'success');
						loadFolder(currentFolder);
					} catch (e) {}
				}
			} else {
				loadFolder(folder.path);
			}
		};

		grid.appendChild(card);
	});

	// 2. Render Files
	files.forEach((file) => {
		const card = document.createElement('div');
		card.className = `item-card file ${deleteMode ? 'delete-candidate' : ''}`;
		card.title = file.name;

		// Select best icon based on category
		const iconSrc = '../assets/view.png';

		card.innerHTML = `
			<div class="card-top">
				<img src="${iconSrc}" alt="Document" class="card-icon" />
				<span class="card-meta-badge">${file.formatted_size}</span>
			</div>
			<div class="card-bottom">
				<div class="card-title">${escapeHtml(file.name)}</div>
				<div class="card-subtitle">
					<span style="text-transform: uppercase;">${escapeHtml(file.category)}</span>
					<span>${deleteMode ? '🗑️ Click to delete' : 'View / Download ➔'}</span>
				</div>
			</div>
		`;

		card.onclick = async () => {
			if (deleteMode) {
				const confirmed = await modal.confirm({
					title: `Delete File?`,
					message: `Are you sure you want to permanently delete '${file.name}'?`,
					confirmText: 'Delete File',
					danger: true,
				});
				if (confirmed) {
					try {
						await api.deleteItem(file.path);
						api.toast(`Deleted file '${file.name}'`, 'success');
						loadFolder(currentFolder);
					} catch (e) {}
				}
			} else {
				handleOpenFile(file);
			}
		};

		grid.appendChild(card);
	});
}

function handleOpenFile(file) {
	const viewableExts = ['.pdf', '.html', '.htm', '.txt', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.mp4', '.webm', '.mp3'];
	const ext = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
	const fileUrl = api.getFileDownloadUrl(file.path);

	if (viewableExts.includes(ext)) {
		window.open(fileUrl, '_blank');
	} else {
		const link = document.createElement('a');
		link.href = fileUrl;
		link.download = file.name;
		document.body.appendChild(link);
		link.click();
		link.remove();
	}
}

function initSearch() {
	const searchInput = document.getElementById('file-search-input');
	if (!searchInput) return;

	searchInput.addEventListener('input', (e) => {
		const query = e.target.value.toLowerCase().trim();
		if (!query) {
			renderGrid(currentFolderData.folders, currentFolderData.files);
			return;
		}

		const filteredFolders = currentFolderData.folders.filter((f) => f.name.toLowerCase().includes(query));
		const filteredFiles = currentFolderData.files.filter((f) => f.name.toLowerCase().includes(query));
		renderGrid(filteredFolders, filteredFiles);
	});
}

function initAdminActions() {
	// 1. Toggle Delete Mode
	const deleteBtn = document.getElementById('dock-delete-btn');
	if (deleteBtn) {
		deleteBtn.onclick = () => {
			deleteMode = !deleteMode;
			deleteBtn.classList.toggle('active', deleteMode);
			api.toast(deleteMode ? 'Delete mode ON: Click any item to remove it' : 'Delete mode turned off', deleteMode ? 'error' : 'info');
			renderGrid(currentFolderData.folders, currentFolderData.files);
		};
	}

	// 2. Create Folder
	const newFolderBtn = document.getElementById('dock-newfolder-btn');
	if (newFolderBtn) {
		newFolderBtn.onclick = async () => {
			const folderName = await modal.prompt({
				title: 'Create New Folder',
				placeholder: 'e.g. Consent Forms 2026',
				confirmText: 'Create Folder',
			});
			if (folderName) {
				try {
					await api.createFolder(currentFolder, folderName);
					api.toast(`Created folder '${folderName}'`, 'success');
					loadFolder(currentFolder);
				} catch (e) {}
			}
		};
	}

	// 3. Upload Files Button
	const uploadBtn = document.getElementById('dock-upload-btn');
	if (uploadBtn) {
		uploadBtn.onclick = () => {
			const targetInput = document.getElementById('target-folder-input');
			if (targetInput) {
				targetInput.value = currentFolder ? `/${currentFolder}` : '/ (Root)';
			}
			selectedFilesForUpload = [];
			renderSelectedFiles();
			modal.open('upload-modal');
		};
	}
}

function initUploadModal() {
	const modalClose = document.getElementById('upload-modal-close');
	const cancelBtn = document.getElementById('upload-cancel-btn');
	const dropzone = document.getElementById('dropzone');
	const filePicker = document.getElementById('file-picker');
	const uploadForm = document.getElementById('upload-form');
	const submitBtn = document.getElementById('upload-submit-btn');

	if (modalClose) modalClose.onclick = () => modal.close('upload-modal');
	if (cancelBtn) cancelBtn.onclick = () => modal.close('upload-modal');

	if (dropzone && filePicker) {
		dropzone.onclick = () => filePicker.click();

		dropzone.addEventListener('dragover', (e) => {
			e.preventDefault();
			dropzone.classList.add('dragover');
		});

		['dragleave', 'dragend'].forEach((type) => {
			dropzone.addEventListener(type, () => dropzone.classList.remove('dragover'));
		});

		dropzone.addEventListener('drop', (e) => {
			e.preventDefault();
			dropzone.classList.remove('dragover');
			if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
				addFilesToUploadQueue(e.dataTransfer.files);
			}
		});

		filePicker.onchange = (e) => {
			if (e.target.files && e.target.files.length > 0) {
				addFilesToUploadQueue(e.target.files);
			}
		};
	}

	if (uploadForm) {
		uploadForm.onsubmit = async (e) => {
			e.preventDefault();
			if (selectedFilesForUpload.length === 0) {
				api.toast('Please select at least one file to upload.', 'error');
				return;
			}

			submitBtn.disabled = true;
			submitBtn.innerHTML = 'Uploading...';

			try {
				await api.uploadFiles(currentFolder, selectedFilesForUpload);
				api.toast(`Uploaded ${selectedFilesForUpload.length} document(s) successfully!`, 'success');
				modal.close('upload-modal');
				selectedFilesForUpload = [];
				filePicker.value = '';
				loadFolder(currentFolder);
			} catch (err) {
			} finally {
				submitBtn.disabled = false;
				submitBtn.innerHTML = 'Upload Files';
			}
		};
	}
}

function addFilesToUploadQueue(fileList) {
	for (let i = 0; i < fileList.length; i++) {
		selectedFilesForUpload.push(fileList[i]);
	}
	renderSelectedFiles();
}

function renderSelectedFiles() {
	const listEl = document.getElementById('selected-files-list');
	if (!listEl) return;

	listEl.innerHTML = '';
	selectedFilesForUpload.forEach((file, idx) => {
		const pill = document.createElement('div');
		pill.className = 'file-item-pill';
		pill.innerHTML = `
			<span>📄 ${escapeHtml(file.name)} (${(file.size / 1024).toFixed(1)} KB)</span>
			<button type="button" style="background: none; border: none; cursor: pointer; color: var(--danger); font-size: 1rem;" onclick="removeUploadFile(${idx})">&times;</button>
		`;
		listEl.appendChild(pill);
	});
}

window.removeUploadFile = function (idx) {
	selectedFilesForUpload.splice(idx, 1);
	renderSelectedFiles();
};

function escapeHtml(str) {
	if (!str) return '';
	return str.replace(/[&<>"']/g, (m) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' }[m]));
}
