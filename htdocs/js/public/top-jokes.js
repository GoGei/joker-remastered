$(document).ready(function () {
    let $container = $('#top-jokes-div');



    getEmptyPage().done(function (emptyPageHTML) {
        let $html = emptyPageHTML;
        if ($html) {
            $container.html($html);
        }
    });


    // $(window).scroll(function () {
    //     if ($(window).scrollTop() + $(window).height() >= $(document).height() - 100) {
    //         // let apiURL = $container.data('api-url');
    //         // if (apiURL) {
    //         //     loadMoreItems(apiURL);
    //         // } else {
    //             let $emptyPageHTML = getEmptyPage();
    //             if ($emptyPageHTML) {
    //                 $container.html($emptyPageHTML);
    //             }
    //         // }
    //     }
    // });
});

function loadMoreItems(apiURL) {
    $.ajax({
        url: apiURL,
        method: 'GET',
        success: function (data) {
            // Append the new items to the item-list
            $('#item-list').append(data);
        }
    });
}