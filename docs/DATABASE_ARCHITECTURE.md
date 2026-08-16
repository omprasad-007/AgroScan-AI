# AgroScan AI — Database Schema & Data Architecture

## Overview
AgroScan AI utilizes SQLAlchemy 2.0 ORM with a default local SQLite engine (`agroscan.db`) for development, seamlessly migrating to PostgreSQL in production via `DATABASE_URL`.

---

## Entity Relationship Model

```
+--------------------+            +------------------------+
|       User         | 1        * |     ScanPrediction     |
|--------------------|<-----------|------------------------|
| id (PK, UUID)      |            | id (PK, UUID)          |
| email (Unique)     |            | user_id (FK -> User)   |
| hashed_password    |            | farm_id (FK -> Farm)   |
| full_name          |            | crop_detected          |
| role (farmer/admin)|            | disease_name           |
| city, state        |            | confidence_score       |
+--------------------+            | severity_percentage    |
                                  | severity_level         |
                                  +------------------------+
                                              | 1
                                              |
                                              | 1
                                  +------------------------+
                                  |     Recommendation     |
                                  |------------------------|
                                  | id (PK, UUID)          |
                                  | prediction_id (FK)     |
                                  | organic_remedy         |
                                  | chemical_remedy        |
                                  | preventive_steps       |
                                  +------------------------+
```

---

## Data Privacy & IDOR Enforcement Controls
- All query operations on `ScanPrediction`, `Farm`, and `Recommendation` filter by `user_id == current_user.id`.
- Orphan records prevented via explicit foreign key relationships and database cascade deletion handlers.
