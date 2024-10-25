from decimal import Decimal
from inference_sdk import InferenceHTTPClient
from config import settings
from .Detect_Eye import classify_and_save_image
from gradio_client import Client
import json
import os
import cv2

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
    image = resize_image(image_path.path)
    result = classify_and_save_image(image)
    if result == "Eye":
        image, label, conf = run_model(image)
        return image, label, conf
    elif result == "Internal-Eye":
        image, label, conf = classify_internalEye_image(image_path.url)
        return image, label, conf

    elif result == "No detection: No eye detected":
        return None, "No eye detected in the image.", None

    elif result == "No sufficient confidence.":
        return None, "The model did not find a confident prediction.", None
    else:
        return None, "Error during RobowFlow inference hint:'Check Internet'.", None





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



def fix_media_path(image_path):
    parts = image_path.split('media/')
    if len(parts) > 1:
         fixed_path = 'media/' + parts[-1]
    return fixed_path

def classify_internalEye_image(image):
    client = Client("mostafasmart/EyesCareVit")
    fixed_image_path = fix_media_path(image)
    image=f"https://eyescareapp.pythonanywhere.com/{fixed_image_path}"
    try:
        result = client.predict(
        image_url=image,
        api_name="/predict"
        )
        result_json = json.loads(result)
        label = result_json['label']
        score = Decimal(result_json['score'])*100
        if score<80:
            return None, "No Diseases detected.", None
        else:
            return None,label,score
    except:
        return None,"Error during RobowFlow inference hint:'Check Internet'.",None






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

