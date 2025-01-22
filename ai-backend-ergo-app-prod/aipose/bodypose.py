import cv2
import mediapipe as mp
import numpy as np
import logging

# Initialize logger
logger = logging.getLogger('myapp')

class PoseAnalyzer:
    def __init__(self):
        """Defines the parameters to be used in the operations for this class.
        """
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose()

    @staticmethod
    def calculate_angle(point1, point2, point3):
        """Calculates the angle between 3 coordinates

        Args:
            point1 (Coordinates): x,y values of the point
            point2 (Coordinates): x,y values of the point
            point3 (Coordinates): x,y values of the point

        Returns:
            Angle: Angle between points in degrees
        """
        # Create vectors from the points
        a = np.array([point1[0] - point2[0], point1[1] - point2[1]])
        b = np.array([point3[0] - point2[0], point3[1] - point2[1]])
        # Calculate dot product and magnitudes
        dot_product = np.dot(a, b)
        magnitude_a = np.linalg.norm(a)
        magnitude_b = np.linalg.norm(b)
        # Calculate the angle and convert to degrees
        angle = np.arccos(dot_product / (magnitude_a * magnitude_b))
        angle_degrees = np.degrees(angle)
        logger.debug(f"Calculated angle: {angle_degrees:.2f} degrees between points {point1}, {point2}, {point3}")
        return angle_degrees

    @staticmethod
    def preprocess_image(image_path):
        """Empty method for further preprocessing of image now acts as a checker

        Args:
            image_path (String): Path of image file

        Raises:
            ValueError: Triggered when the image path or the image format is not correct should be jpeg and png

        Returns:
            image: the initial image at the source
        """
        # Read the image from the path
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Invalid image file. Please check the image path and format.")
        # Convert the image to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image_rgb

    def analyze_pose(self, image_path):
        """Analyses the body image

        Args:
            image_path (String): Path to the image to be processed

        Returns:
            String: Compilation of all the responses for the 3 conditions in one string
        """
        global shoulder, hip, knee, ankle
        # Preprocess the image
        image = self.preprocess_image(image_path)
        logger.debug(f"Image preprocessed: {image_path}")

        # Process the image to get pose landmarks
        results = self.pose.process(image)

        if not results.pose_landmarks:
            logger.warning("No pose landmarks detected.")
            return "Improper picture. Please provide a clearer image.", None, None

        # Extract keypoints and visibility scores
        keypoints = np.array([[landmark.x, landmark.y] for landmark in results.pose_landmarks.landmark])
        scores = np.array([landmark.visibility for landmark in results.pose_landmarks.landmark])
        logger.debug(f"Keypoints: {keypoints}")
        logger.debug(f"Visibility scores: {scores}")

        # Check confidence levels
        low_confidence_points = np.sum(scores < 0.2)
        if low_confidence_points / len(scores) > 0.75:
            logger.warning("Low confidence in more than 75% of keypoints.")
            return "Improper picture. Please provide a clearer image.", keypoints, scores

        # Create a dictionary of landmarks
        landmarks = {landmark: keypoints[self.mp_pose.PoseLandmark[landmark].value]
                     for landmark in self.mp_pose.PoseLandmark.__members__.keys()}

        # Extract specific landmarks
        nose = landmarks['NOSE']
        left_ear = landmarks['LEFT_EAR']
        right_ear = landmarks['RIGHT_EAR']
        left_shoulder = landmarks['LEFT_SHOULDER']
        right_shoulder = landmarks['RIGHT_SHOULDER']
        left_hip = landmarks['LEFT_HIP']
        right_hip = landmarks['RIGHT_HIP']
        left_knee = landmarks['LEFT_KNEE']
        right_knee = landmarks['RIGHT_KNEE']
        left_ankle = landmarks['LEFT_ANKLE']
        right_ankle = landmarks['RIGHT_ANKLE']

        logger.debug(f"Landmarks extracted: {landmarks}")

        analysis_results = ""

        # Determine facing direction by comparing the horizontal positions of the nose and ears
        if abs(nose[0] - left_ear[0]) < abs(nose[0] - right_ear[0]):
            facing_side = "left"
            shoulder, hip, knee, ankle = right_shoulder, right_hip, right_knee, right_ankle
        elif abs(nose[0] - left_ear[0]) > abs(nose[0] - right_ear[0]):
            facing_side = "right"
            shoulder, hip, knee, ankle = left_shoulder, left_hip, left_knee, left_ankle
        else:
            facing_side = "ambiguous"

        logger.info(f"Facing side determined: {facing_side}")

        if facing_side != "ambiguous":
            # Calculate angles between specific landmarks
            shoulder_hip_knee_angle = self.calculate_angle(shoulder, hip, knee)
            hip_knee_ankle_angle = self.calculate_angle(hip, knee, ankle)

            logger.info(f"Shoulder-Hip-Knee angle: {shoulder_hip_knee_angle:.2f}")
            logger.info(f"Hip-Knee-Ankle angle: {hip_knee_ankle_angle:.2f}")

            # Determine posture based on angles
            if 80 <= shoulder_hip_knee_angle <= 120:
                analysis_results += "Neutral\n"
            elif shoulder_hip_knee_angle < 80:
                analysis_results += "Positive\n"
            else:
                analysis_results += "Negative\n"

            if 85 <= hip_knee_ankle_angle <= 115:
                analysis_results += "Neutral\n"
            elif hip_knee_ankle_angle < 85:
                analysis_results += "Positive\n"
            else:
                analysis_results += "Negative\n"

        return analysis_results.strip()
