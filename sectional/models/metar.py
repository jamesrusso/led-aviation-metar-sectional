from sectional.models import AirportCondition
import re
import logging
from datetime import datetime, timedelta

class Metar(object):

    def __init__(self, metar_text):
        self.logger = logging.getLogger(__name__)
        self.metar = metar_text
        self.icao_airport_code = self.metar.split(' ')[0]
        self.issue_time = self.__caculate_issue_time()
        self.visibility = self.__extract_visibility()
        self.ceiling = self.__extract_ceiling()
        self.ceiling_category = self.__calculate_ceiling_category()
        self.category = self.__calculate_category()

    @property
    def age(self):
        """
            Returns the age of the metar in as a timedelta
        """

        if (self.issue_time):
            return datetime.utcnow() - self.issue_time

    def __str__(self):
        return "age={}, metar={}, vis={}, ceiling={}, ceiling_cat={}, cat={}".format(self.age, self.metar, self.visibility, self.ceiling, self.ceiling_category, self.category)

    def __extract_ceiling(self):
        """
        Returns the flight rules classification based on ceiling from a RAW metar.

        Arguments:
            metar {string} -- The RAW weather report in METAR format.

        Returns:
            string -- The flight rules classification, or INVALID in case of an error.
        """

        # Exclude the remarks from being parsed as the current
        # condition as they normally are for events that
        # are in the past.
        components = self.metar.split('RMK')[0].split(' ')
        minimum_ceiling = 10000
        for component in components:
            if 'BKN' in component or 'OVC' in component:
                try:
                    ceiling = int(''.join(filter(str.isdigit, component))) * 100
                    if(ceiling < minimum_ceiling):
                        minimum_ceiling = ceiling
                except Exception as ex:
                    self.logger.error('Unable to decode ceiling component {} from {}. EX:{}'.format(
                        component, self.metar, ex))
        return minimum_ceiling

    def __extract_visibility(self):
        """
        Returns the flight rules classification based on visibility from a RAW metar.

        Arguments:
            metar {string} -- The RAW weather report in METAR format.

        Returns:
            string -- The flight rules classification, or INVALID in case of an error.
        """

        match = re.search('( [0-9] )?([0-9]/?[0-9]?SM)', self.metar)
        is_smoke = re.search('.* FU .*', self.metar) is not None
        # Not returning a visibility indicates UNLIMITED
        if(match is None):
            return AirportCondition.VFR
        (g1, g2) = match.groups()
        if(g2 is None):
            return AirportCondition.INVALID
        if(g1 is not None):
            if is_smoke:
                return AirportCondition.SMOKE
            return AirportCondition.IFR
        if '/' in g2:
            if is_smoke:
                return AirportCondition.SMOKE
            return AirportCondition.LIFR
        vis = int(re.sub('SM', '', g2))
        if vis < 3:
            if is_smoke:
                return AirportCondition.SMOKE
            return AirportCondition.IFR
        if vis <= 5:
            if is_smoke:
                return AirportCondition.SMOKE
            return AirportCondition.MVFR

        return AirportCondition.VFR

    def __calculate_ceiling_category(self):
        """
        Returns the flight rules classification based on the cloud ceiling.

        Arguments:
            ceiling {int} -- Number of feet the clouds are above the ground.

        Returns:
            string -- The flight rules classification.
        """

        if self.ceiling < 500:
            return AirportCondition.LIFR
        if self.ceiling < 1000:
            return AirportCondition.IFR
        if self.ceiling < 3000:
            return AirportCondition.MVFR
        return AirportCondition.VFR

    def __calculate_category(self):
        """
        Returns the flight rules classification based on the metar

        Returns:
            string -- The flight rules classification, or INVALID in case of an error.
        """
        if self.metar is None:
            return AirportCondition.INVALID

        if self.age is not None:
            metar_age_minutes = self.age.total_seconds() / 60.0
            self.logger.info("{} - Issued {:.1f} minutes ago".format(
                self.icao_airport_code, metar_age_minutes))
            if self.ceiling == AirportCondition.INVALID or self.visibility == AirportCondition.INVALID:
                return AirportCondition.INVALID
            elif self.visibility == AirportCondition.SMOKE:
                return AirportCondition.SMOKE
            elif self.visibility == AirportCondition.LIFR or self.ceiling == AirportCondition.LIFR:
                return AirportCondition.LIFR
            elif self.visibility == AirportCondition.IFR or self.ceiling == AirportCondition.IFR:
                return AirportCondition.IFR
            elif self.visibility == AirportCondition.MVFR or self.ceiling == AirportCondition.MVFR:
                return AirportCondition.MVFR
            else:
                return AirportCondition.VFR
        else:
            self.logger.warn("{} - unknown METAR age".format(self.icao_airport_code))
            return AirportCondition.INVALID

    def __caculate_issue_time(self):
        """
        Returns the age of the METAR

        Returns:
            timedelta -- The age of the metar, None if it can not be determined.
        """

        try:
            current_time = datetime.utcnow()
            metar_date = current_time - timedelta(days=31)

            if self.metar is not None:
                partial_date_time = self.metar.split(' ')[1]
                partial_date_time = partial_date_time.split('Z')[0]

                day_number = int(partial_date_time[:2])
                hour = int(partial_date_time[2:4])
                minute = int(partial_date_time[4:6])

                metar_date = datetime(
                    current_time.year, current_time.month, day_number, hour, minute)

                # Assume that the report is from the past, and work backwards.
                days_back = 0
                while metar_date.day != day_number and days_back <= 31:
                    metar_date -= timedelta(days=1)
                    days_back += 1

            return metar_date
        except Exception:
            self.logger.error("Exception while getting METAR age", exc_info=True)
            return None

    def to_json(self):
        return {
            'metar': self.metar,
            'icao_airport_code': self.icao_airport_code,
            'issue_time': self.issue_time,
            'visibility': self.visibility,
            'ceiling': self.ceiling,
            'ceiling_category': self.ceiling_category,
            'self.category': self.category
        }
