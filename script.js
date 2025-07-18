// Dark mode toggle functionality
function setupDarkMode() {
    // Create the toggle button
    const toggle = document.createElement('button');
    toggle.id = 'dark-mode-toggle';
    toggle.innerHTML = '<i class="bx bx-moon"></i>';
    toggle.setAttribute('aria-label', 'Toggle dark mode');
    toggle.title = 'Toggle dark mode';
    
    // Add the button to the page
    document.body.appendChild(toggle);
    
    // Check for saved user preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
      document.body.classList.add('dark-mode');
      toggle.innerHTML = '<i class="bx bx-sun"></i>';
    }
    
    // Toggle functionality
    toggle.addEventListener('click', () => {
      document.body.classList.toggle('dark-mode');
      
      // Update the icon
      if (document.body.classList.contains('dark-mode')) {
        toggle.innerHTML = '<i class="bx bx-sun"></i>';
        localStorage.setItem('theme', 'dark');
      } else {
        toggle.innerHTML = '<i class="bx bx-moon"></i>';
        localStorage.setItem('theme', 'light');
      }
    });
  }
  
// Back to top button functionality
function setupBackToTop() {
  const backToTopButton = document.getElementById('back-to-top');
  
  // Back to top button visibility
  function toggleBackToTop() {
    if (window.scrollY > 300) {
      backToTopButton.classList.add('show');
    } else {
      backToTopButton.classList.remove('show');
    }
  }
  
  // Scroll event listener
  window.addEventListener('scroll', toggleBackToTop);
  
  // Back to top click handler
  backToTopButton.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

// Run when DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
  setupDarkMode();
  setupBackToTop();
});