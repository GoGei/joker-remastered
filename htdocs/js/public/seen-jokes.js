SeenJokes = {};

(function (obj, $) {
    function init() {
        if (!obj.apiURL) {
            loadEmptyPage();
            obj.load_more_jokes = false;
            return;
        }

        obj.loadJokes(true);
    }

    function loadEmptyPage() {
        getEmptyPage().done(function (emptyPageHTML) {
            obj.$mainDiv.html(emptyPageHTML);
            $('#header-navbar').addClass('navbar-transparent');
        });
    }

    function loadJokes(on_init = false) {
        if (!obj.load_more_jokes) {
            return;
        }

        let url = obj.apiURL;
        let baseURL = obj.$mainDiv.data('jokes-url');
        $.ajax({
            url: url,
            method: 'GET',
            data: {
                limit: obj.page_size,
            },
        }).done(function (data) {
            let results = data?.results;

            if ($.isEmptyObject(results) && on_init) {
                obj.load_more_jokes = false;
                obj.loadEmptyPage();
                return;
            }

            let queryString = $.map(results, function (item) {
                return item.id;
            }).join(',');
            $.ajax({
                url: baseURL + `render-items/?jokes=${queryString}`,
                method: 'GET',
                data: {
                    format: 'html'
                },
            }).done(jokeHTML => {
                obj.$container.append(jokeHTML);
            });


            obj.apiURL = data?.next;

            if (!obj.apiURL) {
                obj.load_more_jokes = false;
            }
        }).fail(function (e) {
            obj.loadEmptyPage();
        });
    }

    obj.init = init;
    obj.loadEmptyPage = loadEmptyPage;
    obj.loadJokes = loadJokes;
    obj.page_size = 15;
    obj.load_more_jokes = true;
    obj.$mainDiv = $('#seen-jokes-div');
    obj.apiURL = obj.$mainDiv.data('jokes-url');
    obj.$container = obj.$mainDiv.find('.container');

})(SeenJokes, jQuery);

$(document).ready(function () {
    console.log('seen-jokes.js loaded');
    SeenJokes.init();

    $(window).scroll(function () {
        if ($(window).scrollTop() + $(window).height() === $(document).height()) {
            SeenJokes.loadJokes();
        }
    });
});