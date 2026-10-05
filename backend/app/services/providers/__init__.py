from app.services.providers.base_provider import (
    DiseaseDetectionProvider, ProviderDiagnosisResult, PredictionCandidate, ProviderHealthStatus
)
from app.services.providers.kindwise_provider import KindwisePlantIdProvider
from app.services.providers.plantnet_provider import PlantNetProvider
from app.services.providers.plantix_provider import PlantixProvider
from app.services.providers.agrio_provider import AgrioProvider
from app.services.providers.tajiri_provider import TajiriVisionProvider
from app.services.providers.plant_health_engine_provider import PlantHealthEngineProvider
from app.services.providers.local_model_provider import AgroScanLocalModelProvider

__all__ = [
    "DiseaseDetectionProvider",
    "ProviderDiagnosisResult",
    "PredictionCandidate",
    "ProviderHealthStatus",
    "KindwisePlantIdProvider",
    "PlantNetProvider",
    "PlantixProvider",
    "AgrioProvider",
    "TajiriVisionProvider",
    "PlantHealthEngineProvider",
    "AgroScanLocalModelProvider"
]
