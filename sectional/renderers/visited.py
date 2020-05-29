
class displayVisited(object):

    def __init__(self, pixel_count, airports, configuration):
        """
        Called when display mode is set to "visited"

        """
        self.logger = logging.getLogger(__name__)
        self.pixel_count = pixel_count
        self.airports = airports
        self.configuration = configuration
        self.renderer = configuration.renderer
        self.sunset_evaluation_time = None
        self.is_shutdown = False
        self.self_test_thread = None
        self.led_update_thread = None

    def displayMetar(pixel_count, airports): 
        """
        calls appropriate renderer and lights the appropriate led's

        """


       def set_led(self, idx, color): 
        """Sets the led to the specifed color
        
        Arguments:
            idx {int} -- The index of the pixel/led to set
            color {Color} -- The color object which to set the pixel to.
        """
        self.renderer.set_led(idx, color)