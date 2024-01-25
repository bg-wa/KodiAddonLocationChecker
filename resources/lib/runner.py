import xbmc
import xbmcgui
import xbmcaddon
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
        self.addon = xbmcaddon.Addon()
        self.first_run = True
        self.dialog = None
        self.vpn_country = self.addon.getSetting('vpn_country')
        self.vpn_connected_message = "VPN Connected! You are in ({0}). Enjoy!"
        self.checking_vpn_status_message = 'Checking VPN Status. Please wait...'
        self.error_getting_country_code_message = "An error occurred while trying to get the country code: {0}"
        self.error_getting_ip_message = "An error occurred while trying to get the IP: {0}"
        self.unexpected_error_message = "An unexpected error occurred: {0}"

    def warning_message(self):
        return f"WARNING!! You are in the {self.vpn_country}. \n Please use a VPN to protect your privacy. \n Kodi will now close."

    def close_dialog(self):
        if self.dialog is not None:
            self.dialog.close()
            self.dialog = None

    def process_ip(self, ip):
        url = "http://ip-api.com/json/{0}".format(ip)
        req = Request(url)
        try:
            json_response = urlopen(req)
            response = json.loads(json_response.read().decode('utf-8'))
            country_code = response['countryCode']
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
        except URLError as e:
            print(self.error_getting_country_code_message.format(e))
        except Exception as e:
            print(self.unexpected_error_message.format(e))

    def check_ip(self):
        url = "https://api.ipify.org?format=json"
        req = Request(url)
        try:
            response = urlopen(req)
            ip_address = json.loads(response.read().decode('utf-8'))['ip']
            self.process_ip(ip_address)
        except URLError as e:
            print(self.error_getting_ip_message.format(e))
        except Exception as e:
            print(self.unexpected_error_message.format(e))

    def run(self):
        monitor = xbmc.Monitor()
        if self.first_run:
            self.dialog = xbmcgui.DialogProgress()
            self.dialog.create('Location Checker', self.checking_vpn_status_message)

        self.check_ip()
        while not monitor.abortRequested():
            minutes = 1
            seconds = minutes * 60
            if monitor.waitForAbort(seconds):
                break

            self.check_ip()


if __name__ == "__main__":
    location_checker = LocationChecker()
    location_checker.run()

