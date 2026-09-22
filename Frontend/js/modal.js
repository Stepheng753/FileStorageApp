/**
 * Tooth Manager - Reusable Modal Components
 */

const modal = {
	open(modalId) {
		const el = document.getElementById(modalId);
		if (el) el.classList.add('active');
	},

	close(modalId) {
		const el = document.getElementById(modalId);
		if (el) el.classList.remove('active');
	},

	confirm({ title = 'Are you sure?', message = 'This action cannot be undone.', confirmText = 'Delete', danger = true }) {
		return new Promise((resolve) => {
			let overlay = document.getElementById('tm-confirm-modal');
			if (!overlay) {
				overlay = document.createElement('div');
				overlay.id = 'tm-confirm-modal';
				overlay.className = 'modal-overlay';
				document.body.appendChild(overlay);
			}

			overlay.innerHTML = `
				<div class="modal-box">
					<div class="modal-header">
						<h3 class="modal-title">${escapeHtml(title)}</h3>
						<button class="modal-close" id="confirm-close-btn">&times;</button>
					</div>
					<p style="color: var(--text-secondary); margin-bottom: 1.75rem; font-size: 0.95rem;">
						${escapeHtml(message)}
					</p>
					<div style="display: flex; gap: 0.75rem; justify-content: flex-end;">
						<button class="btn btn-secondary" id="confirm-cancel-btn">Cancel</button>
						<button class="btn ${danger ? 'btn-danger' : 'btn-primary'}" id="confirm-ok-btn">${escapeHtml(confirmText)}</button>
					</div>
				</div>
			`;

			overlay.classList.add('active');

			const cleanup = (res) => {
				overlay.classList.remove('active');
				resolve(res);
			};

			document.getElementById('confirm-close-btn').onclick = () => cleanup(false);
			document.getElementById('confirm-cancel-btn').onclick = () => cleanup(false);
			document.getElementById('confirm-ok-btn').onclick = () => cleanup(true);
		});
	},

	prompt({ title = 'New Folder', placeholder = 'Enter folder name...', confirmText = 'Create' }) {
		return new Promise((resolve) => {
			let overlay = document.getElementById('tm-prompt-modal');
			if (!overlay) {
				overlay = document.createElement('div');
				overlay.id = 'tm-prompt-modal';
				overlay.className = 'modal-overlay';
				document.body.appendChild(overlay);
			}

			overlay.innerHTML = `
				<div class="modal-box">
					<div class="modal-header">
						<h3 class="modal-title">${escapeHtml(title)}</h3>
						<button class="modal-close" id="prompt-close-btn">&times;</button>
					</div>
					<form id="prompt-form">
						<div class="form-group">
							<input type="text" id="prompt-input" class="form-control" placeholder="${escapeHtml(placeholder)}" required autofocus />
						</div>
						<div style="display: flex; gap: 0.75rem; justify-content: flex-end; margin-top: 1.5rem;">
							<button type="button" class="btn btn-secondary" id="prompt-cancel-btn">Cancel</button>
							<button type="submit" class="btn btn-primary" id="prompt-ok-btn">${escapeHtml(confirmText)}</button>
						</div>
					</form>
				</div>
			`;

			overlay.classList.add('active');
			const input = document.getElementById('prompt-input');
			setTimeout(() => input.focus(), 50);

			const cleanup = (val) => {
				overlay.classList.remove('active');
				resolve(val);
			};

			document.getElementById('prompt-close-btn').onclick = () => cleanup(null);
			document.getElementById('prompt-cancel-btn').onclick = () => cleanup(null);
			document.getElementById('prompt-form').onsubmit = (e) => {
				e.preventDefault();
				const val = input.value.trim();
				cleanup(val || null);
			};
		});
	},
};
