$(document).ready(function(e) {
  var words = [{
      text: "Lorem",
      weight: 13
    }, {
      text: "Ipsum",
      weight: 10.5
    }, {
      text: "Dolor",
      weight: 9.4
    }, {
      text: "Sit",
      weight: 8
    }, {
      text: "Amet",
      weight: 6.2
    }, {
      text: "Consectetur",
      weight: 5
    }, {
      text: "Adipiscing",
      weight: 5
    },
    /* ... */
  ];

  var $cloud = $('#wordCloud');

  $cloud.jQCloud(words, {
    height: $cloud.parent().innerWidth() / 2,
    width: $cloud.parent().innerWidth() - 100,
  });

  $('.ui.search').search({
    apiSettings: {
      url: 'api/v1/query/{query}'
    },
    searchFields   : [
      'title'
    ],
    searchFullText: true,
    onSelect: function () {
      console.log('query');
      submitQuery();
    }
  });

  $('.ui.search').keyup(function(e) {
    if (e.keyCode == 13) {
      submitQuery();
      $('.ui.search').search('cancel query');
    }

  });
});

var processData = function(res, status) {
  generateCloud(blah(res.counts));
  $('#summary').html(res.summaries);
  $('#linkHere').html('<a href="' + res.urls + '">' + $('.ui.search').search('get value').trim() + '</a>');
};

var submitQuery = function(e) {
  var query = $('.ui.search').search('get value').trim().replace(' ', '%20');
  $.get('/api/v1/wiki/' + query + '/wc', processData)
    .fail(function(error) {
      console.log('We have encountered an error'); // or whatever
    });
};

var generateCloud = function(words) {
  var $cloud = $('#wordCloud');
  $cloud.jQCloud('update', words);
};


function blah(list) {
  var result = [];
  for (var key in list) {
    if (key !== $('input').val().trim()) {
      result.push({
        text: key,
        weight: list[key]
      });
    }
  }
  return result;
}
