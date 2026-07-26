document.addEventListener('DOMContentLoaded', function () {
    const card = document.getElementById('businessCard');

    // Flip card on click
    card.addEventListener('click', function () {
        card.classList.toggle('is-flipped');
    });

    // Support keyboard accessibility (Space / Enter to flip)
    card.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            card.classList.toggle('is-flipped');
        }
    });
});