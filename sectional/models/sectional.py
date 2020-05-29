from sectional.threads import SelfTestThread, LEDUpdateThread, MetarRefreshThread, SunriseSunsetUpdateThread, ForeflightRefreshThread
from sectional.models import Configuration, Color
from sectional.services import DataService
from threading import Thread
import logging

class CategorySectional(object):

    def __init__(self, configuration):
        """constructor for the CategorySectional object.
        
        Arguments:
            configuration {Configuration} -- The configuration object.
        """
        self.logger = logging.getLogger(__name__)
        self.airports = {}
        self.configuration = configuration
        self.renderer = configuration.renderer
        self.sunset_evaluation_time = None
        self.is_shutdown = False
        self.self_test_thread = None
        self.led_update_thread = None

    def airport(self, airport_icao_code):
        """Obtain an airport given an airport icao code
        
        Arguments:
            airport_icao_code {str} -- The icao airport code
        Returns:
            {Airport} -- The airport object for the given icao airport code
        """
        return self.airports[airport_icao_code]

    #def set_airport_color(self, airport, color):
    #    airport = self.airport(airport)
    #    color = Color(color)
    #    airport.color_override = color

    def initialize(self):
        """Initialize the sectional
        """
        if self.configuration.display == 1:
            self.metar_refresh_thread = MetarRefreshThread(sectional=self)
        elif self.configuration.display == 2:
            self.foreflight_refresh_thread = ForeflightRefreshThread(sectional=self)
        self.update_sunrise_sunset_thread = SunriseSunsetUpdateThread(sectional=self)
        self.led_update_thread = LEDUpdateThread(sectional=self)

    def run_self_test(self):
        """Perform a self test on the sectional
        """
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
        """Sets the led to the specifed color
        
        Arguments:
            idx {int} -- The index of the pixel/led to set
            color {Color} -- The color object which to set the pixel to.
        """
        self.renderer.set_led(idx, color)

    def refresh_sunrise(self):
        """Force a refresh of the sunrise/sunset data
        """
        self.update_sunrise_sunset_thread.wait_condition.acquire()
        self.update_sunrise_sunset_thread.wait_condition.notify()
        self.update_sunrise_sunset_thread.wait_condition.release()

    def refresh_metars(self):
        """Force a refresh of the metar data
        """
        self.metar_refresh_thread.wait_condition.acquire()
        self.metar_refresh_thread.wait_condition.notify()
        self.metar_refresh_thread.wait_condition.release()

    def start(self):
        """Start the sectional. This will first perform a self-test, then 
        begin threads to start the downloading of the sunrise and sunset data,
        the metar data and then finally start the LED update thread.
        """
        try:
            if (self.configuration.setup_complete):
                self.airports = DataService.create_airports(self.configuration)
                self.run_self_test()
                self.update_sunrise_sunset_thread.start()
                if self.configuration.display == 1:
                    self.metar_refresh_thread.start()
                    self.logger.info("Waiting for initial loading of METAR data to complete...")
                    self.metar_refresh_thread.initial_load_event.wait()
                    self.logger.info("Metar data has been loaded...")
                    self.logger.info("Waiting for initial load of sunrise and sunset data to complete...")
                elif self.configuration.display == 2: 
                    self.foreflight_refresh_thread.start()
                    self.logger.info("Waiting for initial loading of Foreflight Logbook to complete...")
                    self.foreflight_refresh_thread.initial_load_event.wait()
                    self.logger.info("Foreflight logbook has loaded...")
                self.update_sunrise_sunset_thread.initial_load_event.wait()
                self.logger.info("initial load of sunrise and sunset data to complete...")
                Thread.join(self.self_test_thread)
                self.led_update_thread.start()
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self):
        """Shutdown the sectional. This will shutdown and wait for all threads to finish.
        """
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
