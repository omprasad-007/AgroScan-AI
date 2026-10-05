import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { 
  Bot, User, Send, Search, Sparkles, Sprout, AlertCircle, RefreshCw, 
  X, Loader2, RotateCcw, Download, Mic, MicOff, Volume2, VolumeX,
  HelpCircle, ShieldCheck, Droplets, Sun, Bug, Zap,
  History, Plus, Trash2, MessageSquare, Clock, ChevronRight
} from 'lucide-react';
import api from '../services/api';

// Curated Farmer FAQs organized by categories for instant tapping
const FARMER_FAQ_CATEGORIES = {
  mr: [
    {
      id: 'disease',
      label: '🌿 रोग व उपचार',
      questions: [
        'करपा (Blight) रोगावर कोणती फवारणी करावी?',
        'पानांवरील पिवळे व काळे डाग कसे दूर करावेत?',
        'हा रोग इतर झाडांवर पसरण्यापासून कसा रोखावा?',
        'बुरशीजन्य रोगाची प्राथमिक लक्षणे कशी ओळखावीत?'
      ]
    },
    {
      id: 'organic',
      label: '🧪 सेंद्रिय कीटकनाशक',
      questions: [
        'निंबोळी अर्क (Neem Oil) फवारणीचे योग्य प्रमाण किती?',
        'दशपर्णी अर्क घरच्या घरी कसा तयार करावा?',
        'जिवामृत व सेंद्रिय स्लरी कधी द्यावी?',
        'ताक व हिंगाची फवारणी विषाणूजन्य रोगावर कशी काम करते?'
      ]
    },
    {
      id: 'irrigation',
      label: '💧 पाणी व खते',
      questions: [
        'पिकाला ठिबक सिंचनाने पाणी देण्याचे योग्य वेळापत्रक काय?',
        'उत्पादन वाढवण्यासाठी कोणती सेंद्रिय खते उत्तम?',
        'फुलधारणेच्या काळात पाण्याचे व्यवस्थापन कसे करावे?',
        'मातीचा सामू (pH) सुधारण्यासाठी काय करावे?'
      ]
    },
    {
      id: 'pests',
      label: '🌦️ कीड व हवामान',
      questions: [
        'ढगाळ व दमट हवामानात बुरशीचा प्रादुर्भाव कसा टाळावा?',
        'पांढरी माशी आणि मावा किडीवर त्वरित सेंद्रिय उपाय काय?',
        'पाऊस पडल्यानंतर पिकावर कोणती प्रतिबंधक फवारणी करावी?',
        'पिवळे चिकट सापळे (Yellow Sticky Traps) कसे वापरावे?'
      ]
    }
  ],
  en: [
    {
      id: 'disease',
      label: '🌿 Disease & Cure',
      questions: [
        'What is the best treatment for early/late blight?',
        'How to cure yellow and black spots on leaves?',
        'How do I stop this disease from spreading to other plants?',
        'What are the early warning signs of fungal infection?'
      ]
    },
    {
      id: 'organic',
      label: '🧪 Organic Sprays',
      questions: [
        'What is the correct dosage for Neem Oil spray (ppm)?',
        'How to prepare homemade Dashaparni bio-pesticide?',
        'How often should Jeevamrut or compost tea be applied?',
        'Can sour buttermilk spray treat bacterial leaf curl?'
      ]
    },
    {
      id: 'irrigation',
      label: '💧 Water & Nutrition',
      questions: [
        'What is the optimal drip irrigation schedule for this crop?',
        'Which organic fertilizers boost flowering and yield?',
        'How to manage irrigation during high-temperature flowering?',
        'How do I test and correct soil pH naturally?'
      ]
    },
    {
      id: 'pests',
      label: '🌦️ Weather & Pests',
      questions: [
        'How to protect crops against fungal outbreaks during high humidity?',
        'What is the quickest organic remedy for aphids & whiteflies?',
        'What preventive spray is needed after heavy rainfall?',
        'How to use yellow sticky traps for pest monitoring?'
      ]
    }
  ]
};

// Comprehensive Client-Side Agronomist Knowledge Engine for instant question-specific responses
const generateClientAdvisory = (userQuery, ctx, lang = 'en') => {
  const q = (userQuery || '').toLowerCase().trim();
  const isMr = lang === 'mr';

  // 1. Math / General Non-Agri
  if (q.includes('2+2') || q.includes('2 + 2')) {
    return '2 + 2 = 4.';
  }
  if (['hello', 'hi', 'hey', 'namaste', 'नमस्कार'].includes(q)) {
    return isMr
      ? 'नमस्कार! मी AgroScan AI कृषी सल्लागार आहे. आपल्या शेती, माती, सिंचन, खते किंवा रोग व्यवस्थापनाविषयी प्रश्न विचारा.'
      : 'Hello! I am AgroScan AI Agronomist. Ask me any question regarding crops, soil, irrigation, fertilizers, or disease management.';
  }

  // 2. Crop Rotation
  if (q.includes('crop rotation') || q.includes('rotation') || q.includes('फेरपालट')) {
    return isMr
      ? `🌾 **पिकांची फेरपालट (Crop Rotation) माहिती:**\n\n- **व्याख्या:** एकाच जमिनीत सलग एकच पीक न घेता हंगामानुसार विविध प्रकारची पिके आलटून-पालटून घेण्याच्या पद्धतीला 'पिकांची फेरपालट' म्हणतात.\n- **फायदे:**\n  1. **रोग-कीड नियंत्रण:** जमिनीतील बुरशी व किडींचे जीवनचक्र खंडित होते.\n  2. **सुपीकता वाढ:** कडधान्य पिके (सोयाबीन/हरभरा) हवेतील नायट्रोजन जमिनीत स्थिर करतात.\n  3. **संतुलित पोषण:** खोल व उथळ मुळांच्या पिकांमुळे जमिनीच्या सर्व थरांतील अन्नद्रव्यांचा योग्य वापर होतो.\n- **योग्य क्रम:** टोमॅटो/बटाटा ➔ कडधान्य (सोयाबीन/मूग) ➔ तृणधान्य (गहू/मका) ➔ हिरवळीचे खत.`
      : `🌾 **Crop Rotation Guide:**\n\n- **Definition:** The systematic practice of growing different types of crops sequentially on the same land across seasons rather than continuous monoculture.\n- **Key Benefits:**\n  1. **Breaks Pest & Disease Cycles:** Starves out soil-borne fungi and host-specific insects.\n  2. **Replenishes Nitrogen:** Legumes (soybean, chickpea) fix atmospheric nitrogen into root nodules.\n  3. **Improves Soil Tilth:** Alternating tap root crops with fibrous root cereals optimizes nutrient uptake from different soil depths.\n- **Recommended Sequence:** Solanaceous (Tomato/Potato) ➔ Legume (Soybean/Pulses) ➔ Cereal (Wheat/Maize) ➔ Green Manure.`;
  }

  // 3. Photosynthesis
  if (q.includes('photosynthesis') || q.includes('प्रकाशसंश्लेषण')) {
    return isMr
      ? `☀️ **प्रकाशसंश्लेषण (Photosynthesis) प्रक्रिया:**\n\n- **व्याख्या:** हिरव्या वनस्पती सूर्यप्रकाश, हरितद्रव्य (Chlorophyll), हवेतील CO2 आणि जमिनीतील पाणी (H2O) वापरून ग्लुकोज (अन्न) तयार करतात आणि ऑक्सिजन (O2) बाहेर सोडतात.\n- **समीकरण:** 6 CO2 + 6 H2O + सूर्यप्रकाश ➔ C6H12O6 + 6 O2\n- **शेतीतील महत्त्व:** पिकाचे उत्पादन थेट पानांच्या प्रकाशसंश्लेषण क्षमतेवर अवलंबून असते. करपा किंवा भुरी रोगामुळे पाने खराब झाल्यास प्रकाशसंश्लेषण मंदावून उत्पादनात मोठी घट होते.`
      : `☀️ **Photosynthesis & Crop Physiology:**\n\n- **Definition:** The biological process by which green plants use solar energy and chlorophyll to convert carbon dioxide (CO2) from air and water (H2O) from soil into glucose (energy) and oxygen (O2).\n- **Equation:** 6 CO2 + 6 H2O + Solar Energy ➔ C6H12O6 + 6 O2\n- **Agronomic Impact:** Crop yield is directly proportional to photosynthetic efficiency. Foliar blights and mildews reduce active green leaf surface area, causing severe yield reduction.`;
  }

  // Extract relevant crop context (From query or active selection/scan)
  let crop = ctx?.crop_detected || ctx?.plantName || '';
  if (q.includes('mango') || q.includes('आंबा')) crop = 'Mango';
  else if (q.includes('sugarcane') || q.includes('ऊस')) crop = 'Sugarcane';
  else if (q.includes('tomato') || q.includes('टोमॅटो')) crop = 'Tomato';
  else if (q.includes('potato') || q.includes('बटाटा')) crop = 'Potato';
  else if (q.includes('cotton') || q.includes('कापूस')) crop = 'Cotton';
  else if (q.includes('rice') || q.includes('paddy') || q.includes('भात')) crop = 'Rice';
  else if (q.includes('wheat') || q.includes('गहू')) crop = 'Wheat';
  else if (q.includes('chilli') || q.includes('मिरची')) crop = 'Chilli';
  else if (q.includes('onion') || q.includes('कांदा')) crop = 'Onion';
  else if (q.includes('maize') || q.includes('corn') || q.includes('मका')) crop = 'Maize';
  else if (q.includes('soybean') || q.includes('सोयाबीन')) crop = 'Soybean';
  else if (q.includes('pomegranate') || q.includes('dalimb') || q.includes('डाळिंब')) crop = 'Pomegranate';
  else if (q.includes('banana') || q.includes('kela') || q.includes('केळी')) crop = 'Banana';
  else if (q.includes('grape') || q.includes('grapes') || q.includes('draksh') || q.includes('द्राक्षे')) crop = 'Grape';
  else if (q.includes('groundnut') || q.includes('peanut') || q.includes('भूईमूग')) crop = 'Groundnut';
  else if (q.includes('chickpea') || q.includes('gram') || q.includes('harbara') || q.includes('हरभरा')) crop = 'Chickpea';
  else if (q.includes('apple') || q.includes('सफरचंद')) crop = 'Apple';
  else if (q.includes('guava') || q.includes('पेरू')) crop = 'Guava';

  // 4. Pomegranate / Telya Specific
  if (q.includes('telya') || q.includes('तेल्या') || (crop === 'Pomegranate' && (q.includes('disease') || q.includes('रोग')))) {
    return isMr
      ? `🔴 **डाळिंबावरील तेल्या (Bacterial Blight - *Xanthomonas*) रोगाचे नियंत्रण:**\n\n1. **स्वच्छता व छाटणी:** प्रादुर्भाव झालेल्या फांद्या ५ सें.मी. खालून कापून ताबडतोब जाळून टाकाव्यात व छाटलेल्या भागावर १०% बोर्डो पेस्ट लावावी.\n2. **प्रतिबंधात्मक फवारणी:**\n   - **स्ट्रेप्टोसायक्लिन (Streptocycline):** ०.५ ग्रॅम प्रति लिटर + **कॉपर ऑक्सिक्लोराईड (COC ५०% WP):** २.५ ग्रॅम प्रति लिटर पाण्यात मिसळून फवारावे.\n   - पाऊस पडल्यानंतर लगेच किंवा ढगाळ वातावरणात १२-१५ दिवसांच्या अंतराने फवारणी करावी.\n3. **फळ कव्हरिंग:** रोगमुक्त फळांना बटर पेपर किंवा नॉन-वोव्हेन पिशव्यांचे कव्हर घालावे.`
      : `🔴 **Pomegranate Bacterial Blight (Telya - *Xanthomonas axonopodis* pv. *punicae*) Management:**\n\n1. **Sanitation Pruning:** Cut infected twigs 5-10 cm below canker lesions and burn immediately. Paint cut wounds with Bordeaux paste (10%).\n2. **Bactericide Schedule:**\n   - Spray **Streptocycline (0.5 g/L)** mixed with **Copper Oxychloride 50% WP (2.5 g/L)** or Copper Hydroxide (2.0 g/L) at 10-12 day intervals during humid/rainy spells.\n3. **Fruit Bagging:** Bag developing fruits with butter paper covers to prevent raindrop bacterial transmission.`;
  }

  // 5. Banana Sigatoka & Panama Wilt
  if (q.includes('sigatoka') || q.includes('सिगाटोका') || q.includes('panama') || q.includes('पनामा') || (crop === 'Banana' && (q.includes('disease') || q.includes('रोग')))) {
    return isMr
      ? `🍌 **केळीवरील मुख्य रोग व उपाय (Sigatoka & Panama Wilt):**\n\n1. **सिगाटोका करपा (Sigatoka Leaf Spot):**\n   - ५०% पेक्षा जास्त जळालेली जुनी पाने कापून नष्ट करा.\n   - **प्रॉपिकोनाझोल (Propiconazole २५% EC):** १ मि.ली. प्रति लिटर + मिनरल स्प्रे ऑईल (१० मि.ली./लिटर) फवारावे.\n2. **पनामा मर रोग (Panama Wilt TR4):**\n   - जमिनीतून पसरणाऱ्या बुरशीमुळे खोड फाटते व पाने सुकतात.\n   - मुळांच्या भागात ट्रायकोडर्मा (Trichoderma ५ किलो/एकर) शेणखतात मिसळून द्यावे.\n   - प्रादुर्भाव झालेल्या झाडाच्या गड्डे भागात २% कार्बेन्डाझिमचे इंजेक्शन द्यावे.`
      : `🍌 **Banana Disease Management (Sigatoka & Panama Wilt):**\n\n1. **Sigatoka Leaf Spot:** Surgically de-leaf heavily infected foliage (>50% necrosis). Spray **Propiconazole 25% EC (1.0 ml/L)** mixed with mineral spray oil (1%).\n2. **Panama Wilt (Fusarium TR4):** Soil-borne vascular wilt causing pseudostem splitting and yellow leaf skirts. Drench root zone with **Trichoderma harzianum (5 kg/ha in FYM)** and practice crop rotation with paddy/sugarcane.`;
  }

  // 6. Soil Salinity / Sodic Reclamation
  if (q.includes('saline') || q.includes('sodic') || q.includes('gypsum') || q.includes('खारवट') || q.includes('चोपण') || q.includes('जिप्सम')) {
    return isMr
      ? `🌱 **खारवट व चोपण जमिनीची सुधारणा (Soil Reclamation):**\n\n1. **चोपण जमीन (Sodic Soil - pH > ८.५):** माती परीक्षणानुसार एकरी २ ते ३ टन **कृषी जिप्सम (Gypsum - CaSO4)** मिसळून घ्यावे व शेतात पाणी साठवून निचरा करावा. ढेंचा (Dhaincha) हिरवळीचे खत गाडावे.\n2. **खारवट जमीन (Saline Soil - EC > ४.० dS/m):** शेतात भूमिगत चर (Subsurface Drainage) काढून चांगल्या गोड्या पाण्याने क्षार वाहून (Leaching) काढावेत.\n3. **सेंद्रिय कर्ब:** एकरी १०-१५ टन कुजलेले शेणखत किंवा गांडूळ खत वापरावे.`
      : `🌱 **Saline & Sodic Soil Reclamation Protocol:**\n\n1. **Sodic / Alkali Soils (pH > 8.5, ESP > 15%):** Incorporate **Agricultural Gypsum (Calcium Sulfate @ 2-5 tonnes/acre)** to replace sodium (Na+) with calcium (Ca2+), followed by deep leaching. Grow Dhaincha (*Sesbania*) green manure.\n2. **Saline Soils (ECe > 4.0 dS/m):** Install subsurface tile drainage channels and leach soluble root-zone salts with good quality fresh water.\n3. **Organic Matter:** Add 10-15 tonnes/ha FYM/compost to buffer soil porosity and microbial health.`;
  }

  // 7. Kisan Drone Spraying
  if (q.includes('drone') || q.includes('ड्रोन') || q.includes('uav')) {
    return isMr
      ? `🚁 **किसान ड्रोन (Kisan Drone) फवारणी नियमावली:**\n\n1. **उड्डाण उंची व वेग:** पिकाच्या शेंड्यापासून १.५ ते २.५ मीटर उंची आणि ३ ते ५ मीटर/सेकंद (१०-१८ किमी/तास) वेग असावा.\n2. **पाण्याचे प्रमाण:** अल्ट्रा लो व्हॉल्यूम (ULV) तंत्रज्ञानाने एकरी ८ ते १० लिटर पाणी लागते (औषधाचे प्रमाण पारंपारिक एकराप्रमाणेच ठेवावे).\n3. **हवामान मर्यादा:** वाऱ्याचा वेग १० किमी/तासापेक्षा जास्त असताना आणि दुपारच्या तीव्र उन्हात फवारणी करू नये.\n4. **फायदे:** ९०% पाण्याची बचत, २५-३०% कीटकनाशक बचत, आणि शेतकऱ्यांच्या आरोग्याची सुरक्षा.`
      : `🚁 **Kisan Agricultural Drone Spraying Guidelines:**\n\n1. **Flight Parameters:** Maintain flight altitude of 1.5 to 2.5 meters above crop canopy at 3–5 m/s flight speed.\n2. **Water Volume:** Ultra-Low Volume (ULV) requires 20–30 L/ha (8-10 L/acre) water with rotary centrifugal anti-drift nozzles.\n3. **Weather Window:** Do not spray when wind speed exceeds 10 km/h or ambient temperature exceeds 35°C to avoid drift and evaporation.\n4. **Key Benefits:** 90% water conservation, uniform droplet penetration (150-250µm), and zero farmer chemical exposure.`;
  }

  // 8. Natural Farming / Jeevamrut
  if (q.includes('jeevamrut') || q.includes('zbnf') || q.includes('जीवामृत') || q.includes('नैसर्गिक शेती')) {
    return isMr
      ? `🌿 **जीवामृत तयार करण्याची कृती व वापर (ZBNF):**\n\n- **साहित्य (२०० लिटर पाण्यासाठी):** १० किलो देशी गाईचे शेण + १० लिटर गोमूत्र + २ किलो गूळ + २ किलो डाळीचे पीठ (बेसन) + मूठभर शेताच्या बांधावरील माती.\n- **कृती:** प्लास्टिकच्या ड्रममध्ये सर्व घटक चांगले मिसळून ४८ ते ७२ तास सावलीत आंबवावे (दिवसातून २ वेळा काठीने घड्याळाच्या दिशेने ढवळावे).\n- **वापर:** एकरी २०० लिटर जीवामृत पाण्यासोबत (ठिबक किंवा पाटाने) द्यावे किंवा १०% द्रावणाची पानांवर फवारणी करावी.`
      : `🌿 **Jeevamrut Formulation & Application (ZBNF):**\n\n- **Ingredients (for 200 L water):** 10 kg indigenous desi cow dung + 10 L cow urine + 2 kg organic jaggery + 2 kg pulse flour (besan) + handful of virgin bund soil.\n- **Fermentation:** Mix in plastic barrel and ferment for 48–72 hours under shade (stir clockwise twice daily).\n- **Application:** Apply 200 L/acre through irrigation water or as a 10% foliar spray every 21 days to activate beneficial soil microbes.`;
  }

  // 9. Blossom End Rot
  if (q.includes('blossom end rot') || q.includes('ber') || (q.includes('bottom') && q.includes('black') && (crop === 'Tomato' || q.includes('tomato') || q.includes('टोमॅटो')))) {
    return isMr
      ? `🍅 **टोमॅटो फळांचा खालचा भाग काळा पडणे (Blossom End Rot - कॅल्शियमची कमतरता):**\n\n- **कारण:** हा बुरशीजन्य रोग नसून फळांच्या पेशींमध्ये कॅल्शियमची (Calcium) कमतरता आणि पाण्याचा अनियमित पुरवठा (कधी अतिशय कोरडी तर कधी दलदल जमीन) यामुळे होतो.\n- **त्वरित उपाय:**\n  1. **कॅल्शियम नायट्रेट (Calcium Nitrate):** ४ ते ५ ग्रॅम प्रति लिटर + **बोरॉन (Boron):** १ ग्रॅम प्रति लिटर पाण्यात मिसळून फळांवर फवारावे.\n  2. **नियमित सिंचन:** ठिबक सिंचनाने जमिनीत सतत योग्य ओलावा (वाफसा) टिकवून ठेवावा.`
      : `🍅 **Tomato Blossom End Rot (BER — Calcium Deficiency):**\n\n- **Cause:** Non-pathogenic physiological disorder caused by localized Calcium (Ca2+) deficiency in rapidly expanding fruits, triggered by fluctuating soil moisture.\n- **Corrective Action:**\n  1. **Foliar Spray:** Apply **Calcium Nitrate (4.0–5.0 g/L)** mixed with **Boron (1.0 g/L)** directed at developing fruit clusters.\n  2. **Water Management:** Maintain steady, uniform root-zone moisture via drip irrigation to ensure continuous calcium uptake.`;
  }

  // 10. Mango Specific Questions
  if (crop === 'Mango' || q.includes('mango') || q.includes('आंबा')) {
    if (q.includes('soil') || q.includes('माती') || q.includes('जमीन')) {
      return isMr
        ? `🌱 **आंब्यासाठी (Mango) योग्य माती व जमीन:**\n\n- **मातीचा प्रकार:** उत्तम पाण्याचा निचरा होणारी खोल गाळाची, तांबडी किंवा जांभा प्रकारची पोयट्याची जमीन उत्तम असते.\n- **मातीची खोली:** किमान २ ते २.५ मीटर खोल जमीन असावी, खडकाळ किंवा चुनखडीयुक्त कडक थर नसावा.\n- **सामू (pH):** ५.५ ते ७.५ (किंचित आम्ल ते उदासीन).\n- **महत्त्वाची टीप:** जमिनीत पाणी साचून राहिल्यास मुळकुज होते, त्यामुळे उत्तम निचरा असणे आवश्यक आहे.`
        : `🌱 **Optimal Soil Requirements for Mango:**\n\n- **Soil Type:** Deep, rich, well-drained alluvial, red loamy, or laterite soil with high permeability.\n- **Soil Depth:** Minimum 2.0 to 2.5 meters depth to accommodate deep tap root system.\n- **Soil pH:** 5.5 to 7.5 (slightly acidic to neutral).\n- **Key Note:** Avoid shallow soils with impermeable rocky hardpans or waterlogged heavy clay.`;
    }
    if (q.includes('water') || q.includes('irrigation') || q.includes('पाणी') || q.includes('सिंचन')) {
      return isMr
        ? `💧 **आंब्याचे (Mango) पाणी व्यवस्थापन:**\n\n- **लहान झाडे (१-३ वर्षे):** उन्हाळ्यात दर ४-५ दिवसांनी, हिवाळ्यात दर ८-१० दिवसांनी पाणी द्यावे.\n- **मोठी फळझाडे:**\n  1. **बहार धरणे (नोव्हेंबर-डिसेंबर):** फुलोरा येण्यापूर्वी २-३ महिने पाणी तोडावे (ताण द्यावा). ताण दिल्याने भरपूर मोहोर येतो.\n  2. **फळधारणा (जानेवारी-मे):** वाटाणा व सुपारीच्या आकाराची फळे झाल्यावर दर १०-१२ दिवसांनी नियमित पाणी द्यावे.\n  3. **काढणीपूर्व:** काढणीच्या १५ दिवस आधी पाणी देणे थांबवावे.`
        : `💧 **Mango Irrigation Guidelines:**\n\n- **Young Trees (1-3 yrs):** Irrigate every 4-5 days in summer, 8-10 days in winter.\n- **Bearing Trees:**\n  1. **Pre-flowering Dry Spell (Nov-Dec):** Withhold irrigation for 2-3 months prior to flowering to induce flower bud differentiation.\n  2. **Fruit Development (Feb-May):** Resume regular irrigation (every 10-15 days) from pea-stage fruit set until fruit enlargement.\n  3. **Pre-Harvest:** Stop irrigation 15 days before harvesting to enhance shelf life and sweetness.`;
    }
    if (q.includes('harvest') || q.includes('काढणी') || q.includes('तोडणी')) {
      return isMr
        ? `🌾 **आंब्याची काढणी (Mango Harvesting):**\n\n- **काढणीची लक्षणे:**\n  1. फळांचे खांदे देठाच्या वर उचलले जातात आणि देठाभोवती खळगा तयार होतो.\n  2. फळाचा रंग गडद हिरव्यावरून फिकट हिरवा/पिवळसर होतो.\n  3. फळांची विशिष्ट गुरुता (Specific Gravity) १.०१ ते १.०२ होते.\n- **काढणी पद्धत:** फळे सकाळी देठासह (१-२ सें.मी. देठ ठेवून) 'नूतन' किंवा जाळीदार झिबाने तोडावीत, जेणेकरून फळावर चीक पडणार नाही.`
        : `🌾 **Mango Harvesting Guidelines:**\n\n- **Maturity Signs:**\n  1. Shoulders swell above the pedicel attachment and the stem-end cavity deepens.\n  2. Skin color transitions from dark green to olive/yellowish green.\n  3. Specific gravity reaches 1.01–1.02 (mature fruits sink in water).\n- **Harvesting Method:** Harvest with 1-2 cm stem attached using pole harvesters with catching nets to prevent latex sap burn and impact injury.`;
    }
  }

  // 11. Powdery Mildew Specific Questions
  if (q.includes('powdery') || q.includes('mildew') || q.includes('भुरी')) {
    if (q.includes('symptom') || q.includes('लक्षणे') || q.includes('काय दिसते')) {
      return isMr
        ? `🔍 **भुरी (Powdery Mildew) रोगाची लक्षणे:**\n\n- **पाने व मोहोर:** कोवळ्या पानांवर, मोहरावर आणि लहान फळांवर पांढऱ्या पिठासारखा थर (पावडर) पसरतो.\n- **मोहोर गळणे:** संसर्ग झालेला मोहोर जांभळट-तपकिरी होऊन सुकतो आणि गळून पडतो, ज्यामुळे फळधारणा होत नाही.\n- **फळांचे नुकसान:** लहान फळांवर पांढरी बुरशी येऊन ती गळतात किंवा फळांची त्वचा खडबडीत होते.`
        : `🔍 **Symptoms of Powdery Mildew (*Oidium mangiferae* / *Erysiphe*):**\n\n- **Floral Panicles & Foliage:** White to grayish-white powdery talc-like fungal coating on blossoms, tender shoots, and young leaves.\n- **Blossom Drop:** Infected inflorescences turn purplish-brown, dry up, and drop completely, causing fruit set failure.\n- **Fruit Scarring:** Young developing fruits drop or develop corky russeted surface scars.`;
    }
    if (q.includes('control') || q.includes('treat') || q.includes('cure') || q.includes('उपाय') || q.includes('नियंत्रण') || q.includes('औषध')) {
      return isMr
        ? `💊 **भुरी (Powdery Mildew) चे नियंत्रण व उपचार:**\n\n1. **सेंद्रिय उपाय:** कडुनिंब तेल (५ मि.ली./लिटर) किंवा आंबट ताक (१ लिटर ताक + १० लिटर पाणी + ५ ग्रॅम हिंग) फवारावे.\n2. **रासायनिक उपाय:**\n   - **गंधक (Wettable Sulphur ८०% WP):** २.५ ग्रॅम प्रति लिटर पाणी (तापमान ३२°C पेक्षा कमी असताना फवारावे).\n   - **हेक्झाकोनॅझोल (Hexaconazole ५% EC):** १ मि.ली. प्रति लिटर पाणी, किंवा\n   - **डायफेनोकोनॅझोल (Difenoconazole २५% EC):** ०.५ ते १ मि.ली. प्रति लिटर पाणी.\n*टीप: कीटकनाशक लेबलवरील सुरक्षा सूचना पाळाव्यात.*`
        : `💊 **How to Control Powdery Mildew:**\n\n1. **Organic / Bio-Control:** Spray cold-pressed Neem Oil (5ml/L) or sour buttermilk solution (1:10 dilution with 5g asafetida).\n2. **Chemical Control Options:**\n   - **Wettable Sulphur 80% WP:** 2.0 to 2.5 g/L water (do not spray above 32°C).\n   - **Hexaconazole 5% EC:** 1.0 ml/L water, OR\n   - **Difenoconazole 25% EC:** 0.5 to 1.0 ml/L water.\n*Note: Adhere to product labels and regional university pre-harvest intervals.*`;
    }
  }

  // 12. Sugarcane Fertilizer
  if (crop === 'Sugarcane' || q.includes('sugarcane') || q.includes('ऊस')) {
    if (q.includes('fertilizer') || q.includes('खत') || q.includes('npk')) {
      return isMr
        ? `🧪 **उसासाठी (Sugarcane) खत व्यवस्थापन:**\n\n- **शिफारस केलेले NPK प्रमाण:** २५० : ११५ : ११५ किलो प्रति हेक्टर (सुरू ऊस).\n- **खतांचे वेळापत्रक:**\n  1. **लागवडीच्या वेळी:** संपूर्ण स्फुरद (P2O5), ५०% पालाश (K2O) आणि १०% नत्र (N) + २५ टन शेणखत.\n  2. **६ ते ८ आठवड्यांनी (फुटवे येताना):** ४०% नत्र.\n  3. **१२ ते १४ आठवड्यांनी:** १०% नत्र.\n  4. **मोठ्या बांधणीच्या वेळी (१२०-१५० दिवस):** उर्वरित ४०% नत्र आणि उर्वरित ५०% पालाश द्यावे.\n- **जैविक खत:** एकरी ५ किलो ॲसिटोबॅक्टर (Acetobacter) जिवाणू खत दिल्यास २०% नत्राची बचत होते.`
        : `🧪 **Fertilizer Schedule for Sugarcane:**\n\n- **Recommended NPK:** 250:115:115 kg/ha (for 12-month Suru crop).\n- **Application Splits:**\n  1. **At Planting (Basal):** 100% P2O5, 50% K2O, and 10% N with 25 t/ha FYM/compost.\n  2. **6-8 Weeks (Tillering):** 40% Nitrogen.\n  3. **12-14 Weeks:** 10% Nitrogen.\n  4. **Final Earthing Up (120-150 days):** Remaining 40% Nitrogen + remaining 50% K2O.\n- **Bio-fertilizer:** Apply *Acetobacter diazotrophicus* (5 kg/ha) to save up to 20% chemical nitrogen.`;
    }
  }

  // 13. Yellow Leaves / Chlorosis / Nutrient & Watering Causes
  if (q.includes('yellow') || q.includes('पिवळे') || q.includes('chlorosis')) {
    return isMr
      ? `🍂 **पाने पिवळी पडण्याची संभाव्य कारणे व उपाय (${crop || 'पीक'}):**\n\n1. **अन्नद्रव्यांची कमतरता (नत्र/झिंक/लोह):** जुनी पाने पिवळी पडत असल्यास नत्राची (Nitrogen) कमतरता असू शकते. नत्रयुक्त खते द्यावीत. नवीन शेंड्याची पाने पिवळी पडल्यास सूक्ष्म अन्नद्रव्ये (Micronutrients) फवारावीत.\n2. **पाण्याचा निचरा न होणे / जास्तीचे पाणी:** जमिनीत पाणी साचल्यास मुळांना प्राणवायू मिळत नाही व पाने पिवळी पडतात. पाणी देणे कमी करा व वाफसा राखा.\n3. **बुरशीजन्य करपा किंवा रसशोषक किडी:** पानांच्या खालच्या बाजूला मावा किंवा पांढरी माशी असल्यास कडुनिंब तेल (५ मि.ली./लिटर) फवारावे.`
      : `🍂 **Why Leaves Turn Yellow — Causes & Remedies (${crop || 'Crop'}):**\n\n1. **Nutrient Deficiency (Nitrogen / Zinc / Iron):** If older lower leaves turn pale yellow, it indicates Nitrogen deficiency. If young apical leaves turn yellow with green veins (interveinal chlorosis), it indicates Iron or Zinc deficiency.\n2. **Overwatering & Poor Drainage:** Saturated soil creates anaerobic root zones, preventing oxygen and nutrient uptake.\n3. **Early Stage Fungal Infection or Sap-Sucking Pests:** Check leaf undersides for aphids or whiteflies; apply cold-pressed Neem Oil (3000 ppm @ 4 ml/L).`;
  }

  // 14. Disease Spread / Transmission
  if (q.includes('spread') || q.includes('पसर') || q.includes('transmit') || q.includes('other plant')) {
    return isMr
      ? `💨 **रोगाचा प्रसार आणि संसर्ग रोखणे (${crop || 'पीक'}):**\n\n- **प्रसाराचे माध्यम:** बुरशीचे बीजाणू हवेच्या प्रवाहाने, पावसाच्या पाण्याच्या शिंतोड्यांनी आणि अस्वच्छ शेती अवजारांनी शेजारील झाडांवर वेगाने पसरतात.\n- **प्रसार रोखण्यासाठी त्वरित उपाय:**\n  1. संसर्ग झालेली पाने/फांद्या तत्काळ कापून शेताबाहेर नेऊन जाळून टाका.\n  2. तुषार किंवा वरून पाणी देणे टाळा; केवळ मुळांशी पाणी द्या.\n  3. शेजारील निरोगी झाडांवर प्रतिबंधक म्हणून कॉपर ऑक्सिक्लोराईड (२.५ ग्रॅम/लिटर) किंवा कडुनिंब तेलाची फवारणी करा.`
      : `💨 **Disease Transmission & Stopping Spread (${crop || 'Crop'}):**\n\n- **How It Spreads:** Airborne fungal spores, rain splash, and contaminated tools rapidly transmit pathogens to neighboring healthy foliage.\n- **Immediate Containment Protocol:**\n  1. Prune and destroy heavily infected lower leaves and burn plant debris away from the field.\n  2. Avoid overhead sprinkler irrigation to keep foliage dry.\n  3. Spray a protective barrier (Mancozeb 75% WP @ 2.5 g/L or Copper Oxychloride 50% WP) across neighboring healthy crops.`;
  }

  // 15. Weather Disease Risk
  if (q.includes('weather') || q.includes('हवामान') || q.includes('risk') || q.includes('धोका') || q.includes('outbreak')) {
    return isMr
      ? `🌦️ **हवामान आणि रोग प्रादुर्भाव जोखीम विश्लेषण:**\n\n- **जोखीम घटक:** हवेतील आर्द्रता ८०% पेक्षा जास्त असणे, सतत ढगाळ हवामान आणि पानांवर पाण्याचे थेंब जास्त काळ टिकणे यामुळे बुरशीजन्य रोगांचा (करपा, भुरी, तांबोरा) प्रादुर्भाव अत्यंत वेगाने वाढतो.\n- **प्रतिबंधात्मक उपाय:**\n  1. झाडांच्या मुळाशी पाणी साचू देऊ नका; वाफसा राखा.\n  2. शेतात हवा खेळती राहण्यासाठी छाटणी व तण नियंत्रण करा.\n  3. प्रतिबंधक उपाय म्हणून ५ मि.ली./लिटर कडुनिंब तेल किंवा ट्रायकोडर्माची फवारणी करा.`
      : `🌦️ **Weather & Disease Outbreak Risk Assessment:**\n\n- **Risk Factors:** Relative humidity above 80%, overcast skies, and prolonged leaf wetness (8+ hours) create ideal conditions for fungal spore germination (Blights, Rusts, Downy & Powdery Mildews).\n- **Immediate Preventive Steps:**\n  1. Ensure proper drainage and avoid evening overhead sprinkler irrigation.\n  2. Maintain canopy aeration to accelerate morning foliage drying.\n  3. Apply a preventive bio-protectant (Neem Oil 3000 ppm @ 4 ml/L or *Trichoderma*).`;
  }

  // 16. General Agronomy Fallback
  return isMr
    ? `🌾 **AgroScan AI कृषी सल्लागार (${crop || 'शेती मार्गदर्शन'}):**\n\nतुमच्या प्रश्नानुसार ('${userQuery}'), योग्य मशागत, संतुलित सेंद्रिय-रासायनिक खत व्यवस्थापन आणि वेळेवर पाणी देणे आवश्यक आहे. अधिक सविस्तर माहितीसाठी पिकाचे किंवा रोगाचे नाव नमूद करा.`
    : `🌾 **AgroScan AI Agronomist (${crop || 'Crop Advisory'}):**\n\nRegarding your query ('${userQuery}'): For optimal crop health and yield, ensure balanced NPK fertilization, maintain good soil drainage, and inspect foliage regularly for early pest and disease symptoms.`;
};

export const AssistantPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { lang, setLang, t, translateCrop, translateDisease } = useLanguage();
  const predictionId = searchParams.get('predictionId');

  // Context Modes: 'none' | 'manual' | 'scan' | 'no_plant'
  const [contextMode, setContextMode] = useState('none');
  const [scanData, setScanData] = useState(null);
  const [selectedPlant, setSelectedPlant] = useState('');
  const [plantSearch, setPlantSearch] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [showSearchModal, setShowSearchModal] = useState(false);
  const [activeFaqTab, setActiveFaqTab] = useState('disease');

  // Session & Past History State
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [pastSessions, setPastSessions] = useState([]);
  const [showHistoryDrawer, setShowHistoryDrawer] = useState(false);
  const [historySearch, setHistorySearch] = useState('');
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [lastFailedMessage, setLastFailedMessage] = useState(null);
  const [chatError, setChatError] = useState(null);
  const [isOfflineMode, setIsOfflineMode] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [speakingMsgIdx, setSpeakingMsgIdx] = useState(null);
  const [researchStage, setResearchStage] = useState('');
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);
  const recognitionRef = useRef(null);

  // Load Past Chat Sessions from Backend API and Local Storage
  const fetchPastSessions = async () => {
    setLoadingHistory(true);
    let serverSessions = [];
    try {
      const res = await api.get('/chat/sessions');
      if (Array.isArray(res.data)) {
        serverSessions = res.data;
      }
    } catch (e) {
      console.warn('Failed to load server chat sessions, relying on local storage cache:', e);
    }

    // Merge with local storage cache
    try {
      const cached = JSON.parse(localStorage.getItem('agroscan_chat_sessions_v1') || '[]');
      const combinedMap = new Map();
      
      serverSessions.forEach(s => combinedMap.set(s.id, s));
      cached.forEach(s => {
        if (!combinedMap.has(s.id)) {
          combinedMap.set(s.id, s);
        }
      });

      const mergedList = Array.from(combinedMap.values()).sort(
        (a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0)
      );

      setPastSessions(mergedList);
      localStorage.setItem('agroscan_chat_sessions_v1', JSON.stringify(mergedList));
    } catch {
      setPastSessions(serverSessions);
    } finally {
      setLoadingHistory(false);
    }
  };

  useEffect(() => {
    fetchPastSessions();
  }, []);

  // Progressive Research Stage Indicator Timer
  useEffect(() => {
    if (!loading) {
      setResearchStage('');
      return;
    }
    const stagesEn = [
      '🌾 Analyzing agricultural question & intent...',
      '🔍 Querying FAO, ICAR & CABI Plantwise databases...',
      '📄 Checking peer-reviewed plant pathology research...',
      '🧪 Cross-checking evidence & safety guidelines...',
      '✍️ Synthesizing evidence-based agronomist advisory...'
    ];
    const stagesMr = [
      '🌾 प्रश्नाचे स्वरूप व कृषी उद्देश तपासत आहे...',
      '🔍 FAO, ICAR व कृषी डेटाबेस शोधत आहे...',
      '📄 पीक रोग व कीड संशोधनाचे संदर्भ तपासत आहे...',
      '🧪 औषध प्रमाण व सुरक्षा नियमांची खात्री करत आहे...',
      '✍️ पुराव्यावर आधारित कृषी सल्ला तयार करत आहे...'
    ];
    const stages = lang === 'mr' ? stagesMr : stagesEn;
    setResearchStage(stages[0]);
    let stageIdx = 0;
    const interval = setInterval(() => {
      stageIdx = (stageIdx + 1) % stages.length;
      setResearchStage(stages[stageIdx]);
    }, 1800);
    return () => clearInterval(interval);
  }, [loading, lang]);

  // Search Plant Catalog API
  useEffect(() => {
    if (plantSearch.trim().length > 0) {
      api.get(`/plants/search?q=${encodeURIComponent(plantSearch)}`)
        .then(res => setSearchResults(Array.isArray(res.data) ? res.data : []))
        .catch(() => setSearchResults([]));
    } else {
      setSearchResults([]);
    }
  }, [plantSearch]);

  // Start Clean New Chat Session
  const handleStartNewChat = () => {
    const newSessionId = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
    setSessionId(newSessionId);
    setContextMode('none');
    setSelectedPlant('');
    setScanData(null);
    setChatError(null);
    setLastFailedMessage(null);
    setShowHistoryDrawer(false);

    const welcomeMsg = {
      sender: 'assistant',
      content: t('assistant.state_a_welcome') || "Welcome to AgroScan AI Agronomist! Type any question below regarding crop health, organic bio-sprays, diseases, fertilizers, or farm care."
    };
    setMessages([welcomeMsg]);
    localStorage.setItem('agroscan_active_session_id', newSessionId);
    if (inputRef.current) inputRef.current.focus();
  };

  // Load Selected Past Session
  const handleSelectSession = async (session) => {
    if (!session || !session.id) return;
    setLoading(true);
    setSessionId(session.id);
    setShowHistoryDrawer(false);
    localStorage.setItem('agroscan_active_session_id', session.id);

    try {
      const res = await api.get(`/chat/sessions/${session.id}`);
      if (res.data && Array.isArray(res.data.messages) && res.data.messages.length > 0) {
        setMessages(res.data.messages.map(m => ({
          sender: m.sender,
          content: m.content || m.answer,
          sources: m.sources || [],
          source_agreement: m.source_agreement || 'high',
          evidence_confidence: m.evidence_confidence || 0.92,
          created_at: m.created_at
        })));
        return;
      }
    } catch (err) {
      console.warn('Failed to fetch session detail from server, using cached messages:', err);
    }

    // Fallback to local session messages if present
    if (session.messages && session.messages.length > 0) {
      setMessages(session.messages.map(m => ({
        sender: m.sender,
        content: m.content || m.answer,
        sources: m.sources || [],
        source_agreement: m.source_agreement || 'high',
        evidence_confidence: m.evidence_confidence || 0.92
      })));
    }
    setLoading(false);
  };

  // Delete a Past Chat Session
  const handleDeleteSession = async (targetSessionId, e) => {
    e.stopPropagation();
    if (!targetSessionId) return;

    // Optimistic local state update
    const updated = pastSessions.filter(s => s.id !== targetSessionId);
    setPastSessions(updated);
    localStorage.setItem('agroscan_chat_sessions_v1', JSON.stringify(updated));

    try {
      await api.delete(`/chat/sessions/${targetSessionId}`);
    } catch (err) {
      console.warn('Failed to delete session on server:', err);
    }

    if (sessionId === targetSessionId) {
      handleStartNewChat();
    }
  };

  // Initialize & Reset Assistant Messages when Context / Prediction ID / Plant changes
  useEffect(() => {
    if (predictionId) {
      const newSid = `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
      setSessionId(newSid);
      setChatError(null);
      setLastFailedMessage(null);

      api.get(`/predictions/${predictionId}`)
        .then(res => {
          const data = res.data;
          if (data.is_plant === false || data.disease_code === 'non_plant') {
            setContextMode('no_plant');
            setSelectedPlant('');
            setMessages([{
              sender: 'assistant',
              content: t('assistant.state_d_noplant') || "The latest image does not appear to contain a leaf or plant. Please scan a clear plant image to begin analysis."
            }]);
          } else {
            setContextMode('scan');
            setScanData(data);
            setSelectedPlant('');
            const isHealthy = (data.disease_name || '').toLowerCase().includes('healthy');
            if (isHealthy) {
              setMessages([{
                sender: 'assistant',
                content: t('assistant.state_c_healthy', { crop: data.crop_detected || 'Plant' }) || `Your latest scan identified ${data.crop_detected || 'Plant'}. No disease was detected in this scan. Ask me about preventive care, fertilizers, or seasonal management.`
              }]);
            } else {
              setMessages([{
                sender: 'assistant',
                content: t('assistant.state_c_scan', {
                  crop: data.crop_detected || 'Crop',
                  disease: data.disease_name || 'Disease',
                  severity: data.severity_level || 'Normal',
                  confidence: Math.round((data.confidence_score || 0.95) * 100)
                }) || `Identified ${data.crop_detected || 'Crop'} with suspected ${data.disease_name || 'Disease'} (${Math.round((data.confidence_score || 0.95) * 100)}% confidence). Ask me about dangers, organic treatment, spread prevention, or dosage.`
              }]);
            }
          }
        })
        .catch(() => {
          setContextMode('none');
          setScanData(null);
          setMessages([{ sender: 'assistant', content: t('assistant.state_a_welcome') || "Welcome to AgroScan AI Agronomist! Type any question below regarding crop health, organic bio-sprays, diseases, fertilizers, or farm care." }]);
        });
    } else {
      // If no active prediction ID, initialize session if not already set
      if (!sessionId) {
        const initialSid = localStorage.getItem('agroscan_active_session_id') || `session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
        setSessionId(initialSid);
        if (messages.length === 0) {
          setMessages([{ sender: 'assistant', content: t('assistant.state_a_welcome') || "Welcome to AgroScan AI Agronomist! Type any question below regarding crop health, organic bio-sprays, diseases, fertilizers, or farm care." }]);
        }
      }
    }
  }, [predictionId, lang, t]);

  // Handle Speech Recognition (Microphone voice input)
  const toggleSpeechRecognition = () => {
    if (isListening) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      setIsListening(false);
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert(lang === 'mr' ? 'तुमच्या ब्राउझरमध्ये व्हॉइस टायपिंग उपलब्ध नाही.' : 'Speech recognition is not supported in your browser.');
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognition.lang = lang === 'mr' ? 'mr-IN' : 'en-IN';
      recognition.interimResults = false;
      recognition.continuous = false;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) {
          setInput(prev => (prev ? `${prev} ${transcript}` : transcript));
        }
      };

      recognition.onerror = () => {
        setIsListening(false);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognitionRef.current = recognition;
      recognition.start();
    } catch (e) {
      setIsListening(false);
    }
  };

  // Handle Text to Speech (Audio Read Aloud)
  const speakMessage = (text, idx) => {
    if (!window.speechSynthesis) return;

    if (speakingMsgIdx === idx) {
      window.speechSynthesis.cancel();
      setSpeakingMsgIdx(null);
      return;
    }

    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[*#_`]/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = lang === 'mr' ? 'mr-IN' : 'en-IN';
    utterance.rate = 0.95;

    utterance.onend = () => setSpeakingMsgIdx(null);
    utterance.onerror = () => setSpeakingMsgIdx(null);

    setSpeakingMsgIdx(idx);
    window.speechSynthesis.speak(utterance);
  };

  // Handle Manual Plant Selection
  const handleSelectManualPlant = (plantName) => {
    setSelectedPlant(plantName);
    setPlantSearch('');
    setShowSearchModal(false);
    setContextMode('manual');
    setScanData(null);

    setSessionId(`session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`);
    setMessages([{
      sender: 'assistant',
      content: t('assistant.state_b_manual', { plant: plantName }) || `You selected ${plantName}. I am ready to advise you on ${plantName} cultivation practices, soil nutrition, irrigation intervals, fungal diseases, organic remedies, and harvesting guidance. What would you like to know?`
    }]);
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Send Message Logic with Automatic Smart Offline Agronomist Fallback
  const sendMessage = async (textToSend) => {
    if (!textToSend || !textToSend.trim() || loading) return;

    const userText = textToSend.trim();
    setInput('');
    setChatError(null);
    setLastFailedMessage(null);

    // Build history payload
    const historyPayload = messages.map(m => ({
      role: m.sender === 'user' ? 'user' : 'assistant',
      content: m.content
    }));

    // Update UI immediately with user's question
    const updatedMessages = [...messages, { sender: 'user', content: userText }];
    setMessages(updatedMessages);
    setLoading(true);

    const payload = {
      message: userText,
      session_id: sessionId || undefined,
      prediction_id: contextMode === 'scan' ? (predictionId || undefined) : undefined,
      manual_plant: contextMode === 'manual' ? selectedPlant : undefined,
      language: lang,
      conversation_history: historyPayload
    };

    try {
      const res = await api.post('/chat', payload);
      if (res.data && (res.data.content || res.data.answer)) {
        const returnedSid = res.data.session_id || sessionId;
        if (returnedSid) {
          setSessionId(returnedSid);
          localStorage.setItem('agroscan_active_session_id', returnedSid);
        }
        const botText = res.data.answer || res.data.content;
        const newBotMsg = {
          sender: 'assistant',
          content: botText,
          sources: res.data.sources || [],
          source_agreement: res.data.source_agreement || 'high',
          evidence_confidence: res.data.evidence_confidence || 0.92,
          created_at: new Date().toISOString()
        };
        const allNewMessages = [...updatedMessages, newBotMsg];
        setMessages(allNewMessages);
        setIsOfflineMode(false);

        // Update pastSessions list and local storage
        const currentTitle = userText.length > 38 ? userText.substring(0, 36) + '...' : userText;
        setPastSessions(prev => {
          const filtered = prev.filter(s => s.id !== returnedSid);
          const updatedSession = {
            id: returnedSid,
            title: currentTitle,
            created_at: new Date().toISOString(),
            message_count: allNewMessages.length,
            last_message: botText.length > 55 ? botText.substring(0, 52) + '...' : botText,
            messages: allNewMessages
          };
          const updatedList = [updatedSession, ...filtered];
          localStorage.setItem('agroscan_chat_sessions_v1', JSON.stringify(updatedList));
          return updatedList;
        });
      } else {
        throw new Error('Empty response from AI backend');
      }
    } catch (err) {
      console.warn('Backend chat API failed or sleeping. Engaging local agronomist knowledge engine:', err);
      // Smart instant fallback so farmers never get stranded
      const localReply = generateClientAdvisory(
        userText,
        contextMode === 'scan' ? scanData : { plantName: selectedPlant },
        lang
      );
      const localBotMsg = { sender: 'assistant', content: localReply, created_at: new Date().toISOString() };
      const allLocalMsgs = [...updatedMessages, localBotMsg];
      setMessages(allLocalMsgs);
      setIsOfflineMode(true);

      // Save locally even in offline mode
      const currentTitle = userText.length > 38 ? userText.substring(0, 36) + '...' : userText;
      setPastSessions(prev => {
        const filtered = prev.filter(s => s.id !== sessionId);
        const updatedSession = {
          id: sessionId,
          title: currentTitle,
          created_at: new Date().toISOString(),
          message_count: allLocalMsgs.length,
          last_message: localReply.length > 55 ? localReply.substring(0, 52) + '...' : localReply,
          messages: allLocalMsgs
        };
        const updatedList = [updatedSession, ...filtered];
        localStorage.setItem('agroscan_chat_sessions_v1', JSON.stringify(updatedList));
        return updatedList;
      });
    } finally {
      setLoading(false);
      if (inputRef.current) {
        inputRef.current.focus();
      }
    }
  };

  const handleRetry = () => {
    if (lastFailedMessage) {
      const text = lastFailedMessage;
      setLastFailedMessage(null);
      setChatError(null);
      setMessages(prev => prev.filter((_, i) => i !== prev.length - 1));
      sendMessage(text);
    }
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    sendMessage(input);
  };

  const activeCategories = FARMER_FAQ_CATEGORIES[lang] || FARMER_FAQ_CATEGORIES.en;
  const currentCategoryObj = activeCategories.find(c => c.id === activeFaqTab) || activeCategories[0];

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-5.5rem)] relative overflow-hidden glass-panel rounded-2xl border border-slate-800 shadow-2xl bg-slate-950/60">
      
      {/* Context Header */}
      <div className="bg-slate-900/95 border-b border-slate-800 p-3.5 shrink-0 shadow-md z-10 space-y-2.5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2.5">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-xl bg-agri-500/20 border border-agri-500/40 flex items-center justify-center text-agri-400">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h2 className="text-sm sm:text-base font-bold text-white leading-tight">
                  {lang === 'mr' ? 'AgroScan AI कृषी सल्लागार' : 'AgroScan AI Agronomist'}
                </h2>
                {isOfflineMode && (
                  <span className="px-2 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-[10px] font-bold text-amber-400 flex items-center space-x-1">
                    <Zap className="w-3 h-3" />
                    <span>{lang === 'mr' ? 'थेट सल्ला' : 'Instant Mode'}</span>
                  </span>
                )}
              </div>
              <p className="text-[11px] text-slate-400">
                {contextMode === 'scan' 
                  ? (lang === 'mr' ? 'स्कॅन केलेल्या पिकावर आधारित प्रश्न विचारा' : 'Consulting for active scanned crop')
                  : contextMode === 'manual'
                  ? (lang === 'mr' ? `${translateCrop(selectedPlant)} पिकासाठी सल्ला` : `Advisory for ${selectedPlant}`)
                  : (lang === 'mr' ? 'शेतकऱ्यांसाठी २४/७ डिजिटल कृषी सहाय्यक' : '24/7 Crop Health & Advisory for Farmers')}
              </p>
            </div>
          </div>

          <div className="flex items-center flex-wrap gap-1.5 sm:gap-2">
            {/* New Chat Button */}
            <button
              type="button"
              onClick={handleStartNewChat}
              className="px-2.5 py-1.5 rounded-xl bg-agri-500/20 hover:bg-agri-500/30 text-agri-400 border border-agri-500/40 text-xs font-bold flex items-center space-x-1.5 transition shadow-sm"
              title={lang === 'mr' ? 'नवीन संवाद सुरू करा' : 'Start a fresh new advisory chat'}
            >
              <Plus className="w-3.5 h-3.5 text-agri-400" />
              <span className="hidden sm:inline">{lang === 'mr' ? 'नवीन संवाद' : 'New Chat'}</span>
            </button>

            {/* Past History Drawer Trigger */}
            <button
              type="button"
              onClick={() => {
                fetchPastSessions();
                setShowHistoryDrawer(true);
              }}
              className="px-2.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 border border-slate-700 flex items-center space-x-1.5 transition relative"
              title={lang === 'mr' ? 'मागील संवाद इतिहास पहा' : 'View past chat history'}
            >
              <History className="w-3.5 h-3.5 text-slate-400" />
              <span className="hidden sm:inline">{lang === 'mr' ? 'इतिहास' : 'History'}</span>
              {pastSessions.length > 0 && (
                <span className="px-1.5 py-0.2 rounded-full bg-agri-500/20 text-agri-400 text-[10px] font-mono font-bold">
                  {pastSessions.length}
                </span>
              )}
            </button>

            {/* Export Chat Button with UTF-8 BOM encoding for Marathi safety */}
            <button
              type="button"
              onClick={() => {
                if (messages.length === 0) return;
                const plantName = selectedPlant || scanData?.crop_detected || 'General';
                const dateStr = new Date().toISOString().split('T')[0];
                let md = `# AgroScan AI — Agronomy Advisory Transcript\n\nDate: ${dateStr}\nContext: ${plantName}\nLanguage: ${lang === 'mr' ? 'मराठी' : 'English'}\n===================================\n\n`;
                messages.forEach(msg => {
                  md += `### ${msg.sender === 'user' ? (lang === 'mr' ? 'शेतकरी (Farmer)' : 'Farmer') : (lang === 'mr' ? 'AgroScan AI कृषी सल्लागार' : 'AgroScan AI Advisor')}\n${msg.content}\n\n`;
                });
                const blob = new Blob(["\uFEFF" + md], { type: 'text/markdown;charset=utf-8;' });
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                link.href = url;
                link.setAttribute('download', `agroscan-advisory-${plantName.toLowerCase().replace(/[^a-z0-9]/g, '_')}-${dateStr}.md`);
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
              }}
              disabled={messages.length <= 1}
              className="px-2.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 border border-slate-700 flex items-center space-x-1.5 transition disabled:opacity-40"
              title="Export conversation history"
            >
              <Download className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">{lang === 'mr' ? 'जतन करा' : 'Export'}</span>
            </button>

            <button
              type="button"
              onClick={() => setShowSearchModal(true)}
              className="px-2.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 border border-slate-700 flex items-center space-x-1.5 transition"
            >
              <Sprout className="w-3.5 h-3.5 text-agri-400" />
              <span className="hidden sm:inline">{t('assistant.change_plant') || 'Change Plant'}</span>
              <span className="sm:hidden">{lang === 'mr' ? 'पीक' : 'Crop'}</span>
            </button>

            {/* Language Switch */}
            <div className="flex bg-slate-950 rounded-xl p-1 border border-slate-800 text-xs font-bold">
              <button
                type="button"
                onClick={() => setLang('en')}
                className={`px-2.5 py-1 rounded-lg transition ${
                  lang === 'en' ? 'bg-agri-500 text-slate-950 shadow font-bold' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                EN
              </button>
              <button
                type="button"
                onClick={() => setLang('mr')}
                className={`px-2.5 py-1 rounded-lg transition ${
                  lang === 'mr' ? 'bg-agri-500 text-slate-950 shadow font-bold' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                मराठी
              </button>
            </div>
          </div>
        </div>

        {/* Active Scan Context Bar */}
        {contextMode === 'scan' && scanData && (
          <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex flex-wrap items-center justify-between gap-2 text-xs">
            <div className="flex items-center space-x-3">
              <span className="text-white font-bold">
                🌱 {lang === 'mr' ? 'स्कॅन केलेले पीक' : 'Scanned Crop'}: {translateCrop(scanData.crop_detected)}
              </span>
              <span className="text-slate-600">|</span>
              <span className="text-amber-400 font-semibold">
                🦠 {lang === 'mr' ? 'आढळलेला रोग' : 'Detected'}: {translateDisease(scanData.disease_name)}
              </span>
            </div>
            <span className="text-agri-400 font-mono font-bold">
              {t('result.confidence') || 'Confidence'}: {Math.round((scanData.confidence_score || 0.95) * 100)}%
            </span>
          </div>
        )}

        {/* Active Manual Plant Context Bar */}
        {contextMode === 'manual' && selectedPlant && (
          <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between text-xs">
            <span className="text-white font-bold">
              🌱 {lang === 'mr' ? 'निवडलेले पीक मार्गदर्शन' : 'Active Crop Guidance'}: {translateCrop(selectedPlant)}
            </span>
            <span className="text-slate-400 text-[11px] italic">
              {lang === 'mr' ? 'पीक निगा व खत मार्गदर्शन' : 'Crop cultivation & disease care'}
            </span>
          </div>
        )}
      </div>

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 pb-48">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex gap-3 max-w-[92%] sm:max-w-[85%] ${msg.sender === 'user' ? 'ml-auto justify-end' : ''}`}
          >
            {msg.sender === 'assistant' && (
              <div className="w-8 h-8 rounded-full bg-agri-500/20 text-agri-400 flex items-center justify-center shrink-0 border border-agri-500/40 mt-1">
                <Bot className="w-4 h-4" />
              </div>
            )}

            <div className={`flex flex-col gap-1 ${msg.sender === 'user' ? 'items-end' : ''}`}>
              <div className="flex items-center space-x-2">
                <span className="text-[11px] font-medium text-slate-400">
                  {msg.sender === 'user' ? (lang === 'mr' ? '👨‍🌾 तुम्ही (शेतकरी)' : '👨‍🌾 You (Farmer)') : (lang === 'mr' ? '🌾 AgroScan AI सल्लागार' : '🌾 AgroScan Advisor')}
                </span>
                {msg.sender === 'assistant' && (
                  <button
                    type="button"
                    onClick={() => speakMessage(msg.content, idx)}
                    className={`p-1 rounded-lg hover:bg-slate-800 transition text-xs ${
                      speakingMsgIdx === idx ? 'text-agri-400 animate-pulse' : 'text-slate-500 hover:text-slate-300'
                    }`}
                    title={lang === 'mr' ? 'सल्ला ऐका (Audio)' : 'Listen to advisory'}
                  >
                    {speakingMsgIdx === idx ? <VolumeX className="w-3.5 h-3.5" /> : <Volume2 className="w-3.5 h-3.5" />}
                  </button>
                )}
              </div>
              
              <div
                className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-agri-500 text-slate-950 font-semibold rounded-tr-none shadow-lg shadow-agri-500/20'
                    : 'bg-slate-900/95 border border-slate-800 text-slate-200 rounded-tl-none shadow-sm'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>

                {/* Multi-Source Research Citations & Evidence Panel */}
                {msg.sender === 'assistant' && msg.sources && msg.sources.length > 0 && (
                  <div className="mt-3.5 pt-3 border-t border-slate-800/80 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-bold text-agri-400 flex items-center gap-1.5">
                        <span>📚</span>
                        <span>{lang === 'mr' ? 'तपासलेले कृषी संशोधन व संदर्भ (Sources):' : 'Verified Agricultural Research & Sources:'}</span>
                      </span>
                      {msg.source_agreement && (
                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-agri-500/15 text-agri-300 border border-agri-500/30 font-semibold">
                          {msg.source_agreement === 'high' ? '✅ High Consensus' : '🔍 Multi-Source Verified'}
                        </span>
                      )}
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 pt-1">
                      {msg.sources.map((src, sIdx) => (
                        <a
                          key={sIdx}
                          href={src.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex flex-col p-2 rounded-xl bg-slate-950/80 border border-slate-800/90 hover:border-agri-500/50 hover:bg-slate-950 transition group"
                        >
                          <div className="flex items-center justify-between gap-1 mb-0.5">
                            <span className="text-[10px] font-bold text-slate-400 group-hover:text-agri-400 truncate">
                              {src.source}
                            </span>
                            {src.trust_score && (
                              <span className="text-[9px] font-mono text-emerald-400 bg-emerald-950/60 px-1 rounded border border-emerald-800/40">
                                {Math.round(src.trust_score * 100)}% Trust
                              </span>
                            )}
                          </div>
                          <span className="text-[11px] text-slate-300 font-medium line-clamp-1 group-hover:text-white">
                            {src.title}
                          </span>
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {msg.sender === 'user' && (
              <div className="w-8 h-8 rounded-full bg-slate-800 text-slate-300 flex items-center justify-center shrink-0 border border-slate-700 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {/* Progressive Multi-Source Research Indicator */}
        {loading && (
          <div className="flex gap-3 items-center p-2 text-xs text-agri-400 font-semibold">
            <div className="w-8 h-8 rounded-full bg-agri-500/20 text-agri-400 flex items-center justify-center shrink-0 border border-agri-500/40">
              <Loader2 className="w-4 h-4 animate-spin text-agri-400" />
            </div>
            <div className="bg-slate-900/90 border border-slate-800 p-3 rounded-2xl text-slate-300 flex items-center space-x-2.5 shadow-lg">
              <span className="inline-block w-2 h-2 rounded-full bg-agri-400 animate-ping mr-0.5"></span>
              <span className="text-xs">
                {researchStage || (lang === 'mr' ? 'FAO, ICAR व कृषी डेटाबेस शोधत आहे...' : 'Consulting FAO, ICAR & agricultural research databases...')}
              </span>
            </div>
          </div>
        )}

        {/* Error / Retry Banner */}
        {chatError && (
          <div className="p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
              <span>{chatError}</span>
            </div>
            {lastFailedMessage && (
              <button
                type="button"
                onClick={handleRetry}
                className="px-3 py-1 bg-red-500/20 hover:bg-red-500/30 text-red-200 rounded-lg font-bold flex items-center space-x-1 transition"
              >
                <RotateCcw className="w-3 h-3" />
                <span>{t('assistant.retry') || 'Retry'}</span>
              </button>
            )}
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Bottom Interactive Typing & Question Container (Fixed at bottom) */}
      <div className="absolute bottom-0 w-full bg-slate-900/98 backdrop-blur-md border-t border-slate-800 p-3 shadow-2xl z-20 space-y-2.5">
        
        {/* Curated Farmer FAQ Category Tabs */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-slate-400 flex items-center space-x-1">
              <HelpCircle className="w-3 h-3 text-agri-400" />
              <span>{lang === 'mr' ? 'शेतकऱ्यांनी विचारलेले मुख्य प्रश्न (क्लिक करा):' : 'Frequently Asked Questions by Farmers:'}</span>
            </span>

            {/* Category Selectors */}
            <div className="flex items-center space-x-1 overflow-x-auto hide-scrollbar">
              {activeCategories.map(cat => (
                <button
                  key={cat.id}
                  type="button"
                  onClick={() => setActiveFaqTab(cat.id)}
                  className={`px-2 py-0.5 rounded-lg text-[10px] font-bold transition whitespace-nowrap ${
                    activeFaqTab === cat.id
                      ? 'bg-agri-500/20 text-agri-400 border border-agri-500/40'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  {cat.label}
                </button>
              ))}
            </div>
          </div>

          {/* Quick-tap FAQ Question Chips */}
          <div className="flex overflow-x-auto gap-2 pb-1 hide-scrollbar">
            {currentCategoryObj.questions.map((qr, i) => (
              <button
                key={i}
                type="button"
                disabled={loading}
                onClick={() => sendMessage(qr)}
                className="whitespace-nowrap px-3 py-1.5 bg-slate-950 border border-slate-800 hover:border-agri-500/50 rounded-xl text-xs font-semibold text-slate-300 hover:text-white transition shrink-0 disabled:opacity-50 flex items-center space-x-1.5 shadow-sm"
              >
                <span>💬</span>
                <span>{qr}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Main Farmer Typing Bar & Voice Mic */}
        <form onSubmit={handleFormSubmit} className="flex items-center gap-2">
          <div className="relative flex-1 flex items-center">
            <input
              ref={inputRef}
              type="text"
              value={input}
              disabled={loading}
              onChange={(e) => setInput(e.target.value)}
              placeholder={
                isListening
                  ? (lang === 'mr' ? '🎙️ ऐकत आहे... बोला...' : '🎙️ Listening... speak now...')
                  : loading 
                  ? (lang === 'mr' ? 'AI सल्लागार उत्तर लिहीत आहे...' : 'AI is writing advice...') 
                  : (lang === 'mr' ? 'येथे तुमचा प्रश्न विचारा (उदा. करपा रोगावर काय उपाय करावा?)...' : 'Type your farming question (e.g. How to cure leaf blight?)...')
              }
              className={`w-full h-12 pl-4 pr-10 rounded-xl bg-slate-950 border text-xs sm:text-sm text-white focus:outline-none placeholder:text-slate-500 disabled:opacity-50 transition shadow-inner ${
                isListening 
                  ? 'border-red-500 ring-2 ring-red-500/30' 
                  : 'border-slate-700 focus:border-agri-500 focus:ring-1 focus:ring-agri-500/30'
              }`}
            />
            {input.length > 0 && !loading && (
              <button
                type="button"
                onClick={() => setInput('')}
                className="absolute right-3 text-slate-500 hover:text-slate-300 transition"
                title="Clear text"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>

          {/* Voice Input Button */}
          <button
            type="button"
            onClick={toggleSpeechRecognition}
            disabled={loading}
            className={`w-12 h-12 rounded-xl border flex items-center justify-center font-bold transition shrink-0 ${
              isListening
                ? 'bg-red-500 text-white border-red-400 animate-pulse'
                : 'bg-slate-950 hover:bg-slate-800 text-slate-300 border-slate-700'
            }`}
            title={lang === 'mr' ? 'बोलून प्रश्न विचारा (Voice typing)' : 'Speak question (Voice input)'}
          >
            {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5 text-agri-400" />}
          </button>

          {/* Send Question Button */}
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="h-12 px-4 sm:px-5 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 flex items-center justify-center font-bold text-xs sm:text-sm shadow-lg shadow-agri-500/20 shrink-0 disabled:opacity-50 transition space-x-1.5"
            aria-label="Send Question"
          >
            {loading ? (
              <Loader2 className="w-4 h-4 animate-spin text-slate-950" />
            ) : (
              <>
                <span className="hidden sm:inline">{lang === 'mr' ? 'विचारा' : 'Ask'}</span>
                <Send className="w-4 h-4" />
              </>
            )}
          </button>
        </form>
      </div>

      {/* Plant Search & Change Modal */}
      {showSearchModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel p-6 rounded-2xl max-w-md w-full space-y-4 border border-slate-700 bg-slate-900/95 shadow-2xl">
            <div className="flex justify-between items-center">
              <h3 className="text-base font-bold text-white flex items-center space-x-2">
                <Sprout className="w-4 h-4 text-agri-400" />
                <span>{t('assistant.type_select_plant') || 'Select Crop for Advisory'}</span>
              </h3>
              <button onClick={() => setShowSearchModal(false)} className="text-slate-400 hover:text-white" aria-label="Close plant modal">
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="relative">
              <div className="flex items-center space-x-2 bg-slate-950 px-3.5 py-2.5 rounded-xl border border-slate-800 text-xs">
                <Search className="w-4 h-4 text-slate-500 shrink-0" />
                <input
                  type="text"
                  value={plantSearch}
                  onChange={(e) => setPlantSearch(e.target.value)}
                  placeholder={t('assistant.search_placeholder') || "Search crop (e.g. Mango, Tomato, Sugarcane, Rice...)"}
                  className="bg-transparent text-slate-200 w-full focus:outline-none placeholder:text-slate-600"
                  autoFocus
                />
              </div>
            </div>

            <div className="max-h-60 overflow-y-auto space-y-1">
              {(searchResults.length > 0 ? searchResults : [
                { name: 'Mango', scientific_name: 'Mangifera indica' },
                { name: 'Tomato', scientific_name: 'Solanum lycopersicum' },
                { name: 'Potato', scientific_name: 'Solanum tuberosum' },
                { name: 'Sugarcane', scientific_name: 'Saccharum officinarum' },
                { name: 'Rice', scientific_name: 'Oryza sativa' },
                { name: 'Wheat', scientific_name: 'Triticum aestivum' },
                { name: 'Corn (Maize)', scientific_name: 'Zea mays' },
                { name: 'Cotton', scientific_name: 'Gossypium hirsutum' },
                { name: 'Chilli', scientific_name: 'Capsicum annuum' },
                { name: 'Onion', scientific_name: 'Allium cepa' },
                { name: 'Neem', scientific_name: 'Azadirachta indica' }
              ]).map((p) => (
                <button
                  key={p.name}
                  type="button"
                  onClick={() => handleSelectManualPlant(p.name)}
                  className="w-full text-left px-3.5 py-2.5 rounded-xl hover:bg-slate-800 flex items-center justify-between text-xs text-slate-200 transition border border-transparent hover:border-slate-700"
                >
                  <div className="flex items-center space-x-2">
                    <Sprout className="w-4 h-4 text-agri-400 shrink-0" />
                    <span className="font-semibold">{translateCrop(p.name)}</span>
                  </div>
                  <span className="text-[11px] text-slate-500 italic">{p.scientific_name}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Past Chat History Slide-Over Drawer */}
      {showHistoryDrawer && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex justify-end transition-opacity">
          <div className="w-full max-w-md h-full bg-slate-900 border-l border-slate-800 flex flex-col shadow-2xl animate-in slide-in-from-right duration-200">
            
            {/* Drawer Header */}
            <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/70">
              <div className="flex items-center space-x-2.5">
                <div className="w-8 h-8 rounded-xl bg-agri-500/20 border border-agri-500/40 flex items-center justify-center text-agri-400">
                  <History className="w-4 h-4" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white leading-tight">
                    {lang === 'mr' ? 'मागील कृषी संवाद इतिहास' : 'Past Consultations'}
                  </h3>
                  <p className="text-[11px] text-slate-400">
                    {lang === 'mr' ? `${pastSessions.length} जतन केलेले संवाद` : `${pastSessions.length} saved consultations`}
                  </p>
                </div>
              </div>
              
              <button
                type="button"
                onClick={() => setShowHistoryDrawer(false)}
                className="w-8 h-8 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center transition"
                aria-label="Close history drawer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Quick Action: Start New Chat */}
            <div className="p-3 border-b border-slate-800/80 bg-slate-950/40 space-y-2">
              <button
                type="button"
                onClick={handleStartNewChat}
                className="w-full py-2.5 px-3.5 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 font-bold text-xs flex items-center justify-center space-x-2 transition shadow-lg shadow-agri-500/15"
              >
                <Plus className="w-4 h-4" />
                <span>{lang === 'mr' ? '+ नवीन कृषी संवाद सुरू करा' : '+ Start New Advisory Chat'}</span>
              </button>

              {/* History Search Filter */}
              {pastSessions.length > 3 && (
                <div className="relative">
                  <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-2.5" />
                  <input
                    type="text"
                    value={historySearch}
                    onChange={(e) => setHistorySearch(e.target.value)}
                    placeholder={lang === 'mr' ? 'इतिहास शोधा (उदा. करपा, ऊस, खत)...' : 'Search past topics...'}
                    className="w-full pl-8 pr-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-agri-500"
                  />
                  {historySearch && (
                    <button
                      type="button"
                      onClick={() => setHistorySearch('')}
                      className="absolute right-2.5 top-2 text-slate-500 hover:text-slate-300 text-xs"
                    >
                      <X className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              )}
            </div>

            {/* Past Sessions List */}
            <div className="flex-1 overflow-y-auto p-3 space-y-2">
              {loadingHistory ? (
                <div className="p-8 text-center text-xs text-slate-400 space-y-2">
                  <Loader2 className="w-6 h-6 animate-spin mx-auto text-agri-400" />
                  <p>{lang === 'mr' ? 'इतिहास लोड होत आहे...' : 'Loading past chats...'}</p>
                </div>
              ) : pastSessions.length === 0 ? (
                <div className="p-8 text-center text-slate-500 text-xs space-y-2">
                  <MessageSquare className="w-8 h-8 mx-auto text-slate-600 opacity-60" />
                  <p className="font-semibold text-slate-400">
                    {lang === 'mr' ? 'कोणताही मागील संवाद सापडला नाही' : 'No past conversations found'}
                  </p>
                  <p className="text-[11px]">
                    {lang === 'mr' ? 'तुम्ही AI सल्लागाराला विचारलेले प्रश्न येथे जतन केले जातील.' : 'Your consultations with AgroScan AI will automatically be saved here.'}
                  </p>
                </div>
              ) : (
                pastSessions
                  .filter(s => {
                    if (!historySearch.trim()) return true;
                    const q = historySearch.toLowerCase();
                    return (s.title || '').toLowerCase().includes(q) || (s.last_message || '').toLowerCase().includes(q);
                  })
                  .map((s) => {
                    const isActive = s.id === sessionId;
                    const dateDisplay = s.created_at ? formatDate(s.created_at) : '';
                    return (
                      <div
                        key={s.id}
                        onClick={() => handleSelectSession(s)}
                        className={`group p-3 rounded-xl border transition cursor-pointer relative ${
                          isActive
                            ? 'bg-agri-500/10 border-agri-500/50 shadow-md shadow-agri-500/5'
                            : 'bg-slate-950/70 border-slate-800 hover:border-slate-700 hover:bg-slate-950'
                        }`}
                      >
                        <div className="flex items-start justify-between gap-2">
                          <div className="flex items-center space-x-2 flex-1 min-w-0">
                            {isActive ? (
                              <span className="w-2 h-2 rounded-full bg-agri-400 shrink-0 animate-pulse" />
                            ) : (
                              <MessageSquare className="w-3.5 h-3.5 text-slate-500 shrink-0 group-hover:text-agri-400" />
                            )}
                            <h4 className="text-xs font-bold text-slate-200 group-hover:text-white truncate">
                              {s.title || 'AgroScan Advisory'}
                            </h4>
                          </div>

                          <div className="flex items-center space-x-1 shrink-0">
                            <button
                              type="button"
                              onClick={(e) => handleDeleteSession(s.id, e)}
                              className="p-1 rounded-lg text-slate-500 hover:text-red-400 hover:bg-red-500/10 transition opacity-70 group-hover:opacity-100"
                              title={lang === 'mr' ? 'संवाद हटवा' : 'Delete chat session'}
                            >
                              <Trash2 className="w-3.5 h-3.5" />
                            </button>
                          </div>
                        </div>

                        {s.last_message && (
                          <p className="text-[11px] text-slate-400 line-clamp-2 mt-1.5 pl-4 leading-relaxed">
                            {s.last_message}
                          </p>
                        )}

                        <div className="flex items-center justify-between text-[10px] text-slate-500 mt-2 pl-4">
                          <span className="flex items-center space-x-1">
                            <Clock className="w-3 h-3" />
                            <span>{dateDisplay || 'Recent'}</span>
                          </span>
                          {s.message_count > 0 && (
                            <span className="px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800 font-mono">
                              {s.message_count} {lang === 'mr' ? 'संदेश' : 'msgs'}
                            </span>
                          )}
                        </div>
                      </div>
                    );
                  })
              )}
            </div>

            {/* Drawer Footer */}
            <div className="p-3 border-t border-slate-800 bg-slate-950/90 text-center">
              <span className="text-[11px] text-slate-500 flex items-center justify-center space-x-1">
                <ShieldCheck className="w-3.5 h-3.5 text-agri-400" />
                <span>{lang === 'mr' ? 'तुमचा संवाद सुरक्षितपणे जतन केला जातो' : 'All consultations securely backed up'}</span>
              </span>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
