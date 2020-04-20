"""
This is a remote renderer. Used mainly for development to allow you to control the LEDs remotely via a restful interface.
"""

import socket
import struct


class RemoteRenderer(object):

    def __init__(self, hostname, port):
        """
        Create a new controller for the WS2811 based lights

        Arguments:
            host {string} -- The host of the service which is used to control the LEDS on the board.
            port {int} -- The port
        """
        self.hostname = hostname
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def set_led(self, pixel_index, color):
        """
        Sets the given airport to the given color

        Arguments:
            pixel_index {int or int array} -- The index of the pixel to set
            color {obj} -- The color object.
        """

        if (color is None):
            raise ValueError("color cannot be None")

        if (pixel_index is None):
            raise ValueError("pixel_index cannot be None")

        if (type(pixel_index) is not list):
            pixel_index = [pixel_index]

        for p in pixel_index:
            msg = struct.pack('hhhh', *(p, color.rgb[0], color.rgb[1], color.rgb[2]))
            self.sock.sendto(msg, (self.hostname, self.port))

    def shutdown(self):
        pass
