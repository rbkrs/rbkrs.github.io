# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal portfolio website for Robin (R.P.M.) Kras, hosted on GitHub Pages. The site showcases data science and machine learning projects, education, skills, and achievements primarily from Kaggle competitions.

## Architecture

The site is built with vanilla HTML, CSS, and JavaScript:

- **`index.html`**: Main portfolio page with sections for about, skills, education, languages, and projects
- **`styles.css`**: Complete styling with CSS custom properties for theming, including dark mode support
- **`script.js`**: Dark mode toggle functionality with localStorage persistence
- **`projects/`**: Directory containing individual project pages (HTML files) and a model-explainer tool
- **`face.png`**: Profile picture
- **`RPM_Kras-resume.pdf`**: Resume file for download

## Key Features

### Dark Mode System
- Implemented via CSS custom properties (CSS variables) in `:root` and `body.dark-mode`
- Toggle button created dynamically in `script.js` with localStorage persistence
- Smooth transitions between light and dark themes

### Project Structure
- Project pages are individual HTML files in the `projects/` directory
- Each project shows versions, rankings, and performance improvements
- Special styling for score changes and explanations with accent colors

### Model Explainer Tool
Located in `projects/model-explainer/`:
- Python-based tool (`model_analyzer.py`) for analyzing ML models in Jupyter notebooks
- Web interface (`index.html`) for browser-based analysis
- Can parse `.ipynb` files and HTML exports to detect models, hyperparameters, and datasets

## Development Notes

### CSS Structure
- Uses CSS custom properties extensively for theming
- Consistent card-based design with hover effects
- Responsive grid layouts for projects, skills, and languages
- Mobile-responsive with media queries at 768px and 480px breakpoints

### No Build Process
This is a static site with no build tools, package managers, or dependencies. All files are served directly.

### Content Management
- Project information is hardcoded in HTML
- Kaggle competition results and rankings are manually maintained
- Projects link to standalone HTML files with detailed analysis

## GitHub Pages Deployment

The site is deployed via GitHub Pages using the main branch. The CNAME file configures the custom domain.

## Working with Projects

When adding new projects:
1. Create HTML file in `projects/` directory
2. Update the project grid in `index.html`
3. Follow existing styling patterns for consistency
4. Include ranking information and performance metrics where applicable