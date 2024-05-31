import cv2
import json
import keras
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Constants
DESIRED_HEIGHT = 480
DESIRED_WIDTH = 480
BG_COLOR = (192, 192, 192)  # gray
MASK_COLOR = (255, 255, 255)  # white


# Function to segmentate image
def segmentate(file):
    base_options = python.BaseOptions(model_asset_path="./hair_segmenter.tflite")
    options = vision.ImageSegmenterOptions(
        base_options=base_options, output_category_mask=True
    )

    with vision.ImageSegmenter.create_from_options(options) as segmenter:
        img_np = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        segmentation_result = segmenter.segment(image)

        category_mask = segmentation_result.category_mask

        image_data = image.numpy_view()
        fg_image = np.zeros(image_data.shape, dtype=np.uint8)
        fg_image[:] = MASK_COLOR
        bg_image = np.zeros(image_data.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR

        condition = np.stack((category_mask.numpy_view(),) * 3, axis=-1) > 0.2
        output_image = np.where(condition, fg_image, bg_image)

        prediction = predict(img)[0][0]
        limits = [0.002, 0.1, 0.4, 0.95, 0.97, 0.991, 1]
        scale = np.where(prediction < limits)[0][0] + 1

        return scale, output_image


def predict(image):
    # Redimensionner et normaliser l'image
    data = cv2.resize(image, (64, 64))
    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    ims = np.reshape(data, (1, 64, 64, 3)) / 255.0

    print(ims.shape)
    model = keras.models.load_model("models/bald_classifity.h5")
    res = model.predict(ims)

    return res


def lambda_handler(event, context):
    if "file" not in event.files:
        return json.dumps({"error": "No file provided"}), 400

    file = event.files["file"]

    scale, _ = segmentate(file)

    return json.dumps({"nordwood_scale": str(scale)})
