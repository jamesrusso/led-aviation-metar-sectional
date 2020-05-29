from threading import Thread, Condition
from sectional.models import Color
import logging


class LEDUpdateThread(Thread):
    def __init__(self, sectional):
        Thread.__init__(self, daemon=True, name="LEDUpdateThread")
        self.logger = logging.getLogger(__name__)
        self.sectional = sectional
        self.running = True
        self.renderer = sectional.renderer
        #self.display = sectional.display
        self.condition = Condition()
        self.on_cycle = True

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
                    color = airport.color
                    self.logger.debug("{}: {}".format(airport_icao_code,airport.color))
                    if (color.blink and not self.on_cycle):
                            color = Color.OFF()

                    self.renderer.set_led(airport.pixels, color)
                self.condition.wait(2)
                self.on_cycle = not self.on_cycle
            except Exception:
                self.logger.error("exception occurred while updating sectional.", exc_info=True)
