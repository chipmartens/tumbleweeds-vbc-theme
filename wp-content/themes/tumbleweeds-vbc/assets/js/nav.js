// Mobile menu toggle. No dependencies.
(function () {
	var btn = document.querySelector('.site-header__toggle');
	var nav = document.getElementById('site-nav');
	if (!btn || !nav) return;
	btn.addEventListener('click', function () {
		var open = btn.getAttribute('aria-expanded') === 'true';
		btn.setAttribute('aria-expanded', open ? 'false' : 'true');
		document.documentElement.classList.toggle('nav-open', !open);
	});
	nav.addEventListener('click', function (e) {
		if (e.target.tagName === 'A') {
			btn.setAttribute('aria-expanded', 'false');
			document.documentElement.classList.remove('nav-open');
		}
	});
})();
