import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { 
  Bot, User, Send, Search, Sparkles, Sprout, AlertCircle, RefreshCw, 
  X, Loader2, RotateCcw, Download, Mic, MicOff, Volume2, VolumeX,
  HelpCircle, ShieldCheck, Droplets, Sun, Bug, Zap
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

// Client-Side Agronomist Knowledge Engine for zero-crash offline resilience
const generateClientAdvisory = (userQuery, ctx, lang = 'en') => {
  const q = (userQuery || '').toLowerCase();
  const crop = ctx?.crop_detected || ctx?.plantName || 'Crop';
  const disease = ctx?.disease_name || 'Plant Health';
  const isMr = lang === 'mr';

  if (q.includes('neem') || q.includes('निंबोळी') || q.includes('सेंद्रिय') || q.includes('organic') || q.includes('दशपर्णी')) {
    return isMr
      ? `🌱 **सेंद्रिय कीटकनाशक मार्गदर्शन (${crop}):**\n\n1. **निंबोळी अर्क (Neem Oil):** ५ मि.ली. निंबोळी तेल (१५०० ते ३००० ppm) प्रति लिटर पाण्यात १ मि.ली. लिक्विड सोप मिसळून संध्याकाळी फवारावे.\n2. **दशपर्णी अर्क:** २०० मि.ली. प्रति १५ लिटर पंपासाठी वापरल्यास रसशोषक किडींचे प्रभावी नियंत्रण होते.\n3. **ताक व हिंग फवारणी:** १०० मि.ली. आंबट ताक + ५ ग्रॅम हिंग प्रति पंप फवारल्यास बुरशी रोखली जाते.\n\n*टीप: तीव्र उन्हात फवारणी टाळावी, संध्याकाळी ४ नंतर फवारणी करावी.*`
      : `🌱 **Organic Bio-Remedy Guide (${crop}):**\n\n1. **Neem Oil Spray:** Mix 5ml cold-pressed Neem Oil (1500–3000 ppm) per 1 Liter water with 1ml liquid soap surfactant. Spray during early morning or late evening.\n2. **Dashaparni Ark:** Use 200ml per 15L spray pump for effective sucking pest & caterpillar deterrence.\n3. **Sour Buttermilk & Hing Spray:** 100ml fermented buttermilk + 5g asafetida per pump acts as a natural broad-spectrum bio-fungicide.\n\n*Best practice: Avoid spraying under intense midday sun to prevent leaf scorching.*`;
  }

  if (q.includes('danger') || q.includes('धोका') || q.includes('खाण्या') || q.includes('spread') || q.includes('पसर')) {
    return isMr
      ? `🛡️ **सुरक्षा व प्रसार माहिती (${crop} - ${disease}):**\n\n1. **मानवी सुरक्षितता:** वनस्पती बुरशी मानवांसाठी संसर्गजन्य नसते, परंतु रोगट भाग खाणे टाळावे.\n2. **प्रसार कसा रोखावा:**\n   - रोगट पाने त्वरित तोडून शेताबाहेर जाळून टाका.\n   - पाण्याचा तुषार वरून पानांवर पडू देऊ नका (ठिबक सिंचन वापरा).\n   - झाडांमधील अंतर योग्य ठेवा जेणेकरून हवा खेळती राहील.\n   - छाटणीची अवजारे जंतुनाशकाने स्वच्छ करा.`
      : `🛡️ **Safety & Outbreak Control (${crop} - ${disease}):**\n\n1. **Human & Produce Safety:** Plant fungal pathogens do not infect humans, but affected spoiled leaves/fruits should not be consumed.\n2. **Preventing Spread to Other Plants:**\n   - Prune and destroy infected leaves immediately away from the field.\n   - Transition to drip irrigation; avoid overhead sprinkler splashing which disperses spores.\n   - Ensure adequate inter-plant spacing for airflow and rapid foliage drying.\n   - Sanitize all pruning shears with 70% isopropyl alcohol after each plant.`;
  }

  if (q.includes('water') || q.includes('पाणी') || q.includes('सिंचन') || q.includes('irrigation') || q.includes('खत') || q.includes('fertilizer')) {
    return isMr
      ? `💧 **सिंचन व पोषण सल्ला (${crop}):**\n\n1. **पाण्याचे नियोजन:** जमिनीत कायम वाफसा (Moisture balance) राखावा. दलदल किंवा अतिपाणी दिल्यास मुळकुज आणि बुरशी वाढते.\n2. **सेंद्रिय पोषण:**\n   - एकरी २ टन चांगले कुजलेले शेणखत किंवा गांडूळ खत द्यावे.\n   - जीवामृत महिन्याला दोनदा ठिबक सिंचनातून सोडावे.\n   - सूक्ष्म अन्नद्रव्यांची (Micronutrients) कमतरता असल्यास चिलेटेड झिंक व बोरॉन फवारावे.`
      : `💧 **Irrigation & Soil Nutrition Advisory (${crop}):**\n\n1. **Water Management:** Maintain optimum field capacity (Vafsa condition). Overwatering promotes root rot (Pythium/Phytophthora) and foliar blights.\n2. **Soil Nutrition:**\n   - Apply 2 tons of well-decomposed Farm Yard Manure (FYM) or Vermicompost per acre.\n   - Supply Jeevamrut liquid organic formulation every 15 days through drip.\n   - Apply foliar spray of chelated Micronutrients (Zinc, Boron, Magnesium) during vegetative and flowering stages.`;
  }

  return isMr
    ? `🌾 **कृषी सल्लागार मार्गदर्शन (${crop} - ${disease}):**\n\n- **प्राथमिक काळजी:** पिकाचे नियमित निरीक्षण करा आणि पिवळी/रोगट पाने त्वरित काढून टाका.\n- **सेंद्रिय उपाय:** निंबोळी तेल (५ मि.ली./लिटर) किंवा ट्रायकोडर्मा व्हिरीडी (Trichoderma viride - ५ ग्रॅम/लिटर) जमिनीजवळ फवारा.\n- **रासायनिक पर्याय (तीव्रतेनुसार):** बुरशीनाशक म्हणून Copper Oxychloride ५०% WP (२.५ ग्रॅम/लिटर) किंवा Mancozeb ७५% WP (२ ग्रॅम/लिटर) चा वापर कृषी तज्ज्ञांच्या सल्ल्याने करा.\n\n*तुम्ही आणखी काही प्रश्न टाइप करून विचारू शकता.*`
    : `🌾 **Agronomist Advisory (${crop} - ${disease}):**\n\n- **Initial Action:** Inspect plants closely and prune yellowing/spotted leaves.\n- **Organic & Biological Control:** Apply cold-pressed Neem Oil (5ml/L) or *Trichoderma viride* bio-fungicide (5g/L) to the root zone and lower canopy.\n- **Chemical Options (If Severe):** Spray Copper Oxychloride 50% WP (2.5g/L) or Mancozeb 75% WP (2g/L) under agronomist guidance.\n\n*Feel free to type any specific question in the box below.*`;
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

  // Session & Message State
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [lastFailedMessage, setLastFailedMessage] = useState(null);
  const [chatError, setChatError] = useState(null);
  const [isOfflineMode, setIsOfflineMode] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [speakingMsgIdx, setSpeakingMsgIdx] = useState(null);
  const chatEndRef = useRef(null);
  const inputRef = useRef(null);
  const recognitionRef = useRef(null);

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

  // Initialize & Reset Assistant Messages when Context / Prediction ID / Plant changes
  useEffect(() => {
    setSessionId(`session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`);
    setChatError(null);
    setLastFailedMessage(null);

    if (predictionId) {
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
      setContextMode('none');
      setScanData(null);
      setMessages([{ sender: 'assistant', content: t('assistant.state_a_welcome') || "Welcome to AgroScan AI Agronomist! Type any question below regarding crop health, organic bio-sprays, diseases, fertilizers, or farm care." }]);
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
      if (res.data && res.data.content) {
        if (res.data.session_id) {
          setSessionId(res.data.session_id);
        }
        setMessages(prev => [...prev, { sender: 'assistant', content: res.data.content }]);
        setIsOfflineMode(false);
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
      setMessages(prev => [...prev, { sender: 'assistant', content: localReply }]);
      setIsOfflineMode(true);
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

          <div className="flex items-center space-x-2">
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
              <span className="hidden sm:inline">{lang === 'mr' ? 'संवाद जतन करा' : 'Export'}</span>
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
              </div>
            </div>

            {msg.sender === 'user' && (
              <div className="w-8 h-8 rounded-full bg-slate-800 text-slate-300 flex items-center justify-center shrink-0 border border-slate-700 mt-1">
                <User className="w-4 h-4" />
              </div>
            )}
          </div>
        ))}

        {/* Loading / Thinking Indicator */}
        {loading && (
          <div className="flex gap-3 items-center p-2 text-xs text-agri-400 font-semibold">
            <div className="w-8 h-8 rounded-full bg-agri-500/20 text-agri-400 flex items-center justify-center shrink-0 border border-agri-500/40">
              <Loader2 className="w-4 h-4 animate-spin text-agri-400" />
            </div>
            <div className="bg-slate-900/90 border border-slate-800 p-3 rounded-2xl text-slate-300 flex items-center space-x-2">
              <span className="inline-block w-2 h-2 rounded-full bg-agri-400 animate-ping mr-1"></span>
              <span>{t('assistant.thinking') || 'AgroScan AI is analyzing crop context & retrieving agronomy knowledge...'}</span>
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

    </div>
  );
};
