"""
Simple driver of the WS2801/SPI-like addressable RGB LED lights.
Based on the AdaFruit code by Tony DiCola
License: Public Domain
"""

# Import the WS2801 module.
import Adafruit_WS2801 # pylint: disable=import-error
import Adafruit_GPIO.SPI as SPI # pylint: disable=import-error

class Ws2801Renderer(object):
    def __init__(self, pixel_count, spi_port, spi_device):
        """
        Create a new controller for the WS2801 based lights

        Arguments:
            pixel_count {int} -- The total number of neopixels. Probably a multple of 25.
            spi_port {int} -- The SPI port the neopixels are on.
            spi_device {int} -- The SPI device on the port that the neopixels are on.
        """

        self.pixel_count = pixel_count

        # Specify a hardware SPI connection on /dev/spidev0.0:
        self.pixels = Adafruit_WS2801.WS2801Pixels(
            self.pixel_count, spi=SPI.SpiDev(spi_port, spi_device))

        # Clear all the pixels to turn them off.
        self.pixels.clear()
        self.pixels.show()  # Make sure to call show() after changing any pixels!

        [self.pixels.set_pixel(pixel, Adafruit_WS2801.RGB_to_color(0, 0, 0))
            for pixel in range(0, self.pixel_count)]

        self.pixels.show()

    def set_led(self, pixel_index, color):
        """
        Sets the given airport to the given color

        Arguments:
            pixel_index {int} -- The index of the pixel to set
            color {Color} -- a color object value from the colors module.
        """
        rgb_tuple = color.rgb
        if (rgb_tuple is None):
            raise ValueError("Unknown color {}".format(color))

        self.pixels.set_pixel(pixel_index, Adafruit_WS2801.RGB_to_color(
            rgb_tuple[0], rgb_tuple[1], rgb_tuple[2]))
        self.pixels.show()

    def shutdown(self):
        pass
