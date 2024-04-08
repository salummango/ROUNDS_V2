// JavaScript code for dashboard interactivity

// Add event listener to toggle previous fixtures
document.getElementById('toggle-previous-fixtures').addEventListener('click', function() {
    var previousFixtures = document.getElementById('previous-fixtures');
    previousFixtures.classList.toggle('hidden');
});

// Add event listener to toggle next fixtures
document.getElementById('toggle-next-fixtures').addEventListener('click', function() {
    var nextFixtures = document.getElementById('next-fixtures');
    nextFixtures.classList.toggle('hidden');
});