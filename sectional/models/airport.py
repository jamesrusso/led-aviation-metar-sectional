from sectional.models import Color, Configuration, AirportCondition
import logging


class Airport(object):

    def __init__(self, configuration, icao_airport_code, lat, long, pixels):
        self.logger = logging.getLogger(__name__)
        self.__icao_airport_code = icao_airport_code
        self.__configuration = configuration
        self.__lat = lat
        self.__long = long
        self.__metar = None
        self.__sunrise_data = None
        self.__pixels = pixels
        self.__color_override = None

    @property
    def pixels(self):
        return self.__pixels

    @property
    def configuration(self):
        return self.__configuration
        
    @property
    def color_override(self):
        return self.__color_override

    @color_override.setter
    def color_override(self, val):
        self.__color_override = val

    @property
    def lat(self):
        return self.__lat

    @property
    def sunrise_data(self):
        return self.__sunrise_data

    @sunrise_data.setter
    def sunrise_data(self, val):
        self.__sunrise_data = val

    @property
    def long(self):
        return self.__long

    def __str__(self):
        return "AIRPORT({}): NAME:{}, (LAT,LONG): ({},{}) CATEGORY: {}, METAR: {}, SUNSRISE_DATA: {},".format(id(self), self.icao_airport_code, self.lat, self.long, self.category, self.metar, self.sunrise_data)

    @property
    def icao_airport_code(self):
        return self.__icao_airport_code

    def should_blink(self):
        return False

    @property
    def color(self):

        if (self.color_override):
            self.logger.info("color color_override is enabled")
            return self.color_override

        if (self.sunrise_data is None or self.configuration.night_lights is False):
            return self.configuration.get_color_for_condition(self.category)

        # Sunrise
        if (self.sunrise_data.is_daylight and self.sunrise_data.is_twilight):
            return self.configuration.get_color_for_condition(AirportCondition.NIGHT_DARK).fade_to(self.configuration.color_for_condition(self.category), self.sunrise_data.proportion)

        # Daylight
        elif (self.sunrise_data.is_daylight):
            return self.configuration.get_color_for_condition(self.category)

        # Sunset
        elif (self.sunrise_data.is_nighttime and self.sunrise_data.is_twilight):
            return self.configuration.get_color_for_condition(self.category).fade_to(self.configuration.get_color_for_condition(AirportCondition.NIGHT), self.sunrise_data.proportion)

        elif (self.sunrise_data.is_nighttime):
            return self.configuration.get_color_for_condition(AirportCondition.NIGHT_DARK)

        else:
            return Color.OFF

    @property
    def metar(self):
        return self.__metar

    @metar.setter
    def metar(self, metar):
        self.__metar = metar

    @property
    def category(self):
        if (self.metar is None):
            return AirportCondition.INVALID
        elif(self.metar.age.total_seconds() > self.configuration.metar_invalid_age):
            return AirportCondition.INVALID
        elif(self.metar.age.total_seconds() > self.configuration.metar_inop_age):
            return AirportCondition.INOP
        else:
            return self.metar.category

    def to_json(self):
        return {
            'id': id(self),
            'icao_airport_code': self.icao_airport_code,
            'lat': self.lat,
            'long': self.long,
            'metar': self.metar.to_json(),
            'pixels': self.pixels,
            'color_override': self.color_override,
            'sunrise_data': self.sunrise_data.to_json()
        }
