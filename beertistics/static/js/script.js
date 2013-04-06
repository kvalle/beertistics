function basic_stats_message(data) {
    return "Hello there, " + data.name + ". " + 
        "In your "+ data.days +" days using Untappd, you have checked in " +
        "a total of " + data.total + " beers, " + data.distinct + " of which " + 
        "are distinct. That averages to "+data.total_avg+" beers per day " + 
        "(" + data.distinct_avg + " distinct). You have also posted " + data.photos +
        " photos, earned "+data.badges+" badges, and made "+data.friends+" friends."
}

function make_photo_list(data) {
    rows = $.map(data, function(checkin) {
        return '<li><a title="'+checkin.beer+' by '+checkin.brewery+'"href="'+checkin.photo_original+'"><img src="'+checkin.photo+'"/></a></li>'
    });
    return $('<ul/>', { html: rows.join("") });
}