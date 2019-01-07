var youtube = document.querySelectorAll(".youtube");

for (var i = 0; i < youtube.length; i++) {
    var source = "https://img.youtube.com/vi/" + youtube[i].dataset.embed + "/sddefault.jpg";
    var image = new Image();
    image.src = source;
    image.addEventListener("load", function () {
        youtube[i].appendChild(image);
    }(i));

    youtube[i].addEventListener("click", function () {
        var iframe = document.createElement("iframe");
        iframe.setAttribute("frameborder", "0");
        iframe.setAttribute("id", "promoVideo");
        iframe.setAttribute("allowfullscreen", "");
        iframe.setAttribute("src", "https://www.youtube.com/embed/" + this.dataset.embed + "?rel=0&showinfo=0&autoplay=1");
        this.appendChild(iframe);
        $(".youtube img").hide();
        $(".youtube .play-button").hide();
    });
}
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
