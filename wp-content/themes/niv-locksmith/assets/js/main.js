/**
 * ניב — UI: תפריט נייד, אקורדיון FAQ נגיש, ולידציית טופס.
 * וניל JS, בלי תלויות. עמיד למקלדת.
 */
(function () {
	'use strict';

	// --- תפריט נייד ---
	var toggle = document.querySelector('.niv-nav__toggle');
	var menu = document.getElementById('niv-primary-menu');
	if (toggle && menu) {
		toggle.addEventListener('click', function () {
			var open = menu.classList.toggle('is-open');
			toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
		});
	}

	// --- FAQ accordion (aria-expanded + hidden) ---
	document.querySelectorAll('.niv-faq__btn').forEach(function (btn) {
		btn.addEventListener('click', function () {
			var expanded = btn.getAttribute('aria-expanded') === 'true';
			var panel = document.getElementById(btn.getAttribute('aria-controls'));
			btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
			if (panel) {
				if (expanded) { panel.setAttribute('hidden', ''); }
				else { panel.removeAttribute('hidden'); }
			}
		});
	});

	// --- ולידציית טופס נגישה ---
	document.querySelectorAll('.js-form').forEach(function (form) {
		form.setAttribute('novalidate', '');
		form.addEventListener('submit', function (e) {
			var valid = true;
			form.querySelectorAll('[required]').forEach(function (field) {
				var errId = field.getAttribute('aria-describedby');
				var err = errId ? document.getElementById(errId) : null;
				var fieldValid = field.checkValidity();

				// טלפון ישראלי בסיסי.
				if (fieldValid && field.type === 'tel') {
					fieldValid = /^0\d{1,2}-?\d{7}$|^\+972\d{8,9}$/.test(field.value.replace(/\s/g, ''));
				}
				if (!fieldValid) {
					valid = false;
					field.setAttribute('aria-invalid', 'true');
					if (err) { err.textContent = field.dataset.error || 'נא למלא שדה זה'; }
				} else {
					field.removeAttribute('aria-invalid');
					if (err) { err.textContent = ''; }
				}
			});
			if (!valid) {
				e.preventDefault();
				var first = form.querySelector('[aria-invalid="true"]');
				if (first) { first.focus(); }
			}
		});
	});
})();
