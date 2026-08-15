"""
AgroScan AI — MobileNetV2 Transfer Learning Model Trainer

Usage:
    python train_mobilenet.py --data_dir ./data/raw --epochs 10
"""

import os
import argparse
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

def train_model(data_dir: str, output_model_path: str, epochs: int = 10, batch_size: int = 32):
    print("=========================================================")
    print(" AgroScan AI — MobileNetV2 Transfer Learning Pipeline")
    print("=========================================================")
    
    try:
        import tensorflow as tf
        from tensorflow.keras.applications import MobileNetV2
        from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
        from tensorflow.keras.models import Model
        from tensorflow.keras.preprocessing.image import ImageDataGenerator

        print(f"TensorFlow Version: {tf.__version__}")

        if not os.path.exists(data_dir):
            print(f"Warning: Dataset directory {data_dir} does not exist yet.")
            print("Please download the PlantVillage dataset to ml/data/raw to train full weights.")
            return

        # Data Augmentation & Train/Val Split
        datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=25,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.15,
            zoom_range=0.2,
            horizontal_flip=True,
            validation_split=0.2
        )

        train_gen = datagen.flow_from_directory(
            data_dir,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='categorical',
            subset='training'
        )

        val_gen = datagen.flow_from_directory(
            data_dir,
            target_size=(224, 224),
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation'
        )

        # Base MobileNetV2 Architecture
        base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        base_model.trainable = False  # Freeze base layers for transfer learning

        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dropout(0.3)(x)
        x = Dense(128, activation='relu')(x)
        predictions = Dense(train_gen.num_classes, activation='softmax')(x)

        model = Model(inputs=base_model.input, outputs=predictions)

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        print(f"Training MobileNetV2 for {epochs} epochs...")
        history = model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=epochs
        )

        os.makedirs(os.path.dirname(output_model_path), exist_ok=True)
        model.save(output_model_path)
        print(f"Model saved successfully to {output_model_path}")

        # Evaluate Metrics
        val_gen.reset()
        y_pred = model.predict(val_gen)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true = val_gen.classes

        print("\n--- Classification Report ---")
        print(classification_report(y_true, y_pred_classes, target_names=list(train_gen.class_indices.keys())))

        print("\n--- Confusion Matrix ---")
        print(confusion_matrix(y_true, y_pred_classes))

    except ImportError as e:
        print(f"TensorFlow or dependencies missing for training: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='../data/raw')
    parser.add_argument('--output', type=str, default='../models/plant_disease_model_v1.h5')
    parser.add_argument('--epochs', type=int, default=10)
    args = parser.parse_args()

    train_model(args.data_dir, args.output, args.epochs)
