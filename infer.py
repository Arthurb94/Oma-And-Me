import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Chemin vers le modèle sauvegardé
model_path = "final_model.keras"

# Chargement du modèle
model = tf.keras.models.load_model(model_path)


# Fonction pour faire de l'inférence sur une seule image
def predict_image(image_path, model):
    # Charger et prétraiter l'image
    img = load_img(image_path, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Ajouter une dimension pour le batch
    img_array /= 255.0  # Normaliser les pixels

    # Faire la prédiction
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])

    return predicted_class + 1, predictions[0]


# Exemple d'utilisation
image_path = "training/datasets/hair_norwood_hamilton-1/test/6/20231224094540Ln5VZt_rgbshift_jpg.rf.126bb810c66904a4d298e9cd2fa4a512.jpg"
predicted_class, scores = predict_image(image_path, model)

print(f"Predicted class: {predicted_class}")
print(f"Scores: {scores}")
