/*global window,document,theme,jQuery,console*/
/*eslint no-console: ["off"] */
window.theme = window.theme || {};
document.documentElement.className = document.documentElement.className.replace("no-js", "js");

import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import 'lazysizes';

gsap.registerPlugin(ScrollTrigger);

var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

(function($) {
    'use strict';

    /**
     * Smooth scroll (Lenis) + GSAP ScrollTrigger sync.
     * Skipped under prefers-reduced-motion. Anchor links hand off to Lenis so the scroll is animated.
     */
    theme.smoothScroll = function() {
        if (reduceMotion) return;

        var lenis = new Lenis({
            duration: 1.2,
            easing: function(t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); },
            smoothWheel: true,
            wheelMultiplier: 0.9,
            touchMultiplier: 1.5
        });
        theme.lenis = lenis;

        lenis.on('scroll', ScrollTrigger.update);
        gsap.ticker.add(function(time) {
            lenis.raf(time * 1000);
        });
        gsap.ticker.lagSmoothing(0);

        $('a[href*="#"]:not([href="#"])').on('click', function(e) {
            var href = this.getAttribute('href');
            var hash = href.indexOf('#') > -1 ? href.split('#')[1] : '';
            var target = hash ? document.getElementById(hash) : null;
            // Only same-page links
            if (!target || this.pathname.replace(/^\//, '') !== window.location.pathname.replace(/^\//, '') || this.hostname !== window.location.hostname) return;
            e.preventDefault();
            if (target.tagName === 'DETAILS') { target.open = true; }
            lenis.scrollTo(target, { offset: -theme.headerHeight() });
        });
    };

    theme.headerHeight = function() {
        var header = document.querySelector('.site-header');
        return header ? header.offsetHeight : 0;
    };

    theme.init = function() {
        theme.smoothScroll();

        // Prevent default on '#' anchors
        $('a[href="#"]').on('click', function(e) {
            e.preventDefault();
        });

        // Open the FAQ item a #hash points to (fees page anchors)
        var openHash = function() {
            var target = window.location.hash ? document.querySelector(window.location.hash) : null;
            if (target && target.tagName === 'DETAILS') { target.open = true; }
        };
        openHash();
        window.addEventListener('hashchange', openHash);
    };

    /**
     * Header state: html.scrolled switches the transparent bar to the solid one.
     */
    theme.header = function() {
        var root = document.documentElement;
        var onScroll = function() {
            root.classList.toggle('scrolled', window.scrollY > 40);
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    };

    /**
     * Reveals: .fade-up elements ease in as they enter the screen. The CSS pre-state only exists under html.js.
     */
    theme.animations = function() {
        var items = gsap.utils.toArray('.fade-up');
        if (reduceMotion) {
            gsap.set(items, { opacity: 1, y: 0 });
            return;
        }
        items.forEach(function(el, i) {
            gsap.fromTo(el,
                { opacity: 0, y: 12 },
                {
                    opacity: 1,
                    y: 0,
                    duration: 0.5,
                    ease: 'power2.out',
                    delay: (i % 3) * 0.06,
                    scrollTrigger: { trigger: el, start: 'top 92%', once: true }
                }
            );
        });
    };

    /**
     * Phone menu: html.menu-open is the single source of truth for "sheet is open".
     */
    theme.menus = (function() {
        var root = document.documentElement;
        var drawer = document.getElementById('drawer');
        var openers = $('.site-header .menu-toggle');

        function setOpen(open) {
            root.classList.toggle('menu-open', open);
            openers.attr('aria-expanded', open ? 'true' : 'false');
            if (drawer) drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
            if (theme.lenis) { open ? theme.lenis.stop() : theme.lenis.start(); }
        }

        openers.on('click', function() { setOpen(true); });
        $('[data-menu-close]').on('click', function() { setOpen(false); });
        $('#drawer a').on('click', function() { setOpen(false); });
        $(document).on('keydown', function(e) {
            if (e.key === 'Escape' && root.classList.contains('menu-open')) setOpen(false);
        });

        // Crossing into the desktop layout closes the sheet
        window.matchMedia('(min-width: 1025px)').addEventListener('change', function(e) {
            if (e.matches) setOpen(false);
        });

        return { close: function() { setOpen(false); } };
    }());

    /**
     * Forms without a backend: submit opens the visitor's email app with the message filled in.
     * Works without JS too: the form's action is a mailto: address.
     */
    theme.mailtoForms = function() {
        $('form[data-mailto-form]').on('submit', function(e) {
            var f = this;
            var to = f.getAttribute('data-mailto');
            if (!to) return;
            e.preventDefault();
            var topic = f.topic ? f.topic.value : (f.getAttribute('data-subject') || 'Message from the website');
            var name = f.name && f.name.value ? f.name.value : '';
            var subject = name ? topic + ' (from ' + name + ')' : topic;
            var body = f.message ? f.message.value + '\n\n' + name + '\n' + f.email.value : 'Please add ' + f.email.value + ' to club updates.';
            window.location.href = 'mailto:' + to + '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
        });
    };

    $(function() {
        theme.init();
        theme.header();
        theme.animations();
        theme.mailtoForms();
    });
}(jQuery));
