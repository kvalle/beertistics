function make_basic_stats(data) {
    var rows = [];
    $.each(data, function(key, val) {
        rows.push('<dt>'+val+'</dt><dd>'+key+'</dd>');
    });
    var table = $('<dl/>', {
        'class': 'dl-horizontal',
        html: rows.join('')
    });
    return table;
}

function make_photo_list(data) {
    rows = $.map(data, function(checkin) {
        return '<li><a title="'+checkin.beer+' by '+checkin.brewery+'"href="'+checkin.photo_original+'"><img src="'+checkin.photo+'"/></a></li>'
    });
    return $('<ul/>', { html: rows.join("") });
}