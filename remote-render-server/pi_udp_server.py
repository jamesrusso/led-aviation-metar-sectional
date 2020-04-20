import neopixel # pylint: disable=import-error
import board # pylint: disable=import-error
import socket
import struct

"""
    Simple Server to allow you to use the remote renderer to debug/test software while still using the real poster
"""

pixel_count = 74
gpio_port = 18

pixels = neopixel.NeoPixel(board.D18, pixel_count)
pixels.fill((0,0,0))

localIP = "0.0.0.0"
localPort = 5006
bufferSize = 1024
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))

while(True):
    print("waiting...")
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    msg = struct.unpack("hhhh", message)
    pixels[msg[0]] = (msg[1], msg[2], msg[3])
