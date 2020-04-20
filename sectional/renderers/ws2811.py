import neopixel # pylint: disable=import-error
import board # pylint: disable=import-error

class Ws2811Renderer(object):
    def __init__(self, pixel_count, gpio_port, pixel_order='RGB'):
        """
        Create a new controller for the WS2811 based lights

        Arguments:
            pixel_count {int} -- The total number of neopixels
            gpio_port {string} -- The GPIO port the neopixels are on. Will be eval'd with board module
        """

        self.pixel_count = pixel_count

        # Specify a hardware SPI connection on /dev/spidev0.0:
        self.pixels = neopixel.NeoPixel(eval("board.D{}".format(gpio_port)), pixel_count, pixel_order=pixel_order, auto_write=False)

        # Clear all the pixels to turn them off.
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def set_led(self, pixel_index, color):
        """
        Sets the given airport to the given color

        Arguments:
            pixel_index {int or int array} -- The index of the pixel to set
            color {Color} -- The RGB (0-255) array of the color we want to set.
        """

        if (type(pixel_index) is not list):
            pixel_index = [pixel_index]

        rgb_tuple = color.rgb
        
        if (rgb_tuple is None):
            raise ValueError("Unknown color {}".format(color))

        for p in pixel_index:
            self.pixels[p] = (rgb_tuple[0], rgb_tuple[1], rgb_tuple[2])

        self.pixels.show()

    def shutdown(self):
        pass
