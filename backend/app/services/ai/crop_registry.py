"""
AgroScan AI — Modular Crop Identification & Support Registry
Maintains comprehensive agronomic taxonomy, explicit support statuses,
model capabilities, and limitations across agricultural plant species.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field


class CropSupportStatus(str, Enum):
    SUPPORTED = "SUPPORTED"                      # Local model weights + verified disease classes exist
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"  # External API or morphological detection, limited local classes
    UNSUPPORTED = "UNSUPPORTED"                  # Recognized botanical species, but no calibrated disease model
    UNKNOWN_CROP = "UNKNOWN_CROP"                # Unrecognized or indeterminate plant species


class CropProfile(BaseModel):
    id: str
    common_name: str
    scientific_name: str
    family: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)
    support_status: CropSupportStatus
    supported_model_ids: List[str] = Field(default_factory=list)
    supported_diseases: List[str] = Field(default_factory=list)
    supported_providers: List[str] = Field(default_factory=list)
    limitations: Optional[str] = None
    knowledge_base_ref: Optional[str] = None


class CropRegistry:
    """
    Centralized Crop Registry for AgroScan AI.
    Provides honest verification of crop coverage, alias resolution,
    and prevents forcing unsupported crops into unrelated model classes.
    """

    # Registered crops database
    _CROPS: Dict[str, CropProfile] = {
        # --- 1. FULLY SUPPORTED CROPS (PlantVillage 38-class Local Models + External APIs) ---
        "tomato": CropProfile(
            id="tomato",
            common_name="Tomato",
            scientific_name="Solanum lycopersicum",
            family="Solanaceae",
            aliases=["tamatar", "lycopersicon", "love apple"],
            support_status=CropSupportStatus.SUPPORTED,
            supported_model_ids=["neghani/plantvillage-mobilenetv2", "rodynaemad/plant-disease-dinov2-small"],
            supported_diseases=[
                "tomato_early_blight", "tomato_late_blight", "tomato_yellow_leaf_curl",
                "tomato_bacterial_spot", "tomato_septoria_leaf_spot", "tomato_leaf_mold",
                "tomato_spider_mites", "tomato_target_spot", "tomato_mosaic_virus", "healthy_leaf"
            ],
            supported_providers=["kindwise", "gemini_vision", "openrouter_vision", "agroscan_local"],
            limitations="Local models calibrated primarily on PlantVillage leaf background conditions.",
            knowledge_base_ref="tomato"
        ),
        "potato": CropProfile(
            id="potato",
            common_name="Potato",
            scientific_name="Solanum tuberosum",
            family="Solanaceae",
            aliases=["batata", "aloo", "alu"],
            support_status=CropSupportStatus.SUPPORTED,
            supported_model_ids=["neghani/plantvillage-mobilenetv2", "rodynaemad/plant-disease-dinov2-small"],
            supported_diseases=["potato_early_blight", "potato_late_blight", "healthy_leaf"],
            supported_providers=["kindwise", "gemini_vision", "openrouter_vision", "agroscan_local"],
            limitations="Tuber rot conditions require root-zone evaluation beyond leaf images.",
            knowledge_base_ref="potato"
        ),
        "apple": CropProfile(
            id="apple",
            common_name="Apple",
            scientific_name="Malus domestica",
            family="Rosaceae",
            aliases=["seb", "pomme"],
            support_status=CropSupportStatus.SUPPORTED,
            supported_model_ids=["neghani/plantvillage-mobilenetv2", "rodynaemad/plant-disease-dinov2-small"],
            supported_diseases=["apple_scab", "apple_black_rot", "cedar_apple_rust", "healthy_leaf"],
            supported_providers=["kindwise", "gemini_vision", "openrouter_vision", "agroscan_local"],
            limitations="Leaf symptoms may overlap with mineral micronutrient chlorosis.",
            knowledge_base_ref="apple"
        ),
        "corn": CropProfile(
            id="corn",
            common_name="Corn (Maize)",
            scientific_name="Zea mays",
            family="Poaceae",
            aliases=["maize", "makka", "makkai", "makai", "sweet corn"],
            support_status=CropSupportStatus.SUPPORTED,
            supported_model_ids=["neghani/plantvillage-mobilenetv2", "rodynaemad/plant-disease-dinov2-small"],
            supported_diseases=["corn_cercospora_leaf_spot", "corn_common_rust", "corn_northern_leaf_blight", "healthy_leaf"],
            supported_providers=["kindwise", "gemini_vision", "openrouter_vision", "agroscan_local"],
            limitations="Severe moisture stress can produce necrosis resembling northern leaf blight.",
            knowledge_base_ref="maize"
        ),
        "grapes": CropProfile(
            id="grapes",
            common_name="Grapes",
            scientific_name="Vitis vinifera",
            family="Vitaceae",
            aliases=["grape", "draksh", "angoor", "angur"],
            support_status=CropSupportStatus.SUPPORTED,
            supported_model_ids=["neghani/plantvillage-mobilenetv2", "rodynaemad/plant-disease-dinov2-small"],
            supported_diseases=["grape_black_rot", "grape_esca_black_measles", "grape_leaf_blight", "healthy_leaf"],
            supported_providers=["kindwise", "gemini_vision", "openrouter_vision", "agroscan_local"],
            limitations="Grapevine downy mildew requires undersurface leaf sporulation inspection.",
            knowledge_base_ref="grapes"
        ),
        "soybean": CropProfile(
            id="soybean",
            common_name="Soybean",
            scientific_name="Glycine max",
            family="Fabaceae",
            aliases=["soya", "soy", "soyabean"],
            support_status=CropSupportStatus.SUPPORTED,
            supported_model_ids=["neghani/plantvillage-mobilenetv2", "rodynaemad/plant-disease-dinov2-small"],
            supported_diseases=["soybean_healthy", "soybean_rust", "healthy_leaf"],
            supported_providers=["kindwise", "gemini_vision", "openrouter_vision", "agroscan_local"],
            limitations="Local models primarily classify healthy vs general foliage conditions.",
            knowledge_base_ref="soybean"
        ),
        "pepper": CropProfile(
            id="pepper",
            common_name="Bell Pepper / Chilli",
            scientific_name="Capsicum annuum",
            family="Solanaceae",
            aliases=["chilli", "mirchi", "capsicum", "chili", "shimla mirch"],
            support_status=CropSupportStatus.SUPPORTED,
            supported_model_ids=["neghani/plantvillage-mobilenetv2", "rodynaemad/plant-disease-dinov2-small"],
            supported_diseases=["pepper_bacterial_spot", "healthy_leaf", "chilli_anthracnose", "chilli_leaf_curl"],
            supported_providers=["kindwise", "gemini_vision", "openrouter_vision", "agroscan_local"],
            limitations="Thrip curl symptoms closely mimic viral leaf curl complex.",
            knowledge_base_ref="chilli"
        ),

        # --- 2. PARTIALLY SUPPORTED INDIAN CASH & FIELD CROPS ---
        # (Supported via External Vision APIs + Microclimate Weather Models + Agronomic Knowledge)
        "mango": CropProfile(
            id="mango",
            common_name="Mango",
            scientific_name="Mangifera indica",
            family="Anacardiaceae",
            aliases=["aam", "amba", "manga"],
            support_status=CropSupportStatus.PARTIALLY_SUPPORTED,
            supported_model_ids=[],
            supported_diseases=["mango_anthracnose", "mango_powdery_mildew", "mango_dieback", "healthy_leaf"],
            supported_providers=["gemini_vision", "kindwise", "openrouter_vision"],
            limitations="Diagnosed via external multimodal vision and microclimate engine; local PlantVillage model does not contain mango classes.",
            knowledge_base_ref="mango"
        ),
        "sugarcane": CropProfile(
            id="sugarcane",
            common_name="Sugarcane",
            scientific_name="Saccharum officinarum",
            family="Poaceae",
            aliases=["ganna", "us", "serum"],
            support_status=CropSupportStatus.PARTIALLY_SUPPORTED,
            supported_model_ids=[],
            supported_diseases=["sugarcane_red_rot", "sugarcane_smut", "sugarcane_rust", "healthy_leaf"],
            supported_providers=["gemini_vision", "kindwise", "openrouter_vision"],
            limitations="Internal stalk red rot requires splitting the cane for conclusive agronomic confirmation.",
            knowledge_base_ref="sugarcane"
        ),
        "cotton": CropProfile(
            id="cotton",
            common_name="Cotton",
            scientific_name="Gossypium hirsutum",
            family="Malvaceae",
            aliases=["kapas", "kappas", "rui"],
            support_status=CropSupportStatus.PARTIALLY_SUPPORTED,
            supported_model_ids=[],
            supported_diseases=["cotton_bacterial_blight", "cotton_leaf_curl", "cotton_alternaria_leaf_spot", "healthy_leaf"],
            supported_providers=["gemini_vision", "kindwise", "openrouter_vision"],
            limitations="Requires multimodal external vision adapter; local PlantVillage model lacks cotton classes.",
            knowledge_base_ref="cotton"
        ),
        "rice": CropProfile(
            id="rice",
            common_name="Rice (Paddy)",
            scientific_name="Oryza sativa",
            family="Poaceae",
            aliases=["paddy", "dhan", "bhat", "tandul", "chawal"],
            support_status=CropSupportStatus.PARTIALLY_SUPPORTED,
            supported_model_ids=[],
            supported_diseases=["rice_blast", "rice_brown_spot", "rice_bacterial_blight", "healthy_leaf"],
            supported_providers=["gemini_vision", "kindwise", "openrouter_vision"],
            limitations="Leaf blast spindle lesions evaluated via multimodal vision; local 38-class weights lack rice.",
            knowledge_base_ref="rice"
        ),
        "wheat": CropProfile(
            id="wheat",
            common_name="Wheat",
            scientific_name="Triticum aestivum",
            family="Poaceae",
            aliases=["gehun", "gahu"],
            support_status=CropSupportStatus.PARTIALLY_SUPPORTED,
            supported_model_ids=[],
            supported_diseases=["wheat_yellow_rust", "wheat_brown_rust", "wheat_leaf_blight", "healthy_leaf"],
            supported_providers=["gemini_vision", "kindwise", "openrouter_vision"],
            limitations="Rust pustule differentiation benefits from high-magnification macro photography.",
            knowledge_base_ref="wheat"
        ),
        "onion": CropProfile(
            id="onion",
            common_name="Onion",
            scientific_name="Allium cepa",
            family="Amaryllidaceae",
            aliases=["pyaz", "kanda"],
            support_status=CropSupportStatus.PARTIALLY_SUPPORTED,
            supported_model_ids=[],
            supported_diseases=["onion_purple_blotch", "onion_downy_mildew", "healthy_leaf"],
            supported_providers=["gemini_vision", "kindwise", "openrouter_vision"],
            limitations="Bulb rot cannot be diagnosed from leaf blades alone.",
            knowledge_base_ref="onion"
        ),
        "pomegranate": CropProfile(
            id="pomegranate",
            common_name="Pomegranate",
            scientific_name="Punica granatum",
            family="Lythraceae",
            aliases=["anar", "dalimb"],
            support_status=CropSupportStatus.PARTIALLY_SUPPORTED,
            supported_model_ids=[],
            supported_diseases=["pomegranate_bacterial_blight", "pomegranate_anthracnose", "healthy_leaf"],
            supported_providers=["gemini_vision", "kindwise", "openrouter_vision"],
            limitations="Bacterial blight (Telya) requires node and fruit inspection.",
            knowledge_base_ref="pomegranate"
        ),
        "banana": CropProfile(
            id="banana",
            common_name="Banana",
            scientific_name="Musa acuminata",
            family="Musaceae",
            aliases=["kela", "kele"],
            support_status=CropSupportStatus.PARTIALLY_SUPPORTED,
            supported_model_ids=[],
            supported_diseases=["banana_sigatoka", "banana_panama_wilt", "healthy_leaf"],
            supported_providers=["gemini_vision", "kindwise", "openrouter_vision"],
            limitations="Panama wilt is a vascular disease originating in the corm.",
            knowledge_base_ref="banana"
        ),

        # --- 3. RECOGNIZED BOTANICAL SPECIES WITHOUT CALIBRATED PATHOLOGY (UNSUPPORTED) ---
        "coffee": CropProfile(
            id="coffee",
            common_name="Coffee",
            scientific_name="Coffea arabica",
            family="Rubiaceae",
            aliases=["kafi"],
            support_status=CropSupportStatus.UNSUPPORTED,
            supported_model_ids=[],
            supported_diseases=[],
            supported_providers=[],
            limitations="Coffee leaf rust requires dedicated tropical plantation model weights not yet bundled.",
            knowledge_base_ref=None
        ),
        "tea": CropProfile(
            id="tea",
            common_name="Tea",
            scientific_name="Camellia sinensis",
            family="Theaceae",
            aliases=["chai"],
            support_status=CropSupportStatus.UNSUPPORTED,
            supported_model_ids=[],
            supported_diseases=[],
            supported_providers=[],
            limitations="Blister blight and red rust on tea require regional plantation extension review.",
            knowledge_base_ref=None
        ),
        "rubber": CropProfile(
            id="rubber",
            common_name="Rubber",
            scientific_name="Hevea brasiliensis",
            family="Euphorbiaceae",
            aliases=["para rubber"],
            support_status=CropSupportStatus.UNSUPPORTED,
            supported_model_ids=[],
            supported_diseases=[],
            supported_providers=[],
            limitations="Rubber leaf fall requires specialized regional diagnostic validation.",
            knowledge_base_ref=None
        ),
        "cardamom": CropProfile(
            id="cardamom",
            common_name="Cardamom",
            scientific_name="Elettaria cardamomum",
            family="Zingiberaceae",
            aliases=["elaichi", "velchi"],
            support_status=CropSupportStatus.UNSUPPORTED,
            supported_model_ids=[],
            supported_diseases=[],
            supported_providers=[],
            limitations="Katte disease and capsule rot require whole-clump agro-ecological inspection.",
            knowledge_base_ref=None
        ),
    }

    @classmethod
    def normalize_crop_name(cls, input_str: Optional[str]) -> str:
        """Cleans and standardizes raw crop query string."""
        if not input_str:
            return ""
        clean = input_str.strip().lower()
        # Strip common prefixes or formatting
        clean = clean.replace("🌿", "").replace("crop:", "").replace("target:", "").strip()
        for token in ["(any plant species)", "(paddy)", "(maize)", "/ pepper", "field plant"]:
            clean = clean.replace(token, "").strip()
        return clean

    @classmethod
    def get_crop(cls, name_or_alias: Optional[str]) -> Optional[CropProfile]:
        """Resolves crop profile by identifier, exact common name, scientific name, or alias."""
        clean = cls.normalize_crop_name(name_or_alias)
        if not clean or clean in ["auto", "auto-detect", "unknown", "all", "general", "other"]:
            return None

        # 1. Direct ID match
        if clean in cls._CROPS:
            return cls._CROPS[clean]

        # 2. Match common names or aliases
        for profile in cls._CROPS.values():
            if clean == profile.common_name.lower():
                return profile
            if clean == profile.scientific_name.lower():
                return profile
            if any(clean == alias.lower() for alias in profile.aliases):
                return profile

        # 3. Substring matching
        for profile in cls._CROPS.values():
            if clean in profile.common_name.lower() or profile.id in clean:
                return profile

        return None

    @classmethod
    def check_support(cls, name_or_alias: Optional[str]) -> Tuple[CropSupportStatus, Optional[CropProfile]]:
        """
        Determines the explicit crop support status.
        Never defaults an unknown crop to 'SUPPORTED'.
        """
        profile = cls.get_crop(name_or_alias)
        if profile is None:
            clean = cls.normalize_crop_name(name_or_alias)
            if not clean or clean in ["auto", "auto-detect", "all"]:
                # Auto-detect mode delegates to image-driven identification
                return CropSupportStatus.SUPPORTED, None
            return CropSupportStatus.UNKNOWN_CROP, None

        return profile.support_status, profile

    @classmethod
    def is_model_supported_for_crop(cls, crop_id: str, model_id: str) -> bool:
        """Verifies if a specific local model is officially capable of classifying the given crop."""
        profile = cls._CROPS.get(crop_id)
        if not profile:
            return False
        return model_id in profile.supported_model_ids

    @classmethod
    def list_supported_crops(cls) -> List[CropProfile]:
        """Returns all crops with full local ML support."""
        return [c for c in cls._CROPS.values() if c.support_status == CropSupportStatus.SUPPORTED]

    @classmethod
    def list_all_crops(cls) -> List[CropProfile]:
        """Returns all registered crop profiles."""
        return list(cls._CROPS.values())
