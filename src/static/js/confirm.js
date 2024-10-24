
function toggleConfirmButton() {
    var agreement = document.getElementById('agreement');
    var confirmButton = document.getElementById('confirmButton');

    if (agreement.checked) {
        confirmButton.disabled = false;
        confirmButton.style.opacity = 1;
    } else {
        confirmButton.disabled = true;
        confirmButton.style.opacity = 0.5;
    }
}