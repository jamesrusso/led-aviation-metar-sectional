from datetime import timedelta, datetime, timezone
from dateutil import parser

""" Used for testing.
"""
EVALUATION_TIME_OVERRIDE = None


class SunriseSunsetData(object):

    def __init__(self, results):
        self.sunrise = parser.isoparse(results['results']['sunrise'])
        self.sunset = parser.isoparse(results['results']['sunset'])
        self.civil_twilight_begin = parser.isoparse(results['results']['civil_twilight_begin'])
        self.civil_twilight_end = parser.isoparse(results['results']['civil_twilight_end'])
        self.nautical_twilight_begin = parser.isoparse(results['results']['nautical_twilight_begin'])
        self.nautical_twilight_end = parser.isoparse(results['results']['nautical_twilight_end'])
        self.astronomical_twilight_begin = parser.isoparse(results['results']['astronomical_twilight_begin'])
        self.astronomical_twilight_end = parser.isoparse(results['results']['astronomical_twilight_end'])

        self.sunrise_begin = self.civil_twilight_begin
        self.sunrise_length = self.sunrise - self.sunrise_begin
        self.sunrise_end = self.sunrise

        self.sunset_begin = self.sunset
        self.sunset_end = self.civil_twilight_end
        self.sunset_length = self.sunset_end - self.sunset
        self.avg_transition_time = timedelta(seconds=(self.sunrise_length.seconds + self.sunset_length.seconds) / 2)

    @property
    def utcnow(self):
        return EVALUATION_TIME_OVERRIDE or datetime.now(tz=timezone.utc)

    @property
    def is_daylight(self):
        """ True from the the begining of civil_twilight_begin until until sunset
        """
        return self.utcnow >= self.civil_twilight_begin and self.utcnow < self.sunset

    @property
    def is_nighttime(self):

        return self.utcnow >= self.sunset or self.utcnow < self.civil_twilight_begin

    @property
    def is_twilight(self):

        if (self.utcnow >= self.civil_twilight_begin and self.utcnow <= self.sunrise):
            return True

        if (self.utcnow >= self.sunset_begin and self.utcnow <= self.civil_twilight_end):
            return True

        return False

    @property
    def proportion(self):
        # civil_twilight_begin > sunrise > day > sunset > civil_twilight_end
        if (self.utcnow >= self.sunrise_begin and self.utcnow <= self.sunrise_end):
            time_left = self.sunrise_end - self.utcnow
            total_time = self.sunrise_length
            return 1 - (time_left / total_time)
        elif (self.utcnow >= self.sunset_begin and self.utcnow <= self.sunset_end):
            time_left = self.sunset_end - self.utcnow
            total_time = self.sunset_length
            return 1 - (time_left / total_time)
        else:
            return 1.0

    def __str__(self):
        return "utcnow={}, civil_twilight_begin={}, sunrise={}, sunset={}, sunset_end={}, is_daylight={}, is_nightlight={}, is_twilight={}, proportion={}".format(self.utcnow.strftime("%c"), self.civil_twilight_begin, self.sunrise, self.sunset, self.civil_twilight_end, self.is_daylight, self.is_nighttime, self.is_twilight, self.proportion)

    def to_json(self):
        return {'utcnow': self.utcnow,
                'civil_twilight_begin': self.civil_twilight_begin,
                'sunrise': self.sunrise,
                'sunset': self.sunset,
                'civil_twilight_end': self.civil_twilight_end,
                'is_daylight': self.is_daylight,
                'is_twilight': self.is_twilight,
                'is_nighttime': self.is_nighttime,
                'sunrise_length': self.sunrise_length,
                'sunset_length': self.sunset_length
                }
