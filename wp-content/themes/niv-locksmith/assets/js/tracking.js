/**
 * ניב — dataLayer events. delegation יחיד, עמיד ל-DOM דינמי.
 * 8 אירועים לפי docs/04. GTM מתרגם ל-tags/conversions.
 */
(function () {
	'use strict';
	window.dataLayer = window.dataLayer || [];

	function push(obj) {
		obj.page_url = location.href;
		obj.page_title = document.title;
		window.dataLayer.push(obj);
	}

	function closest(el, sel) {
		return el && el.closest ? el.closest(sel) : null;
	}

	document.addEventListener('click', function (e) {
		var t = e.target;

		// sticky CTA — נדחף לפני click_to_call/whatsapp כדי לתפוס גם sticky.
		var sticky = closest(t, '.js-sticky-cta');
		if (sticky) {
			push({
				event: 'sticky_cta_click',
				cta_type: sticky.getAttribute('data-cta-type') || ''
			});
		}

		// click_to_call
		var call = closest(t, '.js-call-click');
		if (call) {
			push({
				event: 'click_to_call',
				cta_location: call.getAttribute('data-cta-location') || '',
				phone_number: call.getAttribute('data-phone') || '',
				service: call.getAttribute('data-service') || '',
				area: call.getAttribute('data-area') || ''
			});
			return;
		}

		// whatsapp_click
		var wa = closest(t, '.js-whatsapp-click');
		if (wa) {
			push({
				event: 'whatsapp_click',
				cta_location: wa.getAttribute('data-cta-location') || '',
				service: wa.getAttribute('data-service') || '',
				area: wa.getAttribute('data-area') || ''
			});
			return;
		}

		// service_click
		var svc = closest(t, '.js-service-card');
		if (svc) {
			push({
				event: 'service_click',
				service_name: svc.getAttribute('data-service') || '',
				source_page: location.pathname
			});
			return;
		}

		// service_area_click
		var area = closest(t, '.js-area-card');
		if (area) {
			push({
				event: 'service_area_click',
				area_name: area.getAttribute('data-area') || '',
				source_page: location.pathname
			});
		}
	});

	// --- טפסים ---
	document.querySelectorAll('.js-form').forEach(function (form) {
		var started = false;
		var formId = form.getAttribute('id') || 'lead_form';

		form.addEventListener('input', function () {
			if (started) return;
			started = true;
			push({ event: 'lead_form_start', form_id: formId });
		}, { once: false });

		form.addEventListener('submit', function () {
			// ולידציה ב-main.js; כאן רק מדידה כשתקין.
			if (form.checkValidity && !form.checkValidity()) {
				var invalid = form.querySelector(':invalid');
				push({
					event: 'lead_form_error',
					form_id: formId,
					error_type: invalid ? (invalid.name || invalid.id || 'validation') : 'validation'
				});
				return;
			}
			push({
				event: 'lead_form_submit',
				form_id: formId,
				service: form.getAttribute('data-service') || '',
				area: form.getAttribute('data-area') || ''
			});
		});
	});
})();
