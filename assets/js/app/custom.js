$(window).on('load', function () {
    jQuery(function ($) {
        $("#videos-slider").owlCarousel({
            items: 4,
            loop: true,
            dots: false,
            lazyLoad: true,
            nav: true,
            margin: 0,
            autoplay: true,
            autoplayTimeout: 4000,
            autoplayHoverPause: true,
            responsive: {
                0: {
                    items: 1
                },
                560: {
                    items: 2
                },
                700: {
                    items: 3
                }
            }
        });
    });
});
