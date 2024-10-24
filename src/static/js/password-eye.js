
function togglePasswordVisibility(icon) {
    let inputPass = icon.nextElementSibling;
    if (inputPass.getAttribute('type') === 'password') {
        inputPass.setAttribute('type', 'text');
        icon.innerHTML = '<ion-icon name="lock-open"></ion-icon>';
    } else {
        inputPass.setAttribute('type', 'password');
        icon.innerHTML = '<ion-icon name="lock-closed"></ion-icon>';
    }
}