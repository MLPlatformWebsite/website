// Tracks to search resources for.
var required_tracks = ["AI/ML", "AI and Neural Networks on Arm Summit", "Machine Learning/AI"];
// Local resources JSON file
var resources_file = "/assets/json/resources.json";
// Main function to run once the document is ready/DOM loaded
var items = [];
function extractDateString(dateString) {
    var rx = /(\d\d\d\d)\-(\d\d)\-(\d\d)/g;
    var arr = rx.exec(dateString);
    return arr[0];
}
// Sort function which takes the data array, property to sort by and an asc boolean.
function sort_by_date(a, b) {
    return new Date(b.item_date_published).getTime() - new Date(a.item_date_published).getTime();
}
// This takes and array of items and creates the neccessary page elements
function createPageElements(items){
    var page_elements = [];
    var sorted_items = items.sort(sort_by_date);
    $.each(sorted_items, function (key, val) {
        // Create a new element for resource
        var page_element = "<a href='" + val.item_url + "'>";
        page_element += "<div class='col col-12 col-sm-4 my-4'>";
        page_element += "<div class='resource_block_inner' style='background-image:url(" + val.item_thumbnail + ")'>";
        page_element += "<h3>" + val.item_title + "</h3>";
        page_element += "<small>" + extractDateString(val.item_date_published) + "</small>";
        page_element += "<small>" + val.item_event + "</small>";
        if (val.hasOwnProperty("item_presentation_url")) {
            page_element += "<a class='btn btn-primary' href='" + val.item_presentation_url + "'>Presentation</a>";
        }
        page_element += "<a class='btn btn-primary' href='" + val.item_video_url + "'>Video</a>";
        page_element += "</div>";
        page_element += "</div>";
        page_element += "</a>";
        page_elements.push(page_element);
    });
    return page_elements;
}
$(document).ready(function(){
    // Check if the resources div exists
    if($("#resources").length > 0){
        // Fetch relevant Connect resources
        $.getJSON("https://connect.linaro.org/assets/json/connects.json", function (data) {
            $.each(data, function (key, val) {
                // Get the JSON url for each Linaro Connect
                var json_url = "https://connect.linaro.org/assets/json/" + val.id.toLowerCase() + "/data.json";
                $.getJSON(json_url, function (data) {
                    // Loop through all resources for specific connect
                    $.each(data, function (key, specific_resource) {
                        // Find resources that match the required tracks
                        if (specific_resource.hasOwnProperty("tracks")){
                            // Loop over required tracks
                            $.each(required_tracks, function(key, val){
                                // Check that the resoure contains one of the required tracks
                                if(specific_resource.tracks.indexOf(val) > -1){
                                    var event = specific_resource.event_id.toUpperCase();
                                    // Create a new item
                                    var item = {
                                        item_title: specific_resource.title,
                                        item_url: specific_resource.url,
                                        item_video_url: specific_resource.youtube_video_url,
                                        item_thumbnail: specific_resource.thumbnail,
                                        item_event: "Linaro Connect " + event,
                                        item_date_published: specific_resource.date_published
                                    };
                                    if (specific_resource.hasOwnProperty("amazon_s3_presentation_url")) {
                                        item["item_presentation_url"] = specific_resource.amazon_s3_presentation_url;
                                    }
                                    // Add item to the items array
                                    items.push(item);
                                    // Break out of each loop
                                    return false;
                                }
                            });
                        }
                    });
                });
            });
        });

        // Fetch local JSON
        function loadJSON(callback) {
            var xobj = new XMLHttpRequest();
            xobj.overrideMimeType("application/json");
            xobj.open('GET', '/assets/json/resources.json', true);
            xobj.onreadystatechange = function () {
                if (xobj.readyState == 4 && xobj.status == "200") {
                    callback(xobj.responseText);
                }
            };
            xobj.send(null);
        }
        loadJSON(function (response) {
            // Parse JSON string into object
            var actual_JSON = JSON.parse(response);
            $.each(actual_JSON, function (key, specific_resource) {
                // Get the properties from resource and create a new item
                var item = {
                    item_title: specific_resource.title,
                    item_url: specific_resource.youtube_video_url,
                    item_video_url: specific_resource.youtube_video_url,
                    item_thumbnail: specific_resource.placeholder,
                    item_event: specific_resource.event,
                    item_date_published: specific_resource.date
                };
                if (specific_resource.hasOwnProperty("presentation_url")) {
                    item["item_presentation_url"] = specific_resource.presentation_url;
                }
                // Add item to the items array
                items.push(item);
            });
        });
    }
});
// Display resources once the ajaxStop event is fired
$(document).ajaxStop(function () {
    var page_elements = createPageElements(items);
    $("#resources").html(page_elements);
    $("#resources_count").html(page_elements.length.toString() + " resources found");
});
