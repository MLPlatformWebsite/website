$(document).ready(function() {
  if ($("#connect_resources_embed").length > 0) {
    var session_id = $("#connect_resources_embed").data("session-id");
    console.log(session_id);
    var connect_id = $("#connect_resources_embed").data("connect-id");
    console.log(connect_id);
    var connect_url =
      "https://connect.linaro.org/assets/json/" +
      connect_id.toLowerCase() +
      "/data.json";
    $.getJSON(connect_url, function(data) {
      $.each(data, function(key, val) {
        if (val.session_id == session_id.toUpperCase()) {
          console.log(val);
          var youtube_video = val.youtube_video_url;
          var presentation = val.amazon_s3_presentation_url;

          function getId(url) {
            var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
            var match = url.match(regExp);

            if (match && match[2].length == 11) {
              return match[2];
            } else {
              return "error";
            }
          }
          // Get the ID for the YouTube video.
          var youtubeId = getId(youtube_video);
          // Create the YouTube embed url
          var embedUrl = "//www.youtube.com/embed/" + youtubeId;
          // Set the src to the YouTube emebd url
          $("#youtube-iframe").attr("src", embedUrl);

          $("#youtube-iframe").on("load", function() {
            $("#video-embed").removeClass("hidden-iframe");
            $(this).removeClass("hidden-iframe");
            $("#video-skeleton").hide();
            $(this).addClass("visible-iframe");
            $("#video-embed").addClass("visible-iframe");
          });

          $("#presentation-data-embed").attr("src", presentation);
          // Set the src to the data-src
          $("#presentation-data-embed").ready(function() {
            $("#presentation-embed").removeClass("hidden-iframe");
            $("#presentation-data-embed").removeClass("hidden-iframe");
            $("#presentation-skeleton").hide();
            $("#presentation-embed").addClass("visible-iframe");
            $("#presentation-data-embed").addClass("visible-iframe");
          });
        }
      });
    });
  }
});
