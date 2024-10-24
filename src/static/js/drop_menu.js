document.querySelector('.dropdown').addEventListener('click', function(event) {event.stopPropagation();
    this.querySelector('.dropdown-content').classList.toggle('show');
});

window.addEventListener('click', function() {
    document.querySelector('.dropdown-content').classList.remove('show');
});