import xbmc
import xbmcgui
import xbmcaddon
from geolocation import GeoLocation
from ip_address import IPAddress
import logging
from logger import setup_logging

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

class LocationChecker:
    def __init__(self):
        self.addon = xbmcaddon.Addon()
        self.first_run = True
        self.dialog = None
        self.vpn_country = self.addon.getSetting('vpn_country')
        self.geocode_url = self.addon.getSetting('geocode_url')
        self.public_ip_url = self.addon.getSetting('public_ip_url')
        self.frequency = int(self.addon.getSetting('frequency'))
        self.geo_location = GeoLocation(self.geocode_url)
        self.ip_address = IPAddress(self.public_ip_url)
        self.vpn_connected_message = "VPN Connected! You are in ({0}). Enjoy!"
        self.checking_vpn_status_message = 'Checking VPN Status. Please wait...'
        self.error_getting_country_code_message = "An error occurred while trying to get the country code: {0}"
        self.error_getting_ip_message = "An error occurred while trying to get the IP: {0}"
        self.unexpected_error_message = "An unexpected error occurred: {0}"
        logger.debug("LocationChecker initialized")

    def check_ip(self):
        ip_address = IPAddress(self.public_ip_url).get_ip_address()
        country_code = GeoLocation(self.geocode_url).get_country_code(ip_address)

        if country_code == self.vpn_country:
            if self.dialog is not None:
                self.dialog.update(100, self.warning_message())
            else:
                self.dialog = xbmcgui.DialogProgress()
                self.dialog.create('Location Checker', self.warning_message())

            xbmc.Player().stop()
            xbmc.executebuiltin('Quit')
        else:
            if self.first_run:
                self.dialog.update(100, self.vpn_connected_message.format(country_code))
                self.close_dialog()
        self.first_run = False

    def warning_message(self):
        return f"WARNING!! You are in the {self.vpn_country}. \n Please use a VPN to protect your privacy. \n Kodi will now close."

    def close_dialog(self):
        if self.dialog is not None:
            self.dialog.close()
            self.dialog = None

    def run(self):
        monitor = xbmc.Monitor()
        if self.first_run:
            self.dialog = xbmcgui.DialogProgress()
            self.dialog.create('Location Checker', self.checking_vpn_status_message)

        self.check_ip()
        while not monitor.abortRequested():
            seconds = self.frequency
            if monitor.waitForAbort(seconds):
                break

            self.check_ip()

if __name__ == "__main__":
    logger.debug("Application start")
    location_checker = LocationChecker()
    location_checker.run()
    logger.debug("Application end")
