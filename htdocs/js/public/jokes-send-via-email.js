$('body').on('click', '.send-joke-via-email', function (e) {
    let url = $(this).parent().data("send-via-email-joke-url");
    let $form = getForm();
    $form.attr("action", url);
    clearErrors();
});

$('.joke-send-form').submit(function (e) {
    e.preventDefault();

    let formData = $(this).serialize();
    let url = $(this).attr("action");

    clearErrors();

    $.post(url, formData)
        .done(function (data) {
            closeModal();
            clearErrors();
        })
        .fail(function (xhr, status, error) {
            let $form = getForm();
            Object.entries(xhr.responseJSON).map(function ([key, value]) {
                $form.find(`#${key}`).after('<div class="text-danger">' + value + '</div>');
            });
        });
});

function getModal() {
    return $('#sendJokeViaEmail');
}

function getForm() {
    return getModal().find('form');
}

function closeModal() {
    let $modal = getModal();
    $modal.modal('hide');
}

function clearErrors() {
    $('.text-danger').remove();
}