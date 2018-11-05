import httplib2
import json
from urllib.parse import urlencode
import pickledb


def loadKey(name):
    with open('keys.json', 'r') as f:
        keys = json.loads(f.read())
    return keys[name]


def loadCache():
    return pickledb.load('locations.db', True)


google_api_key = loadKey('google_maps')
cache = loadCache()


def getGeocodeUrl(address):
    '''
    Encode the address into a url suitable for calling the Google
    Geocode API
    '''
    params = {
        'address': address,
        'key': google_api_key
    }
    query = urlencode(params)
    return 'https://maps.googleapis.com/maps/api/geocode/json?{}'.format(query)


def getGeocodeLocation(inputString):
    '''
    Use Google Maps to convert a location into Latitute/Longitute coordinates
    '''
    location = cache.get(inputString)
    if not location:
        print('Calling google geocache for {}'.format(inputString))
        url = getGeocodeUrl(inputString)
        h = httplib2.Http()
        result = json.loads(h.request(url,'GET')[1])
        latitude = result['results'][0]['geometry']['location']['lat']
        longitude = result['results'][0]['geometry']['location']['lng']
        location = (latitude, longitude)
        cache[inputString] = location
    return location


if __name__ == '__main__':
    print(getGeocodeUrl("Tokyo, Japan"))
    print(getGeocodeLocation("Jakarta, Indonesia"))
