from threading import Thread, Condition, Event
from sectional.services import DataService
from sectional.models import Configuration
import logging


class MetarRefreshThread(Thread):

    def __init__(self, sectional):
        self.logger = logging.getLogger(__name__)
        Thread.__init__(self, name="MetarRefreshThread", daemon=True)
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
                self.logger.debug("obtaining {} metars...".format(len(self.sectional.airports)))
                metars = DataService.obtain_metars(self.sectional.airports.keys())
                for metar in metars:
                    self.sectional.airport(metar.icao_airport_code).metar = metar
                self.initial_load_event.set()
                self.wait_condition.wait(self.config.metar_refresh_interval * 60)
            except Exception:
                self.logger.error("exception occurred while obtaining metars.",exc_info=True)
