# Rob Kras

A personal portfolio website showcasing data science and machine learning projects, Kaggle competition achievements, and technical skills.

🌐 **Live Site**: [robkras.com](https://robkras.com) OR [rbkrs.github.io](https://rbkrs.github.io)

## Overview

This is a static website built with vanilla HTML, CSS, and JavaScript, hosted on GitHub Pages. It showcases Robin (R.P.M.) Kras's work in data science, machine learning, and AI, including competition results from Kaggle and various project implementations.

## Features

- **Responsive Design**: Optimized for desktop and mobile viewing
- **Dark Mode**: Toggle between light and dark themes with localStorage persistence
- **Project Showcase**: Individual pages for each machine learning project
- **Kaggle Integration**: Competition rankings and performance metrics
- **Model Explainer Tool**: Interactive tool for analyzing ML models in Jupyter notebooks

## Project Structure

```
rbkrs.github.io/
├── index.html              # Main portfolio page
├── styles.css              # Complete styling with CSS custom properties
├── script.js               # Dark mode toggle functionality
├── face.png                # Profile picture
├── RPM_Kras-resume.pdf     # Resume download
├── CNAME                   # Custom domain configuration
├── projects/               # Individual project pages
│   ├── *.html              # Project analysis pages
│   ├── MLWorkflow.pdf      # Machine learning workflow document
│   └── model-explainer/    # Interactive model analysis tool
│       ├── index.html      # Web interface
│       ├── model_analyzer.py # Python analysis tool
│       └── requirements.txt # Python dependencies
└── CLAUDE.md               # AI assistant instructions
```

## Technology Stack

- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Styling**: CSS Custom Properties (variables) for theming
- **Icons**: Boxicons for social media and UI elements
- **Hosting**: GitHub Pages with custom domain
- **Analytics Tool**: Python-based model explainer with Jupyter notebook support

## Key Sections

### About
Brief introduction and professional summary

### Skills
- **Programming**: Python, C, C++, Scala, Assembly
- **Technical**: Keras, NumPy, Pandas, TensorFlow, PyTorch, SQL/MySQL, NLP, HuggingFace transformers
- **Tools**: Git, Docker, Jupyter, various data science libraries

### Education
Academic background and relevant coursework

### Languages
Proficiency in multiple languages

### Projects
Portfolio of machine learning and data science projects including:
- Kaggle competition solutions
- Predictive modeling projects
- Data analysis and visualization
- Neural network implementations

## Dark Mode Implementation

The site features a sophisticated dark mode system:
- CSS custom properties for seamless theme switching
- localStorage persistence across sessions
- Smooth transitions between light and dark themes
- Dynamically created toggle button

## Model Explainer Tool

Located in `projects/model-explainer/`, this tool provides:
- Analysis of Jupyter notebooks (`.ipynb` files)
- HTML export parsing for model detection
- Hyperparameter extraction
- Dataset identification
- Web-based interface for easy access

## Development

This is a static site with no build process or dependencies. To develop locally:

1. Clone the repository
2. Open `index.html` in a web browser
3. Make changes to HTML, CSS, or JavaScript files
4. Refresh the browser to see updates

## Adding New Projects

To add a new project:
1. Create an HTML file in the `projects/` directory
2. Update the project grid in `index.html`
3. Follow existing styling patterns for consistency
4. Include performance metrics and rankings where applicable

## Deployment

The site is automatically deployed via GitHub Pages when changes are pushed to the main branch. The custom domain is configured through the CNAME file.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contact

- **Email**: robkraseu@gmail.com
- **LinkedIn**: [Robin Kras](https://www.linkedin.com/in/robin-r-p-m-kras-8b4bb31bb/)
- **GitHub**: [rbkrs](https://github.com/rbkrs)
- **Kaggle**: [robkraseu](https://www.kaggle.com/robkraseu)
