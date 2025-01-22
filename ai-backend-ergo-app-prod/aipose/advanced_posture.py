import mediapipe as mp
import cv2
import numpy as np
import torch
import os
from django.conf import settings

class AdvancedPostureAnalyzer:
    def __init__(self):
        # Initialize MediaPipe Pose
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        # Initialize YOLO model for chair detection
        model_path = os.path.join(settings.BASE_DIR, 'models', 'yolov5')
        self.chair_model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        
        # Define thresholds
        self.DISTANCE_THRESHOLDS = {
            'good': 15,      # cm
            'moderate': 25   # cm
        }
        self.ANGLE_THRESHOLDS = {
            'min_good': 5,   # degrees
            'max_good': 20   # degrees
        }
        self.SIDE_VIEW_THRESHOLD = 100  # pixels for shoulder width

    def detect_chair(self, image):
        """
        Enhanced chair detection using YOLO
        """
        results = self.chair_model(image)
        chairs = results.pandas().xyxy[0][results.pandas().xyxy[0]['name'] == 'chair']
        
        if chairs.empty:
            return None
            
        # Get the chair with highest confidence
        best_chair = chairs.loc[chairs['confidence'].idxmax()]
        
        chair_bbox = {
            'x1': int(best_chair['xmin']),
            'y1': int(best_chair['ymin']),
            'x2': int(best_chair['xmax']),
            'y2': int(best_chair['ymax']),
            'confidence': float(best_chair['confidence'])
        }
        
        return chair_bbox

    def detect_body_landmarks(self, image):
        """
        Enhanced body landmark detection
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        
        if not results.pose_landmarks:
            return None
            
        h, w = image.shape[:2]
        landmarks = results.pose_landmarks.landmark
        
        body_points = {
            'nose': np.array([landmarks[self.mp_pose.PoseLandmark.NOSE].x * w,
                            landmarks[self.mp_pose.PoseLandmark.NOSE].y * h]),
            'left_shoulder': np.array([landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * w,
                                     landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * h]),
            'right_shoulder': np.array([landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * w,
                                      landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * h]),
            'left_hip': np.array([landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].x * w,
                                landmarks[self.mp_pose.PoseLandmark.LEFT_HIP].y * h]),
            'right_hip': np.array([landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].x * w,
                                 landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP].y * h])
        }
        
        return body_points

    def calculate_posture_metrics(self, body_points, chair_bbox):
        """
        Calculate comprehensive posture metrics with side view handling
        """
        # Calculate spine midline
        mid_shoulder = (body_points['left_shoulder'] + body_points['right_shoulder']) / 2
        mid_hip = (body_points['left_hip'] + body_points['right_hip']) / 2
        
        # Calculate spine angle
        spine_vector = mid_shoulder - mid_hip
        vertical = np.array([0, -1])
        spine_angle = np.degrees(np.arccos(np.dot(spine_vector, vertical) / 
                                         (np.linalg.norm(spine_vector) * np.linalg.norm(vertical))))
        
        # Detect if image is side view
        shoulder_width = np.linalg.norm(body_points['left_shoulder'] - body_points['right_shoulder'])
        is_side_view = shoulder_width < self.SIDE_VIEW_THRESHOLD
        
        # Calculate chair reference point
        if is_side_view:
            # For side view, use the middle of the chair back
            chair_reference = chair_bbox['x2'] - (chair_bbox['x2'] - chair_bbox['x1']) * 0.2
        else:
            # For front/back view, use the back of the chair
            chair_reference = chair_bbox['x2']
        
        # Calculate distance to chair
        spine_points = [mid_shoulder, mid_hip]
        distances = [abs(point[0] - chair_reference) for point in spine_points]
        avg_distance_pixels = np.mean(distances)
        
        # Convert to cm using chair as reference
        chair_width_pixels = chair_bbox['x2'] - chair_bbox['x1']
        pixels_per_cm = chair_width_pixels / 45  # assuming standard chair width
        distance_cm = avg_distance_pixels / pixels_per_cm
        
        # Apply minimum distance threshold
        distance_cm = max(0, min(distance_cm, 50))  # Cap at 50cm
        
        return {
            'spine_angle': spine_angle,
            'distance_cm': distance_cm,
            'is_side_view': is_side_view
        }

    def analyze_image(self, image):
        """
        Complete posture analysis
        """
        # Detect chair
        chair_bbox = self.detect_chair(image)
        if chair_bbox is None:
            return None, "No chair detected in image"
        
        # Detect body landmarks
        body_points = self.detect_body_landmarks(image)
        if body_points is None:
            return None, "Could not detect body landmarks"
            
        # Calculate metrics
        metrics = self.calculate_posture_metrics(body_points, chair_bbox)
        
        # Analyze posture
        status = []
        
        # Analyze back angle
        if metrics['spine_angle'] < self.ANGLE_THRESHOLDS['min_good']:
            status.append("Back is too straight")
        elif metrics['spine_angle'] > self.ANGLE_THRESHOLDS['max_good']:
            status.append("Excessive forward lean")
        else:
            status.append("Good back alignment")
            
        # Analyze chair support
        if metrics['distance_cm'] <= self.DISTANCE_THRESHOLDS['good']:
            status.append("Good use of chair support")
        elif metrics['distance_cm'] <= self.DISTANCE_THRESHOLDS['moderate']:
            status.append("Moderate distance from chair support")
        else:
            status.append("Not using chair support")
            
        return metrics, status, chair_bbox, body_points

    def visualize_results(self, image, body_points, chair_bbox, metrics):
        """
        Create visualization of analysis
        """
        vis_image = image.copy()
        
        # Draw chair bbox
        cv2.rectangle(vis_image, 
                     (chair_bbox['x1'], chair_bbox['y1']), 
                     (chair_bbox['x2'], chair_bbox['y2']), 
                     (0, 255, 0), 2)
        
        if metrics['is_side_view']:
            chair_reference = chair_bbox['x2'] - (chair_bbox['x2'] - chair_bbox['x1']) * 0.2
        else:
            chair_reference = chair_bbox['x2']
            
        # Draw chair reference line
        cv2.line(vis_image, 
                (int(chair_reference), chair_bbox['y1']), 
                (int(chair_reference), chair_bbox['y2']), 
                (0, 255, 255), 2)
        
        if body_points:
            # Draw spine line
            mid_shoulder = (body_points['left_shoulder'] + body_points['right_shoulder']) / 2
            mid_hip = (body_points['left_hip'] + body_points['right_hip']) / 2
            
            cv2.line(vis_image, 
                    tuple(mid_shoulder.astype(int)), 
                    tuple(mid_hip.astype(int)), 
                    (0, 0, 255), 2)
            
            # Draw distance lines
            cv2.line(vis_image, 
                    tuple(mid_shoulder.astype(int)), 
                    (int(chair_reference), int(mid_shoulder[1])), 
                    (255, 165, 0), 2)
            
        # Add measurements
        cv2.putText(vis_image, 
                   f"Spine Angle: {metrics['spine_angle']:.1f}°", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(vis_image, 
                   f"Distance: {metrics['distance_cm']:.1f}cm", 
                   (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(vis_image,
                   f"View: {'Side' if metrics['is_side_view'] else 'Front/Back'}", 
                   (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        return vis_image
