import os
import cv2
from inference_sdk import InferenceHTTPClient
from config import settings
from . import Detect_Eye

# Initialize the inference client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=settings.ROBOFLOW_API_KEY
)
BASE_DIR = os.path.join(settings.MEDIA_ROOT,"Detect_Eye")
EYE_Resize_DIR = os.path.join(BASE_DIR, "resizeeye")

def resize_image(image_path):
    n_image = cv2.imread(image_path)
    n_image_resized = cv2.resize(n_image, (640, 640))
    os.makedirs(EYE_Resize_DIR, exist_ok=True)
    image_name = os.path.basename(image_path)  # استخراج اسم الصورة
    resized_image_path = os.path.join(EYE_Resize_DIR, image_name)  # مسار الصورة المعدلة
    cv2.imwrite(resized_image_path, n_image_resized)
    return resized_image_path

def disease_detect(image_path):
    image=resize_image(image_path)
    result = Detect_Eye.classify_and_save_image(image)
    if result == "Eye":
        image,label=run_model(image)
        return image,label
    
    elif result == "No eye detected":
        return None, "No eye detected in the image."
    
    elif result == "No sufficient confidence.":
        return None, "The model did not find a confident prediction."
    
    else:
        return None, "Error during RobowFlow inference hint:'Check Internet'."

def run_model(image):
    response = CLIENT.infer(image, "ccatract/4")
    
    predictions = response.get('predictions', [])
    
    if predictions:
        label = None  # تعيين قيمة افتراضية للـ label
        for prediction in predictions:
            label = prediction.get('class')
            # image, label = draw_box(image, prediction)
        return image, label
    else:
        return image, "No Diseases detected."
        # response = CLIENT.infer(image, "ccatract/4")
        # if response['predictions']:
        #     for prediction in response['predictions']:
        #         image, label=draw_box(image,prediction)
        #     return image, label
        # else:
        #     # return None, "No Diseases detected."
        #     return image, "No Diseases detected."

def draw_box(image,prediction):
                x, y = prediction['x'], prediction['y']
                width, height = prediction['width'], prediction['height']
                predicted_conf=prediction['confidence']*100
                label = prediction['class']
                # label = prediction.get('class')
                start_point = (int(x - width / 2), int(y - height / 2))
                end_point = (int(x + width / 2), int(y + height / 2))
                text_position = (start_point[0], start_point[1] - 10)
                # Draw the bounding box and label on the image
                formatted_conf = f"{predicted_conf:.1f}"
                text = f"{label} {formatted_conf}"
                cv2.rectangle(image, start_point, end_point, (255, 0, 0), 2)
                cv2.putText(image, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 2)
                return image,label

