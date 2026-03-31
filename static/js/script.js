function showCategory(category) {
    let cards = document.querySelectorAll(".card");

    cards.forEach(card => {
        if (category === "all" || card.dataset.category === category) {
            card.style.display = "block";
        } else {
            card.style.display = "none";
        }
    });
}
console.log("Website loaded");

function validateForm() {
    let name = document.getElementById("name").value;

    if (name === "") {
        alert("Name is required!");
        return false;
    }
}

function changeTitle() {
    document.querySelector("h2").innerText = "Welcome to African Fashion!";
}
let currentSlide = 0;

function showSlide(index) {
    let slides = document.querySelectorAll(".slide");

    if (index >= slides.length) currentSlide = 0;
    if (index < 0) currentSlide = slides.length - 1;

    slides.forEach(slide => slide.classList.remove("active"));

    slides[currentSlide].classList.add("active");
}

function changeSlide(direction) {
    currentSlide += direction;
    showSlide(currentSlide);
}
