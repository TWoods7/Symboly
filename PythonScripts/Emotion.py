# Emotion.py
import os
import cv2
import numpy as np
import mediapipe as mp

# Setup paths relative to this script
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, 'face_landmarker.task')

# Initialize MediaPipe once when the script is imported
base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
options = mp.tasks.vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=True,
    num_faces=1
)
detector = mp.tasks.vision.FaceLandmarker.create_from_options(options)

def get_alertness_score(pil_screenshot):
    # Convert PIL screenshot to NumPy array (RGB)
    frame = np.array(pil_screenshot)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
    
    detection_result = detector.detect(mp_image)
    
    if detection_result.face_blendshapes:
        scores = {b.category_name: b.score for b in detection_result.face_blendshapes[0]}
        # eyeBlink: 1.0 is closed, 0.0 is open.
        avg_openness = 1.0 - ((scores['eyeBlinkLeft'] + scores['eyeBlinkRight']) / 2)
        brow_lift = (scores['browOuterUpLeft'] + scores['browOuterUpRight']) / 2
        
        raw_score = (avg_openness * 0.8) + (brow_lift * 0.2)
        return int(np.clip(raw_score * 10, 1, 10))
    
    return 1 # Default if no face found