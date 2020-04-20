from flask import Flask, jsonify, request, abort, send_from_directory
from threading import Thread
from flask_socketio import SocketIO
import socket
import struct

app = Flask(__name__, static_url_path=None)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True, engineio_logger=True, async_mode='threading')

pixel_count = 74
gpio_port = 18

@app.route('/')
def index():
    return send_from_directory('angular/dist/test-renderer', 'index.html')

@app.route('/<path:path>')
def root(path):
    return send_from_directory('angular/dist/test-renderer', path)

@app.route('/api/v1.0/led/<int:index>', methods=['POST'])
def set_led(index):
    if not request.json:
        abort(400)

    socketio.emit('led:set', {'index': index, 'color': request.json})
    return jsonify({'status': 'OK'})

@app.route('/api/v1.0/ledcount', methods=['GET'])
def get_led_count():
    return jsonify({'count': pixel_count})

class UDPServerThread(Thread):

    def __init__(self):
        Thread.__init__(self, daemon=True)
        self.localIP = "0.0.0.0"
        self.localPort = 5006
        self.bufferSize = 1024
        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind((self.localIP, self.localPort))

    def run(self):
        while(True):
            print("waiting...")
            bytesAddressPair = self.UDPServerSocket.recvfrom(self.bufferSize)
            message = bytesAddressPair[0]
            msg = struct.unpack("hhhh", message)
            socketio.emit('led:set', {'index': msg[0], 'color': (msg[1], msg[2], msg[3])})

if __name__ == '__main__':
    thread = UDPServerThread()
    thread.start()
    socketio.run(app, port=5005)
