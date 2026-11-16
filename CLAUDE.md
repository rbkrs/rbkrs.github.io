# CLAUDE.md

Personal portfolio for Robin (Rob) Kras, served at **robkras.com** (GitHub Pages; `CNAME` sets the domain). Static site, no build step.

## Hard rule

There is no profile photo or face picture on the site. Do not add one.

## Files

- `index.html`: single-screen, dark-only homepage (starfield background, floating "rob kras" logo, round social buttons, Kaggle highlights carousel). Content lives in panels switched by the bottom nav: `#home`, `#experience`, `#skills`, `#projects` (`#contact` → home; `#kaggle`, `#personal`, `#opensource` → projects with that category open). Without JS (`html.no-js`) all panels show stacked and the page scrolls.
- `home.css` / `home.js`: styles and behaviour for `index.html` only (stars, cursor glow, logo drift, panel switching, carousel, copy-email toast). Honours `prefers-reduced-motion`.
- `resume.html`: résumé page (print-friendly; nav/footer hidden when printing)
- `styles.css` / `script.js`: used by `resume.html` only now (light/dark theme toggle, mobile nav). Theme tokens are on `:root`; dark mode follows `prefers-color-scheme`, overridden by `data-theme` on `<html>`
- `page.css`: classless styles for every page under `projects/**` (linked as `../../page.css`)
- `projects/`: write-ups and stripped notebook exports (`kaggle-competitions/`, `models/`, `personal-projects/`, `utilities/`, `documents/`)
- `larz/`: standalone birthday page, not linked from the portfolio
- `Robin_Kras_CV.pdf` / `.docx`: CV downloads

## Adding a project

1. Put the HTML under `projects/<category>/`. For notebook exports, strip nbconvert's `<script>`, `<style>`, `<link>`, `class`/`style`/`data-*` attributes, then add the `page.css` link before `</head>`.
2. Add an `<article class="project-row">` to the right `.project-group` in `index.html`, using a `.rank` badge (add `.top` for top-1% or medal finishes), and update the count in the matching `.seg` button. Standout results can also get an `.hl-card` in the home carousel.
3. For a Kaggle result, also add a row to the Kaggle Results table in `resume.html`.
