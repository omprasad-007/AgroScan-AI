# AgroScan AI — Model Download & Manifest Report
**Model:** `neghani/plantvillage-mobilenetv2` | **Revision:** `v1.1` | **Status:** DOWNLOADED & VERIFIED

---

## 1. Executive Summary

This report documents the download, verification, SHA-256 checksumming, and manifest generation for the **Hugging Face PlantVillage MobileNetV2** image classification model inside AgroScan AI.

- **Source Repository:** [https://huggingface.co/neghani/plantvillage-mobilenetv2](https://huggingface.co/neghani/plantvillage-mobilenetv2)
- **Selected Tag:** `v1.1`
- **Immutable Commit SHA:** `77e6d262dca53b818f7ad1d67088700754515639`
- **Annotated Tag Target SHA:** `8bacd1d165f1cb5d0608e280e3caeb0da4e49424`
- **Local Target Directory:** `backend/models/plantvillage-mobilenetv2`
- **Manifest Location:** `backend/models/model_manifest.json`
- **Weights Format:** Safetensors (`model.safetensors`, 9,264,680 bytes / ~9.26 MB)
- **License:** Apache 2.0
- **Total Files Downloaded:** 33 files (including weights, configuration, reports, and real-world evaluation splits)

---

## 2. Version Selection & Commit Pinning

To prevent silent upstream regressions and guarantee deterministic, reproducible deployments, the model was pinned to its immutable Git commit SHA rather than tracking the moving `main` branch.

1. **Tag Inspection:** Inspected the Git refs of `neghani/plantvillage-mobilenetv2` via Hugging Face Hub API.
2. **Revision Selection:** The tagged release `v1.1` was identified as the author's recommended stable release.
3. **Commit Resolution:** Tag `v1.1` was resolved to commit SHA `77e6d262dca53b818f7ad1d67088700754515639`.
4. **Offline Capability:** All weights, tokenizer/processor configs, and metadata were saved locally. The application runs 100% offline with `local_files_only=True`.

---

## 3. Download Execution Details

The model repository was downloaded using Python's `huggingface_hub.snapshot_download`:

```python
from huggingface_hub import snapshot_download

snapshot_download(
    repo_id="neghani/plantvillage-mobilenetv2",
    revision="77e6d262dca53b818f7ad1d67088700754515639",
    local_dir="backend/models/plantvillage-mobilenetv2",
    local_dir_use_symlinks=False
)
```

---

## 4. Complete Downloaded File Inventory & Checksums

All 33 files downloaded were verified for integrity. Below are the key system and configuration files with their byte sizes and SHA-256 hashes:

| File Name | Size (Bytes) | SHA-256 Checksum | Purpose |
|---|---|---|---|
| `model.safetensors` | 9,264,680 | `4903b6e3647ffedb5182c6e2f87200c56c4472d1bdbbcd8ce6a84650f14df084` | Primary MobileNetV2 neural network weights |
| `config.json` | 3,923 | `21c97f48e3cf7ae9a9418659d58a8a4f6d4d126fc213df6a117b11d95be51717` | Architecture definition & 38 `id2label` mapping |
| `preprocessor_config.json` | 396 | `39fcf958a74e50337c7c3ec12fb8aa40d34197607a01fa2eb086fb46960cfd21` | MobileNetV2ImageProcessor settings (224x224, mean/std) |
| `calibration.json` | 212 | `3f5ef5b8dd5ce18a22d7ba5ea9f6c0e256b82531d05aaefea6bb5cb560c5a085` | Temperature scaling parameter ($T = 0.8845188$) |
| `threshold.json` | 6,368 | `0015ce2a51f893d98eb82208a0d94812a6cb3da321a57c5bf33eb63683f1246d` | Optimal decision threshold ($\theta = 0.50$) |
| `eval_results.json` | 557 | `99ffc2f57ef51a7be477cfd0fe89c2cefb21ee7b1988898144026da6ddae2089` | Accuracy, loss, and top-3 benchmark numbers |
| `README.md` | 5,595 | `2eb46356bc0d805e3ec403f5cefe432d0c2794025d48dd907ce71bb575d1656c` | Model documentation & dataset specifications |
| `reports/classification_report.txt` | 3,866 | `667995e92e2fb54a435e8a9e2c36af12c83e092fa98cb3b78f9b001ec8ec7bcf` | Per-class precision, recall, and F1 scores |
| `reports/confusion_matrix.png` | 336,161 | `75f59c612fb2a579349ebbddd41a4a695d387e126ccf378d60c5e9c6a7d95ffa` | Visual confusion matrix on test evaluation |
| `reports/metrics.json` | 21,817 | `bd618d9a9b7330581bbac7f6f5ce65ea45ab1d427cc5b31cccbdb97e84c481e9` | Detailed per-class precision/recall metrics |
| `reports/threshold_sweep.csv` | 752 | `cf53115f189e8f8b0d0b7edd1d0b8216fc92bc2279ecc9083b335fffc0c62451` | Threshold sweep data (0.30 to 0.95) |

---

## 5. Model Manifest Structure

The model manifest was generated automatically at [backend/models/model_manifest.json](file:///d:/Projects/AgroScan%20AI/backend/models/model_manifest.json). A summarized excerpt:

```json
{
  "repository_id": "neghani/plantvillage-mobilenetv2",
  "selected_revision": "v1.1",
  "immutable_commit_sha": "77e6d262dca53b818f7ad1d67088700754515639",
  "annotated_tag_target_sha": "8bacd1d165f1cb5d0608e280e3caeb0da4e49424",
  "model_architecture": "MobileNetV2ForImageClassification",
  "base_model": "google/mobilenet_v2_1.0_224",
  "task": "image-classification",
  "license": "Apache-2.0",
  "download_date": "2026-11-19T07:53:46.232108+00:00",
  "model_directory": "backend/models/plantvillage-mobilenetv2",
  "label_count": 38,
  "calibration": {
    "temperature": 0.8845188130635788,
    "source_file": "calibration.json"
  },
  "decision_threshold": {
    "threshold": 0.5,
    "best_available": 0.95,
    "source_file": "threshold.json"
  }
}
```

---

## 6. Git Version Control Protection

To prevent inadvertent check-in of large binary weights into Git, [.gitignore](file:///d:/Projects/AgroScan%20AI/.gitignore) was updated with the following rules:

```gitignore
# Machine Learning Model Weights
backend/models/**/*.safetensors
backend/models/**/*.bin
backend/models/**/*.pt
backend/models/**/*.pth
backend/models/**/*.onnx
backend/models/**/*.h5

# Preserve manifest and documentation
!backend/models/model_manifest.json
!backend/models/**/config.json
!backend/models/**/preprocessor_config.json
!backend/models/**/calibration.json
!backend/models/**/threshold.json
!backend/models/**/eval_results.json
```

---

## 7. Verification Checklist

- [x] Hugging Face snapshot downloaded without errors
- [x] Revision pinned to immutable SHA `77e6d262dca53b818f7ad1d67088700754515639`
- [x] Weights file `model.safetensors` verified (9,264,680 bytes)
- [x] Exactly 38 classification labels confirmed in `config.json`
- [x] Preprocessor configuration confirmed for 224x224 input
- [x] Temperature calibration file `calibration.json` confirmed ($T = 0.8845$)
- [x] Decision threshold file `threshold.json` confirmed ($\theta = 0.50$)
- [x] SHA-256 checksums calculated and verified for all 33 files
- [x] Machine-readable `backend/models/model_manifest.json` generated
- [x] Local model loads successfully in PyTorch CPU inference mode without internet connection
