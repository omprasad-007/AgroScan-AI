import hashlib
import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field
from datetime import datetime, timezone

from app.core.config import settings
from app.services.disease_knowledge_base import get_disease_by_code, ALL_DISEASES
from app.services.providers.base_provider import (
    DiseaseDetectionProvider, ProviderDiagnosisResult, PredictionCandidate, ProviderHealthStatus
)
from app.services.providers.gemini_vision_provider import GeminiVisionProvider
from app.services.providers.openrouter_vision_provider import OpenRouterVisionProvider
from app.services.providers.kindwise_provider import KindwisePlantIdProvider
from app.services.providers.plantnet_provider import PlantNetProvider
from app.services.providers.plantix_provider import PlantixProvider
from app.services.providers.agrio_provider import AgrioProvider
from app.services.providers.tajiri_provider import TajiriVisionProvider
from app.services.providers.local_model_provider import AgroScanLocalModelProvider

logger = logging.getLogger("agroscan")

class ConsensusResult(BaseModel):
    scan_id: str
    image_hash: str
    plant: str
    scientific_name: str
    disease: str
    disease_code: str
    confidence: float
    consensus_score: float
    providers_called: int
    providers_agreed: int
    agreement_ratio: float
    agreement_level: str  # "HIGH", "MODERATE", "LOW_CONFLICTING"
    is_healthy: bool
    primary_provider: str
    supporting_providers: List[str]
    alternative_diagnoses: List[Dict[str, Any]]
    all_provider_results: List[Dict[str, Any]]
    uncertainty_note: Optional[str] = None
    is_demo: bool = False

# Mapping from common provider disease names to canonical AgroScan disease codes
CANONICAL_DISEASE_MAP: Dict[str, str] = {
    # Tomato
    "tomato_early_blight": "tomato_early_blight",
    "alternaria_solani": "tomato_early_blight",
    "early_blight": "tomato_early_blight",
    "tomato_late_blight": "tomato_late_blight",
    "phytophthora_infestans": "tomato_late_blight",
    "late_blight": "tomato_late_blight",
    "tomato_yellow_leaf_curl": "tomato_yellow_leaf_curl",
    "tylcv": "tomato_yellow_leaf_curl",
    "tomato_bacterial_spot": "tomato_bacterial_spot",
    "xanthomonas": "tomato_bacterial_spot",
    "tomato_septoria_leaf_spot": "tomato_septoria_leaf_spot",
    "septoria_lycopersici": "tomato_septoria_leaf_spot",
    
    # Potato
    "potato_late_blight": "potato_late_blight",
    "potato_early_blight": "potato_early_blight",

    # Mango
    "mango_anthracnose": "mango_anthracnose",
    "anthracnose": "mango_anthracnose",
    "colletotrichum_gloeosporioides": "mango_anthracnose",
    "mango_powdery_mildew": "mango_powdery_mildew",
    "oidium_mangiferae": "mango_powdery_mildew",

    # Sugarcane
    "sugarcane_red_rot": "sugarcane_red_rot",
    "colletotrichum_falcatum": "sugarcane_red_rot",
    "red_rot": "sugarcane_red_rot",
    "sugarcane_smut": "sugarcane_smut",
    "sporisorium_scitamineum": "sugarcane_smut",
    "sugarcane_rust": "sugarcane_rust",

    # Cotton
    "cotton_bacterial_blight": "cotton_bacterial_blight",
    "xanthomonas_malvacearum": "cotton_bacterial_blight",
    "blackarm": "cotton_bacterial_blight",
    "cotton_leaf_curl": "cotton_leaf_curl",
    "cotton_alternaria_leaf_spot": "cotton_alternaria_leaf_spot",

    # Rice
    "rice_blast": "rice_blast",
    "magnaporthe_oryzae": "rice_blast",
    "blast": "rice_blast",
    "rice_brown_spot": "rice_brown_spot",
    "bipolaris_oryzae": "rice_brown_spot",

    # Wheat
    "wheat_yellow_rust": "wheat_yellow_rust",
    "stripe_rust": "wheat_yellow_rust",
    "puccinia_striiformis": "wheat_yellow_rust",
    "wheat_leaf_blight": "wheat_leaf_blight",

    # Soybean
    "soybean_rust": "soybean_rust",
    "phakopsora_pachyrhizi": "soybean_rust",
    "soybean_frogeye_leaf_spot": "soybean_frogeye_leaf_spot",
    "cercospora_sojina": "soybean_frogeye_leaf_spot",

    # Chilli
    "chilli_leaf_curl": "chilli_leaf_curl",
    "chilli_anthracnose": "chilli_anthracnose",

    # Grapes
    "grape_downy_mildew": "grape_downy_mildew",
    "plasmopara_viticola": "grape_downy_mildew",
    "grape_powdery_mildew": "grape_powdery_mildew",
    "grape_black_rot": "grape_black_rot",

    # Corn
    "corn_common_rust": "corn_common_rust",
    "puccinia_sorghi": "corn_common_rust",
    "corn_northern_leaf_blight": "corn_northern_leaf_blight",

    # Onion
    "onion_purple_blotch": "onion_purple_blotch",
    "alternaria_porri": "onion_purple_blotch",

    # Pomegranate
    "pomegranate_bacterial_blight": "pomegranate_bacterial_blight",
    "telya": "pomegranate_bacterial_blight",

    # Banana
    "banana_sigatoka": "banana_sigatoka",
    "sigatoka": "banana_sigatoka",

    # Citrus
    "citrus_canker": "citrus_canker",
    "citrus_greening": "citrus_greening",

    # Healthy
    "healthy_leaf": "healthy_leaf",
    "healthy": "healthy_leaf",
    "no_disease": "healthy_leaf"
}

class MultiProviderConsensusEngine:
    """
    Multi-API Evidence Fusion, Intelligent Routing, and Disease Normalization Engine.
    """

    def __init__(self):
        # Register all available provider instances
        self.providers: Dict[str, DiseaseDetectionProvider] = {
            "gemini_vision": GeminiVisionProvider(),
            "openrouter_vision": OpenRouterVisionProvider(),
            "kindwise": KindwisePlantIdProvider(),
            "plantnet": PlantNetProvider(),
            "plantix": PlantixProvider(),
            "agrio": AgrioProvider(),
            "tajiri": TajiriVisionProvider(),
            "agroscan_local": AgroScanLocalModelProvider()
        }
        # In-memory deterministic cache: hash -> (timestamp, ConsensusResult)
        self._cache: Dict[str, Tuple[datetime, ConsensusResult]] = {}

    @staticmethod
    def calculate_image_hash(image_bytes: bytes) -> str:
        """Calculates SHA-256 hash of image bytes for session isolation and duplicate detection."""
        return hashlib.sha256(image_bytes).hexdigest()

    @staticmethod
    def normalize_disease_code(raw_name: str, raw_code: str) -> str:
        """Maps diverse provider disease labels into canonical AgroScan codes."""
        clean_code = raw_code.lower().replace("-", "_").replace(" ", "_")
        clean_name = raw_name.lower().replace("-", "_").replace(" ", "_")

        if clean_code in CANONICAL_DISEASE_MAP:
            return CANONICAL_DISEASE_MAP[clean_code]
        if clean_name in CANONICAL_DISEASE_MAP:
            return CANONICAL_DISEASE_MAP[clean_name]

        # Substring fuzzy match
        for key, canonical in CANONICAL_DISEASE_MAP.items():
            if key in clean_code or key in clean_name:
                return canonical

        return clean_code if clean_code else "healthy_leaf"

    def select_active_providers(self, target_crop: Optional[str] = None) -> List[DiseaseDetectionProvider]:
        """
        Selects active, healthy disease detection providers with valid credentials.
        """
        active = []
        # Priority 1: Configured External Cloud & Vision AI Providers (Gemini Vision first!)
        for p_name in ["gemini_vision", "openrouter_vision", "kindwise", "plantnet", "plantix", "agrio", "tajiri"]:
            p = self.providers.get(p_name)
            if p and p.is_available():
                active.append(p)

        # Priority 2: AgroScan Local Vision Engine (always available as reliable fallback)
        local_p = self.providers.get("agroscan_local")
        if local_p and local_p.is_available():
            active.append(local_p)

        return active

    async def diagnose_with_consensus(
        self,
        image_bytes: bytes,
        scan_id: str,
        target_crop: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None,
        language: str = "en"
    ) -> ConsensusResult:
        """
        Executes parallel multi-provider routing, normalizes responses, and calculates cross-provider consensus.
        """
        img_hash = self.calculate_image_hash(image_bytes)

        # Select candidate providers
        active_providers = self.select_active_providers(target_crop)
        if not active_providers:
            # Fall back directly to local provider
            active_providers = [self.providers["agroscan_local"]]

        # Cache key binds image hash, target crop, and active provider set
        prov_sig = ",".join(sorted(p.name for p in active_providers))
        cache_key = f"{img_hash}:{target_crop or 'auto'}:{prov_sig}"
        if cache_key in self._cache:
            ts, cached_result = self._cache[cache_key]
            if (datetime.now(timezone.utc) - ts).total_seconds() < 3600:
                cached_copy = cached_result.model_copy()
                cached_copy.scan_id = scan_id
                return cached_copy

        # Execute Provider Calls in Parallel with 8.0s timeout
        async def _call_with_timeout(p: DiseaseDetectionProvider) -> ProviderDiagnosisResult:
            try:
                return await asyncio.wait_for(
                    p.diagnose(image_bytes=image_bytes, plant_name=target_crop, location=location, language=language),
                    timeout=8.0
                )
            except asyncio.TimeoutError:
                logger.warning(f"Provider '{p.name}' timed out after 8.0s")
                return ProviderDiagnosisResult(
                    provider=p.name,
                    status="timeout",
                    plant="Unknown",
                    disease="Unknown",
                    disease_code="provider_timeout",
                    confidence=0.0,
                    error="Provider response timed out."
                )

        tasks = [_call_with_timeout(p) for p in active_providers]
        raw_results = await asyncio.gather(*tasks, return_exceptions=True)
        results: List[ProviderDiagnosisResult] = []
        for i, r in enumerate(raw_results):
            if isinstance(r, Exception):
                p_name = active_providers[i].name
                logger.warning(f"Provider '{p_name}' failed during diagnosis: {r}")
                results.append(ProviderDiagnosisResult(
                    provider=p_name,
                    status="error",
                    plant="Unknown",
                    disease="Unknown",
                    disease_code="provider_error",
                    confidence=0.0,
                    error=str(r)
                ))
            elif isinstance(r, ProviderDiagnosisResult):
                results.append(r)

        # Filter successful results
        valid_results = [r for r in results if r.status == "success"]

        if not valid_results:
            # Check if any provider explicitly flagged non-leaf
            non_leaf = next((r for r in results if r.status == "non_leaf_detected"), None)
            if non_leaf:
                raise ValueError(non_leaf.error or "No plant leaf detected by diagnosis providers.")

            # Automatic fallback to local botanical classifier
            local_p = self.providers["agroscan_local"]
            fallback_res = await local_p.diagnose(image_bytes=image_bytes, plant_name=target_crop, location=location, language=language)
            valid_results = [fallback_res]
            results.append(fallback_res)

        # Perform Multi-API Evidence Fusion
        consensus = self._fuse_evidence(valid_results, scan_id, img_hash)
        
        # Save to deterministic cache only for successful non-conflicting predictions
        if consensus.agreement_level != "LOW_CONFLICTING" and consensus.confidence >= 0.50:
            self._cache[cache_key] = (datetime.now(timezone.utc), consensus)

        return consensus

    def _fuse_evidence(
        self,
        results: List[ProviderDiagnosisResult],
        scan_id: str,
        img_hash: str
    ) -> ConsensusResult:
        """
        Combines predictions across independent providers using weighted consensus fusion.
        Accurately preserves the identified plant species and scientific name.
        """
        disease_votes: Dict[str, Dict[str, Any]] = {}
        plant_votes: Dict[str, float] = {}
        plant_sci_names: Dict[str, str] = {}

        for res in results:
            canon_code = self.normalize_disease_code(res.disease, res.disease_code)
            
            # Vision AI providers carry higher weight than generic baseline
            weight = 1.5 if res.provider in ["gemini_vision", "openrouter_vision"] else 1.0
            weighted_conf = res.confidence * weight

            if canon_code not in disease_votes:
                disease_votes[canon_code] = {
                    "disease_name": res.disease,
                    "scientific_name": res.scientific_name,
                    "is_healthy": res.is_healthy,
                    "total_weight": 0.0,
                    "conf_sum": 0.0,
                    "providers": [],
                    "raw_confs": [],
                    "plant": res.plant
                }

            disease_votes[canon_code]["total_weight"] += weight
            disease_votes[canon_code]["conf_sum"] += weighted_conf
            disease_votes[canon_code]["providers"].append(res.provider)
            disease_votes[canon_code]["raw_confs"].append(res.confidence)

            # Track plant crop votes
            c_name = res.plant.title() if res.plant and res.plant != "Unknown" else "General Crop"
            plant_votes[c_name] = plant_votes.get(c_name, 0.0) + weight
            if res.scientific_name and res.scientific_name != "N/A":
                plant_sci_names[c_name] = res.scientific_name

        # Determine consensus winner
        sorted_diseases = sorted(
            disease_votes.items(),
            key=lambda x: (x[1]["total_weight"], x[1]["conf_sum"]),
            reverse=True
        )

        top_code, top_info = sorted_diseases[0]
        consensus_plant = top_info["plant"] if top_info.get("plant") and top_info["plant"] != "Unknown" else max(plant_votes.items(), key=lambda x: x[1])[0]

        agreeing_providers = top_info["providers"]
        providers_agreed = len(agreeing_providers)
        providers_called = len(results)
        agreement_ratio = round(providers_agreed / providers_called, 2)

        # Composite Confidence calculation
        avg_raw_conf = sum(top_info["raw_confs"]) / len(top_info["raw_confs"])
        agreement_boost = 0.04 if providers_agreed > 1 else 0.0
        final_confidence = min(0.98, max(0.50, round(avg_raw_conf + agreement_boost, 3)))
        consensus_score = round(final_confidence * agreement_ratio, 3)

        # Agreement level
        if agreement_ratio >= 0.75 or providers_agreed >= 2:
            agreement_level = "HIGH"
            uncertainty_note = None
        elif agreement_ratio >= 0.50:
            agreement_level = "MODERATE"
            uncertainty_note = "Moderate agreement between diagnostic models. Follow preventive scouting."
        else:
            agreement_level = "LOW_CONFLICTING"
            uncertainty_note = "The available diagnostic models produced conflicting results. Please capture another clear leaf image."

        # Compile Top-N Alternative Possibilities
        alternatives = []
        for code, info in sorted_diseases[1:4]:
            alt_avg_conf = sum(info["raw_confs"]) / len(info["raw_confs"])
            alternatives.append({
                "disease": info["disease_name"],
                "disease_code": code,
                "confidence": round(alt_avg_conf, 3),
                "providers_supporting": info["providers"]
            })

        # Enrich scientific name from Knowledge Base if not set
        kb_data = get_disease_by_code(top_code)
        sci_name = top_info.get("scientific_name") or plant_sci_names.get(consensus_plant)
        if (not sci_name or sci_name == "N/A") and kb_data.get("scientific_name"):
            sci_name = kb_data["scientific_name"]

        return ConsensusResult(
            scan_id=scan_id,
            image_hash=img_hash,
            plant=consensus_plant,
            scientific_name=sci_name or "N/A",
            disease=top_info["disease_name"],
            disease_code=top_code,
            confidence=final_confidence,
            consensus_score=consensus_score,
            providers_called=providers_called,
            providers_agreed=providers_agreed,
            agreement_ratio=agreement_ratio,
            agreement_level=agreement_level,
            is_healthy=top_info["is_healthy"],
            primary_provider=agreeing_providers[0] if agreeing_providers else results[0].provider,
            supporting_providers=agreeing_providers,
            alternative_diagnoses=alternatives,
            all_provider_results=[r.model_dump() for r in results],
            uncertainty_note=uncertainty_note,
            is_demo=False
        )

    def get_all_provider_health(self) -> List[ProviderHealthStatus]:
        """Returns health monitoring status for all configured disease providers."""
        return [p.get_health_status() for p in self.providers.values()]

# Global Singleton Instance
consensus_engine = MultiProviderConsensusEngine()
