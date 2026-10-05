from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class PredictionCandidate(BaseModel):
    crop: str
    disease_name: str
    disease_code: str
    confidence: float
    scientific_name: Optional[str] = None
    is_healthy: bool = False
    symptoms_summary: Optional[str] = None

class ProviderDiagnosisResult(BaseModel):
    provider: str
    status: str  # "success", "error", "rate_limited", "unsupported_crop", "non_leaf_detected"
    plant: str
    scientific_name: Optional[str] = "N/A"
    disease: str
    disease_code: str
    confidence: float
    is_healthy: bool = False
    top_predictions: List[PredictionCandidate] = Field(default_factory=list)
    raw_reference: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    latency_ms: float = 0.0
    error: Optional[str] = None
    is_demo: bool = False

class ProviderHealthStatus(BaseModel):
    provider_name: str
    display_name: str
    status: str  # "AVAILABLE", "DEGRADED", "RATE_LIMITED", "NOT_CONFIGURED", "OFFLINE"
    is_configured: bool
    requires_key: bool
    latency_ms: float = 0.0
    last_success_at: Optional[datetime] = None
    failure_count: int = 0
    total_calls: int = 0
    success_rate: float = 1.0
    supported_crops: List[str] = Field(default_factory=list)
    notes: str = ""

class DiseaseDetectionProvider(ABC):
    """
    Standardized Abstract Provider Interface for Multi-API Plant Disease Detection.
    """

    def __init__(self, name: str, display_name: str):
        self.name = name
        self.display_name = display_name
        self.total_calls = 0
        self.failure_count = 0
        self.last_latency_ms = 0.0
        self.last_success_at: Optional[datetime] = None

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if provider has valid credentials and is ready for inference."""
        pass

    @abstractmethod
    async def diagnose(
        self,
        image_bytes: bytes,
        plant_name: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None,
        language: str = "en"
    ) -> ProviderDiagnosisResult:
        """
        Executes disease diagnosis on leaf image bytes and returns normalized ProviderDiagnosisResult.
        """
        pass

    def get_health_status(self) -> ProviderHealthStatus:
        rate = 1.0 if self.total_calls == 0 else max(0.0, (self.total_calls - self.failure_count) / self.total_calls)
        status_str = "AVAILABLE" if self.is_available() else "NOT_CONFIGURED"
        if self.failure_count > 3:
            status_str = "DEGRADED"

        return ProviderHealthStatus(
            provider_name=self.name,
            display_name=self.display_name,
            status=status_str,
            is_configured=self.is_available(),
            requires_key=True,
            latency_ms=round(self.last_latency_ms, 1),
            last_success_at=self.last_success_at,
            failure_count=self.failure_count,
            total_calls=self.total_calls,
            success_rate=round(rate, 2),
            supported_crops=[],
            notes=""
        )
