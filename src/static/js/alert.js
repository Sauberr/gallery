
var alert = document.querySelector('.alert-warning, .alert-success, .alert-error');

    setTimeout( function () {
        if (alert) {
            alert.style.display = 'none';
        }
    }, 2500);