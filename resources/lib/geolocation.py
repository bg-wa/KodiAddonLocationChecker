import json
from urllib.request import Request, urlopen
from urllib.error import URLError
import logging
from logger import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

class GeoLocation:
    def __init__(self, geocode_url):
        self.geocode_url = geocode_url
        logger.debug("GeoLocation initialized with URL: %s", geocode_url)

    def get_country_code(self, ip):
        url = (self.geocode_url + "{0}").format(ip)
        logger.debug("Making geocode request to URL: %s", url)
        req = Request(url)
        try:
            json_response = urlopen(req)
            response = json.loads(json_response.read().decode('utf-8'))
            country_code = response['countryCode']
            logger.debug("Received country code: %s for IP: %s", country_code, ip)
            return country_code
        except URLError as e:
            logger.error("Error getting country code: %s", e)
            raise
