import cv2
import json
import base64
import numpy as np
import mediapipe as mp
import tensorflow as tf
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from tensorflow.keras.preprocessing.image import img_to_array

# Constants
DESIRED_HEIGHT = 480
DESIRED_WIDTH = 480
BG_COLOR = (192, 192, 192)  # gray
MASK_COLOR = (255, 255, 255)  # white


# Function to segmentate image
def segmentate(file):
    base_options = python.BaseOptions(model_asset_path="hair_segmenter.tflite")
    options = vision.ImageSegmenterOptions(
        base_options=base_options, output_category_mask=True
    )

    with vision.ImageSegmenter.create_from_options(options) as segmenter:
        decoded_image = base64.b64decode(file)
        img_np = np.frombuffer(decoded_image, np.uint8)
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


def predict_image(file):
    decoded_image = base64.b64decode(file)
    img_np = np.frombuffer(decoded_image, np.uint8)
    image = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (224, 224))
    image_array = img_to_array(image) / 255.0
    img_array = np.expand_dims(image_array, axis=0)

    model = tf.keras.models.load_model("models/final_model.keras")

    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])

    return predicted_class + 1, predictions[0]


def predict(image):
    # Redimensionner et normaliser l'image
    data = cv2.resize(image, (64, 64))
    data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    ims = np.reshape(data, (1, 64, 64, 3)) / 255.0

    model = tf.keras.models.load_model("models/bald_classifity.h5")
    res = model.predict(ims)

    return res


def lambda_handler(event, context):
    # Log pour débogage
    print(event)

    # Gestion des requêtes OPTIONS pour CORS
    if event["httpMethod"] == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Headers": "Content-Type",
                "Content-Type": "application/json",
            },
            "body": json.dumps("CORS preflight response"),
        }

    body = json.loads(event["body"])

    # Vérifier si le fichier est présent dans l'événement
    if "file_front" not in body.keys() or "file_top" not in body.keys():
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "No file provided"}),
        }

    file_front = body["file_front"]
    file_top = body["file_top"]

    # Appeler la fonction segmentate et traiter l'image
    try:
        print("front pic")
        scale, _ = segmentate(file_front)
        print("scale: ", scale)

        print("top pic")
        scale2, _ = predict_image(file_top)
        print("scale:", scale2)

        print("final scale:")
        final_scale = max(scale, scale2)
        print(final_scale)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "OPTIONS,POST",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps({"nordwood_scale": str(final_scale)}),
        }
    except Exception as e:
        # Gérer les exceptions et log pour débogage
        print(f"Error during processing: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "Internal server error", "details": str(e)}),
        }
