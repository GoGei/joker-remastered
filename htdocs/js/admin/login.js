$('span.password-toggler, span.password-toggler i').click(function (e) {
    e.preventDefault();
    let $field = $(this).closest('div').find('input');
    let $icon = $(this).find('i');
    let currentType = $field.attr('type');

    if ('password' === currentType) {
        $field.attr('type', 'text');
        $icon.removeClass('bx-hide').addClass('bx-show');
    } else {
        $field.attr('type', 'password');
        $icon.removeClass('bx-show').addClass('bx-hide');
    }
});
