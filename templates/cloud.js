$(document).ready(function(e){
    var words = [
        {text: "Lorem", weight: 13},
        {text: "Ipsum", weight: 10.5},
        {text: "Dolor", weight: 9.4},
        {text: "Sit", weight: 8},
        {text: "Amet", weight: 6.2},
        {text: "Consectetur", weight: 5},
        {text: "Adipiscing", weight: 5},
        /* ... */
    ];

    generateCloud(words);
});

$.fn.api.settings.api = {
    'submit query': '/api/v1/{query}/wc',
};

var submitQuery = function(e){
    const query = $('input').val().replaceAll(' ', '%20');
    $.get({
        url: 'localhost:5000/api/v1/'+query+'/wc',
        success: processData(res),
        dataType: 'json',
    })
};

var processData = function(res){
    generateCloud(res.counts[0]);
    $('#summary').innerText(res.summaries[0]);
};

var generateCloud = function(words){
    const $cloud = $('#wordCloud');
    $cloud.jQCloud(words, {
        height: $cloud.parent().innerWidth()/2,
        width: $cloud.parent().innerWidth()-100,
    });
}