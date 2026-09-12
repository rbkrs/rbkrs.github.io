document.addEventListener('DOMContentLoaded', function () {
    // ---- Dark mode ----
    var toggle = document.querySelector('.theme-toggle');
    var stored = null;
    try { stored = localStorage.getItem('theme'); } catch (e) {}

    var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (stored === 'dark' || (!stored && prefersDark)) {
        document.body.classList.add('dark-mode');
    }

    if (toggle) {
        toggle.addEventListener('click', function () {
            document.body.classList.toggle('dark-mode');
            try {
                localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
            } catch (e) {}
        });
    }

    // ---- Mobile nav ----
    var navToggle = document.querySelector('.nav-toggle');
    var navLinks = document.querySelector('.nav-links');
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function () {
            navLinks.classList.toggle('open');
        });
        navLinks.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                navLinks.classList.remove('open');
            });
        });
    }

    // ---- Project category tabs ----
    var tabs = document.querySelectorAll('.tab-btn');
    var groups = document.querySelectorAll('.project-group');
    tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
            var target = tab.getAttribute('data-target');
            tabs.forEach(function (t) { t.classList.remove('active'); });
            tab.classList.add('active');
            groups.forEach(function (g) {
                g.classList.toggle('active', g.getAttribute('data-group') === target);
            });
        });
    });

    // ---- Legacy: flip-card business card (only present on older pages) ----
    var card = document.getElementById('businessCard');
    if (card) {
        card.addEventListener('click', function (e) {
            if (e.target.closest('a')) return;
            card.classList.toggle('is-flipped');
        });
        card.addEventListener('keydown', function (e) {
            if ((e.key === 'Enter' || e.key === ' ') && !e.target.closest('a')) {
                e.preventDefault();
                card.classList.toggle('is-flipped');
            }
        });
    }
});
