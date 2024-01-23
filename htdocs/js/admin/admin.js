function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    xhrFields: {withCredentials: true},
    headers: {'X-CSRFToken': getCookie('csrftoken')},
});


$(document).ready(function () {
    $('li.breadcrumb-item').last().addClass('active');
});


/*
$('input[type="password"]').click(function (e) {
    e.preventDefault();
    let $field = $(this);
    let $icon = $field.find('i');
    let currentType = $field.attr('type');
    if ('password' === currentType) {
        $field.attr('type', 'text');
        $icon.removeClass('bx-hide');
        $icon.addClass('bx-show');
    } else {
        $field.attr('type', 'password');
        $icon.addClass('bx-hide');
        $icon.removeClass('bx-show');
    }
})*/


