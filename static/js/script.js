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
function showCategory(category) {
    let cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        if (category === 'all') {
            card.style.display = 'block';
        } else {
            if (card.getAttribute('data-category') === category) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        }
    });
}

function showCategory(category) {
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        const cardCategory = card.getAttribute('data-category').trim().toLowerCase();

        if (category === 'all') {
            card.style.display = 'block';
        } else if (cardCategory === category.toLowerCase()) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function changeSlide(direction) {
    showSlide(currentSlide + direction);
}

// ✅ AUTO SLIDE 
setInterval(() => {
    changeSlide(1);
}, 3000);
function submitFormJSON(event) {
    event.preventDefault();

    const data = {
        name: document.querySelector('[name="name"]').value,
        category: document.querySelector('[name="category"]').value,
        description: document.querySelector('[name="description"]').value,
        image_url: document.querySelector('[name="image_url"]').value,
        quantity: parseInt(document.querySelector('[name="quantity"]').value),
        price: parseFloat(document.querySelector('[name="price"]').value)
    };

    fetch('/api/add-outfit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(response => {
        alert(response.message || response.error);
        window.location.href = "/gallery";
    })
    .catch(error => console.error(error));
}