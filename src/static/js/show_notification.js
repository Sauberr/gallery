function showNotification() {
    const banner = $('#notification-banner');
    const timer = $('#notification-timer');
    banner.show();
    timer.css('width', '100%');
    timer.animate({ width: '0%' }, 5000, function() {
        banner.hide();
    });
}