"""
AgroScan AI — Agricultural Knowledge Base & RAG Retrieval Service.
Provides fast, keyword-matched reference facts for crop diseases, treatment safety,
spread prevention, cultivation care, and microclimate sensitivity.
Used to inject precise reference grounding into the LLM system prompt.
"""
import re
from typing import List, Dict, Any, Optional

# Curated Agricultural Reference Knowledge Base
AGRICULTURE_KNOWLEDGE_BASE: List[Dict[str, Any]] = [
    {
        "id": "kb_general_safety",
        "keywords": ["dangerous", "harmful", "toxic", "poisonous", "human", "eat", "edible", "safe", "consumption"],
        "crops": ["all"],
        "title": "Disease Toxicity and Produce Safety",
        "snippet": (
            "Most plant foliar diseases (such as leaf blight, rust, and powdery mildew) are caused by fungi or bacteria "
            "that do not infect humans or animals. However, heavily diseased leaves or fruits should NOT be eaten raw, "
            "and infected plant parts may harbor mycotoxins or secondary molds. When spraying copper fungicides or "
            "chemical protectants, always observe the Pre-Harvest Interval (PHI, typically 3-14 days) and wash produce thoroughly."
        )
    },
    {
        "id": "kb_disease_spread",
        "keywords": ["spread", "contagious", "neighboring", "trees", "plants", "orchard", "wind", "rain splash", "infect"],
        "crops": ["all"],
        "title": "Disease Transmission & Orchard Spread Prevention",
        "snippet": (
            "Fungal and bacterial foliar pathogens spread rapidly via windblown spores, rain splashes, and contaminated pruning tools. "
            "To stop disease from spreading to adjacent healthy plants: 1) Immediately prune and safely destroy/bury heavily infected foliage. "
            "2) Disinfect shears with 70% isopropyl alcohol or 10% bleach between plants. 3) Avoid overhead sprinkler irrigation during warm humid evenings. "
            "4) Apply a broad-spectrum protective bio-spray (such as Bacillus subtilis or neem oil) to create a protective canopy barrier on surrounding plants."
        )
    },
    {
        "id": "kb_organic_fungicides",
        "keywords": ["organic", "neem", "spray", "bio", "natural", "home remedy", "compost tea", "curd", "buttermilk"],
        "crops": ["all"],
        "title": "Organic Treatment and Bio-Protectants",
        "snippet": (
            "Organic management relies on preventive bio-fungicides: Cold-pressed Neem Oil (3000 ppm) applied at 3-5 ml/L water with a mild emulsifier; "
            "Fermented sour buttermilk/curd spray (1:10 dilution) rich in lactic acid bacteria against fungal spots; and Trichoderma viride / Pseudomonas fluorescens "
            "applied as foliar or root drench to suppress fungal sporulation without chemical residues."
        )
    },
    {
        "id": "kb_chemical_control",
        "keywords": ["chemical", "fungicide", "pesticide", "mancozeb", "copper", "dosage", "difenoconazole", "hexaconazole"],
        "crops": ["all"],
        "title": "Targeted Chemical Intervention Guidelines",
        "snippet": (
            "For severe or rapidly spreading infections exceeding economic threshold (ETL): Use Copper Oxychloride 50% WP (2.5 g/L) for bacterial and early fungal blights, "
            "Mancozeb 75% WP (2.0 g/L) for protective contact action, or systemic triazoles like Hexaconazole 5% SC / Difenoconazole 25% EC (1 ml/L) for deep tissue rusts and powdery mildews. "
            "Always wear personal protective gear (mask, gloves) and spray during calm early morning or late afternoon hours."
        )
    },
    {
        "id": "kb_mango_anthracnose",
        "keywords": ["mango", "anthracnose", "black spot", "colletotrichum", "blossom", "dieback"],
        "crops": ["mango"],
        "title": "Mango Anthracnose Management",
        "snippet": (
            "Mango Anthracnose (Colletotrichum gloeosporioides) causes dark brown sunken necrotic spots on leaves, blossoms, and young fruits. "
            "Control: Prune dead twigs after harvest and spray Copper Oxychloride (3g/L) or Carbendazim 50 WP (1g/L). "
            "Improve canopy ventilation to facilitate quick drying after monsoon showers."
        )
    },
    {
        "id": "kb_mango_powdery_mildew",
        "keywords": ["mango", "powdery mildew", "white powder", "oidium", "flowering"],
        "crops": ["mango"],
        "title": "Mango Powdery Mildew Control",
        "snippet": (
            "Mango Powdery Mildew (Oidium mangiferae) attacks inflorescences and tender shoots during cool nights and humid mornings. "
            "Control: Apply Wettable Sulphur 80% WP (2g/L) or Hexaconazole 5% EC (1ml/L) at panicle emergence and fruit set stages."
        )
    },
    {
        "id": "kb_tomato_late_blight",
        "keywords": ["tomato", "potato", "late blight", "phytophthora", "water soaked", "dark lesion"],
        "crops": ["tomato", "potato"],
        "title": "Tomato & Potato Late Blight Protocol",
        "snippet": (
            "Late Blight (Phytophthora infestans) is an aggressive oomycete thriving in temperatures 16-22°C with >85% humidity. "
            "Control: Apply preventive Mancozeb (2.5g/L) or Metalaxyl + Mancozeb (2g/L) immediately upon noticing water-soaked margins under leaves. "
            "Destroy volunteer potato tubers and ensure good air circulation."
        )
    },
    {
        "id": "kb_tomato_early_blight",
        "keywords": ["tomato", "early blight", "alternaria", "concentric rings", "target spot"],
        "crops": ["tomato", "potato"],
        "title": "Early Blight / Alternaria Target Spots",
        "snippet": (
            "Alternaria solani creates characteristic concentric target-board brown rings on older lower foliage. "
            "Control: Stake plants off the soil, mulch beneath rows to prevent soil splash, and apply Chlorothalonil (2g/L) or Azoxystrobin (1ml/L)."
        )
    },
    {
        "id": "kb_corn_leaf_blight",
        "keywords": ["corn", "maize", "northern leaf blight", "turcicum", "cigar", "lesion"],
        "crops": ["corn", "maize"],
        "title": "Northern Corn Leaf Blight Management",
        "snippet": (
            "Northern Corn Leaf Blight (Exserohilum turcicum) produces long, elliptical grayish-green cigar-shaped lesions. "
            "Control: Rotate with non-grass crops, avoid excessive nitrogen fertilization, and apply Propiconazole 25% EC (1ml/L) if lesions appear before silking."
        )
    },
    {
        "id": "kb_rice_blast",
        "keywords": ["rice", "paddy", "blast", "magnaporthe", "spindle", "neck blast"],
        "crops": ["rice", "paddy"],
        "title": "Rice Leaf and Neck Blast Control",
        "snippet": (
            "Rice Blast (Magnaporthe oryzae) produces spindle-shaped lesions with grayish centers and brown borders. "
            "Control: Avoid excessive urea top-dressing. Maintain uniform field water depth. Spray Tricyclazole 75% WP (0.6g/L) or Isoprothiolane 40% EC (1.5ml/L)."
        )
    },
    {
        "id": "kb_sugarcane_red_rot",
        "keywords": ["sugarcane", "red rot", "colletotrichum falcatum", "alcoholic smell", "sett"],
        "crops": ["sugarcane"],
        "title": "Sugarcane Red Rot Management",
        "snippet": (
            "Sugarcane Red Rot causes third-to-fourth leaf yellowing and red pith discoloration with cross-wise white patches. "
            "Control: Use disease-free certified setts, dip in Carbendazim solution (1g/L) for 15 minutes before planting, and ensure proper field drainage."
        )
    },
    {
        "id": "kb_cotton_bacterial_blight",
        "keywords": ["cotton", "angular leaf spot", "black arm", "xanthomonas"],
        "crops": ["cotton"],
        "title": "Cotton Bacterial Blight / Black Arm Protocol",
        "snippet": (
            "Angular leaf spot is caused by Xanthomonas citri. Control: Seed treatment with Streptocycline (100 ppm) + Copper Oxychloride (2.5g/L). "
            "Spray Copper Oxychloride (2.5g/L) combined with Streptocycline (0.1g/L) at 15-day intervals during warm humid weather."
        )
    }
]


class AgriRAGService:
    """
    Lightweight keyword-matching RAG retrieval service for Agricultural Advisory.
    Matches queries based on crop context, disease name, and specific user question keywords.
    """

    @classmethod
    def retrieve_context(cls, question: str, crop_name: Optional[str] = None, disease_name: Optional[str] = None, top_k: int = 2) -> List[Dict[str, Any]]:
        clean_q = (question or "").lower()
        clean_crop = (crop_name or "").lower()
        clean_disease = (disease_name or "").lower()

        # Tokenize question
        q_tokens = set(re.findall(r"\b\w{3,}\b", clean_q))
        
        scored_docs = []

        for doc in AGRICULTURE_KNOWLEDGE_BASE:
            score = 0
            doc_crops = [c.lower() for c in doc.get("crops", [])]

            # Crop matching
            if clean_crop and any(c in clean_crop or clean_crop in c for c in doc_crops if c != "all"):
                score += 3
            elif "all" in doc_crops:
                score += 1

            # Keyword overlap matching
            for kw in doc.get("keywords", []):
                kw_lower = kw.lower()
                if kw_lower in clean_q:
                    score += 4
                elif any(token in kw_lower for token in q_tokens):
                    score += 2

            # Disease name overlap
            if clean_disease and any(kw.lower() in clean_disease for kw in doc.get("keywords", [])):
                score += 3

            if score > 1:
                scored_docs.append((score, doc))

        # Sort by relevance score descending
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored_docs[:top_k]]

    @classmethod
    def build_reference_block(cls, question: str, crop_name: Optional[str] = None, disease_name: Optional[str] = None) -> str:
        snippets = cls.retrieve_context(question, crop_name=crop_name, disease_name=disease_name, top_k=2)
        if not snippets:
            return ""

        formatted = ["Reference Information (Agronomy Knowledge Base):"]
        for s in snippets:
            formatted.append(f"- {s['title']}: {s['snippet']}")
        return "\n".join(formatted)

    @classmethod
    def is_weather_relevant(cls, question: str) -> bool:
        """Determines if the question mentions weather, climate, rain, humidity, temperature, or seasonal factors."""
        w_keywords = [
            "weather", "rain", "rainfall", "climate", "temperature", "humidity", "monsoon",
            "season", "forecast", "cloudy", "sunny", "storm", "wind", "heat", "cold",
            "हवामान", "पाऊस", "तापमान", "आर्द्रता", "ऋतू"
        ]
        q_lower = (question or "").lower()
        return any(k in q_lower for k in w_keywords)
