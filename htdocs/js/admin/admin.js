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
