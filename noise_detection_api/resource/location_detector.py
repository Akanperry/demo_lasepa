# importing modules
from geopy.geocoders import Nominatim
import requests

class LocationDetector():
    def __str__(self):
        """Returns a string representation of the class."""

    # Function to fetch user's location using IP-based geolocation
    def get_user_location():
        try:
            response = requests.get('https://ipinfo.io')
            data = response.json()
            lat, lon = data['loc'].split(',')
            return lat, lon, data['ip']
        except Exception as e:
            print(e)
            return None, None, None

    def get_location(lat, lon):
        # calling the nominatim tool
        geoLoc = Nominatim(user_agent="GetLoc")
        
        # passing the coordinates
        locname = geoLoc.reverse((lat, lon))
        
        # return the address/location name
        return locname.address