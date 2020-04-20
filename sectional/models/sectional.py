from sectional.threads import SelfTestThread, LEDUpdateThread, MetarRefreshThread, SunriseSunsetUpdateThread
from sectional.models import Configuration, Color
from sectional.services import DataService
from threading import Thread
import logging


class CategorySectional(object):
    def __init__(self, configuration):
        self.logger = logging.getLogger(__name__)
        self.airports = {}
        self.configuration = configuration
        self.renderer = configuration.renderer
        self.sunset_evaluation_time = None
        self.is_shutdown = False
        self.self_test_thread = None
        self.led_update_thread = None

    def airport(self, airport_icao_code):
        return self.airports[airport_icao_code]

    def set_airport_color(self, airport, color):
        airport = self.airport(airport)
        color = Color(color)
        airport.color_override = color

    def initialize(self):
        self.metar_refresh_thread = MetarRefreshThread(sectional=self)
        self.update_sunrise_sunset_thread = SunriseSunsetUpdateThread(sectional=self)
        self.led_update_thread = LEDUpdateThread(sectional=self)

    def run_self_test(self):
        self.logger.info("run_self_test begin....")
        if (self.led_update_thread and self.led_update_thread.is_alive()):
            self.logger.info("shutting down led_update_thread...")
            self.led_update_thread.shutdown()
            Thread.join(self.led_update_thread)

        if (self.self_test_thread and self.self_test_thread.is_alive()):
            self.logger.info("shutting down existing self_test_thread...")
            self.self_test_thread.shutdown()
            Thread.join(self.self_test_thread)

        self.logger.info("creating and running self_test_thread...")
        self.self_test_thread = SelfTestThread(sectional=self)
        self.self_test_thread.start()
        self.logger.info("self_test_thread has been started.")

    def set_led(self, idx, color): 
        self.renderer.set_led(idx, color)

    def refresh_sunrise(self):
        self.update_sunrise_sunset_thread.wait_condition.acquire()
        self.update_sunrise_sunset_thread.wait_condition.notify()
        self.update_sunrise_sunset_thread.wait_condition.release()

    def refresh_metars(self):
        self.metar_refresh_thread.wait_condition.acquire()
        self.metar_refresh_thread.wait_condition.notify()
        self.metar_refresh_thread.wait_condition.release()

    def start(self):
        try:
            if (self.configuration.setup_complete):
                self.airports = DataService.create_airports(self.configuration)
                self.run_self_test()
                self.update_sunrise_sunset_thread.start()
                self.metar_refresh_thread.start()
                self.logger.info("Waiting for initial loading of METAR data to complete...")
                self.metar_refresh_thread.initial_load_event.wait()
                self.logger.info("Metar data has been loaded...")
                self.logger.info("Waiting for initial load of sunrise and sunset data to complete...")
                self.update_sunrise_sunset_thread.initial_load_event.wait()
                self.logger.info("initial load of sunrise and sunset data to complete...")
                Thread.join(self.self_test_thread)
                self.led_update_thread.start()
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        self.logger.info("shutting down...")
        self.led_update_thread.shutdown()
        self.metar_refresh_thread.shutdown()
        self.self_test_thread.shutdown()
        self.update_sunrise_sunset_thread.shutdown()

        self.logger.info("shutting down led_update_thread...")
        Thread.join(self.led_update_thread)
        self.logger.info("shutting down metar_refresh_thread...")
        Thread.join(self.metar_refresh_thread)
        self.logger.info("shutting down self test thread...")
        if (self.self_test_thread.is_alive()):
            Thread.join(self.self_test_thread)
        self.logger.info("shutting down sunrise data refresh thread")
        Thread.join(self.update_sunrise_sunset_thread)
        self.is_shutdown = True

    def __str__(self):
        return "\n".join([str(airport) for key, airport in self.airports.items()])
