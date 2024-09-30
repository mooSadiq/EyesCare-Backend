from transformers import AutoModelForImageClassification, pipeline
from transformers import AutoFeatureExtractor


# تحديد المعرف الصحيح للنموذج
model_id = "smartgmin/Entrnal_5class_agumm_last_newV7_model"


# تحميل النموذج من TensorFlow باستخدام from_tf=True
model = AutoModelForImageClassification.from_pretrained(
    model_id, from_tf=True, cache_dir="apps/diagnosis/path"
)

# تحميل feature extractor إذا كان النموذج بحاجة إليه
feature_extractor = AutoFeatureExtractor.from_pretrained(
    model_id, cache_dir="apps/diagnosis/path"
)

classifier = pipeline(
    "image-classification", model=model, feature_extractor=feature_extractor
)

yl = classifier("GLAUCOMA-ON1-700x467.jpg")
max_item = max(yl, key=lambda x: x["score"])
nn = "{:f}".format(max_item["score"])
dd = max_item["label"]

from transformers import AutoModelForImageClassification, pipeline
from transformers import AutoFeatureExtractor
import cv2
import numpy as np

# تحديد المعرف الصحيح للنموذج المستخدم في التصنيف
model_id = "smartgmin/Entrnal_5class_agumm_last_newV7_model"

# تحميل نموذج تصنيف الصور من TensorFlow
image_classification_model = AutoModelForImageClassification.from_pretrained(model_id, from_tf=True, cache_dir="apps/diagnosis/path"
)

# تحميل معالج الميزات الذي يساعد في تجهيز الصور للنموذج
feature_extractor = AutoFeatureExtractor.from_pretrained(model_id, cache_dir="apps/diagnosis/path"
)

# إنشاء أنبوب التصنيف باستخدام النموذج ومعالج الميزات
image_classifier = pipeline(
    "image-classification",
    model=image_classification_model,
    feature_extractor=feature_extractor,
)


def classify_image(image):
    
   

    # التحقق من تحميل الصورة بنجاح
    if image is None:
        return {"error": "لم يتم العثور على الصورة   "}

    # استخدام الأنبوب لتصنيف الصورة
    classification_results = image_classifier(image)

    # استخراج أعلى نتيجة من التصنيفات
    best_prediction = max(classification_results, key=lambda x: x["score"])

    # تنسيق درجة الثقة لتكون بشكل عدد عشري
    confidence_score = "{:f}".format(best_prediction["score"])
    predicted_label = best_prediction["label"]

    # إعادة نتيجة التصنيف كقاموس
    return {"label": predicted_label, "confidence": confidence_score}


# مثال على كيفية استخدام الدالة
# result = classify_image('path/to/image.jpg')
# print(result)
