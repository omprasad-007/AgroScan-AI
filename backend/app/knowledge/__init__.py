"""
AgroScan AI Knowledge Base Module
Provides structured access to plant data, disease pathology, and general agronomic science.
"""

from app.knowledge.plants_data import PLANTS_KNOWLEDGE_BASE, get_plant_data, list_all_plants
from app.knowledge.diseases_data import DISEASES_KNOWLEDGE_BASE, get_disease_data, check_disease_plant_relevance
from app.knowledge.general_agri_data import GENERAL_AGRI_KNOWLEDGE_BASE, get_general_agri_concept

__all__ = [
    "PLANTS_KNOWLEDGE_BASE",
    "get_plant_data",
    "list_all_plants",
    "DISEASES_KNOWLEDGE_BASE",
    "get_disease_data",
    "check_disease_plant_relevance",
    "GENERAL_AGRI_KNOWLEDGE_BASE",
    "get_general_agri_concept"
]
