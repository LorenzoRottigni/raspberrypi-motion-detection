from flask import Blueprint, render_template, Response, current_app
from .streamer import Streamer
import json

main = Blueprint('main', __name__)
streamer = Streamer()

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/set_strategy/<strategy>')
def set_strategy(strategy):
    current_app.config['RECORDING_STRATEGY'] = strategy
    return capture()

@main.route('/feed')
def feed():
    if not streamer.stream: capture()
    return Response(
        streamer.stream,
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@main.route('/stats')
def stats():
    return Response(
        json.dumps({
            "capturing": streamer.capture,
            "recording": streamer.recording,
            "recording_start_time": streamer.recording_start_time,
            "strategy": current_app.config.get('RECORDING_STRATEGY', 'live'),
            "continuity_threshold": current_app.config.get('CONTINUITY_THRESHOLD', 5),
        }),
        mimetype='application/json'
    )

@main.route('/capture')
def capture():
    strategy = current_app.config.get('RECORDING_STRATEGY', 'live')
    continuity_threshold = int(current_app.config.get('CONTINUITY_THRESHOLD', 5))
    if streamer.stream:
        streamer.close_stream()
    if not streamer.stream: streamer.boot(strategy, continuity_threshold)
    return stats()
