# AgroScan AI — Machine Learning Model Repository

This directory contains trained weights, architecture specifications, and evaluation metrics for **AgroScan AI's** custom Computer Vision models.

## Repository Structure

```
ml/
├── data/           # Dataset storage (PlantVillage & Field Leaf Samples)
├── notebooks/      # Data exploration & training Jupyter Notebooks
├── preprocessing/  # Image decoding, color space conversion, resizing & augmentation
├── training/       # MobileNetV2 transfer learning training pipeline
├── evaluation/     # Precision, Recall, F1 score, Accuracy & Confusion Matrix evaluation
├── inference/      # Custom model inference engine wrapper
└── models/         # Trained model binaries (.h5 / .onnx / .tflite)
```

## Tracked Metrics
- **Accuracy**: Overall classification accuracy
- **Precision**: Class-wise precision
- **Recall**: Class-wise sensitivity/recall
- **F1 Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Full confusion matrix array
- **Inference Time (ms)**: Measured end-to-end model execution speed
