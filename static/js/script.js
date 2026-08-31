// Client-side enhancements stay optional: all important operations work without JavaScript.

// Wait until the DOM is ready before attaching event listeners.
document.addEventListener("DOMContentLoaded", () => {

    // Validate dispatch amount before the form submits to the /dispatch/<id> route.
    // Prevents a server round-trip for obviously invalid input (non-integer or < 1).
    document.querySelectorAll(".dispatch-form").forEach(form => {
        form.addEventListener("submit", event => {
            const amount = Number(form.elements.amount.value);
            if (!Number.isInteger(amount) || amount < 1) {
                event.preventDefault();
                alert("Enter a whole number greater than zero.");
            }
        });
    });

    // Require explicit confirmation before a delete form is submitted.
    // This guards against accidental clicks because the delete action is irreversible.
    document.querySelectorAll(".delete-form").forEach(form => {
        form.addEventListener("submit", event => {
            if (!window.confirm("Are you sure you want to delete this outfit?")) {
                event.preventDefault();
            }
        });
    });
});

// Update the rename and delete form actions whenever a different image is selected
// in the image-management dropdown on the categories page.
// The filename is URL-encoded so that filenames with spaces or special characters work correctly.
function updateImageActions(select) {
    const filename = encodeURIComponent(select.value);
    document.getElementById("rename-image-form").action = `/images/${filename}/rename`;
    document.getElementById("delete-image-form").action = `/images/${filename}/delete`;
    document.getElementById("rename-image-name").value = select.value;
}