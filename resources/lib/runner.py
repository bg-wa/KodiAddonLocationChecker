import xbmc
import xbmcgui
import json

try:  # PY2 / PY3
    from urllib2 import Request, urlopen
    from urllib2 import URLError
    from urllib import urlencode
except ImportError:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
    from urllib.parse import urlencode


class LocationChecker:
    def __init__(self):
        self.first_run = True
        self.dialog = None

    def close_dialog(self):
            if self.dialog is not None:
                self.dialog.close()
                self.dialog = None

    def process_ip(self, ip):
        # get country code from ip address
        url = "http://ip-api.com/json/{0}".format(ip)
        req = Request(url)
        try:
            json_response = urlopen(req)
        except URLError as e:
            return e
        response = json.loads(json_response.read().decode('utf-8'))
        country_code = response['countryCode']
        if country_code == 'US':
            if self.dialog is not None:
                self.dialog.update(100, "WARNING!! You are in the US. Please use a VPN to protect your privacy.")
            else:
                self.dialog = xbmcgui.DialogProgress()
                self.dialog.create('Location Checker', 'WARNING!! You are in the US. Please use a VPN to protect your privacy.')

            xbmc.Player().stop()
            xbmc.executebuiltin('Quit')
        else:
            if self.first_run:
                self.dialog.update(100, "VPN Connected! You are in ({0}). Enjoy!".format(country_code))
                self.close_dialog()

        self.first_run = False


    def check_ip(self):
        url = "http://ip.42.pl/raw"
        req = Request(url)
        try:
            response = urlopen(req)
        except URLError as e:
            return e
        ip_address = response.read().decode('utf-8')
        self.process_ip(ip_address)

    def run(self):
        monitor = xbmc.Monitor()
        if self.first_run:
            self.dialog = xbmcgui.DialogProgress()
            self.dialog.create('Location Checker', 'Checking VPN Status. Please wait...')

        self.check_ip()
        while not monitor.abortRequested():
            # Sleep/wait for abort for 1 minutes
            minutes = 1
            seconds = minutes * 60
            if monitor.waitForAbort(seconds):
                # Abort was requested while waiting. We should exit
                break

            self.check_ip()


if __name__ == "__main__":
    location_checker = LocationChecker()
    location_checker.run()

