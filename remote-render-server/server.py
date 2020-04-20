from flask import Flask, jsonify, request, abort, send_from_directory
from flask_socketio import SocketIO

app = Flask(__name__, static_url_path='/', static_folder='test-renderer/dist/test-renderer')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, logger=True, engineio_logger=True)

pixel_count = 74
gpio_port = 18

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):
    return send_from_directory('/', path)

@app.route('/')
def root():
    return send_from_directory('/static', 'index.html')

@app.route('/api/v1.0/led/<int:index>', methods=['POST'])
def set_led(index):
    if not request.json:
        abort(400)

    socketio.emit('led:set', {'index': index, 'color': request.json})
    return jsonify({'status': 'OK'})

@app.route('/api/v1.0/ledcount', methods=['GET'])
def get_led_count():
    return jsonify({'count': pixel_count})

if __name__ == '__main__':
    socketio.run(app, port=5001)
