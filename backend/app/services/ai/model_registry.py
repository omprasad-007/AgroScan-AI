"""
AgroScan AI — Model Registry & Lifecycle Manager
Manages lazy loading, local weight caching, CPU/CUDA hardware selection,
and health status reporting for Hugging Face neural networks.
"""

import os
import time
import logging
from typing import Dict, Any, Optional, Tuple, List
from app.core.config import settings

logger = logging.getLogger("agroscan.ai.model_registry")

# Lazy-loaded ML imports to preserve memory in constrained cloud environments (e.g. Render 512MB RAM)
_torch = None
_AutoImageProcessor = None
_AutoModelForImageClassification = None

def _get_torch():
    global _torch
    if _torch is None:
        try:
            import torch
            _torch = torch
        except Exception as e:
            logger.info(f"PyTorch runtime not available in this environment: {e}")
            _torch = None
    return _torch

def _get_transformers():
    global _AutoImageProcessor, _AutoModelForImageClassification
    if _AutoImageProcessor is None or _AutoModelForImageClassification is None:
        try:
            from transformers import AutoImageProcessor, AutoModelForImageClassification
            _AutoImageProcessor = AutoImageProcessor
            _AutoModelForImageClassification = AutoModelForImageClassification
        except Exception as e:
            logger.info(f"Transformers runtime not available in this environment: {e}")
            _AutoImageProcessor = None
            _AutoModelForImageClassification = None
    return _AutoImageProcessor, _AutoModelForImageClassification


class ModelInitializationError(RuntimeError):
    """Raised when model weights cannot be loaded or initialized."""
    pass


class ModelMetadata:
    def __init__(self, repo_id: str, display_name: str, architecture: str, size_mb: float, classes_count: int):
        self.repo_id = repo_id
        self.display_name = display_name
        self.architecture = architecture
        self.size_mb = size_mb
        self.classes_count = classes_count
        self.is_loaded = False
        self.device = "cpu"
        self.loaded_at: Optional[float] = None
        self.total_inferences = 0
        self.total_latency_ms = 0.0
        self.last_error: Optional[str] = None


class ModelRegistry:
    """
    Central Hugging Face Model Registry for AgroScan AI.
    Features:
    - Lazy loading on first inference call.
    - Local weight caching in settings.MODEL_CACHE_DIR.
    - Zero redundant downloads.
    - CPU/CUDA hardware compatibility detection.
    - Health monitoring and memory tracking.
    """

    _MODELS_META: Dict[str, ModelMetadata] = {
        "neghani/plantvillage-mobilenetv2": ModelMetadata(
            repo_id="neghani/plantvillage-mobilenetv2",
            display_name="PlantVillage MobileNetV2",
            architecture="MobileNetV2ForImageClassification",
            size_mb=9.2,
            classes_count=38
        ),
        "rodynaemad/plant-disease-dinov2-small": ModelMetadata(
            repo_id="rodynaemad/plant-disease-dinov2-small",
            display_name="DINOv2 Small Vision Transformer",
            architecture="Dinov2ForImageClassification",
            size_mb=85.0,
            classes_count=38
        ),
        "sanjeevani-04/indian-crop-disease-mobilenetv2": ModelMetadata(
            repo_id="sanjeevani-04/indian-crop-disease-mobilenetv2",
            display_name="Indian Crop Disease MobileNetV2",
            architecture="MobileNetV2ForImageClassification",
            size_mb=9.5,
            classes_count=35
        )
    }

    _loaded_models: Dict[str, Any] = {}
    _loaded_processors: Dict[str, Any] = {}

    @classmethod
    def get_preferred_device(cls) -> Any:
        """Determines whether CUDA or CPU should be used safely."""
        torch = _get_torch()
        if torch is not None and torch.cuda.is_available():
            try:
                # Test a minimal tensor allocation on CUDA
                t = torch.zeros(1, device="cuda")
                del t
                return torch.device("cuda")
            except Exception as err:
                logger.warning(f"CUDA reported available but tensor allocation failed: {err}. Falling back to CPU.")
                return torch.device("cpu")
        return torch.device("cpu") if torch is not None else "cpu"

    @classmethod
    def load_model(cls, repo_id: str) -> Tuple[Any, Any, Any]:
        """
        Lazily loads the processor and model for repo_id.
        Reuses cached instance if already initialized.
        """
        if repo_id in cls._loaded_models:
            device = cls.get_preferred_device()
            return cls._loaded_models[repo_id], cls._loaded_processors[repo_id], device

        torch = _get_torch()
        AutoImageProcessor, AutoModelForImageClassification = _get_transformers()
        if torch is None or AutoImageProcessor is None or AutoModelForImageClassification is None:
            raise ModelInitializationError("PyTorch or Transformers runtime not available in this environment.")

        meta = cls._MODELS_META.get(repo_id)
        if not meta:
            # Allow custom compatible repo IDs
            meta = ModelMetadata(
                repo_id=repo_id,
                display_name=repo_id.split("/")[-1],
                architecture="AutoModelForImageClassification",
                size_mb=25.0,
                classes_count=38
            )
            cls._MODELS_META[repo_id] = meta

        cache_dir = settings.MODEL_CACHE_DIR
        os.makedirs(cache_dir, exist_ok=True)
        device = cls.get_preferred_device()

        # Check for verified local model weights directory (offline priority)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        if "indian" in repo_id or "sanjeevani" in repo_id:
            repo_subfolder = "indian-crop-disease-mobilenetv2"
        elif "dinov2" in repo_id:
            repo_subfolder = "plant-disease-dinov2-small"
        else:
            repo_subfolder = "plantvillage-mobilenetv2"
        local_model_candidates = [
            os.path.join(base_dir, "backend", "models", repo_subfolder),
            os.path.join(base_dir, "models", repo_subfolder),
            os.path.abspath(f"backend/models/{repo_subfolder}")
        ]
        local_model_dir = None
        for cand in local_model_candidates:
            if os.path.exists(os.path.join(cand, "model.safetensors")):
                local_model_dir = cand
                break

        if local_model_dir:
            model_target = local_model_dir
            local_files_only = True
            logger.info(f"Loading local weights for '{repo_id}' from verified directory: {local_model_dir} (offline mode)")
        else:
            model_target = repo_id
            local_files_only = False
            logger.info(f"Loading Hugging Face model '{repo_id}' on device '{device}' (cache: {cache_dir})...")

        t0 = time.time()

        try:
            processor = AutoImageProcessor.from_pretrained(
                model_target,
                cache_dir=cache_dir if not local_files_only else None,
                local_files_only=local_files_only,
                use_fast=True
            )
            model = AutoModelForImageClassification.from_pretrained(
                model_target,
                cache_dir=cache_dir if not local_files_only else None,
                local_files_only=local_files_only
            )
            model.to(device)
            model.eval()

            cls._loaded_models[repo_id] = model
            cls._loaded_processors[repo_id] = processor

            load_time = round((time.time() - t0) * 1000.0, 1)
            meta.is_loaded = True
            meta.device = str(device)
            meta.loaded_at = time.time()
            meta.last_error = None
            logger.info(f"Model '{repo_id}' successfully loaded in {load_time}ms.")

            return model, processor, device

        except Exception as err:
            meta.last_error = str(err)
            logger.error(f"Failed to initialize Hugging Face model '{repo_id}': {err}")
            raise ModelInitializationError(
                f"Could not initialize local model '{repo_id}'. "
                "Verify network connection for initial weight download or check disk space."
            )

    @classmethod
    def record_inference_metric(cls, repo_id: str, latency_ms: float):
        """Records inference metrics for observability."""
        meta = cls._MODELS_META.get(repo_id)
        if meta:
            meta.total_inferences += 1
            meta.total_latency_ms += latency_ms

    @classmethod
    def get_health_status(cls) -> List[Dict[str, Any]]:
        """Returns health and performance status of registered local models."""
        result = []
        for repo_id, meta in cls._MODELS_META.items():
            avg_latency = (
                round(meta.total_latency_ms / meta.total_inferences, 1)
                if meta.total_inferences > 0 else 0.0
            )
            status_str = "LOADED_HEALTHY" if meta.is_loaded else "READY_TO_LOAD"
            if meta.last_error:
                status_str = "INITIALIZATION_FAILED"

            result.append({
                "model_id": repo_id,
                "display_name": meta.display_name,
                "architecture": meta.architecture,
                "size_mb": meta.size_mb,
                "classes_count": meta.classes_count,
                "is_loaded": meta.is_loaded,
                "device": meta.device,
                "status": status_str,
                "total_inferences": meta.total_inferences,
                "average_latency_ms": avg_latency,
                "last_error": meta.last_error
            })
        return result

    @classmethod
    def unload_models(cls):
        """Releases model weights from memory to reclaim RAM."""
        cls._loaded_models.clear()
        cls._loaded_processors.clear()
        for meta in cls._MODELS_META.values():
            meta.is_loaded = False
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        logger.info("All local Hugging Face model instances unloaded from RAM.")
