# AgroScan AI — Machine Learning Model Artifacts

This directory houses the trained Deep Learning weights for crop disease identification:

- `plant_disease_model_v1.h5` – MobileNetV2 Transfer Learning weights trained on PlantVillage dataset classes.
- When `DEMO_MODE=true` is enabled in backend `.env`, the application automatically operates in mock inference mode without requiring `.h5` model files.
