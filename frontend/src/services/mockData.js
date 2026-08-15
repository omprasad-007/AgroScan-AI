export const MOCK_USER = {
  id: "usr_101",
  email: "farmer@agroscan.ai",
  full_name: "Kisan Ramesh Patil",
  role: "farmer",
  city: "Pune",
  state: "Maharashtra",
  created_at: new Date().toISOString()
};

export const MOCK_ADMIN = {
  id: "usr_admin_01",
  email: "admin@agroscan.ai",
  full_name: "Dr. Agro Admin",
  role: "admin",
  city: "Pune",
  state: "Maharashtra",
  created_at: new Date().toISOString()
};

export const MOCK_FARMS = [
  {
    id: "farm_01",
    name: "Green Valley Organics",
    location: "Pune, Maharashtra",
    crop_types: "Tomato, Potato, Corn",
    area_acres: 3.5,
    created_at: "2026-05-10T10:00:00Z"
  },
  {
    id: "farm_02",
    name: "Patil Farm Estate",
    location: "Solapur, Maharashtra",
    crop_types: "Tomato, Groundnut",
    area_acres: 5.0,
    created_at: "2026-06-15T14:30:00Z"
  }
];

export const MOCK_PREDICTIONS = [
  {
    id: "pred_001",
    crop_detected: "Tomato",
    disease_name: "Tomato Late Blight",
    disease_code: "tomato_late_blight",
    confidence_score: 0.945,
    severity_percentage: 24.5,
    severity_level: "Moderate",
    affected_area_cm2: 12.25,
    ambient_temp_c: 26.5,
    humidity_pct: 82.0,
    rainfall_mm: 5.0,
    weather_risk_score: 82.5,
    weather_risk_level: "High",
    is_demo: true,
    created_at: new Date(Date.now() - 3600000 * 2).toISOString(),
    image_url: "https://images.unsplash.com/photo-1592417817098-8f3d6eb16431?w=600&q=80"
  },
  {
    id: "pred_002",
    crop_detected: "Potato",
    disease_name: "Potato Late Blight",
    disease_code: "potato_late_blight",
    confidence_score: 0.912,
    severity_percentage: 14.0,
    severity_level: "Mild",
    affected_area_cm2: 7.0,
    ambient_temp_c: 24.0,
    humidity_pct: 78.0,
    rainfall_mm: 2.0,
    weather_risk_score: 65.0,
    weather_risk_level: "Medium",
    is_demo: true,
    created_at: new Date(Date.now() - 3600000 * 24).toISOString(),
    image_url: "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=600&q=80"
  },
  {
    id: "pred_003",
    crop_detected: "Corn (Maize)",
    disease_name: "Corn Common Rust",
    disease_code: "corn_common_rust",
    confidence_score: 0.885,
    severity_percentage: 8.2,
    severity_level: "Mild",
    affected_area_cm2: 4.1,
    ambient_temp_c: 22.0,
    humidity_pct: 65.0,
    rainfall_mm: 0.0,
    weather_risk_score: 35.0,
    weather_risk_level: "Low",
    is_demo: true,
    created_at: new Date(Date.now() - 3600000 * 48).toISOString(),
    image_url: "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=600&q=80"
  },
  {
    id: "pred_004",
    crop_detected: "General Crop",
    disease_name: "Healthy Leaf (No Disease Detected)",
    disease_code: "healthy_leaf",
    confidence_score: 0.985,
    severity_percentage: 0.0,
    severity_level: "Healthy",
    affected_area_cm2: 0.0,
    ambient_temp_c: 25.0,
    humidity_pct: 60.0,
    rainfall_mm: 0.0,
    weather_risk_score: 15.0,
    weather_risk_level: "Low",
    is_demo: true,
    created_at: new Date(Date.now() - 3600000 * 72).toISOString(),
    image_url: "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=600&q=80"
  }
];

export const MOCK_RECOMMENDATIONS = {
  tomato_late_blight: {
    disease_name: "Tomato Late Blight",
    crop: "Tomato",
    symptoms: "Dark water-soaked spots on leaf tips and stems rapidly enlarging into brown lesions with pale green halos. White mold visible on undersides in high humidity.",
    organic_treatment: "Apply copper octanoate (copper soap) or neem oil sprays every 7-10 days. Remove and destroy infected leaves immediately. Improve airflow around plants.",
    chemical_treatment: "Spray systemic fungicides containing Chlorothalonil, Mancozeb, or Cymoxanil at first sign of infection. Follow product label instructions strictly.",
    prevention: "Use certified disease-free seeds. Avoid overhead irrigation. Practice 3-year crop rotation with non-solanaceous crops.",
    general_guidance: "Late Blight spreads rapidly in warm, humid conditions. Inspect leaf undersides daily during rainy periods.",
    disclaimer: "Decision-support guidance only. Follow locally approved product labels and agricultural extension guidelines."
  },
  potato_late_blight: {
    disease_name: "Potato Late Blight",
    crop: "Potato",
    symptoms: "Irregular dark brown leaf spots with white fungal growth on undersides. Tuber rot turns flesh reddish-brown.",
    organic_treatment: "Apply Bordeaux mixture (1%) or copper oxychloride before wet weather sets in. Hill up soil around potato plants to protect tubers.",
    chemical_treatment: "Apply Metalaxyl + Mancozeb or Dimethomorph sprays. Rotate active ingredients to avoid fungal resistance.",
    prevention: "Plant resistant varieties like Kufri Girdhari. Destroy volunteer potato plants and crop residues after harvest.",
    general_guidance: "Monitor field after fog or rains. Protect tubers during harvesting.",
    disclaimer: "Decision-support guidance only. Follow locally approved product labels and agricultural extension guidelines."
  },
  corn_common_rust: {
    disease_name: "Corn Common Rust",
    crop: "Corn (Maize)",
    symptoms: "Small, oval, golden-brown to cinnamon-brown powdery pustules on upper and lower leaf surfaces.",
    organic_treatment: "Spray sulfur-based organic fungicides. Maintain balanced soil fertility avoiding excessive nitrogen application.",
    chemical_treatment: "Spray Tebuconazole or Propiconazole at 15-day intervals if rust covers >5% leaf area prior to flowering.",
    prevention: "Plant rust-resistant maize hybrids. Rotate with legumes like soybean or groundnut.",
    general_guidance: "Favored by cool temperatures (16-23°C) and high dew duration.",
    disclaimer: "Decision-support guidance only. Follow locally approved product labels and agricultural extension guidelines."
  },
  healthy_leaf: {
    disease_name: "Healthy Leaf (No Disease Detected)",
    crop: "General Crop",
    symptoms: "Vibrant green foliage with smooth uniform leaf surface. No lesions, discoloration, or fungal pustules detected.",
    organic_treatment: "Maintain regular watering schedule and organic compost application. Continue weekly monitoring.",
    chemical_treatment: "No chemical treatment required. Avoid unnecessary pesticide application to preserve beneficial insects.",
    prevention: "Maintain soil health, crop rotation, balanced NPK fertilization, and proper field drainage.",
    general_guidance: "Crop is healthy. Keep recording routine observations.",
    disclaimer: "Decision-support guidance only. Follow locally approved product labels and agricultural extension guidelines."
  }
};

export const MOCK_DASHBOARD_ANALYTICS = {
  total_predictions: 50,
  healthy_count: 26,
  diseased_count: 24,
  average_confidence: 0.932,
  top_diseases: [
    { name: "Tomato Late Blight", crop: "Tomato", percentage: 38.0 },
    { name: "Potato Late Blight", crop: "Potato", percentage: 24.0 },
    { name: "Corn Common Rust", crop: "Corn", percentage: 18.0 }
  ],
  disease_distribution: [
    { name: "Tomato Late Blight", count: 19 },
    { name: "Potato Late Blight", count: 12 },
    { name: "Corn Common Rust", count: 9 },
    { name: "Healthy Leaf", count: 10 }
  ],
  severity_distribution: [
    { name: "Healthy (<5%)", value: 10 },
    { name: "Mild (5-15%)", value: 18 },
    { name: "Moderate (15-35%)", value: 15 },
    { name: "Severe (>35%)", value: 7 }
  ],
  monthly_trends: [
    { month: "Mar", scans: 12, healthy: 8, diseased: 4, avg_severity: 8.5 },
    { month: "Apr", scans: 18, healthy: 11, diseased: 7, avg_severity: 12.0 },
    { month: "May", scans: 25, healthy: 14, diseased: 11, avg_severity: 14.5 },
    { month: "Jun", scans: 34, healthy: 18, diseased: 16, avg_severity: 18.2 },
    { month: "Jul", scans: 42, healthy: 22, diseased: 20, avg_severity: 21.0 },
    { month: "Aug", scans: 50, healthy: 26, diseased: 24, avg_severity: 16.4 }
  ],
  weather_risk_summary: {
    overall_risk_level: "High",
    current_temp: 26.5,
    current_humidity: 82.0,
    alert: "High relative humidity and warm temperatures promote late blight spore germination."
  }
};
