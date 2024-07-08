import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# Chemins des répertoires de données
train_dir = "training/datasets/hair_norwood_hamilton-1/train"
validation_dir = "training/datasets/hair_norwood_hamilton-1/valid"
test_dir = "training/datasets/hair_norwood_hamilton-1/test"

# Générateurs de données avec augmentation pour l'entraînement
train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode="nearest",
)

val_test_datagen = ImageDataGenerator(rescale=1.0 / 255)

train_generator = train_datagen.flow_from_directory(
    train_dir, target_size=(224, 224), batch_size=32, class_mode="categorical"
)

validation_generator = val_test_datagen.flow_from_directory(
    validation_dir, target_size=(224, 224), batch_size=32, class_mode="categorical"
)

test_generator = val_test_datagen.flow_from_directory(
    test_dir, target_size=(224, 224), batch_size=32, class_mode="categorical"
)

# Calculer steps_per_epoch et validation_steps
steps_per_epoch = train_generator.samples // train_generator.batch_size
validation_steps = validation_generator.samples // validation_generator.batch_size

# Construction du modèle CNN
model = Sequential(
    [
        Conv2D(32, (3, 3), activation="relu", input_shape=(224, 224, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation="relu"),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation="relu"),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(512, activation="relu"),
        Dropout(0.5),
        Dense(7, activation="softmax"),  # 7 classes pour l'échelle de Norwood
    ]
)

# Compilation du modèle
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Callbacks
checkpoint = ModelCheckpoint(
    "best_model2.keras", save_best_only=True, monitor="val_loss", mode="min"
)
# early_stopping = EarlyStopping(
#     monitor="val_loss", patience=10, restore_best_weights=True
# )

# Entraînement du modèle
history = model.fit(
    train_generator,
    steps_per_epoch=steps_per_epoch,
    validation_data=validation_generator,
    validation_steps=validation_steps,
    epochs=25,
    callbacks=[checkpoint],
)

# Évaluation sur le jeu de test
test_loss, test_acc = model.evaluate(
    test_generator, steps=test_generator.samples // test_generator.batch_size
)
print(f"Test accuracy: {test_acc}")

# Sauvegarde du modèle final
model.save("final_model2.keras")
