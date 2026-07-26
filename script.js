document.addEventListener('DOMContentLoaded', function () {
    const card = document.getElementById('businessCard');

    card.addEventListener('click', function (e) {
        // If user clicks a link (socials, email, CV), don't flip the card
        if (e.target.closest('a')) {
            return;
        }

        // Click anywhere else on front/back or on the "Front ↺" button flips it back
        card.classList.toggle('is-flipped');
    });

    // Keyboard support (Space / Enter)
    card.addEventListener('keydown', function (e) {
        if ((e.key === 'Enter' || e.key === ' ') && !e.target.closest('a')) {
            e.preventDefault();
            card.classList.toggle('is-flipped');
        }
    });
});