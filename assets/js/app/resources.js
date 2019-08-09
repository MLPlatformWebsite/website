// This global array stores the concatenated and sorted jsonp data
var allConnectResourcesData = [];
// The counter variable counts the number of times results are added to the allJSONData array
// so we know when to process the concatenated data.
var counter = 0;
// Define the sources to append the jsonp script elements and retreive the data.
var event_data_sources = [
    ""
];
var allJSONData = [];
// Stores the URLS for the JSON data file of each Connect
var connectJSONSources = [];
// Get the connects.json file then pa.titlerse and loop through each connect adding the jsonp script
function connects(connectsJSON) {
    // Loop through the connects.json index JSON file.
    for (i = 0; i < connectsJSON.length; i++) {
        // Get the URL of the Connect Resources JSON file
        var jsonp_url = "https://connect.linaro.org/assets/json/" + connectsJSON[i].id.toLowerCase() + "/data.json?callback=connectResources";
        // Add the new array to the connectJSONSourcs Array
        connectJSONSources.push(jsonp_url);
        // Create a new script element and set the type and src
        script = document.createElement("script");
        script.type = "text/javascript";
        script.src = jsonp_url;
        // Append the new script element to the head.
        $("head").append(script);
    }
}
// This function takes the JSONP data for a specific conncet and concatenates the data.
function connectResources(connectJSON) {
    // Check to see if this is the last source to be loaded in.
    if (counter == (connectJSONSources.length - 1)) {
        console.log(counter);
        // Concat the final data source to the master JSON array
        allConnectResourcesData = allConnectResourcesData.concat(connectJSON);
        // Sort the data by the date
        // Add the resources to the HTML
        listResults(allConnectResourcesData);
        allJSONData = allConnectResourcesData;
        // Add the size of the results
        $('#size').html(allJSONData.length);
        // Run function on each keyup event triggered by the search input
    }
    else {
        allConnectResourcesData = allConnectResourcesData.concat(connectJSON);
        counter += 1;
        console.log(counter);
    }
}
// Simple delay function for use on the search input
var delay = (function () {
    var timer = 0;
    return function (callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    };
})();
// Main function to run once the document is ready/DOM loaded
$(document).ready(function(){
    if($("#resources").length > 0){
        // Get the JSONP url of the main connects.json file.
        var jsonp_url = "https://connect.linaro.org/assets/json/connects.json?callback=connects";
        // Add the JSONP to a script element
        // Create a new script element and set the type and src
        script = document.createElement("script");
        script.type = "text/javascript";
        script.src = jsonp_url;
        // Append the new script element to the head.
        $("head").append(script);
        // Detect when the user has stopped typing then show the results.
        // $('#search-query').keyup(function () {
        //     delay(function () {
        //         listResults(allConnectResourcesData);
        //     }, 1000);
        // });
        // Enable Bootstrap tooltips for displaying details of resources
        $(function () {
            $('[data-toggle="tooltip"]').tooltip({ container: 'body' });
        });
    }
});
