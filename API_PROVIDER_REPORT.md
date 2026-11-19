# AgroScan AI — External Botanical & Disease API Provider Report
**Date:** November 2026  
**System:** AgroScan AI Hybrid Intelligence Engine  
**Subject:** Cloud API Providers Evaluation, Adapters, Limits, and Security  

---

## 1. Provider Adapter Architecture

External botanical and plant disease APIs are integrated as optional, fail-safe cloud adapters behind the abstract base class `DiseaseDetectionProvider` (`backend/app/services/providers/base_provider.py`).

### Standard Interface Contract
Every provider adapter implements:
1. `is_available() -> bool`: Returns `True` only if valid credentials are configured in backend environment variables and `DEMO_MODE` is disabled.
2. `diagnose(image_bytes, plant_name, location, language) -> ProviderDiagnosisResult`: Executes disease diagnosis and returns normalized candidates.
3. `get_health_status() -> ProviderHealthStatus`: Reports latency, failure rate, and operational status without leaking API keys.
4. `get_supported_capabilities() -> Dict[str, Any]`: Returns supported image formats, crops, and diagnostic features.

**Fail-Safe Mandate:** All provider invocations are wrapped in individual `asyncio.wait_for` timeouts (6.0 seconds). If an external API is unconfigured, rate-limited, or fails, the failure is isolated. The engine never crashes and never manufactures synthetic responses.

---

## 2. In-Depth Evaluation of External Providers

### 2.1 Kindwise / Plant.id API

- **Service:** Kindwise Plant.id (FlowerChecker s.r.o.)
- **Endpoints:**
  - Identification: `POST https://api.plant.id/v3/identification`
  - Health & Disease Diagnosis: `POST https://api.plant.id/v2/identify`
- **Authentication:** HTTP Header `Api-Key: <PLANT_ID_API_KEY>`
- **Request Format:** JSON with base64-encoded JPEG image string (`data:image/jpeg;base64,...`), latitude, longitude, and `"health": "all"`.
- **Response Format:**
  - `result.classification.suggestions`: Top plant species with botanical probability.
  - `result.disease.suggestions`: Identified foliar pathogens, symptoms, and biological disease names.
- **Crop & Disease Coverage:** Covers $> 30,000$ plant taxa worldwide and hundreds of foliar diseases.
- **Pricing & Free Tier:**
  - Free trial: Tier with limited monthly credits.
  - Commercial tier: Metered pricing per API identification request.
- **Rate Limits:** Typically 10 requests per minute on basic tiers.
- **Data Retention & Privacy:** Images uploaded may be stored for model improvement unless opt-out enterprise agreements are contracted.
- **Status in AgroScan AI:** Fully implemented in `kindwise_provider.py`. Active when `PLANT_ID_API_KEY` is supplied in backend `.env`.

### 2.2 Google Gemini Multimodal Vision API

- **Service:** Google Cloud Generative Language API
- **Model:** `gemini-3.5-flash` / `gemini-3.5-flash-lite`
- **Authentication:** Query parameter or header with `GEMINI_API_KEY`
- **Request Format:** JSON payload containing base64 inline image bytes and a structured agronomic prompt enforcing strict JSON schema output.
- **Capabilities:**
  - Zero-shot identification of any global or regional Indian crop species (Mango, Sugarcane, Cotton, Rice, Wheat, Soybean, Turmeric, Ginger, etc.).
  - Botanical Latin binomial taxonomy and plant family identification.
  - Multi-candidate alternative differential diagnoses.
- **Rate Limits:** Standard Google AI Studio rate limits (15 RPM on free tier, 360 RPM on pay-as-you-go).
- **Status in AgroScan AI:** Fully implemented in `gemini_vision_provider.py`. Provides zero-shot crop identification for crops not present in local 38-class weights.

### 2.3 Pl@ntNet API

- **Service:** Pl@ntNet Citizen Science Identification Platform (CIRAD / INRIA)
- **Endpoint:** `POST https://my-api.plantnet.org/v2/identify/{project}`
- **Authentication:** Query parameter `api-key=<PLANTNET_API_KEY>`
- **Capabilities:** High-accuracy botanical species taxonomy identification; limited direct pathogen diagnosis.
- **Pricing:** Free tier for academic/research use (500 requests/day).
- **Status in AgroScan AI:** Implemented in `plantnet_provider.py` as an auxiliary botanical validation adapter.

### 2.4 Plantix & Agrio API Integrations

- **Plantix (PEAT GmbH):** Specializes in smallholder crop pathology in South Asia. Requires enterprise partner access.
- **Agrio (Saillog Ltd.):** AI-based precision agricultural pathology engine.
- **Status in AgroScan AI:** Provider adapter skeletons exist in `plantix_provider.py` and `agrio_provider.py`. Skeletons report `NOT_CONFIGURED` gracefully when enterprise API keys are not supplied.

---

## 3. Provider Failover and Error Handling Matrix

| Scenario | Engine Response | User-Facing Result |
|---|---|---|
| **Invalid or Expired API Key** | `ProviderDiagnosisResult(status="not_configured", error="...")` | Local Hugging Face inference runs uninterrupted. Health endpoint shows `NOT_CONFIGURED`. |
| **API Timeout ($> 6.0$ s)** | Timeout caught via `asyncio.TimeoutError`; provider flagged as degraded | Local model prediction delivered within 25 ms. |
| **Rate Limit (HTTP 429)** | Caught and logged without application crash | Local model prediction delivered; zero user disruption. |
| **Cloud Disconnected (Offline)** | Network exception caught; all cloud providers marked offline | 100% of diagnostic inference handled by local MobileNetV2/DINOv2. |
