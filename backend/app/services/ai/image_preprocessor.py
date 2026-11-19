"""
AgroScan AI — Image Preprocessing Service
Handles safe byte-level decoding, image integrity checks, dimension validation,
color normalization, and PyTorch tensor preparation for computer vision inference.
"""

import io
import logging
from typing import Tuple, Dict, Any, Optional
from PIL import Image
import numpy as np

logger = logging.getLogger("agroscan.ai.preprocessor")

# Guard against decompression bomb Denial-of-Service attacks
Image.MAX_IMAGE_PIXELS = 25_000_000

MIN_DIMENSION = 100
MAX_DIMENSION = 4096
DEFAULT_INFERENCE_SIZE = (224, 224)

# Standard ImageNet normalization parameters used by MobileNetV2 and DINOv2
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


class ImagePreprocessingError(ValueError):
    """Raised when an uploaded file cannot be decoded or fails dimension criteria."""
    pass


class ImagePreprocessor:
    """
    Production Image Preprocessor for Local & Hybrid Vision Inference.
    Validates file headers, dimensions, and converts images into normalized
    PyTorch tensors and RGB arrays.
    """

    _tensor_transform = None

    @classmethod
    def _get_transform(cls, size: Tuple[int, int]):
        import torchvision.transforms as transforms
        return transforms.Compose([
            transforms.Resize(size, interpolation=transforms.InterpolationMode.BILINEAR),
            transforms.ToTensor(),
            transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
        ])

    @classmethod
    def decode_and_validate(cls, image_bytes: bytes) -> Tuple[Image.Image, np.ndarray, Dict[str, Any]]:
        """
        Safely decodes raw bytes into a PIL Image and RGB NumPy array with dimension bounds.
        """
        if not image_bytes or len(image_bytes) < 150:
            raise ImagePreprocessingError("Uploaded image byte stream is empty or truncated.")

        try:
            # Verify file integrity without rasterizing the whole image first
            verifier = Image.open(io.BytesIO(image_bytes))
            img_format = verifier.format or "JPEG"
            verifier.verify()
        except Exception as err:
            raise ImagePreprocessingError(f"Corrupt or invalid image stream: {err}")

        try:
            pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        except Exception as err:
            raise ImagePreprocessingError(f"Failed to rasterize RGB pixels: {err}")

        width, height = pil_image.size

        if width < MIN_DIMENSION or height < MIN_DIMENSION:
            raise ImagePreprocessingError(
                f"Image resolution {width}x{height}px is below minimum required {MIN_DIMENSION}x{MIN_DIMENSION}px."
            )

        if width > MAX_DIMENSION or height > MAX_DIMENSION:
            raise ImagePreprocessingError(
                f"Image resolution {width}x{height}px exceeds maximum allowed dimension {MAX_DIMENSION}px."
            )

        np_rgb = np.array(pil_image, dtype=np.float32)

        metadata = {
            "width": width,
            "height": height,
            "format": img_format,
            "byte_size": len(image_bytes),
            "channels": 3,
            "mean_luminance": round(float(np.mean(0.299 * np_rgb[:, :, 0] + 0.587 * np_rgb[:, :, 1] + 0.114 * np_rgb[:, :, 2])), 1)
        }

        return pil_image, np_rgb, metadata

    @classmethod
    def prepare_inference_tensor(cls, pil_image: Image.Image, target_size: Tuple[int, int] = DEFAULT_INFERENCE_SIZE) -> Any:
        """
        Converts a PIL Image into a normalized 4D PyTorch tensor: (1, C, H, W).
        """
        transform = cls._get_transform(target_size)
        tensor = transform(pil_image)

        # Add batch dimension: (1, 3, 224, 224)
        return tensor.unsqueeze(0)
