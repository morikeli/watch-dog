(function() {
	"use strict";

	// Easy selector helper function
	const select = (el, all = false) => {
		el = el.trim()
		if (all) {
			return [...document.querySelectorAll(el)]
		} else {
			return document.querySelector(el)
		}
	}

	// Easy event listener function
	const on = (type, el, listener, all = false) => {
		if (all) {
			select(el, all).forEach(e => e.addEventListener(type, listener))
		} else {
			select(el, all).addEventListener(type, listener)
		}
	}

	// Easy on scroll event listener 
	const onscroll = (el, listener) => {
		el.addEventListener('scroll', listener)
	}

	// side menu toggle
	if (select('.toggle-sidebar-btn')) {
		on('click', '.toggle-sidebar-btn', function(e) {
			select('#sidebar').classList.toggle('expand')
		})

		select('body').classList.add('toggle-sidebar');
	}

	// back to top button
	let backtotop = select('.back-to-top')
	if (backtotop) {
		const toggleBacktotop = () => {
		if (window.scrollY > 100) {
			backtotop.classList.add('active')
		} else {
			backtotop.classList.remove('active')
		}
		}
		window.addEventListener('load', toggleBacktotop)
		onscroll(document, toggleBacktotop)
	}

	// Preloader
	let preloader = select('#preloader');
	if (preloader) {
		setTimeout(() => {
			preloader.remove();
		}, 1000)	// preloader timeout: 1s
		
		const showPreloader = () => {
            preloader.style.display = 'block';
        };
        const hidePreloader = () => {
            preloader.style.display = 'none';
        };

        document.body.addEventListener('htmx:configRequest', showPreloader);
        document.body.addEventListener('htmx:responseEnd', hidePreloader);
        document.body.addEventListener('htmx:afterRequest', hidePreloader);
	}

	// tootlips
	const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');

	// Convert NodeList to an array and initialize tooltips for each element
	const tooltipList = Array.from(tooltipTriggerList).map(tooltipTriggerEl => {
		const tooltip = new bootstrap.Tooltip(tooltipTriggerEl);

		// Add click event listener to hide tooltip when link is clicked
		tooltipTriggerEl.addEventListener('click', () => {
			tooltip.hide(); // Hide the tooltip
		});

	});
	
})();