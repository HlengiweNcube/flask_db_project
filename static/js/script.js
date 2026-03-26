function showCategory(category) {
    const sections = document.querySelectorAll(".tab-content");
    sections.forEach(section => {
        section.style.display = "none";
    });

    document.getElementById(category).style.display = "flex";
}
// Interaction 1: alert on page load
console.log("Website loaded");

// Interaction 2: simple form validation
function validateForm() {
    let name = document.getElementById("name").value;

    if (name === "") {
        alert("Name is required!");
        return false;
    }
}

// Interaction 3: DOM manipulation
function changeTitle() {
    document.querySelector("h2").innerText = "Welcome to African Fashion!";
}