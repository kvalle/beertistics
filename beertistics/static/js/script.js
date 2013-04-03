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

