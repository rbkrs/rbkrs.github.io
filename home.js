(function () {
    'use strict';

    var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var finePointer = window.matchMedia && window.matchMedia('(pointer: fine)').matches;
    var shell = document.querySelector('.shell');

    /* ---------- Starfield ---------- */
    (function stars() {
        var layer = document.querySelector('.star-layer');
        if (!layer) return;
        var sizes = [0.8, 0.8, 0.8, 0.8, 1.5, 0.8, 2.2];
        var frag = document.createDocumentFragment();
        for (var i = 0; i < 72; i++) {
            var s = document.createElement('i');
            // Deterministic scatter so the sky looks the same on every visit
            s.style.setProperty('--l', ((i * 37 + 11) % 100) + '%');
            s.style.setProperty('--t', ((i * 61 + 7) % 100) + '%');
            s.style.setProperty('--s', sizes[i % sizes.length] + 'px');
            s.style.setProperty('--delay', (-(i * 0.73) % 7.5).toFixed(2) + 's');
            s.style.setProperty('--dur', (3.2 + (i * 1.17) % 5).toFixed(2) + 's');
            frag.appendChild(s);
        }
        layer.appendChild(frag);
    })();

    /* ---------- Cursor glow + logo letters drifting away from the cursor ---------- */
    (function pointer() {
        if (reduceMotion || !finePointer) return;
        var letters = Array.prototype.slice.call(document.querySelectorAll('.logo-letter'));
        var px = 0, py = 0, queued = false;

        function frame() {
            queued = false;
            shell.style.setProperty('--mx', px + 'px');
            shell.style.setProperty('--my', py + 'px');

            letters.forEach(function (el) {
                if (!el.offsetParent) return; // home panel hidden
                var r = el.getBoundingClientRect();
                var cx = r.left + r.width / 2, cy = r.top + r.height / 2;
                var dx = cx - px, dy = cy - py;
                var dist = Math.sqrt(dx * dx + dy * dy) || 1;
                var reach = 200;
                if (dist < reach) {
                    var push = (1 - dist / reach) * 16;
                    el.style.setProperty('--dx', (dx / dist * push).toFixed(1) + 'px');
                    el.style.setProperty('--dy', (dy / dist * push).toFixed(1) + 'px');
                } else {
                    el.style.removeProperty('--dx');
                    el.style.removeProperty('--dy');
                }
            });
        }

        window.addEventListener('pointermove', function (e) {
            px = e.clientX; py = e.clientY;
            if (!queued) { queued = true; requestAnimationFrame(frame); }
        }, { passive: true });
    })();

    /* ---------- Panels / bottom nav ---------- */
    var panels = {};
    document.querySelectorAll('[data-panel]').forEach(function (p) { panels[p.getAttribute('data-panel')] = p; });
    var navLinks = document.querySelectorAll('.bottom-nav a');
    var aliases = { contact: 'home', top: 'home', kaggle: 'projects', personal: 'projects', opensource: 'projects' };
    var current = null;

    function showPanel(name) {
        if (!panels[name]) name = 'home';
        if (name !== current) {
            Object.keys(panels).forEach(function (k) { panels[k].hidden = k !== name; });
            navLinks.forEach(function (a) {
                if (a.getAttribute('data-tab') === name) a.setAttribute('aria-current', 'page');
                else a.removeAttribute('aria-current');
            });
            current = name;
        }
        // Fragment navigation can scroll an overflow:hidden container; undo that
        shell.scrollTop = 0;
        window.scrollTo(0, 0);
    }

    function fromHash() {
        var id = location.hash.slice(1);
        var panel = aliases[id] || id || 'home';
        showPanel(panel);
        if (id === 'kaggle' || id === 'personal' || id === 'opensource') selectGroup(id);
    }

    navLinks.forEach(function (a) {
        a.addEventListener('click', function (e) {
            e.preventDefault();
            var name = a.getAttribute('data-tab');
            if (name === current) return;
            history.pushState(null, '', name === 'home' ? location.pathname : '#' + name);
            showPanel(name);
        });
    });

    // Arrow keys move between tabs when focus is on the nav
    document.querySelector('.bottom-nav').addEventListener('keydown', function (e) {
        if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
        var list = Array.prototype.slice.call(navLinks);
        var i = list.indexOf(document.activeElement);
        if (i < 0) return;
        var next = list[(i + (e.key === 'ArrowRight' ? 1 : list.length - 1)) % list.length];
        next.focus();
        next.click();
        e.preventDefault();
    });

    window.addEventListener('popstate', fromHash);
    window.addEventListener('hashchange', fromHash);

    /* ---------- Project category tabs ---------- */
    var segButtons = document.querySelectorAll('.seg button');
    var groups = document.querySelectorAll('.project-group');
    function selectGroup(target) {
        segButtons.forEach(function (b) {
            b.setAttribute('aria-selected', b.getAttribute('data-target') === target ? 'true' : 'false');
        });
        groups.forEach(function (g) { g.hidden = g.getAttribute('data-group') !== target; });
        var scroller = document.querySelector('.project-scroll');
        if (scroller) scroller.scrollTop = 0;
    }
    segButtons.forEach(function (b) {
        b.addEventListener('click', function () { selectGroup(b.getAttribute('data-target')); });
    });
    selectGroup('kaggle');

    fromHash();

    /* ---------- Copy email ---------- */
    var toast = document.querySelector('.toast');
    var toastTimer;
    function say(msg) {
        if (!toast) return;
        toast.textContent = msg;
        toast.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(function () { toast.classList.remove('show'); }, 2200);
    }
    var mail = document.querySelector('.email-social');
    if (mail && navigator.clipboard && window.isSecureContext) {
        mail.addEventListener('click', function (e) {
            e.preventDefault();
            var addr = mail.getAttribute('data-email');
            navigator.clipboard.writeText(addr).then(function () {
                mail.classList.add('copied');
                say('Copied ' + addr);
                setTimeout(function () { mail.classList.remove('copied'); }, 1800);
            }, function () {
                location.href = mail.href; // fall back to opening the mail client
            });
        });
    }

    /* ---------- Highlights carousel ---------- */
    (function carousel() {
        var root = document.querySelector('.highlight-carousel');
        if (!root) return;
        var cards = Array.prototype.slice.call(root.querySelectorAll('.hl-card'));
        var n = cards.length;
        if (!n) return;

        var pos = 0;           // fractional index of the front card
        var spacing = 132;
        var drag = null;       // { x0, pos0, moved }
        var suppressClick = false;
        var timer = null;

        function wrap(o) { return ((o + n / 2) % n + n) % n - n / 2; }

        function layout() {
            spacing = cards[0].offsetWidth * 0.8;
            var front = ((Math.round(pos) % n) + n) % n;
            cards.forEach(function (c, i) {
                var o = wrap(i - pos);
                var a = Math.abs(o);
                c.style.setProperty('--x', (o * spacing) + 'px');
                c.style.setProperty('--sc', Math.max(0.55, 1 - 0.13 * a).toFixed(3));
                c.style.setProperty('--o', a > 2.6 ? '0' : Math.max(0, 1 - 0.26 * a).toFixed(3));
                c.style.zIndex = String(20 - Math.round(a * 2));
                c.classList.toggle('front', i === front);
                c.tabIndex = i === front ? 0 : -1;
                c.setAttribute('aria-hidden', i === front ? 'false' : 'true');
            });
        }

        function goTo(p) { pos = p; layout(); }
        function step(d) { goTo(Math.round(pos) + d); }

        function startAuto() {
            if (reduceMotion || timer) return;
            timer = setInterval(function () {
                if (root.offsetParent) step(1);
            }, 4500);
        }
        function stopAuto() { clearInterval(timer); timer = null; }

        root.addEventListener('pointerdown', function (e) {
            if (e.button !== 0) return;
            drag = { x0: e.clientX, pos0: pos, moved: false };
            stopAuto();
        });
        window.addEventListener('pointermove', function (e) {
            if (!drag) return;
            var dx = e.clientX - drag.x0;
            if (!drag.moved && Math.abs(dx) > 6) { drag.moved = true; root.classList.add('dragging'); }
            if (drag.moved) { pos = drag.pos0 - dx / spacing; layout(); }
        });
        window.addEventListener('pointerup', function () {
            if (!drag) return;
            if (drag.moved) {
                suppressClick = true;
                setTimeout(function () { suppressClick = false; }, 0);
                root.classList.remove('dragging');
                goTo(Math.round(pos));
            }
            drag = null;
            startAuto();
        });
        window.addEventListener('pointercancel', function () {
            if (!drag) return;
            root.classList.remove('dragging');
            drag = null;
            goTo(Math.round(pos));
        });

        cards.forEach(function (c, i) {
            c.addEventListener('dragstart', function (e) { e.preventDefault(); });
            c.addEventListener('click', function (e) {
                if (suppressClick) { e.preventDefault(); return; }
                if (!c.classList.contains('front')) {
                    // Side card: bring it to the front instead of following the link
                    e.preventDefault();
                    goTo(Math.round(pos) + wrap(i - Math.round(pos)));
                }
            });
        });

        root.addEventListener('keydown', function (e) {
            if (e.key === 'ArrowRight') { step(1); e.preventDefault(); }
            else if (e.key === 'ArrowLeft') { step(-1); e.preventDefault(); }
        });
        var wheelLock = 0;
        root.addEventListener('wheel', function (e) {
            if (Math.abs(e.deltaX) <= Math.abs(e.deltaY)) return;
            e.preventDefault();
            var now = Date.now();
            if (now < wheelLock || Math.abs(e.deltaX) < 12) return;
            wheelLock = now + 450; // one card per swipe gesture
            step(e.deltaX > 0 ? 1 : -1);
        }, { passive: false });

        root.addEventListener('mouseenter', stopAuto);
        root.addEventListener('mouseleave', startAuto);
        root.addEventListener('focusin', stopAuto);
        root.addEventListener('focusout', startAuto);
        window.addEventListener('resize', layout);

        layout();
        startAuto();
    })();
})();
