# AgroScan AI - Stitch UI/UX Design Connection & Mapping

This document connects and maps all **Stitch UI/UX Design System** screens and assets directly to the **AgroScan AI Frontend Application** codebase.

---

## 🎨 Design System Foundation
* **Stitch Project Name:** AgroScan AI Assistant
* **Stitch Project ID:** `10267818660884263807`
* **Local Design System Token File:** [`agroscan_design_system/DESIGN.md`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/agroscan_design_system/DESIGN.md)
* **Frontend Stylesheet:** [`frontend/src/index.css`](file:///d:/Projects/AgroScan%20AI/frontend/src/index.css)
* **Tailwind Config:** [`frontend/tailwind.config.js`](file:///d:/Projects/AgroScan%20AI/frontend/tailwind.config.js)

---

## 🗺️ Screen & Component Mapping Table

| # | Stitch Screen Title | Screen ID | Local Folder | Application Route | React Page Component |
|---|---------------------|-----------|--------------|-------------------|----------------------|
| 1 | **AgroScan AI - Welcome** | `13fb6ea49a4a4dd892294344a15068a3` | [`agroscan_ai_welcome`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/agroscan_ai_welcome) | `/` | [`LandingPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/LandingPage.jsx) |
| 2 | **Farmer Registration** | `7f66bf3546574aed83069e369595e36a` | [`farmer_registration`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/farmer_registration) | `/register` | [`RegisterPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/RegisterPage.jsx) |
| 3 | **Farmer Dashboard** | `6b61dbc32e744634b103cea62b333d69` | [`farmer_dashboard`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/farmer_dashboard) | `/dashboard` | [`DashboardPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/DashboardPage.jsx) |
| 4 | **Scan a Leaf (v1)** | `8e7ead7d835f4dfe912d40a45ecf8d39` | [`scan_a_leaf`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/scan_a_leaf) | `/scan` | [`ScanPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/ScanPage.jsx) |
| 5 | **Scan a Leaf (v2)** | `4b0113bc82d6465c97e957c9d4f5bab4` | [`scan_a_leaf_2`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/scan_a_leaf_2) | `/scan` | [`ScanPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/ScanPage.jsx) |
| 6 | **Analyzing... (v1)** | `5847b6920c3e435495cca0ecd0a9a315` | [`analyzing`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/analyzing) | `/analysis` | [`AnalysisPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/AnalysisPage.jsx) |
| 7 | **Analyzing... (v2)** | `b4f161ef0c104a88a0028f5d051fbf81` | [`analyzing_2`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/analyzing_2) | `/analysis` | [`AnalysisPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/AnalysisPage.jsx) |
| 8 | **Diagnosis Result** | `948773e83ae54348acdccd13faefad47` | [`diagnosis_result`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/diagnosis_result) | `/results/:scanId` | [`ResultPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/ResultPage.jsx) |
| 9 | **Scan History** | `9af7142a951644edb94687095fcbcac1` | [`scan_history`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/scan_history) | `/history` | [`HistoryPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/HistoryPage.jsx) |
| 10 | **Farm Analytics** | `9ae97ab56a2c41bca3958b748ec6bcaa` | [`farm_analytics`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/farm_analytics) | `/analytics` | [`AnalyticsPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/AnalyticsPage.jsx) |
| 11 | **Farm Analytics (Farmer View)** | `86e7d4b2189c491ea6f989f37d890fd5` | [`farm_analytics_farmer_view`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/farm_analytics_farmer_view) | `/analytics` | [`AnalyticsPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/AnalyticsPage.jsx) |
| 12 | **Weather & Disease Risk** | `ab66ec76a5924cdfb885fbb166853b2b` | [`weather_disease_risk`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/weather_disease_risk) | `/weather` | [`WeatherRiskPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/WeatherRiskPage.jsx) |
| 13 | **Weather & Disease Risk Details** | `04e8021060884d958d071d4cb64a86bf` | [`weather_disease_risk_details`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/weather_disease_risk_details) | `/weather` | [`WeatherRiskPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/WeatherRiskPage.jsx) |
| 14 | **AI Assistant** | `d683bd75c92b4109b17fc2e39bbae9cc` | [`ai_assistant`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/ai_assistant) | `/assistant` | [`AssistantPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/AssistantPage.jsx) |
| 15 | **Agriculture AI Assistant** | `9f848e2f7b22403dbf11e09338bdf52c` | [`agriculture_ai_assistant`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/agriculture_ai_assistant) | `/assistant` | [`AssistantPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/AssistantPage.jsx) |
| 16 | **My Farm Profile** | `7eae9f419dda415b9733289a14a758b6` | [`my_farm_profile`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/my_farm_profile) | `/profile` | [`ProfilePage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/ProfilePage.jsx) |
| 17 | **Admin Overview** | `fcffaa817b1d426184fb75acf8bb5d0f` | [`admin_overview`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/admin_overview) | `/admin` | [`AdminDashboardPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/AdminDashboardPage.jsx) |
| 18 | **Admin Overview Analytics** | `f1d98d1b88e247448b54f772c5212b10` | [`admin_overview_analytics`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/admin_overview_analytics) | `/admin` | [`AdminDashboardPage.jsx`](file:///d:/Projects/AgroScan%20AI/frontend/src/pages/AdminDashboardPage.jsx) |
| 19 | **AgroScan Prototype** | `f758671a3f924b3fa9ef2ba2dd5f7b1c` | [`agroscan_ai_crop_protection_prototype`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/agroscan_ai_crop_protection_prototype) | Prototype | Prototype Reference |
| 20 | **Antigravity IDE Design Brief** | `1538ce5784d24873872bbc5313839fad` | [`antigravity_ide_design_brief`](file:///d:/Projects/AgroScan%20AI/.agents/stitch_agroscan_ai_assistant/antigravity_ide_design_brief) | Docs | System Architecture Spec |

---

## 🛠️ Sync & Re-Fetch Commands

To re-fetch the latest code and screenshots from Stitch MCP at any time, run:
```powershell
python "C:\Users\ompra\.gemini\antigravity-ide\brain\c5d9c783-f229-40c9-a43d-9392633a949b\scratch\download_stitch_screens.py"
```
