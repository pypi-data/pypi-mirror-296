from ultralytics import YOLO

# VIDEO OUTPUT SHAPE
OUTPUT_WIDTH = 1280
OUTPUT_HEIGHT = 720

# MODEL PATH
MODEL_POSE = YOLO('models/yolov8n-pose.pt')

# MODEL HYPERPARAMETERS
CONF = 0.5
IOU = 0.5
MAX_DET = 10
IS_SHOW = False
IS_VERBOSE = False
IS_STREAM = False

# MODEL KEYPOINTS
KEYPOINTS = {
    "Nose": 0,
    "Left Eye": 1,
    "Right Eye": 2,
    "Left Ear": 3,
    "Right Ear": 4,
    "Left Shoulder": 5,
    "Right Shoulder": 6,
    "Left Elbow": 7,
    "Right Elbow": 8,
    "Left Wrist": 9,
    "Right Wrist": 10,
    "Left Hip": 11,
    "Right Hip": 12,
    "Left Knee": 13,
    "Right Knee": 14,
    "Left Ankle": 15,
    "Right Ankle": 16
}

THRESHOLD = {"trunk": [0, 40],
             "hip": [90, 120],
             "knee": [90, 130],
             "elbow": [90, 120]}