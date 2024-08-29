from flask import Blueprint, render_template, Response, current_app
from .stream import Streamer

main = Blueprint('main', __name__)

stream = None
streamer = None

@main.route('/init')
def init():
    global stream, streamer
    streamer = Streamer()
    stream = streamer.boot(
        current_app.config.get('RECORDING_STRATEGY', 'live'),
        int(current_app.config.get('CONTINUITY_THRESHOLD', 5))
    )
    return Response(
        'true',
        mimetype='text/plain'
    )

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/set_strategy/<strategy>')
def set_strategy(strategy):
    current_app.config['RECORDING_STRATEGY'] = strategy
    init()
    return f"Recording strategy set to {strategy}"

@main.route('/feed')
def feed():
    if not stream: init()
    return Response(
        stream,
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@main.route('/stats')
def stats():
    if not stream: init()
    import json
    return Response(
        json.dumps({
            "recording": streamer.recording,
            "recording_start_time": streamer.recording_start_time,
            "strategy": current_app.config.get('RECORDING_STRATEGY', 'live'),
            "continuity_threshold": int(current_app.config.get('CONTINUITY_THRESHOLD', 5)),
        }),
        mimetype='application/json'
    )
