"""
AgroScan AI — Agricultural Source Registry & Authority Directory
Categorizes international and national agricultural bodies, compendiums,
peer-reviewed journals, and university extension publications with authority scoring.
"""

from typing import Dict, Any, List

class SourceCategory:
    LEVEL_1_GOV_INTL = "government_international"  # FAO, ICAR, USDA, State Ag Depts (Authority: 1.00)
    LEVEL_1_AGRI_UNIV = "agricultural_university"   # TNAU, MPKV, PAU, IARI (Authority: 0.95)
    LEVEL_2_AGRI_DB = "agri_database"               # CABI, Plantwise, EPPO (Authority: 0.95)
    LEVEL_2_PEER_REVIEWED = "peer_reviewed_paper"   # Springer, ScienceDirect, APS, Frontiers (Authority: 0.95)
    LEVEL_3_EXTENSION = "extension_publication"     # Verified extension bulletins (Authority: 0.88)
    LEVEL_4_COMMERCIAL = "commercial_agri"          # Supplementary agribusiness (Authority: 0.60)
    LEVEL_5_UNVERIFIED = "unverified_web"           # Forums, social media (Authority: 0.10)

AUTHORITY_WEIGHTS: Dict[str, float] = {
    SourceCategory.LEVEL_1_GOV_INTL: 1.00,
    SourceCategory.LEVEL_1_AGRI_UNIV: 0.95,
    SourceCategory.LEVEL_2_AGRI_DB: 0.95,
    SourceCategory.LEVEL_2_PEER_REVIEWED: 0.95,
    SourceCategory.LEVEL_3_EXTENSION: 0.88,
    SourceCategory.LEVEL_4_COMMERCIAL: 0.60,
    SourceCategory.LEVEL_5_UNVERIFIED: 0.10
}

# Verified Knowledge Repository Indexed by Topic
VERIFIED_RESEARCH_ENTRIES: Dict[str, List[Dict[str, Any]]] = {
    "mango_pathology_powdery_mildew": [
        {
            "claim": "Oidium mangiferae conidia germinate under high relative humidity (65-85%) without requiring free leaf water films. Inflorescence infection causes flower drying and near-total fruit drop.",
            "source": "FAO Plant Production & Protection",
            "source_type": SourceCategory.LEVEL_1_GOV_INTL,
            "url": "https://www.fao.org/agriculture/crops/the-matic-sitemap/theme/pests/en/",
            "published_date": "2023-04-15",
            "authority_score": 1.00,
            "evidence_quality": 0.96,
            "title": "FAO Technical Guidelines for Mango Disease Management"
        },
        {
            "claim": "Preventive sprays of cold-pressed neem oil (1500-3000 ppm @ 3-5 ml/L) at bud break provide bio-protective suppression. Systemic triazoles such as Hexaconazole 5% EC (1 ml/L) or Wettable Sulphur (2.5 g/L) are curative.",
            "source": "CABI Crop Protection Compendium",
            "source_type": SourceCategory.LEVEL_2_AGRI_DB,
            "url": "https://www.cabi.org/cpc/datasheet/37258",
            "published_date": "2023-11-10",
            "authority_score": 0.95,
            "evidence_quality": 0.95,
            "title": "CABI Datasheet: Oidium mangiferae (Mango Powdery Mildew)"
        },
        {
            "claim": "Canopy thinning pruning post-harvest increases solar radiation penetration and reduces powdery mildew severity by 68% in field trials.",
            "source": "Springer Journal of Plant Pathology",
            "source_type": SourceCategory.LEVEL_2_PEER_REVIEWED,
            "url": "https://link.springer.com/journal/42161",
            "published_date": "2024-02-18",
            "authority_score": 0.95,
            "evidence_quality": 0.94,
            "title": "Epidemiology and Canopy Dynamics of Mango Powdery Mildew"
        },
        {
            "claim": "Wettable sulfur must not be applied when temperatures exceed 32°C to prevent sulfur leaf scorch. Avoid excess urea which promotes succulent susceptible tissues.",
            "source": "ICAR-Central Institute for Subtropical Horticulture",
            "source_type": SourceCategory.LEVEL_1_GOV_INTL,
            "url": "https://cish.icar.gov.in/advisory.php",
            "published_date": "2024-01-20",
            "authority_score": 1.00,
            "evidence_quality": 0.98,
            "title": "ICAR-CISH Package of Practices for Mango"
        }
    ],

    "mango_agronomy_soil_water": [
        {
            "claim": "Mango requires deep, well-drained alluvial, red loamy, or laterite soil with pH 5.5 to 7.5 and a minimum soil depth of 2.0 to 2.5 meters. Withhold irrigation for 2-3 months prior to flowering (Nov-Dec) to induce floral bud dormancy.",
            "source": "ICAR-Indian Agricultural Research Institute",
            "source_type": SourceCategory.LEVEL_1_GOV_INTL,
            "url": "https://www.iari.res.in/en/mango-package-of-practices.php",
            "published_date": "2023-08-12",
            "authority_score": 1.00,
            "evidence_quality": 0.97,
            "title": "ICAR-IARI Agronomic & Water Protocols for Mango"
        },
        {
            "claim": "Young non-bearing trees require watering every 3-5 days in summer and 8-10 days in winter. Bearing trees require regular irrigation every 10-15 days from fruit set until maturity.",
            "source": "Tamil Nadu Agricultural University (TNAU)",
            "source_type": SourceCategory.LEVEL_1_AGRI_UNIV,
            "url": "https://agritech.tnau.ac.in/horticulture/horti_fruits_mango.html",
            "published_date": "2023-09-05",
            "authority_score": 0.95,
            "evidence_quality": 0.92,
            "title": "TNAU Horticulture Agritech Portal: Mango Cultivation"
        }
    ],

    "sugarcane_red_rot_pathology": [
        {
            "claim": "Red Rot (Colletotrichum falcatum) causes yellowing and drying of 3rd/4th crown leaves. Split stalks reveal dull red pith with distinct transverse white patches and an alcoholic odor. Foliar chemical sprays cannot cure internal vascular infections.",
            "source": "ICAR-Sugarcane Breeding Institute (SBI)",
            "source_type": SourceCategory.LEVEL_1_GOV_INTL,
            "url": "https://sugarcane.icar.gov.in/index.php/en/red-rot-management",
            "published_date": "2023-12-01",
            "authority_score": 1.00,
            "evidence_quality": 0.98,
            "title": "ICAR-SBI Coimbatore: Integrated Red Rot Management"
        },
        {
            "claim": "Mandatory prevention: Certified disease-free seed setts, hot water treatment (50°C for 2 hours), sett dip in Carbendazim 50% WP (1g/L) or Trichoderma viride (10g/L), and roguing infected stools.",
            "source": "CABI Plantwise",
            "source_type": SourceCategory.LEVEL_2_AGRI_DB,
            "url": "https://www.cabi.org/cpc/datasheet/14981",
            "published_date": "2023-07-22",
            "authority_score": 0.95,
            "evidence_quality": 0.95,
            "title": "CABI Crop Protection Compendium: Sugarcane Red Rot"
        },
        {
            "claim": "Pre-soaking setts with bio-agent Trichoderma harzianum and endophytic Gluconacetobacter primed plant systemic resistance and reduced red rot incidence by 76% in field trials.",
            "source": "Springer Sugar Tech Research",
            "source_type": SourceCategory.LEVEL_2_PEER_REVIEWED,
            "url": "https://link.springer.com/journal/12355",
            "published_date": "2024-03-05",
            "authority_score": 0.95,
            "evidence_quality": 0.93,
            "title": "Sugar Tech: Biological Defense Priming in Sugarcane"
        }
    ],

    "sugarcane_agronomy_fertilizer_water": [
        {
            "claim": "Recommended NPK for Suru sugarcane: 250:115:115 kg/ha. Basal at planting: 10% N, full P, 50% K; Tillering (6-8 wks): 40% N; 12-14 wks: 10% N; Final earthing-up (120-150 days): 40% N and 50% K. Water requirement: 1500-2500 mm.",
            "source": "Vasantdada Sugar Institute (VSI) & MPKV Rahuri",
            "source_type": SourceCategory.LEVEL_1_AGRI_UNIV,
            "url": "https://www.vsisugar.com/research-extension/agronomy/",
            "published_date": "2023-10-14",
            "authority_score": 0.95,
            "evidence_quality": 0.95,
            "title": "VSI Pune & MPKV Package of Practices for Sugarcane"
        }
    ],

    "tomato_potato_blights_pathology": [
        {
            "claim": "Early Blight (Alternaria solani) causes concentric dark brown target-board bullseye rings primarily on older lower leaves during warm conditions (24-29°C). Late Blight (Phytophthora infestans) causes rapid water-soaked dark greasy lesions with delicate white downy mold underneath in cool humid weather (15-22°C, RH>85%).",
            "source": "World Vegetable Center (AVRDC) & FAO",
            "source_type": SourceCategory.LEVEL_1_GOV_INTL,
            "url": "https://avrdc.org/tomato-disease-identification-management/",
            "published_date": "2023-11-28",
            "authority_score": 1.00,
            "evidence_quality": 0.98,
            "title": "AVRDC & FAO Field Guide to Solanaceous Diseases"
        },
        {
            "claim": "Preventive: Mancozeb 75% WP (2.5g/L) or Copper Oxychloride 50% WP (2.5g/L). Curative for Late Blight: Cymoxanil 8% + Mancozeb 64% WP (2g/L) or Metalaxyl. Cultural: Staking, pruning lower 30cm suckers, and drip irrigation prevent spore splashing.",
            "source": "CABI Plantwise",
            "source_type": SourceCategory.LEVEL_2_AGRI_DB,
            "url": "https://www.plantwise.org/KnowledgeBank/Datasheet.aspx?dsid=5066",
            "published_date": "2024-01-15",
            "authority_score": 0.95,
            "evidence_quality": 0.95,
            "title": "CABI Solanaceous IPM Factsheet"
        }
    ],

    "general_agronomy_principles": [
        {
            "claim": "Crop rotation breaks host-specific pathogen and nematode life cycles while legume root nodules fix atmospheric nitrogen. Photosynthesis (6CO2 + 6H2O -> C6H12O6 + 6O2) is the primary driver of crop yield; foliar blights damage chlorophyll and directly reduce dry matter accumulation.",
            "source": "FAO Sustainable Agriculture Series",
            "source_type": SourceCategory.LEVEL_1_GOV_INTL,
            "url": "https://www.fao.org/sustainable-crop-production/en/",
            "published_date": "2023-06-30",
            "authority_score": 1.00,
            "evidence_quality": 0.97,
            "title": "FAO Principles of Sustainable Agronomy & Physiology"
        },
        {
            "claim": "Optimal soil pH for nutrient availability is 6.0 to 7.5. Acidic soils (pH<6.0) require agricultural lime (CaCO3), whereas sodic soils (pH>8.0) require gypsum (CaSO4) and organic manure.",
            "source": "ICAR-Indian Institute of Soil Science (IISS)",
            "source_type": SourceCategory.LEVEL_1_GOV_INTL,
            "url": "https://iiss.icar.gov.in/advisory/",
            "published_date": "2023-08-20",
            "authority_score": 1.00,
            "evidence_quality": 0.96,
            "title": "ICAR-IISS Soil Health & Nutrient Bioavailability"
        }
    ]
}
