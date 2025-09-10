// Professional portfolio functionality with enhanced UX
document.addEventListener('DOMContentLoaded', function() {
    // Create dark mode toggle button
    const toggleButton = document.createElement('button');
    toggleButton.className = 'dark-mode-toggle';
    toggleButton.setAttribute('aria-label', 'Toggle light mode');
    toggleButton.setAttribute('title', 'Switch to light mode');
    toggleButton.innerHTML = '☀️';
    document.body.appendChild(toggleButton);

    // Check for saved theme preference - default to dark mode (navy)
    const savedTheme = localStorage.getItem('theme') || 'dark';
    
    if (savedTheme === 'light') {
        document.body.classList.remove('dark-mode');
        toggleButton.innerHTML = '🌙';
        toggleButton.setAttribute('aria-label', 'Toggle dark mode');
        toggleButton.setAttribute('title', 'Switch to dark mode');
    } else {
        document.body.classList.add('dark-mode');
        toggleButton.innerHTML = '☀️';
        toggleButton.setAttribute('aria-label', 'Toggle light mode');
        toggleButton.setAttribute('title', 'Switch to light mode');
    }

    // Toggle theme functionality
    toggleButton.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        
        if (document.body.classList.contains('dark-mode')) {
            localStorage.setItem('theme', 'dark');
            toggleButton.innerHTML = '☀️';
            toggleButton.setAttribute('aria-label', 'Toggle light mode');
            toggleButton.setAttribute('title', 'Switch to light mode');
        } else {
            localStorage.setItem('theme', 'light');
            toggleButton.innerHTML = '🌙';
            toggleButton.setAttribute('aria-label', 'Toggle dark mode');
            toggleButton.setAttribute('title', 'Switch to dark mode');
        }
    });

    // Add smooth scroll behavior for any future anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add subtle animation delays for cards on scroll (progressive enhancement)
    const observeElements = () => {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 100);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        // Observe project cards and highlights for subtle fade-in
        document.querySelectorAll('.project, .highlight').forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(el);
        });
    };

    // Initialize animations only if user hasn't disabled them
    if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        observeElements();
    }

    // Add keyboard navigation support
    document.addEventListener('keydown', function(e) {
        // Toggle theme with Ctrl/Cmd + D
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            toggleButton.click();
        }
    });

    // Add tech-style loading effect for skill pills
    const addSkillHighlights = () => {
        const highlights = document.querySelectorAll('.highlight');
        highlights.forEach(highlight => {
            const strongElements = highlight.querySelectorAll('strong');
            strongElements.forEach(element => {
                if (element.textContent.includes(':')) {
                    element.style.color = 'var(--accent-color)';
                    element.style.fontFamily = 'var(--font-mono)';
                    element.style.fontSize = '0.95em';
                }
            });
        });
    };

    // Add subtle typing animation to tagline
    const animateTagline = () => {
        const tagline = document.querySelector('.tagline');
        if (tagline && !tagline.classList.contains('animated')) {
            tagline.classList.add('animated');
            const text = tagline.textContent.replace('> ', '');
            tagline.textContent = '> ';
            
            let i = 0;
            const typeWriter = () => {
                if (i < text.length) {
                    tagline.textContent += text.charAt(i);
                    i++;
                    setTimeout(typeWriter, 100);
                }
            };
            
            setTimeout(typeWriter, 500);
        }
    };

    // Initialize enhancements
    setTimeout(() => {
        addSkillHighlights();
        animateTagline();
    }, 300);

    // Add particle effect on hover for profile picture
    const profilePic = document.querySelector('.profile-pic');
    if (profilePic) {
        profilePic.addEventListener('mouseenter', function() {
            this.style.filter = 'brightness(1.1) saturate(1.2)';
        });
        
        profilePic.addEventListener('mouseleave', function() {
            this.style.filter = 'brightness(1) saturate(1)';
        });
    }

    // Update last updated timestamp from GitHub
    const updateTimestamp = async () => {
        try {
            const response = await fetch('https://api.github.com/repos/rbkrs/rbkrs.github.io/commits?per_page=1');
            if (response.ok) {
                const commits = await response.json();
                if (commits.length > 0) {
                    const lastCommitDate = new Date(commits[0].commit.author.date);
                    const day = String(lastCommitDate.getDate()).padStart(2, '0');
                    const month = String(lastCommitDate.getMonth() + 1).padStart(2, '0');
                    const year = lastCommitDate.getFullYear();
                    const hours = String(lastCommitDate.getHours()).padStart(2, '0');
                    const minutes = String(lastCommitDate.getMinutes()).padStart(2, '0');
                    
                    const timestamp = `${day}-${month}-${year} ${hours}:${minutes}`;
                    const lastUpdatedElement = document.getElementById('last-updated');
                    if (lastUpdatedElement) {
                        lastUpdatedElement.textContent = `Last updated: ${timestamp}`;
                    }
                }
            } else {
                const lastUpdatedElement = document.getElementById('last-updated');
                if (lastUpdatedElement) {
                    lastUpdatedElement.textContent = 'Last updated: GitHub API unavailable';
                }
            }
        } catch (error) {
            const lastUpdatedElement = document.getElementById('last-updated');
            if (lastUpdatedElement) {
                lastUpdatedElement.textContent = 'Last updated: Unable to fetch';
            }
        }
    };

    // Set initial timestamp
    updateTimestamp();
});