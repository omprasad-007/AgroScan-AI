#!/usr/bin/env python3
"""
AgroScan AI — Safe Development Database Reset Script
Refuses execution when ENVIRONMENT=production or DEMO_MODE=false.
Requires explicit command-line flag: --confirm-reset
"""

import os
import sys
import argparse

# Add backend directory to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.all_models import ScanPrediction, Recommendation, ChatMessage, ChatSession, Farm

def reset_dev_data():
    parser = argparse.ArgumentParser(description="AgroScan AI Development Database Reset Utility")
    parser.add_argument("--confirm-reset", action="store_true", help="Explicit confirmation flag required to execute data reset")
    args = parser.parse_args()

    # Rule 3 Safety Checks: Refuse execution in production
    app_env = getattr(settings, "APP_ENV", "development").lower()
    if app_env == "production":
        print("❌ SAFETY BLOCK: Cannot reset database when ENVIRONMENT=production.")
        sys.exit(1)

    if not getattr(settings, "DEMO_MODE", True):
        print("❌ SAFETY BLOCK: Database reset is disabled when DEMO_MODE=false.")
        sys.exit(1)

    if not args.confirm-reset:
        print("⚠️ SAFETY GUARD: Execution requires explicit command line confirmation flag.")
        print("Usage: python scripts/reset_dev_data.py --confirm-reset")
        sys.exit(1)

    db = SessionLocal()
    try:
        print("Cleaning test recommendations...")
        db.query(Recommendation).delete()

        print("Cleaning test scan predictions...")
        db.query(ScanPrediction).delete()

        print("Cleaning test chat messages & sessions...")
        db.query(ChatMessage).delete()
        db.query(ChatSession).delete()

        print("Cleaning test farm entries...")
        db.query(Farm).delete()

        db.commit()
        print("✅ Local development database test data reset successfully. Database schema preserved.")
    except Exception as e:
        db.rollback()
        print(f"❌ Database reset failed: {e}")
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    reset_dev_data()
