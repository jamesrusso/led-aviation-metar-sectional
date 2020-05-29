import logging


class DummyRenderer(object):
    def __init__(self, pixel_count):
        """
        Create a new controller for the WS2811 based lights

        Arguments:
            pixel_count {int} -- The total number of neopixels
        """

        self.logger = logging.getLogger(__name__)
        self.pixel_count = pixel_count
        self.pixels = [(0, 0, 0)] * self.pixel_count

    def get_led(self, pixel_index):
        """
        Obtain the LED status for the specified pixel index.

        Arguments:
            pixel_index {int} -- the index of pixel value to obtain.
        """

        return self.pixels[pixel_index]

    def set_led(self, pixel_index, color):
        """
        Sets the given airport to the given color

        Arguments:
            pixel_index {int or int array} -- The index of the pixel to set
            color {int array} -- The RGB (0-255) array of the color we want to set.
        """

        if (type(pixel_index) is not list):
            pixel_index = [pixel_index]

        for p in pixel_index:
            self.logger.debug("pixel {} set to {}".format(p, color))
