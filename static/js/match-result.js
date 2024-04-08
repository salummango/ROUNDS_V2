// match-results.js

// Get the modal element
const modal = document.querySelector(".modal");
// Get the button that opens the modal
const detailsBtn = document.querySelectorAll(".details-btn");
// Get the <span> element that closes the modal
const closeBtn = document.querySelector(".close-btn");

// Function to open the modal
function openModal() {
    modal.style.display = "flex";
}

// Function to close the modal
function closeModal() {
    modal.style.display = "none";
}

// Event listener for each "View Details" button to open the modal
detailsBtn.forEach(btn => {
    btn.addEventListener("click", openModal);
});

// Event listener for the close button to close the modal
closeBtn.addEventListener("click", closeModal);
// Event listener for clicking outside the modal to close it
window.addEventListener("click", (e) => {
    if (e.target === modal) {
        closeModal();
    }
});