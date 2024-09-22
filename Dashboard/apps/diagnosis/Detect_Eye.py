import os
import cv2
from inference_sdk import InferenceHTTPClient
from django.conf import settings

# Initialize the inference client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=settings.ROBOFLOW_API_KEY_For_Detection
)

# Define directories
BASE_DIR = os.path.join(settings.MEDIA_ROOT,"Detect_Eye")
EYE_DETECT_DIR = os.path.join(BASE_DIR, "eyedetect")
EYE_DIR = os.path.join(BASE_DIR, "eye")
NO_EYE_DETECT_DIR = os.path.join(BASE_DIR, "No_Eye_Detect")

# Define colors for each class
CLASS_COLORS = {
    'Eye': (0, 255, 255),
    'Internal-Eye': (255, 0, 255)
}

def save_image(image_path, folder):
    """Save the original image in the specified folder."""
    os.makedirs(folder, exist_ok=True)
    image = cv2.imread(image_path)
    image_name = os.path.basename(image_path)
    cv2.imwrite(os.path.join(folder, image_name), image)

def save_image_with_boxes(image_path, prediction, folder):
    """Draw bounding boxes and save the image with predictions in the specified folder."""
    os.makedirs(folder, exist_ok=True)
    image = cv2.imread(image_path)
    x, y = prediction['x'], prediction['y']
    width, height = prediction['width'], prediction['height']
    predicted_class = prediction['class']
    predicted_conf=prediction['confidence']*100
    formatted_conf = f"{predicted_conf:.2f}"
    # Create the text to be displayed: class name and confidence
    text = f"{predicted_class} ({formatted_conf})"
    color = CLASS_COLORS.get(predicted_class)
    start_point = (int(x - width / 2), int(y - height / 2))
    end_point = (int(x + width / 2), int(y + height / 2))
    thickness = 2
    image_with_boxes = cv2.rectangle(image, start_point, end_point, color, thickness)
    
    # Add class name above the rectangle
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    font_thickness = 2
    text_position = (start_point[0], start_point[1] + 50)
    image_with_text = cv2.putText(image_with_boxes, text, text_position, font, font_scale, color, font_thickness, cv2.LINE_AA)
    
    image_name = os.path.basename(image_path)
    cv2.imwrite(os.path.join(folder, image_name), image_with_text)

def classify_and_save_image(image_path, model_id="all_eye_detect/2", confidence_threshold=55):
    """Classify the image, save it based on the detection result, and return the classification result."""
    try:
        result = CLIENT.infer(image_path, model_id=model_id)
        predictions = result.get('predictions', [])
        
        if not predictions:
            save_image(image_path, NO_EYE_DETECT_DIR)
            return "No detection: No eye detected"
        
        for prediction in predictions:
            if prediction['confidence'] >= confidence_threshold / 100:
                save_image(image_path, EYE_DIR)
                save_image_with_boxes(image_path, prediction, EYE_DETECT_DIR)
                predicted_class = prediction['class']
                return predicted_class
        
        save_image(image_path, NO_EYE_DETECT_DIR)
        return "No sufficient confidence."
    except Exception as e:
        save_image(image_path, NO_EYE_DETECT_DIR)
        return "Error during RobowFlow inference hint:'Check Internet'."

