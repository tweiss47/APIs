from geocode import getGeocodeLocation, loadKey
import json
import httplib2
from urllib.parse import urlencode

import sys
import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)


foursquare_client_id = loadKey('foursquare_client_id')
foursquare_client_secret = loadKey('foursquare_client_secret')


def findARestaurant(mealType,location):
    ll = getGeocodeLocation(location)
    url = 'https://api.foursquare.com/v2/venues/search?'
    params = {
        'client_id': foursquare_client_id,
        'client_secret': foursquare_client_secret,
        'v': 20180323,
        'll': '{},{}'.format(ll[0], ll[1]),
        'radius': 2000,
        'intent': 'browse',
        'query': mealType,
        'limit': 1
    }
    url += urlencode(params)

    h = httplib2.Http()
    data = json.loads(h.request(url, 'GET')[1])
    # print(data)

    venues = data['response']['venues']
    if len(venues) == 0:
        print('No {} in {}'.format(mealType, location))
        print()
        return

    name = data['response']['venues'][0]['name']
    address = data['response']['venues'][0]['location']['address']
    venue_id = data['response']['venues'][0]['id']

    url = 'https://api.foursquare.com/v2/venues/{}/photos?'.format(venue_id)
    params = {
        'client_id': foursquare_client_id,
        'client_secret': foursquare_client_secret,
        'v': 20180323,
        'group': 'venue',
        'limit': 1
    }
    url += urlencode(params)

    h = httplib2.Http()
    data = json.loads(h.request(url, 'GET')[1])
    # print(data)

    count = data['response']['photos']['count']
    if count == 0:
        image = 'http://default'
    else:
        image = data['response']['photos']['items'][0]['prefix']
        image += '300x300'
        image += data['response']['photos']['items'][0]['suffix']
        image = image.replace('\/', '/')

    print(name)
    print(address)
    print(image)
    print()

	#6. If no image is available, insert default a image url
	#7. Return a dictionary containing the restaurant name, address, and image url

if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")
