import torch
import numpy as np
from .ErgoUtils import *
from .config import THRESHOLD
from ultralytics import YOLO

class ErgoEval:
    """
    A class to handle ergonomic sensing using a YOLO model to track keypoints and evaluate angles.

    Attributes:
        frame (any): The frame or image data.
        model (YOLO): The YOLO model for keypoint tracking.
        keypoints_dict (dict): A dictionary mapping keypoint names to indices.
        confidence (float): The confidence threshold for the model.
        iou (float): The IoU threshold for the model.
        max_det (int): The maximum number of detections.
        is_show (bool): Flag to show the frame.
        is_verbose (bool): Flag for verbose output.
        is_stream (bool): Flag to stream the output.
    """

    def __init__(self, 
                 model: YOLO, 
                 keypoints_dict: dict,
                 confidence: float, 
                 iou: float,
                 max_det: int, 
                 is_show: bool, 
                 is_verbose: bool, 
                 is_stream: bool):
        """
        Initializes the ErgoSense class with the given parameters.

        Args:
            frame (any): The frame or image data.
            model (YOLO): The YOLO model for keypoint tracking.
            keypoints_dict (dict): A dictionary mapping keypoint names to indices.
            confidence (float): The confidence threshold for the model.
            iou (float): The IoU threshold for the model.
            max_det (int): The maximum number of detections.
            is_show (bool): Flag to show the frame.
            is_verbose (bool): Flag for verbose output.
            is_stream (bool): Flag to stream the output.
        """
        self.model = model
        self.keypoints_dict = keypoints_dict
        self.confidence = confidence
        self.iou = iou
        self.max_det = max_det
        self.is_show = is_show
        self.is_verbose = is_verbose
        self.is_stream = is_stream

        self.warnings_timer = np.zeros(4)

    def predict(self, frame: any):
        """
        Performs keypoint prediction and stores the keypoints, bounding boxes, and angles.
        """
        self.frame = frame
        results = self.model.track(source=self.frame, 
                                   conf=self.confidence, 
                                   iou=self.iou,
                                   max_det=self.max_det, 
                                   show=self.is_show, 
                                   verbose=self.is_verbose, 
                                   stream=self.is_stream)
        self.keypoints = results[0].keypoints.xy.type(torch.long)
        self.bbox = results[0].boxes.xyxy.type(torch.long)

        # storing angle of each person
        self.angles = np.zeros((self.keypoints.shape[0], 4))

        # storing warning for each angles
        self.warning = np.zeros((self.keypoints.shape[0], 4))
    
    def eval(self, mode: str):
        """
        Evaluates the angles based on the given mode.

        Args:
            mode (str): The mode for evaluation ('trunk', 'hip', 'knee', 'elbow').
        """
        n_person = self.keypoints.shape[0]
        
        for person in range(n_person):
            bbox = self.bbox[person]
            draw_rectangle(self.frame, bbox[:2].tolist(), bbox[2:].tolist())

            if mode.lower() == 'trunk':
                self.eval_mode = 0

                left_eye = self.keypoints[person][self.keypoints_dict['Left Eye'], :].tolist()
                right_eye = self.keypoints[person][self.keypoints_dict['Right Eye'], :].tolist()
                eye = midpoint(left_eye, right_eye)

                left_shoulder = self.keypoints[person][self.keypoints_dict['Left Shoulder'], :].tolist()
                right_shoulder = self.keypoints[person][self.keypoints_dict['Right Shoulder'], :].tolist()
                shoulder = midpoint(left_shoulder, right_shoulder)

                left_hip = self.keypoints[person][self.keypoints_dict['Left Hip'], :].tolist()
                right_hip = self.keypoints[person][self.keypoints_dict['Right Hip'], :].tolist()
                hip = midpoint(left_hip, right_hip)

                spine = extend_point(hip, shoulder, target_point=eye)
                
                # calculate angle
                self.angles[person][self.eval_mode] = calculate_angle(shoulder, eye, spine)
                if not THRESHOLD["trunk"][0] <= self.angles[person][self.eval_mode] <= THRESHOLD["trunk"][1]:
                    self.warning[person][self.eval_mode] = True

                self.visualize_eval(person, shoulder, eye, spine)

            elif mode.lower() == 'hip':
                self.eval_mode = 1

                left_shoulder = self.keypoints[person][self.keypoints_dict['Left Shoulder'], :].tolist()
                right_shoulder = self.keypoints[person][self.keypoints_dict['Right Shoulder'], :].tolist()
                shoulder = midpoint(left_shoulder, right_shoulder)
                
                left_hip = self.keypoints[person][self.keypoints_dict['Left Hip'], :].tolist()
                right_hip = self.keypoints[person][self.keypoints_dict['Right Hip'], :].tolist()
                hip = midpoint(left_hip, right_hip)
                
                left_knee = self.keypoints[person][self.keypoints_dict['Left Knee'], :].tolist()
                right_knee = self.keypoints[person][self.keypoints_dict['Right Knee'], :].tolist()
                knee = midpoint(left_knee, right_knee)
                
                # calculate angle
                self.angles[person][self.eval_mode] = calculate_angle(hip, shoulder, knee)
                if not THRESHOLD["hip"][0] <= self.angles[person][self.eval_mode] <= THRESHOLD["hip"][1]:
                    self.warning[person][self.eval_mode] = True

                self.visualize_eval(person, hip, shoulder, knee)
            
            elif mode.lower() == 'knee':
                self.eval_mode = 2
                
                left_hip = self.keypoints[person][self.keypoints_dict['Left Hip'], :].tolist()
                right_hip = self.keypoints[person][self.keypoints_dict['Right Hip'], :].tolist()
                hip = midpoint(left_hip, right_hip)
                
                left_knee = self.keypoints[person][self.keypoints_dict['Left Knee'], :].tolist()
                right_knee = self.keypoints[person][self.keypoints_dict['Right Knee'], :].tolist()
                knee = midpoint(left_knee, right_knee)
                
                left_ankle = self.keypoints[person][self.keypoints_dict['Left Ankle'], :].tolist()
                right_ankle = self.keypoints[person][self.keypoints_dict['Right Ankle'], :].tolist()
                ankle = midpoint(left_ankle, right_ankle)
                
                # calculate angle
                self.angles[person][self.eval_mode] = calculate_angle(knee, hip, ankle)
                if not THRESHOLD["knee"][0] <= self.angles[person][self.eval_mode] <= THRESHOLD["knee"][1]:
                    self.warning[person][self.eval_mode] = True

                self.visualize_eval(person, knee, hip, ankle)
            
            elif mode.lower() == 'elbow':
                self.eval_mode = 3
                
                left_shoulder = self.keypoints[person][self.keypoints_dict['Left Shoulder'], :].tolist()
                right_shoulder = self.keypoints[person][self.keypoints_dict['Right Shoulder'], :].tolist()
                shoulder = midpoint(left_shoulder, right_shoulder)
                
                left_elbow = self.keypoints[person][self.keypoints_dict['Left Elbow'], :].tolist()
                right_elbow = self.keypoints[person][self.keypoints_dict['Right Elbow'], :].tolist()
                elbow = midpoint(left_elbow, right_elbow)
                
                left_wrist = self.keypoints[person][self.keypoints_dict['Left Wrist'], :].tolist()
                right_wrist = self.keypoints[person][self.keypoints_dict['Right Wrist'], :].tolist()
                wrist = midpoint(left_wrist, right_wrist)
                
                # calculate angle
                self.angles[person][self.eval_mode] = calculate_angle(elbow, shoulder, wrist)
                if not THRESHOLD["elbow"][0] <= self.angles[person][self.eval_mode] <= THRESHOLD["elbow"][1]:
                    self.warning[person][self.eval_mode] = True

                self.visualize_eval(person, elbow, shoulder, wrist)


    def visualize_eval(self, 
                       person: int,
                       reference_point: list[int], 
                       point1: list[int], 
                       point2: list[int]):
        """
        Visualizes the evaluation by drawing points, lines, and angles on the frame.

        Args:
            person (int): The index of the person.
            reference_point (list[int]): The reference point coordinates.
            point1 (list[int]): The first point coordinates.
            point2 (list[int]): The second point coordinates.
        """
        
        check = check_zero_points(reference_point, point1, point2)

        if check:
            addText(self.frame, self.angles[person][self.eval_mode], reference_point)
            draw_point(self.frame, reference_point)
            draw_point(self.frame, point1)
            draw_point(self.frame, point2)
            draw_line(self.frame, reference_point, point1)
            draw_line(self.frame, reference_point, point2)
    
    def calculate_warning(self, fps):
        sum_warning = self.warning.sum(axis=0)
        self.warnings_timer = self.warnings_timer + (sum_warning / fps)
        self.visualize_warnings()

    def visualize_warnings(self):
        addText(self.frame, f"Trunk timer: {self.warnings_timer[0]:.2f}", [50, 50])
        addText(self.frame, f"Hip timer  : {self.warnings_timer[1]:.2f}", [50, 100])
        addText(self.frame, f"Knee timer : {self.warnings_timer[2]:.2f}", [50, 150])
        addText(self.frame, f"Elbow timer: {self.warnings_timer[3]:.2f}", [50, 200])