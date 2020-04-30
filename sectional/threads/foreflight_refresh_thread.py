from threading import Thread, Condition, Event
from sectional.services import DataService
from sectional.models import Configuration
import logging
import csv


class ForeflightRefreshThread(Thread):

    def __init__(self, sectional):
        self.logger = logging.getLogger(__name__)
        Thread.__init__(self, name="ForeflightRefreshThread", daemon=True)
        self.sectional = sectional
        self.configuration = sectional.configuration
        self.ff_refresh_interval = sectional.configuration.foreflight_refresh_interval
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
                self.logger.debug("obtaining ForeFlight logbook data")
                self.sectional.logbook = DataService.obtain_ff_logbook(self.configuration)
                self.initial_load_event.set()
                self.wait_condition.wait(self.ff_refresh_interval * 3600)
            except Exception:
                self.logger.error("exception occurred while obtaining ForeFlight logbook data.",exc_info=True)
