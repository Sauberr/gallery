$(document).on('submit', '#contact-form-ajax', function (e) {
    e.preventDefault();
    console.log('Form submitted');

    let full_name = $('#full_name').val();
    let email = $('#email').val();
    let message = $('#message').val();
    let csrf_token = $('[name=csrfmiddlewaretoken]').val();

    console.log('Name:', full_name);
    console.log('Email:', email);
    console.log('Message:', message);

    $.ajax({
        url: '/ajax-contact-form/',
        type: 'POST',
        data: {
            'full_name': full_name,
            'email': email,
            'message': message,
            'csrfmiddlewaretoken': csrf_token
        },
        dataType: 'json',
        beforeSend: function () {
        },
        success: function (res) {
            console.log('Data sent successfully');
            if (res.data.bool) {
                $('button[type="submit"]').html('<i class="fa-solid fa-check"></i>');
                showNotification();
            } else {
            }
        },
    });
});