from math import dist
import cv2
import mediapipe as mp
import numpy as np
import logging

# Initialize logger
logger = logging.getLogger('myapp')

class DeskPoseAnalyzer:
    def __init__(self):
        """Defines the parameters to be used in the operations for this class."""
        self.mp_pose = mp.solutions.pose
        # Initialize the pose estimator with specific parameters
        self.pose = self.mp_pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False)
        # Define confidence and angle thresholds
        self.CONFIDENCE_THRESHOLD = 0.2
        self.ANGLE_THRESHOLD_LOW = 45
        self.ANGLE_THRESHOLD_HIGH = 135
        self.BODY_TOLERANCE = 0.2
        self.EYE_ANGLE_THRESHOLD_HIGH = 50
        self.EYE_ANGLE_THRESHOLD_LOW = -50
        self.WRIST_ELBOW_VERTICAL_TOLERANCE = 0.1
        self.SHOULDER_HIP_ANGLE_THRESHOLD = 160
        self.SHOULDER_BALANCE_TOLERANCE = 0.1

    @staticmethod
    def calculate_angle(point1, point2, point3):
        """Calculates the angle between 3 coordinates.

        Args:
            point1 (Coordinates): x,y values of the point.
            point2 (Coordinates): x,y values of the point.
            point3 (Coordinates): x,y values of the point.

        Returns:
            Angle: Angle between points in degrees.
        """
        # Create vectors from the points
        a = point1 - point2
        b = point3 - point2
        # Calculate dot product and magnitudes
        dot_product = np.dot(a, b)
        magnitude_a = np.linalg.norm(a)
        magnitude_b = np.linalg.norm(b)
        if magnitude_a == 0 or magnitude_b == 0:
            return 0
        # Calculate the angle and convert to degrees
        angle = np.arccos(dot_product / (magnitude_a * magnitude_b))
        angle_degrees = np.degrees(angle)
        logger.debug(f"Calculated angle: {angle_degrees:.2f} degrees between points {point1}, {point2}, {point3}")
        return angle_degrees

    @staticmethod
    def calculate_horizontal_angle(point1, point2):
        """Calculates the angle between the line connecting two points and the horizontal line at point2,
        with the angle being positive if point1 is above point2 and negative if below.

        Args:
            point1 (Coordinates): x, y values of the first point (e.g., eye).
            point2 (Coordinates): x, y values of the second point (e.g., ear).

        Returns:
            float: Angle in degrees, in the range of -90 to +90.
        """
        if point1[1] < point2[1]:
            return -100 
        # Calculate vector from point2 to point1
        vector = point1 - point2
        # Calculate the angle using arctan2, where the first argument is the y-component, and the second is the x-component
        angle_rad = np.arctan2(vector[1], vector[0])
        # Convert the angle from radians to degrees
        angle_deg = np.degrees(angle_rad)
        # Ensure the angle is within -90 to +90
        if angle_deg > 90:
            angle_deg -= 180
        elif angle_deg < -90:
            angle_deg += 180
        logger.debug(f"Calculated horizontal angle: {angle_deg:.2f} degrees between points {point1}, {point2}")
        return angle_deg

    @staticmethod
    def is_elbow_behind_shoulder_hip_line(side, shoulder, hip, elbow, wrist):
        """Checks if the elbow is behind or in front of the line from the shoulder to the hip.

        Args:
            side (str): 'left' or 'right' side of the body.
            shoulder (Coordinates): x,y values of the shoulder.
            hip (Coordinates): x,y values of the hip.
            elbow (Coordinates): x,y values of the elbow.
            wrist (Coordinates): x,y values of the wrist.

        Returns:
            int: -1, 0, or 1 based on the position and angle conditions.
        """
        # Create vectors from the points
        shoulder_to_hip = hip - shoulder
        shoulder_to_elbow = elbow - shoulder
        elbow_to_wrist = wrist - elbow
        
        # Calculate cross product to determine relative position
        cross_product = np.cross(shoulder_to_hip, shoulder_to_elbow)
        
        # Calculate the distance from the elbow to the line formed by shoulder and hip
        line_length = np.linalg.norm(shoulder_to_hip)
        distance = np.abs(cross_product) / line_length
        
        # Calculate the angle between the shoulder-elbow and elbow-wrist vectors
        shoulder_elbow_unit = shoulder_to_elbow / np.linalg.norm(shoulder_to_elbow)
        elbow_wrist_unit = elbow_to_wrist / np.linalg.norm(elbow_to_wrist)
        dot_product = np.dot(shoulder_elbow_unit, elbow_wrist_unit)
        
        # Clamp dot_product to avoid any potential floating-point errors outside the valid range for arccos
        dot_product = np.clip(dot_product, -1.0, 1.0)
        
        # Calculate the angle in degrees
        angle = np.degrees(np.arccos(dot_product))
        
        # Determine the return value based on the cross product, distance, angle, and normalized wrist y-coordinate
        if side == "left":
            if cross_product < 0 and distance < 0.035:
                if 80 <= angle <= 130:
                    logger.debug(f"Elbow position: Neutral (left side, angle: {angle:.2f}, distance: {distance:.4f})")
                    return 0 
                logger.debug(f"Elbow position: Positive (left side, angle: {angle:.2f}, distance: {distance:.4f})")
                return 1 if angle > 130 else -1
            logger.debug(f"Elbow position: Positive (left side, distance: {distance:.4f})")
            return 1 if cross_product and distance > 0.03 < 0 else -1
        elif side == "right":
            if cross_product > 0 and distance < 0.035:
                if 80 <= angle <= 130:
                    logger.debug(f"Elbow position: Neutral (right side, angle: {angle:.2f}, distance: {distance:.4f})")
                    return 0 
                logger.debug(f"Elbow position: Positive (right side, angle: {angle:.2f}, distance: {distance:.4f})")
                return 1 if angle > 130 else -1
            logger.debug(f"Elbow position: Positive (right side, distance: {distance:.4f})")
            return 1 if cross_product > 0 and distance > 0.03 else -1

    @staticmethod
    def preprocess_image(image_path):
        """Empty method for further preprocessing of image now acts as a checker.

        Args:
            image_path (String): Path of image file.

        Raises:
            ValueError: Triggered when the image path or the image format is not correct should be jpeg and png.

        Returns:
            image: the initial image at the source.
        """
        # Read the image from the path
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Invalid image file. Please check the image path and format.")
        return image

    def analyze_pose(self, image_path):
        """Analyses the body image.

        Args:
            image_path (String): Path to the image to be processed.

        Returns:
            String: Compilation of all the responses for the 3 conditions in one string.
        """
        # Preprocess the image
        image = self.preprocess_image(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        logger.debug(f"Image preprocessed: {image_path}")

        with self.mp_pose.Pose(static_image_mode=True, model_complexity=1, enable_segmentation=False) as pose:
            # Process the image to get pose landmarks
            results = pose.process(image_rgb)

            if not results.pose_landmarks:
                logger.warning("No pose landmarks detected.")
                return "Improper picture. Please take a better picture.", None, None

            # Extract keypoints and visibility scores
            keypoints_with_scores = np.array([[lm.x, lm.y, lm.visibility] for lm in results.pose_landmarks.landmark])
            keypoints = keypoints_with_scores[:, :2]
            scores = keypoints_with_scores[:, 2]
            logger.debug(f"Keypoints: {keypoints}")
            logger.debug(f"Visibility scores: {scores}")

            # Define keypoints of interest
            keypoints_of_interest_indices = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            low_confidence_points = np.sum(scores[keypoints_of_interest_indices] < self.CONFIDENCE_THRESHOLD)
            if low_confidence_points / len(keypoints_of_interest_indices) > 0.75:
                logger.warning("Low confidence in more than 75% of keypoints.")
                return "Improper picture. Please take a better picture.", keypoints_with_scores, scores

            # Extract specific landmarks
            nose, left_eye, right_eye, left_ear, right_ear, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip = \
                keypoints[[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]]

            # Determine facing direction by comparing the horizontal positions of the nose and ears
            facing_side = "right" if abs(nose[0] - left_ear[0]) < abs(nose[0] - right_ear[0]) else "left" if abs(
                nose[0] - left_ear[0]) > abs(nose[0] - right_ear[0]) else "ambiguous"

            logger.info(f"Facing side determined: {facing_side}")

            results_text = ""

            if facing_side != "ambiguous":
                # Select shoulder, elbow, wrist, hip, eye, and ear based on facing direction
                shoulder, elbow, wrist, hip, eye, ear = (
                    (right_shoulder, right_elbow, right_wrist, right_hip, right_eye, right_ear) 
                    if facing_side == "left" else 
                    (left_shoulder, left_elbow, left_wrist, left_hip, left_eye, left_ear)
                )

                # Calculate angles between specific landmarks
                shoulder_elbow_wrist_angle = self.calculate_angle(shoulder, elbow, wrist)
                eye_angle = self.calculate_horizontal_angle(eye, ear)
                
                logger.info(f"Shoulder-Elbow-Wrist angle: {shoulder_elbow_wrist_angle:.2f}")
                logger.info(f"Eye angle: {eye_angle:.2f}")
                
                # Normalize wrist coordinates by subtracting shoulder coordinates
                normalized_wrist = [(wrist[0] - shoulder[0])/shoulder[0], (wrist[1] - shoulder[1])/shoulder[1]]
                logger.debug(f"Normalized wrist coordinates: {normalized_wrist}")
                
                # Determine posture based on angles
                if shoulder_elbow_wrist_angle < self.ANGLE_THRESHOLD_LOW:
                    results_text += "positive\n"
                elif shoulder_elbow_wrist_angle > self.ANGLE_THRESHOLD_HIGH:
                    results_text += "negative\n"
                else:
                    # Check if the normalized wrist coordinates are higher than the normalized shoulder coordinates
                    if normalized_wrist[1] < 0.15:  # Assuming a lower y-coordinate means higher in your coordinate system
                        results_text += "negative\n"
                    else:
                        results_text += "neutral\n"
                
                # Determine eye angle posture
                if eye_angle > 10 and eye_angle<35:
                    results_text += "positive\n"
                elif eye_angle > 35:
                    results_text += "negative\n"
                else:
                    results_text += "neutral\n"

                # Check elbow position relative to shoulder-hip line
                elbow_position = self.is_elbow_behind_shoulder_hip_line(facing_side, shoulder, hip, elbow, wrist)
                if elbow_position == 0:
                    side = "neutral"
                elif elbow_position == 1:
                    side = "positive"
                else:
                    side = "negative"
                results_text += f"{side}\n"
            return results_text
