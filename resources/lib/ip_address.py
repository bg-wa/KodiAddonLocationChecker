import json
from urllib.request import Request, urlopen
from urllib.error import URLError
import logging
from logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

class IPAddress:
    def __init__(self, public_ip_url):
        self.public_ip_url = public_ip_url
        logger.debug("IPAddress initialized with URL: %s", public_ip_url)

    def get_ip_address(self):
        logger.debug("Making IP address request")
        req = Request(self.public_ip_url)
        try:
            response = urlopen(req)
            ip_address = json.loads(response.read().decode('utf-8'))['ip']
            logger.debug("Received IP address: %s", ip_address)
            return ip_address
        except URLError as e:
            logger.error("Error getting IP address: %s", e)
            raise
