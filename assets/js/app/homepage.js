
$(document).ready(function () {
    
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

    // Check for modal close event
    $(".closeVideo").on('click', function () {
        // Reload Iframe
        var iframe = document.getElementById("promoVideo");
        iframe.src = iframe.src;
        console.log($("#youtube-container").attr("data-embed"));
        console.log("Closed and paused.");
    });


});