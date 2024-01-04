$('#passwordToggler').click(function (e) {
    e.preventDefault();
    let $field = $('#password');
    let $icon = $(this).find('i');
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
})