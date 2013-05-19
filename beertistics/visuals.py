visuals = [
    {
        'visual_id': 'punchcard',
        'template_name': 'punchcard.html'
    }, {
        'visual_id': 'by-country',
        'template_name': 'beers-by-country.html'
    }, {
        'visual_id': 'locations',
        'template_name': 'checkin-locations.html'
    }, {
        'visual_id': 'consumption',
        'template_name': 'consumption-per-month.html'
    }, {
        'visual_id': 'country',
        'template_name': 'country-chart.html'
    }, {
        'visual_id': 'influence',
        'template_name': 'influenced-ratings.html'
    }, {
        'visual_id': 'rating-distribution',
        'template_name': 'rating-distribution.html'
    }, {
        'visual_id': 'rating-vs-abv',
        'template_name': 'rating-vs-abv.html'
    }
]


def get_visual(visual_id):
    return filter(lambda v: v['visual_id'] == visual_id, visuals)[0]

def get_next_url_for(visual_id):
    return "hei, jeg er en test"
