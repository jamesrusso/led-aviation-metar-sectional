import logging
import os
from datetime import datetime
import csv
import requests
import urllib
import re
from sectional.models import SunriseSunsetData, Airport, Metar
import ssl 

class DataService(object):
    @classmethod
    def obtain_sunrise_and_sunset_data(cls, lat, long):
        logger = logging.getLogger(__name__)
        url = "http://api.sunrise-sunset.org/json?lat={}&lng={}&date={}&formatted=0".format(lat, long, datetime.utcnow().strftime("%Y"))
        json_result = []
        try:
            session = requests.Session()
            json_result = session.get(url, timeout=5).json()

            if (json_result['status'] != 'OK'):
                raise RuntimeError("Unable to obtain sunrise/sunset data, since the API returned a non-successful status. {}".format(json_result['status']))

            return SunriseSunsetData(json_result)

        except Exception as ex:
            logger.error('failed to obtain sunrise/sunset data', exc_info=ex)
            return None

    @classmethod
    def airportsearch(cls, q):
        working_directory = os.path.dirname(os.path.abspath(__file__))
        airport_data_file = "../../config/airports.csv"
        full_file_path = os.path.join(
            working_directory, os.path.normpath(airport_data_file))

        csvfile = open(full_file_path, 'r', encoding='utf-8')
        reader = csv.DictReader(csvfile)

        airports = []

        for row in reader:
            if (q.upper() in row['ident'] or q.upper() in row['name'].upper()):
                airports.append({'icao_airport_code': row['ident'], 'name': row['name']})

        return airports

    @classmethod
    def create_airports(cls, configuration):
        """
        Create all the airport objects which are required for the applicaiton

        Keyword Arguments:
            airport_codes {array} -- The file that contains the airports (default: {"./config/airports.csv"})

        Returns:
            dictionary -- A map of the airport data keyed by ICAO code.
        """
        logger = logging.getLogger(__name__)
        logger.info("creating airports...")
        working_directory = os.path.dirname(os.path.abspath(__file__))
        airport_data_file = "../../config/airports.csv"
        full_file_path = os.path.join(
            working_directory, os.path.normpath(airport_data_file))

        csvfile = open(full_file_path, 'r', encoding='utf-8')
        reader = csv.DictReader(csvfile)

        airport_map = {}

        for row in reader:
            if (row['ident'] in configuration.airports.keys()):
                pixels = configuration.airports[row['ident']]
                airport_map[row['ident']] = Airport(configuration=configuration, icao_airport_code=row["ident"], lat=row["latitude_deg"], long=row["longitude_deg"], pixels=pixels)

        return airport_map

    @classmethod
    def obtain_metars(cls, airport_codes):
        ssl._create_default_https_context = ssl._create_unverified_context
        logger = logging.getLogger(__name__)
        logger.info("Obtaining METAR data for {}".format(list(airport_codes)))
        metar_list = "%20".join(airport_codes)
        request_url = 'http://www.aviationweather.gov/metar/data?ids={}&format=raw&hours=0&taf=off&layout=off&date=0'.format(metar_list)
        stream = urllib.request.urlopen(request_url, timeout=15)
        content = stream.read().decode('utf-8')
        metars = re.findall("<code>(.*)</code>", content)
        return [Metar(x) for x in metars]

    @classmethod
    def obtain_ff_logbook(cls, ff_username, ff_password):
        # hack for stupid mac and giving up on getting certificates installed
        ssl._create_default_https_context = ssl._create_unverified_context
        logger = logging.getLogger(__name__)
        logger.info("Logging into Foreflight as {}".format(ff_username))
        foreflight_url = 'https://plan.foreflight.com'
        request_url = foreflight_url + '/api/1/logbook/export/csv'
        logout_url = foreflight_url + '/auth/logout'
        with requests.Session() as s:
            s.get(foreflight_url)
            s.post(foreflight_url, data={'username': ff_username, 'password': ff_password})
            logger.info("Downloading Logbook for {}".format(ff_username))
            logbook = s.get(request_url)
            s.get(logout_url)
        return logbook
        