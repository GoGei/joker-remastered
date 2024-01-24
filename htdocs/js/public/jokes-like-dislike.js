const LIKED_CLASS = 'liked';
const DISLIKED_CLASS = 'disliked';
const ANIMATE_SPEED = 100;


$('body').on('click', '.joke-like', function (e) {
    e.preventDefault();

    let $likedElem = $(this)
    let $parentDiv = getParentDiv($likedElem);
    let $dislikedElem = $parentDiv.find('.joke-dislike');

    if (!$likedElem.hasClass(LIKED_CLASS)) {
        likeJoke($likedElem, $dislikedElem);
    } else {
        deactivateJoke($likedElem, $dislikedElem);
    }
});

$('body').on('click', '.joke-dislike', function (e) {
    e.preventDefault();

    let $dislikedElem = $(this)
    let $parentDiv = getParentDiv($dislikedElem);
    let $likedElem = $parentDiv.find('.joke-like');

    if (!$dislikedElem.hasClass(DISLIKED_CLASS)) {
        dislikeJoke($likedElem, $dislikedElem);
    } else {
        deactivateJoke($likedElem, $dislikedElem);
    }
});

function likeJoke($likedElem, $dislikedElem) {
    let $parentDiv = getParentDiv($likedElem);
    let url = $parentDiv.data('like-joke-url');

    $.ajax({
        url: url,
        method: 'POST',
    }).done(function () {
        addClsAnimated($likedElem, LIKED_CLASS);
        removeClsAnimated($dislikedElem, DISLIKED_CLASS);
    }).fail(function (error) {
        console.log('error', error);
    });
}

function dislikeJoke($likedElem, $dislikedElem) {
    let $parentDiv = getParentDiv($likedElem);
    let url = $parentDiv.data('dislike-joke-url');

    $.ajax({
        url: url,
        method: 'POST',
    }).done(function () {
        removeClsAnimated($likedElem, LIKED_CLASS);
        addClsAnimated($dislikedElem, DISLIKED_CLASS);
    }).fail(function (error) {
        console.log('error', error);
    });
}

function deactivateJoke($likedElem, $dislikedElem) {
    let $parentDiv = getParentDiv($likedElem);
    let url = $parentDiv.data('deactivate-joke-url');

    $.ajax({
        url: url,
        method: 'POST',
    }).done(function () {
        removeClsAnimated($likedElem, LIKED_CLASS);
        removeClsAnimated($dislikedElem, DISLIKED_CLASS);
    }).fail(function (error) {
        console.log('error', error);
    });
}

function getParentDiv($elem) {
    return $elem.closest('.joke-container');
}

function removeClsAnimated($elem, cls) {
    if (!$elem.hasClass(cls)) {
        return;
    }

    $elem.animate({
        opacity: 0
    }, ANIMATE_SPEED, function () {
        $elem.removeClass(cls).animate({
            opacity: 1
        }, ANIMATE_SPEED);
    });
}

function addClsAnimated($elem, cls) {
    if ($elem.hasClass(cls)) {
        return;
    }

    $elem.animate({
        opacity: 0
    }, ANIMATE_SPEED, function () {
        $elem.addClass(cls).animate({
            opacity: 1
        }, ANIMATE_SPEED);
    });
}