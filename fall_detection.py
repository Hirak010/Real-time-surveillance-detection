import cv2
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle > 180.0:
        angle = 360-angle
        
    return int(angle)

def detect_fall(frame, pose):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if not results.pose_landmarks:
        return image, None, None

    image_height, image_width, _ = image.shape
    landmarks = results.pose_landmarks.landmark

    # Extract relevant landmarks
    nose = [int(landmarks[mp_pose.PoseLandmark.NOSE].x * image_width),
            int(landmarks[mp_pose.PoseLandmark.NOSE].y * image_height)]
    left_heel = [int(landmarks[mp_pose.PoseLandmark.LEFT_HEEL].x * image_width),
                 int(landmarks[mp_pose.PoseLandmark.LEFT_HEEL].y * image_height)]
    right_heel = [int(landmarks[mp_pose.PoseLandmark.RIGHT_HEEL].x * image_width),
                  int(landmarks[mp_pose.PoseLandmark.RIGHT_HEEL].y * image_height)]

    # Calculate the midpoint between heels
    heel_midpoint = [(left_heel[0] + right_heel[0]) // 2, (left_heel[1] + right_heel[1]) // 2]

    # Calculate the fall distance
    fall_distance = heel_midpoint[0] - nose[0]

    # Determine if falling or standing
    falling = abs(fall_distance) > 50
    standing = abs(fall_distance) <= 50

    # Draw landmarks
    mp_drawing.draw_landmarks(
        image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(255,255,255), thickness=2, circle_radius=2), 
        mp_drawing.DrawingSpec(color=(0,0,0), thickness=2, circle_radius=2) 
    )

    return image, falling, standing

# You can add more helper functions here if needed
