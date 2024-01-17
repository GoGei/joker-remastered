function getEmptyPage() {
    /*usage
    getEmptyPage().done(function (emptyPageHTML) {
        do the staffs
    });*/
    return $.ajax({
        url: $('#main-container').data('empty-page-api-url'),
        method: 'GET'
    });
}