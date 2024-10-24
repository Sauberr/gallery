function togglePasswordVisibility(icon) {
    let inputPass = icon.previousElementSibling;
    if (inputPass.getAttribute('type') === 'password') {
        inputPass.setAttribute('type', 'text');
        icon.innerHTML = '<i class="fas fa-lock-open"></i>';
    } else {
        inputPass.setAttribute('type', 'password');
        icon.innerHTML = '<i class="fas fa-lock"></i>';
    }
}

document.querySelectorAll('.input-box .icon').forEach(icon => {
    icon.addEventListener('click', function() {
        togglePasswordVisibility(this);
    });
});