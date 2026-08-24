// Client-side enhancements stay optional: all important operations work without JavaScript.
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".dispatch-form").forEach(form => {
        form.addEventListener("submit", event => {
            const amount = Number(form.elements.amount.value);
            if (!Number.isInteger(amount) || amount < 1) {
                event.preventDefault();
                alert("Enter a whole number greater than zero.");
            }
        });
    });

    document.querySelectorAll(".delete-form").forEach(form => {
        form.addEventListener("submit", event => {
            if (!window.confirm("Are you sure you want to delete this outfit?")) {
                event.preventDefault();
            }
        });
    });
});