$(document).ready(function(e){
});

var processData = function(res){
    console.log(res);
    generateCloud(res.counts[0]);
    $('#summary').innerText(res.summaries[0]);
};

var submitQuery = function (e) {
    console.log($('input').val().replace(' ', '%20'));
    const query = $('input').val().trim().replace(' ', '%20');
    $.get('http//localhost:5000/api/v1/' + query + '/wc', processData);
};
var generateCloud = function(words){
    const $cloud = $('#wordCloud');

    $cloud.jQCloud(words, {
        height: $cloud.parent().innerWidth()/2,
        width: $cloud.parent().innerWidth()-100,
    });
};