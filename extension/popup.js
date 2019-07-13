$(document).ready(function() {
    var youtubeURL = ""
chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
    youtubeURL = (tabs[0].url);
    });
    $("button").click(function() {
        var xhr = new XMLHttpRequest();
        var url = "http://localhost:5000/send_youtube_url";
        xhr.open("POST", url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                var json = JSON.parse(xhr.responseText);
            }
        };
        var data = JSON.stringify({
            "youtube_url": youtubeURL
        });
        xhr.send(data);
    });
});