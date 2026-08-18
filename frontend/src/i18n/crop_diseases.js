export const CROP_TRANSLATIONS = {
  // English to Marathi
  "Mango": "आंबा",
  "Tomato": "टोमॅटो",
  "Potato": "बटाटा",
  "Sugarcane": "ऊस",
  "Rice": "भात / तांदूळ",
  "Paddy": "भात / धान",
  "Wheat": "गहू",
  "Corn": "मका",
  "Maize": "मका",
  "Corn (Maize)": "मका",
  "Cotton": "कापूस",
  "Chilli": "मिरची",
  "Pepper": "मिरची / शिमला मिरची",
  "Onion": "कांदा",
  "Soybean": "सोयाबीन",
  "Neem": "कडुनिंब",
  "Brinjal": "वांगी",
  "Eggplant": "वांगी",
  "Banana": "केळी",
  "Grapes": "द्राक्षे",
  "Pomegranate": "डाळिंब",
  "Citrus": "लिंबूवर्गीय (लिंबू/संत्री)",
  "Lemon": "लिंबू",
  "Orange": "संत्री",
  "Apple": "सफरचंद",
  "Papaya": "पपई",
  "Guava": "पेरू",
  "Turmeric": "हळद",
  "Ginger": "आले",
  "Garlic": "लसूण",
  "General Crop": "सर्वसाधारण पीक",
  "General Plant": "सर्वसाधारण वनस्पती"
};

export const DISEASE_TRANSLATIONS = {
  "Healthy": "निरोगी पीक (कोणताही रोग नाही)",
  "Healthy Plant": "निरोगी वनस्पती",
  "Healthy Crop": "निरोगी पीक",
  "Late Blight": "करपा (लेट ब्लाईट)",
  "Early Blight": "लवकर येणारा करपा (अल्टरनेरिया)",
  "Powdery Mildew": "भुरी रोग",
  "Downy Mildew": "केवडा रोग",
  "Leaf Spot": "पानांवरील ठिपके रोग",
  "Cercospora Leaf Spot": "सार्कोस्पोरा पानांवरील ठिपके",
  "Septoria Leaf Spot": "सेप्टोरिया पानांवरील ठिपके",
  "Bacterial Blight": "जिवाणूजन्य करपा",
  "Bacterial Spot": "जिवाणूजन्य ठिपके",
  "Anthracnose": "करपा (अँथ्रॅकनोज)",
  "Common Rust": "तांबेरा रोग",
  "Rust": "तांबेरा रोग",
  "Yellow Leaf Virus": "पिवळा पान विषाणू",
  "Mosaic Virus": "मोझॅक विषाणू रोग",
  "Tomato Mosaic Virus": "टोमॅटो मोझॅक विषाणू",
  "Tomato Yellow Leaf Curl Virus": "टोमॅटो पिवळा पर्णगुच्छ विषाणू",
  "Leaf Curl": "पर्णगुच्छ / चुरडा-मुरडा",
  "Wilt": "मर रोग",
  "Fusarium Wilt": "फ्युजारियम मर रोग",
  "Root Rot": "मूळ कुजव्या रोग",
  "Die Back": "शेंडा सुकणे (डाय बॅक)",
  "Black Rot": "काळा कुजव्या",
  "Target Spot": "लक्ष्य ठिपके रोग",
  "Spider Mites": "लाल कोळी कीड",
  "Aphids": "मावा कीड",
  "Whitefly": "पांढरी माशी",
  "General Cultivation & Care": "सर्वसाधारण लागवड व काळजी",
  "Non-Plant Image": "वनस्पती नसलेली प्रतिमा"
};

export const SEVERITY_TRANSLATIONS = {
  "Healthy": "निरोगी",
  "Mild": "सौम्य",
  "Moderate": "मध्यम",
  "Severe": "तीव्र",
  "Critical": "गंभीर",
  "Normal": "सर्वसाधारण",
  "Standard": "प्रमाणित"
};

export const RISK_TRANSLATIONS = {
  "Low": "कमी धोका",
  "Medium": "मध्यम धोका",
  "Moderate": "मध्यम धोका",
  "High": "उच्च धोका",
  "Critical": "गंभीर धोका",
  "Safe": "सुरक्षित",
  "Warning": "इशारा",
  "Danger": "धोकादायक"
};

/**
 * Translates crop name dynamically to Marathi if lang is 'mr', or returns English original.
 */
export const translateCropName = (cropName, lang = 'en') => {
  if (!cropName) return lang === 'mr' ? 'पीक' : 'Crop';
  if (lang !== 'mr') return cropName;
  return CROP_TRANSLATIONS[cropName] || cropName;
};

/**
 * Translates disease name dynamically to Marathi if lang is 'mr', or returns English original.
 */
export const translateDiseaseName = (diseaseName, lang = 'en') => {
  if (!diseaseName) return lang === 'mr' ? 'रोग' : 'Disease';
  if (lang !== 'mr') return diseaseName;
  return DISEASE_TRANSLATIONS[diseaseName] || diseaseName;
};

/**
 * Translates severity level.
 */
export const translateSeverityLevel = (severity, lang = 'en') => {
  if (!severity) return severity || 'Normal';
  if (lang !== 'mr') return severity;
  return SEVERITY_TRANSLATIONS[severity] || severity;
};

/**
 * Translates weather risk level.
 */
export const translateRiskLevel = (risk, lang = 'en') => {
  if (!risk) return risk || 'Low';
  if (lang !== 'mr') return `${risk} Risk`;
  return RISK_TRANSLATIONS[risk] || `${risk} धोका`;
};
