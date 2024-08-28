from flask import Blueprint, render_template, Response, current_app
from .streaming import generate_frames

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/set_strategy/<strategy>')
def set_strategy(strategy):
    current_app.config['RECORDING_STRATEGY'] = strategy
    return f"Recording strategy set to {strategy}"

@main.route('/video_feed')
def video_feed():
    return Response(
        generate_frames(
            current_app.config.get('RECORDING_STRATEGY', 'live'),
            int(current_app.config.get('CONTINUITY_THRESHOLD', 5))
        ),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
