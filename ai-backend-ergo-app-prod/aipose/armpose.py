import cv2
import mediapipe as mp
import numpy as np
import torch

def calculate_path_length(points):
    """
    Calculate the length of path given a list of points
    """
    length = 0
    for i in range(len(points)-1):
        length += np.sqrt(
            (points[i][0] - points[i+1][0])**2 + 
            (points[i][1] - points[i+1][1])**2
        )
    return length

def detect_screen(image, model):
    """
    Detect laptop/monitor screen with improved confidence
    """
    results = model(image)
    df = results.pandas().xyxy[0]
    
    # Filter for screens with higher confidence
    screens = df[
        (df['name'].isin(['laptop', 'monitor', 'tv'])) & 
        (df['confidence'] > 0.3)
    ]
    
    if not screens.empty:
        screen = screens.iloc[screens['confidence'].argmax()]
        bbox = screen[['xmin', 'ymin', 'xmax', 'ymax']].values.astype(int)
        return bbox
    return None

def detect_arm_and_screen(image):
    """
    Detect arm paths and screen distance with improved screen detection
    """
    mp_holistic = mp.solutions.holistic
    
    # Load YOLOv5 model
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    model.conf = 0.3
    
    # Detect screen first
    screen_bbox = detect_screen(image, model)
    
    # Process pose landmarks
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    with mp_holistic.Holistic(
        static_image_mode=True,
        model_complexity=2,
        enable_segmentation=True,
        min_detection_confidence=0.5) as holistic:
        
        results = holistic.process(image_rgb)
        annotated_image = image.copy()
        
        if results.pose_landmarks:
            h, w, _ = image.shape
            
            # Get shoulders and arm points
            left_arm_indices = [11, 13, 15, 17, 19, 21]  # Left shoulder to finger
            right_arm_indices = [12, 14, 16, 18, 20, 22]  # Right shoulder to finger
            
            # Process left arm
            left_points = []
            for idx in left_arm_indices:
                if idx < len(results.pose_landmarks.landmark):
                    landmark = results.pose_landmarks.landmark[idx]
                    point = (int(landmark.x * w), int(landmark.y * h))
                    left_points.append(point)
                    cv2.circle(annotated_image, point, 8, (0, 0, 255), -1)
            
            # Process right arm
            right_points = []
            for idx in right_arm_indices:
                if idx < len(results.pose_landmarks.landmark):
                    landmark = results.pose_landmarks.landmark[idx]
                    point = (int(landmark.x * w), int(landmark.y * h))
                    right_points.append(point)
                    cv2.circle(annotated_image, point, 8, (0, 0, 255), -1)
            
            # Draw arm paths
            for i in range(len(left_points)-1):
                cv2.line(annotated_image, left_points[i], left_points[i+1], (0, 255, 0), 3)
            for i in range(len(right_points)-1):
                cv2.line(annotated_image, right_points[i], right_points[i+1], (0, 255, 0), 3)
            cv2.line(annotated_image, left_points[0], right_points[0], (0, 255, 0), 3)
            
            # Calculate arm measurements
            left_arm_length = calculate_path_length(left_points)
            right_arm_length = calculate_path_length(right_points)
            
            # Convert to real-world measurements
            AVERAGE_ARM_LENGTH_CM = 74
            pixel_to_cm = AVERAGE_ARM_LENGTH_CM / ((left_arm_length + right_arm_length) / 2)
            left_arm_cm = left_arm_length * pixel_to_cm
            right_arm_cm = right_arm_length * pixel_to_cm
            
            # Calculate shoulder to screen distance if screen detected
            shoulder_center = ((left_points[0][0] + right_points[0][0])//2, 
                             (left_points[0][1] + right_points[0][1])//2)
            
            screen_distance_cm = 0
            if screen_bbox is not None:
                # Draw screen bbox
                cv2.rectangle(annotated_image, 
                            (screen_bbox[0], screen_bbox[1]), 
                            (screen_bbox[2], screen_bbox[3]), 
                            (255, 165, 0), 2)
                
                # Calculate screen center
                screen_center = (
                    (screen_bbox[0] + screen_bbox[2]) // 2,
                    (screen_bbox[1] + screen_bbox[3]) // 2
                )
                
                # Draw line from shoulder to screen
                cv2.line(annotated_image, shoulder_center, screen_center, (255, 165, 0), 3)
                cv2.circle(annotated_image, screen_center, 8, (255, 165, 0), -1)
                
                # Calculate screen distance
                screen_distance = np.sqrt(
                    (shoulder_center[0] - screen_center[0])**2 + 
                    (shoulder_center[1] - screen_center[1])**2
                )
                screen_distance_cm = screen_distance * pixel_to_cm
            
            # Convert annotated image to base64 for response
            _, buffer = cv2.imencode('.jpg', annotated_image)
            annotated_image_base64 = buffer.tobytes()
            
            return {
                'success': True,
                'left_arm_length': float(left_arm_cm),
                'right_arm_length': float(right_arm_cm),
                'screen_distance': float(screen_distance_cm),
                'annotated_image': annotated_image_base64
            }
            
        return {
            'success': False,
            'error': 'No body points detected in the image'
        }
