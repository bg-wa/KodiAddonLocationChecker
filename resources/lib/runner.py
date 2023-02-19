# -*- coding: utf-8 -*-
import xbmc
import json

try:  # PY2 / PY3
    from urllib2 import Request, urlopen
    from urllib2 import URLError
    from urllib import urlencode
except ImportError:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
    from urllib.parse import urlencode


def alert(message, title="Location Checker", time=5000, image=""):
    xbmc.executebuiltin('Notification({0}, {1}, {2}, {3})'.format(title, message, time, image))


def process_ip(ip):
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
        alert("WARNING!! You are in the US. Please use a VPN to protect your privacy.")
        xbmc.Player().stop()
        xbmc.executebuiltin('ActivateWindow(Home)')


def check_ip():
    url = "http://ip.42.pl/raw"
    req = Request(url)
    try:
        response = urlopen(req)
    except URLError as e:
        return e
    ip_address = response.read().decode('utf-8')
    process_ip(ip_address)


if __name__ == "__main__":
    monitor = xbmc.Monitor()
    check_ip()
    while not monitor.abortRequested():
        # Sleep/wait for abort for 5 minutes
        minutes = 5
        seconds = minutes * 60
        if monitor.waitForAbort(seconds):
            # Abort was requested while waiting. We should exit
            break
        check_ip()
