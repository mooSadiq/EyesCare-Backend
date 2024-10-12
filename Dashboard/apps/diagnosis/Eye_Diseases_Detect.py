# from transformers import AutoModelForImageClassification, pipeline
# from transformers import AutoFeatureExtractor
from inference_sdk import InferenceHTTPClient
from config import settings
from .Detect_Eye import classify_and_save_image
import os
import cv2
import numpy as np

# Load The Internal Eye Model
model_id = "smartgmin/Entrnal_5class_agumm_last_newV7_model"

# تحميل نموذج تصنيف الصور من TensorFlow
image_classification_model = AutoModelForImageClassification.from_pretrained(model_id, from_tf=True, cache_dir="apps/diagnosis/Internal_Eye_Model/path")

# تحميل معالج الميزات الذي يساعد في تجهيز الصور للنموذج
feature_extractor = AutoFeatureExtractor.from_pretrained(model_id, cache_dir="apps/diagnosis/Internal_Eye_Model/path")

image_classifier = pipeline(
    "image-classification",
    model=image_classification_model,
    feature_extractor=feature_extractor,
)

# Initialize the inference client For External Eye
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key=settings.ROBOFLOW_API_KEY
)


BASE_DIR = os.path.join(settings.MEDIA_ROOT, "Detect_Eye")
EYE_Resize_DIR = os.path.join(BASE_DIR, "resizeeye")
EYE_Dig_DIR = os.path.join(BASE_DIR, "Dign")


def get_full_media_url(relative_path):
    media_url = os.path.join(settings.MEDIA_URL, relative_path)
    media_url = media_url.replace("\\", "/")
    return media_url


def makedir(dir, imagepath):
    os.makedirs(dir, exist_ok=True)
    image_name = os.path.basename(imagepath)
    new_image_path = os.path.join(dir, image_name)
    return new_image_path


def resize_image(image_path):
    n_image = cv2.imread(image_path)
    n_image_resized = cv2.resize(n_image, (640, 640))
    resized_image_path = makedir(EYE_Resize_DIR, image_path)
    cv2.imwrite(resized_image_path, n_image_resized)
    return resized_image_path


def disease_detect(image_path):
    image = resize_image(image_path)
    result = classify_and_save_image(image)
    if result == "Eye":
        image, label, conf = run_model(image)
        return image, label, conf
    elif result == "Internal-Eye":
        image, label, conf = classify_internalEye_image(image)
        return image, label, conf
    elif result == "No detection: No eye detected":
        return None, "No eye detected in the image.", None
    
    elif result == "No sufficient confidence.":
        return None, "The model did not find a confident prediction.", None
    else:
        return None, "Error during RobowFlow inference hint:'Check Internet'.", None


def run_model(image):
    response = CLIENT.infer(image, "ccatract/4")
    predictions = response.get('predictions', [])
    
    if predictions:
        for prediction in predictions:
            image, label, conf = draw_box(image, prediction)
            if conf >= 65:
                return image, label, conf
            else:
                return image, "No Diseases detected.", None
    else:
        return image, "No Diseases detected.", None


def draw_box(image, prediction):
    x, y = prediction['x'], prediction['y']
    width, height = prediction['width'], prediction['height']
    predicted_conf = prediction['confidence'] * 100
    label = prediction['class']
    start_point = (int(x - width / 2), int(y - height / 2))
    end_point = (int(x + width / 2), int(y + height / 2))
    text_position = (start_point[0], start_point[1] - 10)
    formatted_conf = f"{predicted_conf:.1f}"
    text = f"{label} {formatted_conf}"
    image_read = cv2.imread(image)
    cv2.rectangle(image_read, start_point, end_point, (255, 0, 0), 2)
    cv2.putText(image_read, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
    dig_image_path = makedir(EYE_Dig_DIR, image)
    cv2.imwrite(dig_image_path, image_read)
    relative_path = os.path.relpath(dig_image_path, settings.MEDIA_ROOT)
    dig_image_url = get_full_media_url(relative_path)
    return dig_image_url, label, predicted_conf


def classify_internalEye_image(image):
    classification_results = image_classifier(image)
    best_prediction = max(classification_results, key=lambda x: x["score"])
    confidence_score = "{:f}".format(best_prediction["score"]*100)
    predicted_label = best_prediction["label"]
    return None, predicted_label, confidence_score
