$('#main-joke-button').on('click', function (e) {
        e.preventDefault();
        let $button = $(this);
        let apiURL = $button.attr('href');

        $.ajax({
            url: apiURL,
            method: 'GET',
        }).done(function (data, status, xhr) {
            let $container = $('#joke-container');
            if (xhr?.status == 200) {
                $container.html(data?.text);
            } else if (xhr?.status == 202) {
                $container.html(data?.text);
                $('#main-clear-seen-jokes-button').show();
            }
            $('html, body').animate({scrollTop: 500}, 500);
        })
    }
)

$('#main-clear-seen-jokes-button').on('click', function (e) {
        e.preventDefault();
        let $button = $(this);
        let apiURL = $button.attr('href');

        $.ajax({
            url: apiURL,
            method: 'POST',
        }).done(function () {
            $button.hide();
        })
    }
)