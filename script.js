(function () {
    var root = document.documentElement;
    root.classList.remove('no-js');

    // ---- Theme: stored choice wins, otherwise follow the OS ----
    var stored = null;
    try { stored = localStorage.getItem('theme'); } catch (e) {}
    if (stored === 'dark' || stored === 'light') root.setAttribute('data-theme', stored);

    function isDark() {
        var t = root.getAttribute('data-theme');
        if (t) return t === 'dark';
        return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    document.addEventListener('DOMContentLoaded', function () {
        var toggle = document.querySelector('.theme-toggle');
        if (toggle) {
            toggle.addEventListener('click', function () {
                var next = isDark() ? 'light' : 'dark';
                root.setAttribute('data-theme', next);
                try { localStorage.setItem('theme', next); } catch (e) {}
            });
        }

        // ---- Mobile nav ----
        var navToggle = document.querySelector('.nav-toggle');
        var navLinks = document.querySelector('.nav-links');
        if (navToggle && navLinks) {
            navToggle.addEventListener('click', function () {
                var open = navLinks.classList.toggle('open');
                navToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
            });
            navLinks.querySelectorAll('a').forEach(function (a) {
                a.addEventListener('click', function () {
                    navLinks.classList.remove('open');
                    navToggle.setAttribute('aria-expanded', 'false');
                });
            });
        }

        // ---- Project tabs ----
        var tabs = document.querySelectorAll('.tab-btn');
        var groups = document.querySelectorAll('.project-group');
        function select(target) {
            tabs.forEach(function (t) {
                t.setAttribute('aria-selected', t.getAttribute('data-target') === target ? 'true' : 'false');
            });
            groups.forEach(function (g) {
                g.hidden = g.getAttribute('data-group') !== target;
            });
        }
        tabs.forEach(function (tab) {
            tab.addEventListener('click', function () { select(tab.getAttribute('data-target')); });
        });
        if (tabs.length) select(tabs[0].getAttribute('data-target'));

        // Deep links like #personal / #opensource open the matching tab
        function fromHash() {
            var id = location.hash.slice(1);
            if (document.querySelector('.tab-btn[data-target="' + id + '"]')) {
                select(id);
                var p = document.getElementById('projects');
                if (p) p.scrollIntoView();
            }
        }
        window.addEventListener('hashchange', fromHash);
        fromHash();
    });
})();
