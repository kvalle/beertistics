visuals = [
    {
        'visual_id': 'punchcard',
        'name': 'The punchcard',
        'type': 'scatter-plot',
        'description': 'When do you do your drinking? This scatter plot shows what time of day and day of week you have checked in your brews.',
        'template_name': 'punchcard.html'
    }, {
        'visual_id': 'by-country',
        'name': 'Beers by country',
        'type': 'horizontal-bar-chart',
        'description': 'Which nation brews the best beer? Find out which countries brews the bulk of your brews.',
        'template_name': 'beers-by-country.html'
    }, {
        'visual_id': 'locations',
        'name': 'Checkin locations',
        'type': 'horizontal-bar-chart',
        'description': 'Where do you drink the most? This chart shows the distribution of checkins in different locations.',
        'template_name': 'checkin-locations.html'
    }, {
        'visual_id': 'consumption',
        'name': 'Consumption per month',
        'type': 'bar-chart',
        'description': 'This plot shows how much you drink each month, and how many of those brews are new and exciting (and how many you\'ve tasted before).',
        'template_name': 'consumption-per-month.html'
    }, {
        'visual_id': 'country',
        'name': 'Country chart',
        'type': 'map',
        'description': 'How international are your drinking habits? Find out where your brews originate in this chart.',
        'template_name': 'country-chart.html'
    }, {
        'visual_id': 'influence',
        'name': 'Influenced ratings?',
        'type': 'scatter-plot',
        'description': 'How much is your rating influenced by your drinking? Find out in this plot of your ratings vs how many you\'ve had.',
        'template_name': 'influenced-ratings.html'
    }, {
        'visual_id': 'rating-distribution',
        'name': 'Rating distribution',
        'type': 'bar-chart',
        'description': 'How much do you use the different ratings? Check the distribution in this chart.',
        'template_name': 'rating-distribution.html'
    }, {
        'visual_id': 'rating-vs-abv',
        'name': 'Rating vs ABV',
        'type': 'scatter-plot',
        'description': 'Is there a correlation between the alcohol content of the beer and how much you like it? Find out here.',
        'template_name': 'rating-vs-abv.html'
    }, {
        'visual_id': 'photos',
        'name': 'Checkin photos',
        'type': 'photos',
        'description': 'Photo gallery of all the photos you have checked into Untappd, along with some basic information about each beer.',
        'template_name': 'photos.html'
    }, {
        'visual_id': 'map',
        'name': 'Beer map',
        'type': 'map',
        'description': 'A map showing where all your checked in beers were brewed, and where you were when you drank them.',
        'template_name': 'map.html'
    }
]


def get_visual(visual_id):
    return filter(lambda v: v['visual_id'] == visual_id, visuals)[0]

def get_next_url_for(visual_id):
    return "hei, jeg er en test"
