class Config:
    RECORDING_STRATEGY = 'live'  # 'live' or 'motion_detection'
    CONTINUITY_THRESHOLD = 5  # seconds of inactivity before saving
    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    FPS = 10.0
