function showCategory(category) {
    const sections = document.querySelectorAll(".tab-content");
    sections.forEach(section => {
        section.style.display = "none";
    });

    document.getElementById(category).style.display = "flex";
}
