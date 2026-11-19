"""
AgroScan AI — Agricultural Crop Registry & Model Coverage Service
Maintains explicit support statuses for agricultural crops across local models and cloud providers.
Guarantees that unsupported crops are never forcibly coerced into unrelated model classifications.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class CropSupportStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    PARTIALLY_SUPPORTED = "PARTIALLY_SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    UNKNOWN = "UNKNOWN"


class CropRegistryEntry(BaseModel):
    crop_id: str
    crop_name: str
    scientific_name: str
    status: CropSupportStatus
    supported_model_labels: List[str] = Field(default_factory=list)
    supported_diseases: List[str] = Field(default_factory=list)
    provider_support: List[str] = Field(default_factory=list)
    known_limitations: str


# Comprehensive Crop Registry for AgroScan AI
CROP_REGISTRY: Dict[str, CropRegistryEntry] = {
    # -------------------------------------------------------------
    # 14 Crops Supported Directly by Local MobileNetV2 (PlantVillage v1.1)
    # -------------------------------------------------------------
    "apple": CropRegistryEntry(
        crop_id="apple",
        crop_name="Apple",
        scientific_name="Malus domestica",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=[
            "Apple___Apple_scab",
            "Apple___Black_rot",
            "Apple___Cedar_apple_rust",
            "Apple___healthy"
        ],
        supported_diseases=["Apple Scab", "Black Rot", "Cedar Apple Rust", "Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Trained predominantly on single leaves on uniform backgrounds. Severe canopy occlusion may reduce confidence."
    ),
    "blueberry": CropRegistryEntry(
        crop_id="blueberry",
        crop_name="Blueberry",
        scientific_name="Vaccinium corymbosum",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=["Blueberry___healthy"],
        supported_diseases=["Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Local MobileNetV2 contains only the healthy class for blueberry; diseases require cloud vision consensus."
    ),
    "cherry": CropRegistryEntry(
        crop_id="cherry",
        crop_name="Cherry",
        scientific_name="Prunus avium",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=[
            "Cherry_(including_sour)___Powdery_mildew",
            "Cherry_(including_sour)___healthy"
        ],
        supported_diseases=["Powdery Mildew", "Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Covers sour and sweet cherry powdery mildew and healthy foliage."
    ),
    "corn": CropRegistryEntry(
        crop_id="corn",
        crop_name="Corn (Maize)",
        scientific_name="Zea mays",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=[
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
            "Corn_(maize)___Common_rust_",
            "Corn_(maize)___Northern_Leaf_Blight",
            "Corn_(maize)___healthy"
        ],
        supported_diseases=["Gray Leaf Spot (Cercospora)", "Common Rust", "Northern Leaf Blight", "Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Long linear leaf lesions must be in focus; leaf edges outside camera frame can lower confidence."
    ),
    "grape": CropRegistryEntry(
        crop_id="grape",
        crop_name="Grapes",
        scientific_name="Vitis vinifera",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=[
            "Grape___Black_rot",
            "Grape___Esca_(Black_Measles)",
            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
            "Grape___healthy"
        ],
        supported_diseases=["Black Rot", "Esca (Black Measles)", "Isariopsis Leaf Blight", "Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Downy and powdery mildew in grapes require cloud vision or botanical knowledge base mapping."
    ),
    "orange": CropRegistryEntry(
        crop_id="orange",
        crop_name="Orange / Citrus",
        scientific_name="Citrus sinensis",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=["Orange___Haunglongbing_(Citrus_greening)"],
        supported_diseases=["Huanglongbing (Citrus Greening)"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Only covers Huanglongbing greening; citrus canker is supported via cloud consensus."
    ),
    "peach": CropRegistryEntry(
        crop_id="peach",
        crop_name="Peach",
        scientific_name="Prunus persica",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=[
            "Peach___Bacterial_spot",
            "Peach___healthy"
        ],
        supported_diseases=["Bacterial Spot", "Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Covers bacterial leaf spot and healthy leaves."
    ),
    "pepper": CropRegistryEntry(
        crop_id="pepper",
        crop_name="Pepper (Bell)",
        scientific_name="Capsicum annuum",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=[
            "Pepper,_bell___Bacterial_spot",
            "Pepper,_bell___healthy"
        ],
        supported_diseases=["Bacterial Spot", "Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Covers bell pepper bacterial spot. For tropical chilli leaf curl, cloud consensus is recommended."
    ),
    "potato": CropRegistryEntry(
        crop_id="potato",
        crop_name="Potato",
        scientific_name="Solanum tuberosum",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=[
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy"
        ],
        supported_diseases=["Early Blight", "Late Blight", "Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Target board concentric rings distinguish early blight from late blight."
    ),
    "raspberry": CropRegistryEntry(
        crop_id="raspberry",
        crop_name="Raspberry",
        scientific_name="Rubus idaeus",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=["Raspberry___healthy"],
        supported_diseases=["Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Only healthy class available in local model."
    ),
    "soybean": CropRegistryEntry(
        crop_id="soybean",
        crop_name="Soybean",
        scientific_name="Glycine max",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=["Soybean___healthy"],
        supported_diseases=["Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Local MobileNetV2 supports healthy soybean; soybean rust and frogeye leaf spot are routed to cloud consensus."
    ),
    "squash": CropRegistryEntry(
        crop_id="squash",
        crop_name="Squash / Cucurbits",
        scientific_name="Cucurbita pepo",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=["Squash___Powdery_mildew"],
        supported_diseases=["Powdery Mildew"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="White powdery surface fungal mycelium only."
    ),
    "strawberry": CropRegistryEntry(
        crop_id="strawberry",
        crop_name="Strawberry",
        scientific_name="Fragaria ananassa",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=[
            "Strawberry___Leaf_scorch",
            "Strawberry___healthy"
        ],
        supported_diseases=["Leaf Scorch", "Healthy"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Covers leaf scorch and healthy foliage."
    ),
    "tomato": CropRegistryEntry(
        crop_id="tomato",
        crop_name="Tomato",
        scientific_name="Solanum lycopersicum",
        status=CropSupportStatus.SUPPORTED,
        supported_model_labels=[
            "Tomato___Bacterial_spot",
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___Leaf_Mold",
            "Tomato___Septoria_leaf_spot",
            "Tomato___Spider_mites Two-spotted_spider_mite",
            "Tomato___Target_Spot",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
            "Tomato___Tomato_mosaic_virus",
            "Tomato___healthy"
        ],
        supported_diseases=[
            "Bacterial Spot",
            "Early Blight",
            "Late Blight",
            "Leaf Mold",
            "Septoria Leaf Spot",
            "Spider Mites (Two-spotted)",
            "Target Spot",
            "Tomato Yellow Leaf Curl Virus (TYLCV)",
            "Tomato Mosaic Virus",
            "Healthy"
        ],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="High precision on standard PlantVillage classes. Multi-infection leaves should be reviewed by an agronomist."
    ),

    # -------------------------------------------------------------
    # Crops with Cloud & Botanical Knowledge Support (Not in MobileNetV2)
    # -------------------------------------------------------------
    "sugarcane": CropRegistryEntry(
        crop_id="sugarcane",
        crop_name="Sugarcane",
        scientific_name="Saccharum officinarum",
        status=CropSupportStatus.PARTIALLY_SUPPORTED,
        supported_model_labels=[],
        supported_diseases=["Red Rot", "Smut", "Rust"],
        provider_support=["gemini", "openrouter", "kindwise", "botanical_species_classifier"],
        known_limitations="Not supported in MobileNetV2 PlantVillage weights. Handled via hybrid cloud vision or botanical species classifier."
    ),
    "cotton": CropRegistryEntry(
        crop_id="cotton",
        crop_name="Cotton",
        scientific_name="Gossypium hirsutum",
        status=CropSupportStatus.PARTIALLY_SUPPORTED,
        supported_model_labels=[],
        supported_diseases=["Bacterial Blight (Blackarm)", "Leaf Curl Virus", "Alternaria Leaf Spot"],
        provider_support=["gemini", "openrouter", "kindwise", "botanical_species_classifier"],
        known_limitations="Not supported in MobileNetV2 PlantVillage weights. Handled via hybrid cloud vision or botanical species classifier."
    ),
    "rice": CropRegistryEntry(
        crop_id="rice",
        crop_name="Rice (Paddy)",
        scientific_name="Oryza sativa",
        status=CropSupportStatus.PARTIALLY_SUPPORTED,
        supported_model_labels=[],
        supported_diseases=["Blast", "Brown Spot", "Sheath Blight"],
        provider_support=["gemini", "openrouter", "kindwise", "botanical_species_classifier"],
        known_limitations="Not supported in MobileNetV2 PlantVillage weights. Handled via hybrid cloud vision or botanical species classifier."
    ),
    "wheat": CropRegistryEntry(
        crop_id="wheat",
        crop_name="Wheat",
        scientific_name="Triticum aestivum",
        status=CropSupportStatus.PARTIALLY_SUPPORTED,
        supported_model_labels=[],
        supported_diseases=["Stripe / Yellow Rust", "Leaf Blight", "Powdery Mildew"],
        provider_support=["gemini", "openrouter", "kindwise", "botanical_species_classifier"],
        known_limitations="Not supported in MobileNetV2 PlantVillage weights. Handled via hybrid cloud vision or botanical species classifier."
    ),
    "mango": CropRegistryEntry(
        crop_id="mango",
        crop_name="Mango",
        scientific_name="Mangifera indica",
        status=CropSupportStatus.PARTIALLY_SUPPORTED,
        supported_model_labels=[],
        supported_diseases=["Anthracnose", "Powdery Mildew", "Dieback"],
        provider_support=["gemini", "openrouter", "kindwise", "botanical_species_classifier"],
        known_limitations="Not supported in MobileNetV2 PlantVillage weights. Handled via hybrid cloud vision or botanical species classifier."
    ),
    "chilli": CropRegistryEntry(
        crop_id="chilli",
        crop_name="Chilli / Hot Pepper",
        scientific_name="Capsicum frutescens",
        status=CropSupportStatus.PARTIALLY_SUPPORTED,
        supported_model_labels=["Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy"],
        supported_diseases=["Chilli Leaf Curl Virus", "Anthracnose / Dieback", "Bacterial Spot"],
        provider_support=["gemini", "openrouter", "kindwise", "botanical_species_classifier"],
        known_limitations="MobileNetV2 covers Bell Pepper; specific Asian chilli leaf curl requires cloud vision."
    ),
    "banana": CropRegistryEntry(
        crop_id="banana",
        crop_name="Banana",
        scientific_name="Musa acuminata",
        status=CropSupportStatus.PARTIALLY_SUPPORTED,
        supported_model_labels=[],
        supported_diseases=["Sigatoka Leaf Spot", "Panama Wilt"],
        provider_support=["gemini", "openrouter", "kindwise", "botanical_species_classifier"],
        known_limitations="Not present in MobileNetV2 PlantVillage dataset."
    ),
    "pomegranate": CropRegistryEntry(
        crop_id="pomegranate",
        crop_name="Pomegranate",
        scientific_name="Punica granatum",
        status=CropSupportStatus.PARTIALLY_SUPPORTED,
        supported_model_labels=[],
        supported_diseases=["Bacterial Blight (Telya)", "Anthracnose"],
        provider_support=["gemini", "openrouter", "kindwise", "botanical_species_classifier"],
        known_limitations="Not present in MobileNetV2 PlantVillage dataset."
    ),
    "onion": CropRegistryEntry(
        crop_id="onion",
        crop_name="Onion",
        scientific_name="Allium cepa",
        status=CropSupportStatus.PARTIALLY_SUPPORTED,
        supported_model_labels=[],
        supported_diseases=["Purple Blotch", "Stemphylium Leaf Blight"],
        provider_support=["gemini", "openrouter", "kindwise", "botanical_species_classifier"],
        known_limitations="Not present in MobileNetV2 PlantVillage dataset."
    ),
    "citrus": CropRegistryEntry(
        crop_id="citrus",
        crop_name="Citrus / Lemon",
        scientific_name="Citrus limon",
        status=CropSupportStatus.PARTIALLY_SUPPORTED,
        supported_model_labels=["Orange___Haunglongbing_(Citrus_greening)"],
        supported_diseases=["Citrus Canker", "Huanglongbing"],
        provider_support=["mobilenetv2_local", "gemini", "openrouter", "kindwise"],
        known_limitations="Local model covers citrus greening on orange. Lemon canker is covered via cloud consensus."
    ),
}

# Crop name alias normalization mapping
CROP_ALIASES: Dict[str, str] = {
    "tomatoes": "tomato",
    "lycopersicon": "tomato",
    "potatoes": "potato",
    "maize": "corn",
    "corn": "corn",
    "zea mays": "corn",
    "grape": "grape",
    "grapes": "grape",
    "vine": "grape",
    "vitis": "grape",
    "apples": "apple",
    "bell pepper": "pepper",
    "capsicum": "pepper",
    "sweet pepper": "pepper",
    "chili": "chilli",
    "chilli": "chilli",
    "peppers": "pepper",
    "strawberries": "strawberry",
    "cherries": "cherry",
    "blueberries": "blueberry",
    "raspberries": "raspberry",
    "soya": "soybean",
    "soybeans": "soybean",
    "soya bean": "soybean",
    "paddy": "rice",
    "sugar cane": "sugarcane",
    "sugarcane": "sugarcane",
    "lemons": "citrus",
    "lemon": "citrus",
    "oranges": "orange",
}


def normalize_crop_key(name: Optional[str]) -> str:
    """Normalizes arbitrary crop name strings into canonical registry keys."""
    if not name:
        return ""
    cleaned = name.strip().lower()
    for alias, canonical in CROP_ALIASES.items():
        if alias in cleaned:
            return canonical
    for key in CROP_REGISTRY:
        if key in cleaned:
            return key
    return cleaned


def get_crop_support(crop_name: Optional[str]) -> CropRegistryEntry:
    """Retrieves full registry record for a given crop name."""
    key = normalize_crop_key(crop_name)
    if key in CROP_REGISTRY:
        return CROP_REGISTRY[key]
    
    return CropRegistryEntry(
        crop_id=key or "unknown",
        crop_name=crop_name or "Unknown Crop",
        scientific_name="N/A",
        status=CropSupportStatus.UNKNOWN,
        supported_model_labels=[],
        supported_diseases=[],
        provider_support=[],
        known_limitations="This crop is not indexed in the AgroScan crop registry."
    )


def is_crop_supported_by_local_model(crop_name: Optional[str]) -> bool:
    """Checks whether the crop has native trained classes in the local MobileNetV2 model."""
    entry = get_crop_support(crop_name)
    return entry.status == CropSupportStatus.SUPPORTED and len(entry.supported_model_labels) > 0


def get_all_supported_crops() -> List[CropRegistryEntry]:
    """Returns all registered crop entries."""
    return list(CROP_REGISTRY.values())
