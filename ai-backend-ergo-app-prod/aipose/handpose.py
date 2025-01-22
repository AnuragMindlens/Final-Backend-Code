import mediapipe as mp
import numpy as np
import os
import requests
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import logging

# Initialize logger
logger = logging.getLogger('myapp')

def download_model(url, save_path):
    """Download the AI model if not present on system.

    Args:
        url (String): Location where model is on the web
        save_path (String): Path to save the model after download
    """
    if not os.path.exists(save_path):
        try:
            response = requests.get(url)
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                file.write(response.content)
            logger.info(f"Model downloaded and saved as {save_path}")
        except requests.RequestException as e:
            logger.error(f"An error occurred while downloading the model: {e}")


def analyze_hand_bend(landmarks):
    """Checks if the hands are bent 

    Args:
        landmarks (Array): Contains an array of all the points and their x and y coordinates

    Returns:
        String: Positive, negative, neutral depending on how the hand is.
        Overbend is positive,
        Underbend is negative,
        No bend is neutral.
    """
    # Extract relevant landmarks
    wrist = landmarks[0]
    middle_mcp = landmarks[9]
    middle_tip = landmarks[12]

    buffer = 0.05  # Adjusted buffer for neutral category
    if middle_tip.y < middle_mcp.y - buffer and middle_tip.y < wrist.y - buffer:
        logger.info(f"Hand bend detected: Overbend (Positive) - Wrist: {wrist}, Middle MCP: {middle_mcp}, Middle Tip: {middle_tip}")
        return "Positive\n"
    elif middle_tip.y > middle_mcp.y + buffer and middle_tip.y > wrist.y + buffer:
        logger.info(f"Hand bend detected: Underbend (Negative) - Wrist: {wrist}, Middle MCP: {middle_mcp}, Middle Tip: {middle_tip}")
        return "Negative\n"
    else:
        logger.info(f"Hand bend detected: No bend (Neutral) - Wrist: {wrist}, Middle MCP: {middle_mcp}, Middle Tip: {middle_tip}")
        return "Neutral\n"


def analyze_wrist_flexion(landmarks):
    """Checks if the hands are flexed

    Args:
        landmarks (Array): Contains an array of all the points and their x and y coordinates

    Returns:
        String: Positive, negative, neutral depending on how the hand is.
        Overflexion is positive,
        Underflexion is negative,
        No flexion is neutral.
    """
    # Extract relevant landmarks
    wrist = landmarks[0]
    index_mcp = landmarks[5]
    pinky_mcp = landmarks[17]

    buffer = 0.05  # Adjusted buffer for neutral category
    if index_mcp.y < wrist.y - buffer and pinky_mcp.y < wrist.y - buffer:
        logger.info(f"Wrist flexion detected: Overflexion (Positive) - Wrist: {wrist}, Index MCP: {index_mcp}, Pinky MCP: {pinky_mcp}")
        return "Positive\n"
    elif index_mcp.y > wrist.y + buffer and pinky_mcp.y > wrist.y + buffer:
        logger.info(f"Wrist flexion detected: Underflexion (Negative) - Wrist: {wrist}, Index MCP: {index_mcp}, Pinky MCP: {pinky_mcp}")
        return "Negative\n"
    else:
        logger.info(f"Wrist flexion detected: No flexion (Neutral) - Wrist: {wrist}, Index MCP: {index_mcp}, Pinky MCP: {pinky_mcp}")
        return "Neutral\n"


def analyze_claw_grip(landmarks):
    """Checks if hand is like a claw when operating mouse

    Args:
        landmarks (Array): Contains an array of all the points and their x and y coordinates
    Returns:
         String: Positive, negative depending on how the hand is.
        No claw grip is positive,
        Claw grip is negative.
    """
    threshold = 0.15  # Slightly increased threshold for neutral category
    bent_fingers = sum(
        np.linalg.norm(np.array([landmarks[tip_index].x, landmarks[tip_index].y]) -
                       np.array([landmarks[tip_index - 2].x, landmarks[tip_index - 2].y])) < threshold
        for tip_index in [8, 12, 16, 20]
    )

    logger.info(f"Claw grip detected: {'Claw grip (Negative)' if bent_fingers >= 3 else 'No claw grip (Positive)'} - Bent fingers: {bent_fingers}")
    return "Negative\n" if bent_fingers >= 3 else "Positive\n"


def get_landmarks_string(detection_result):
    """Combines all the results together to send to the website

    Args:
        detection_result : Models response to the images given

    Returns:
        String: Compilation of all the responses for flexion, bend, claw grip in one string
    """
    results = ""
    for i, handedness_list in enumerate(detection_result.handedness):
        for _ in handedness_list:
            landmarks = detection_result.hand_landmarks[i]
            # Analyze hand bend, wrist flexion, and claw grip for each detected hand
            results += analyze_hand_bend(landmarks)
            results += analyze_wrist_flexion(landmarks)
            results += analyze_claw_grip(landmarks)
    return results


class HandPoseAnalyzer:
    landmark_names = [
        "WRIST", "THUMB_CMC", "THUMB_MCP", "THUMB_IP", "THUMB_TIP",
        "INDEX_FINGER_MCP", "INDEX_FINGER_PIP", "INDEX_FINGER_DIP", "INDEX_FINGER_TIP",
        "MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP",
        "RING_FINGER_MCP", "RING_FINGER_PIP", "RING_FINGER_DIP", "RING_FINGER_TIP",
        "PINKY_MCP", "PINKY_PIP", "PINKY_DIP", "PINKY_TIP"
    ]

    def __init__(self):
        """Defines the parameters to be used in the operations for this class.
        """
        self.detector = None
        self.options = None
        self.model_url = ('https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1'
                          '/hand_landmarker.task')
        self.model_path = 'hand_landmarker.task'
        # Download the model if not already present
        download_model(self.model_url, self.model_path)
        # Set up the hand detector
        self.setup_detector()

    def setup_detector(self):
        """Start up the hand detector.
        """
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        self.options = vision.HandLandmarkerOptions(base_options=base_options, num_hands=2)
        self.detector = vision.HandLandmarker.create_from_options(self.options)

    def analyze_hand_pose(self, image_path):
        """Analyzes the hand image

        Args:
            image_path (String): Location of the image

        Returns:
            String: Compilation of all the responses for flexion, bend, claw grip in one string
        """
        # Read the image from the file
        image = mp.Image.create_from_file(image_path)
        # Detect hand landmarks in the image
        detection_result = self.detector.detect(image)

        if not detection_result.hand_landmarks:
            logger.warning("No hands detected.")
            return "No hands detected. Please take another picture."

        # Get the analysis results for the detected hand landmarks
        results = get_landmarks_string(detection_result)
        return results
