from threading import Thread, Condition, Event
from sectional.services import DataService
from sectional.models import Configuration
import logging


class SunriseSunsetUpdateThread(Thread):

    def __init__(self, sectional):
        self.logger = logging.getLogger(__name__)
        Thread.__init__(self, daemon=True, name="SunriseSunsetUpdateThread")
        self.sectional = sectional
        self.config = Configuration()
        self.wait_condition = Condition()
        self.initial_load_event = Event()
        self.running = True

    def shutdown(self):
        self.wait_condition.acquire()
        self.running = False
        self.wait_condition.notify()
        self.wait_condition.release()

    def run(self):
        while (self.running):
            try:
                self.wait_condition.acquire()
                self.logger.debug("obtaining {} sunrise and sunset data...".format(len(self.sectional.airports)))
                for (key, airport) in self.sectional.airports.items():
                    try:
                        sunrise_data = DataService.obtain_sunrise_and_sunset_data(lat=airport.lat, long=airport.long)
                        airport.sunrise_data = sunrise_data
                        self.logger.debug("sunrise info for {} is {}".format(key, airport))
                    except Exception:
                        self.logger.error("failed to obtain sunrise data for {}".format(key))
                self.initial_load_event.set()
                self.wait_condition.wait(self.config.sunrise_refresh_interval * 60)
            except Exception:
                self.logger.error("exception occurred while obtaining metars.")
