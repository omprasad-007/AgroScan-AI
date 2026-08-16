from fastapi import APIRouter, Query
from typing import List, Dict, Any

router = APIRouter()

# Large Extensible Plant & Crop Catalog
PLANT_CATALOG = [
    {"name": "Mango", "scientific_name": "Mangifera indica", "family": "Anacardiaceae", "category": "Fruit Tree"},
    {"name": "Neem", "scientific_name": "Azadirachta indica", "family": "Meliaceae", "category": "Medicinal Tree"},
    {"name": "Sugarcane", "scientific_name": "Saccharum officinarum", "family": "Poaceae", "category": "Cash Crop"},
    {"name": "Rice", "scientific_name": "Oryza sativa", "family": "Poaceae", "category": "Cereal Grain"},
    {"name": "Wheat", "scientific_name": "Triticum aestivum", "family": "Poaceae", "category": "Cereal Grain"},
    {"name": "Tomato", "scientific_name": "Solanum lycopersicum", "family": "Solanaceae", "category": "Vegetable"},
    {"name": "Potato", "scientific_name": "Solanum tuberosum", "family": "Solanaceae", "category": "Tuber Vegetable"},
    {"name": "Corn (Maize)", "scientific_name": "Zea mays", "family": "Poaceae", "category": "Cereal Grain"},
    {"name": "Cotton", "scientific_name": "Gossypium hirsutum", "family": "Malvaceae", "category": "Fiber Crop"},
    {"name": "Soybean", "scientific_name": "Glycine max", "family": "Fabaceae", "category": "Legume / Oilseed"},
    {"name": "Chilli", "scientific_name": "Capsicum annuum", "family": "Solanaceae", "category": "Spice / Vegetable"},
    {"name": "Onion", "scientific_name": "Allium cepa", "family": "Amaryllidaceae", "category": "Vegetable"},
    {"name": "Guava", "scientific_name": "Psidium guajava", "family": "Myrtaceae", "category": "Fruit Tree"},
    {"name": "Papaya", "scientific_name": "Carica papaya", "family": "Caricaceae", "category": "Fruit Tree"},
    {"name": "Banana", "scientific_name": "Musa acuminata", "family": "Musaceae", "category": "Fruit Crop"},
    {"name": "Turmeric", "scientific_name": "Curcuma longa", "family": "Zingiberaceae", "category": "Spice Crop"},
    {"name": "Ginger", "scientific_name": "Zingiber officinale", "family": "Zingiberaceae", "category": "Spice Crop"},
    {"name": "Grape", "scientific_name": "Vitis vinifera", "family": "Vitaceae", "category": "Fruit Vine"},
    {"name": "Pomegranate", "scientific_name": "Punica granatum", "family": "Lythraceae", "category": "Fruit Tree"},
    {"name": "Brinjal (Eggplant)", "scientific_name": "Solanum melongena", "family": "Solanaceae", "category": "Vegetable"}
]

@router.get("/search", response_model=List[Dict[str, Any]])
def search_plants(q: str = Query("", description="Query string for searching plant or crop species")):
    query = (q or "").strip().lower()
    if not query:
        return PLANT_CATALOG[:10]

    results = [
        p for p in PLANT_CATALOG
        if query in p["name"].lower() or query in p["scientific_name"].lower() or query in p["category"].lower()
    ]
    return results
