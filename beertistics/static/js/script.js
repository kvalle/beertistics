function make_photo_list(data) {
    rows = $.map(data, function(checkin) {
        return '<li><a title="'+checkin.beer+' by '+checkin.brewery+'"href="'+checkin.photo_original+'"><img src="'+checkin.photo+'"/></a></li>'
    });
    return $('<ul/>', { html: rows.join("") });
}