$(document).ready(function(e) {
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

    const $cloud = $('#wordCloud');

    $cloud.jQCloud(words, {
        height: $cloud.parent().innerWidth() / 2,
        width: $cloud.parent().innerWidth() - 100,
    });


    $('#queryInput').keyup(function(e){
       if(e.keyCode == 13){
           submitQuery();
       };
    });
});

var processData = function(res){
    console.log(res);
    generateCloud(blah(res.counts));
    $('#summary').html(res.summaries);
    $('#linkHere').html('<a href="'+ res.urls + '">' + $('input').val().trim() + '</a>');
};

var submitQuery = function (e) {
    console.log($('input').val().replace(' ', '%20'));
    const query = $('input').val().trim().replace(' ', '%20');
    $.get('http://127.0.0.1:5000/api/v1/wiki/' + query + '/wc', processData);
};

var generateCloud = function(words){
    const $cloud = $('#wordCloud');
    $cloud.jQCloud('update', words);
};


function blah(list) {
  var result = [];
  for (var key in list) {
    if(key!==$('input').val().trim()){
      result.push({
        text: key,
        weight: list[key]
      });
    }
  }
  return result;
}
