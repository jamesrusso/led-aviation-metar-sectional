from threading import Thread, Condition
import logging


class LEDUpdateThread(Thread):
    def __init__(self, sectional):
        Thread.__init__(self, daemon=True, name="LEDUpdateThread")
        self.logger = logging.getLogger(__name__)
        self.sectional = sectional
        self.running = True
        self.renderer = sectional.renderer
        self.condition = Condition()

    def shutdown(self):
        self.condition.acquire()
        self.running = False
        self.condition.notify()
        self.condition.release()

    def run(self):
        while (self.running):
            try:
                self.condition.acquire()
                for (airport_icao_code, airport) in self.sectional.airports.items():
                    self.logger.debug("{}: {}".format(airport_icao_code,airport.color))
                    self.renderer.set_led(airport.pixels, airport.color)
                self.condition.wait(2)
            except Exception:
                self.logger.error("exception occurred while updating sectional.", exc_info=True)
