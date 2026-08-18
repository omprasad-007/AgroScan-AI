import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { Bot, User, Send, Search, Sparkles, Sprout, AlertCircle, RefreshCw, X, Loader2, RotateCcw, Download } from 'lucide-react';
import api from '../services/api';

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

  // Session & Message State
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [lastFailedMessage, setLastFailedMessage] = useState(null);
  const [chatError, setChatError] = useState(null);
  const chatEndRef = useRef(null);

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
    // Generate fresh session ID when active scan or plant changes
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
                content: t('assistant.state_c_healthy', { crop: data.crop_detected || 'Plant' }) || `Your latest scan identified ${data.crop_detected || 'Plant'}. No disease was detected in this scan. Ask me about preventive care or seasonal management.`
              }]);
            } else {
              setMessages([{
                sender: 'assistant',
                content: t('assistant.state_c_scan', {
                  crop: data.crop_detected || 'Crop',
                  disease: data.disease_name || 'Healthy',
                  severity: data.severity_level || 'Normal',
                  confidence: Math.round((data.confidence_score || 0.95) * 100)
                }) || `Identified ${data.crop_detected || 'Crop'} with suspected ${data.disease_name || 'Disease'} (${Math.round((data.confidence_score || 0.95) * 100)}% confidence). Ask me about danger, treatment options, spread prevention, or weather impact.`
              }]);
            }
          }
        })
        .catch(() => {
          setContextMode('none');
          setScanData(null);
          setMessages([{ sender: 'assistant', content: t('assistant.state_a_welcome') || "Welcome to AgroScan AI Agronomist! Ask any question about crop health, diseases, organic remedies, or seasonal farm care." }]);
        });
    } else {
      setContextMode('none');
      setScanData(null);
      setMessages([{ sender: 'assistant', content: t('assistant.state_a_welcome') || "Welcome to AgroScan AI Agronomist! Ask any question about crop health, diseases, organic remedies, or seasonal farm care." }]);
    }
  }, [predictionId, lang, t]);

  // Handle Manual Plant Selection
  const handleSelectManualPlant = (plantName) => {
    setSelectedPlant(plantName);
    setPlantSearch('');
    setShowSearchModal(false);
    setContextMode('manual');
    setScanData(null);

    // Reset conversation history for the new plant to prevent cross-plant context bleed
    setSessionId(`session_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`);
    setMessages([{
      sender: 'assistant',
      content: t('assistant.state_b_manual', { plant: plantName }) || `You have selected ${plantName}. I am ready to advise you on ${plantName} cultivation practices, soil nutrition, irrigation intervals, common fungal diseases, and harvesting guidance. What would you like to know?`
    }]);
  };

  // Dynamic Suggested Questions based on Active Context & Language
  const getDynamicQuickReplies = () => {
    if (contextMode === 'scan' && scanData) {
      const isHealthy = (scanData.disease_name || '').toLowerCase().includes('healthy');
      const cropLabel = translateCrop(scanData.crop_detected);
      const diseaseLabel = translateDisease(scanData.disease_name);

      if (lang === 'mr') {
        if (isHealthy) {
          return [
            `${cropLabel} चे आरोग्य चांगले कसे ठेवावे?`,
            `${cropLabel} साठी सर्वोत्तम सेंद्रिय खते कोणती?`,
            `${cropLabel} साठी योग्य सिंचन वेळापत्रक काय आहे?`,
            `हंगामातील संभाव्य किडींपासून संरक्षण कसे करावे?`
          ];
        }
        return [
          `हा रोग मानवांसाठी किंवा खाण्यासाठी धोकादायक आहे का?`,
          `${diseaseLabel} वर कोणते प्रभावी उपचार करावेत?`,
          `हा रोग इतर ${cropLabel} पिकांवर कसा पसरू शकतो?`,
          `यासाठी कोणते सेंद्रिय कीटकनाशक वापरावे?`
        ];
      }

      if (isHealthy) {
        return [
          `How to keep my ${scanData.crop_detected} healthy?`,
          `Best organic fertilizers for ${scanData.crop_detected}`,
          `Recommended irrigation schedule for ${scanData.crop_detected}`,
          `Common seasonal pests to watch for`
        ];
      }
      return [
        `Is this dangerous to human health or produce?`,
        `How do I treat ${scanData.disease_name}?`,
        `Will this spread to my other ${scanData.crop_detected} plants?`,
        `What organic bio-sprays work best for this?`
      ];
    }

    if (contextMode === 'manual' && selectedPlant) {
      const plantLabel = translateCrop(selectedPlant);
      if (lang === 'mr') {
        return [
          `${plantLabel} साठी कोणती माती व हवामान उत्तम आहे?`,
          `${plantLabel} चे उत्पादन वाढवण्यासाठी सेंद्रिय खते कोणती?`,
          `${plantLabel} साठी किती सिंचन आवश्यक आहे?`,
          `${plantLabel} मधील मुख्य रोग व कीड कोणती?`,
          `${plantLabel} ची काढणी कधी करावी?`
        ];
      }
      return [
        `What soil and climate is best for ${selectedPlant}?`,
        `What organic fertilizers boost ${selectedPlant} yield?`,
        `How much irrigation is required for ${selectedPlant}?`,
        `What are common diseases in ${selectedPlant}?`,
        `How long does ${selectedPlant} take to harvest?`
      ];
    }

    if (lang === 'mr') {
      return [
        "करपा रोग खाण्यासाठी धोकादायक आहे का?",
        "सेंद्रिय कंपोस्ट खत कसे तयार करावे?",
        "एकात्मिक कीड व्यवस्थापन (IPM) काय आहे?",
        "ठिबक सिंचनासाठी कोणती पिके योग्य आहेत?",
        "बुरशीजन्य रोग कसा रोखावा?"
      ];
    }

    return [
      "Is leaf blight dangerous to eat?",
      "How to prepare organic bio-compost?",
      "What is Integrated Pest Management (IPM)?",
      "Which crops suit Drip Irrigation?",
      "How to prevent fungal leaf spot?"
    ];
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const sendMessage = async (textToSend) => {
    if (!textToSend.trim() || loading) return;

    const userText = textToSend.trim();
    setInput('');
    setChatError(null);
    setLastFailedMessage(null);

    // 1. Build conversation history from all prior turns
    const historyPayload = messages.map(m => ({
      role: m.sender === 'user' ? 'user' : 'assistant',
      content: m.content
    }));

    // 2. Add current message to UI
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

    console.log('AgroScan AI Outgoing Chat Payload:', payload);

    try {
      const res = await api.post('/chat', payload);
      if (res.data && res.data.content) {
        if (res.data.session_id) {
          setSessionId(res.data.session_id);
        }
        setMessages(prev => [...prev, { sender: 'assistant', content: res.data.content }]);
      } else {
        throw new Error('Empty response from AI assistant');
      }
    } catch (err) {
      console.warn('Chat request error:', err);
      setLastFailedMessage(userText);
      setChatError(t('assistant.error_generic') || 'Failed to get answer from AI advisor. Please check your connection and try again.');
    } finally {
      setLoading(false);
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

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-6rem)] relative overflow-hidden glass-panel rounded-2xl border border-slate-800 shadow-2xl">
      
      {/* Context Header */}
      <div className="bg-slate-900/90 border-b border-slate-800 p-4 shrink-0 shadow-sm z-10 space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center space-x-2">
            <Bot className="w-5 h-5 text-agri-400" />
            <h2 className="text-sm sm:text-base font-bold text-white">
              {t('assistant.title') || 'AgroScan AI Advisor'}
            </h2>
            <span className="px-2 py-0.5 rounded-full bg-agri-500/10 border border-agri-500/30 text-[10px] font-bold text-agri-400 uppercase">
              {contextMode === 'scan' ? (t('assistant.context_scan') || 'Scan Context') : contextMode === 'manual' ? (t('assistant.context_manual') || 'Plant Mode') : (t('assistant.context_none') || 'General Advisory')}
            </span>
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
                  md += `### ${msg.sender === 'user' ? (lang === 'mr' ? 'शेतकरी' : 'Farmer') : (lang === 'mr' ? 'AgroScan AI कृषी सल्लागार' : 'AgroScan AI Advisor')}\n${msg.content}\n\n`;
                });
                // Prefix with UTF-8 BOM (\uFEFF) to prevent mojibake in text viewers
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
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 border border-slate-700 flex items-center space-x-1.5 transition disabled:opacity-50"
              title="Export conversation history"
            >
              <Download className="w-3.5 h-3.5" />
              <span>{lang === 'mr' ? 'संवाद जतन करा' : 'Export Chat'}</span>
            </button>

            <button
              type="button"
              onClick={() => setShowSearchModal(true)}
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-bold text-slate-200 border border-slate-700 flex items-center space-x-1.5 transition"
            >
              <Sprout className="w-3.5 h-3.5 text-agri-400" />
              <span>{t('assistant.change_plant') || 'Change Plant'}</span>
            </button>

            {/* Language Switch */}
            <div className="flex bg-slate-950 rounded-xl p-1 border border-slate-800 text-xs font-bold">
              <button
                type="button"
                onClick={() => setLang('en')}
                className={`px-3 py-1 rounded-lg transition ${
                  lang === 'en' ? 'bg-agri-500 text-slate-950 shadow font-bold' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                EN
              </button>
              <button
                type="button"
                onClick={() => setLang('mr')}
                className={`px-3 py-1 rounded-lg transition ${
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
          <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between text-xs">
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
              {lang === 'mr' ? 'बहु-टप्प्यांचा कृषी सल्ला' : 'Multi-turn cultivation care advisory'}
            </span>
          </div>
        )}
      </div>

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 pb-40">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex gap-3 max-w-[90%] ${msg.sender === 'user' ? 'ml-auto justify-end' : ''}`}
          >
            {msg.sender === 'assistant' && (
              <div className="w-9 h-9 rounded-full bg-agri-500/20 text-agri-400 flex items-center justify-center shrink-0 border border-agri-500/40">
                <Bot className="w-5 h-5" />
              </div>
            )}

            <div className={`flex flex-col gap-1 ${msg.sender === 'user' ? 'items-end' : ''}`}>
              <span className="text-[11px] font-medium text-slate-400">
                {msg.sender === 'user' ? (lang === 'mr' ? 'तुम्ही (शेतकरी)' : 'You') : (lang === 'mr' ? 'AgroScan AI कृषी सल्लागार' : 'AgroScan AI Advisor')}
              </span>
              
              <div
                className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-agri-500 text-slate-950 font-semibold rounded-tr-none shadow-lg shadow-agri-500/20'
                    : 'bg-slate-900/90 border border-slate-800 text-slate-200 rounded-tl-none shadow-sm'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            </div>
          </div>
        ))}

        {/* Loading / Thinking Indicator */}
        {loading && (
          <div className="flex gap-3 items-center p-2 text-xs text-agri-400 font-semibold">
            <div className="w-9 h-9 rounded-full bg-agri-500/20 text-agri-400 flex items-center justify-center shrink-0 border border-agri-500/40">
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

      {/* Input Area (Fixed at bottom) */}
      <div className="absolute bottom-0 w-full bg-slate-900 border-t border-slate-800 p-3 shadow-2xl z-20">
        {/* Dynamic Quick Reply Suggestions */}
        <div className="flex overflow-x-auto gap-2 pb-2.5 hide-scrollbar">
          {getDynamicQuickReplies().map((qr, i) => (
            <button
              key={i}
              type="button"
              disabled={loading}
              onClick={() => sendMessage(qr)}
              className="whitespace-nowrap px-3.5 py-1.5 bg-slate-950 border border-slate-800 rounded-full text-xs font-semibold text-slate-300 hover:bg-slate-800 hover:text-white transition shrink-0 disabled:opacity-50"
            >
              {qr}
            </button>
          ))}
        </div>

        <form onSubmit={handleFormSubmit} className="flex items-center gap-2">
          <input
            type="text"
            value={input}
            disabled={loading}
            onChange={(e) => setInput(e.target.value)}
            placeholder={loading ? (lang === 'mr' ? 'AI उत्तराची वाट पाहत आहे...' : "Waiting for AI response...") : (t('assistant.placeholder_input') || "Ask a question about this crop or disease...")}
            className="flex-1 h-11 px-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-agri-500 placeholder:text-slate-500 disabled:opacity-50"
          />

          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="w-11 h-11 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 flex items-center justify-center font-bold shadow-lg shadow-agri-500/20 shrink-0 disabled:opacity-50 transition"
            aria-label="Send Message"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin text-slate-950" /> : <Send className="w-4 h-4" />}
          </button>
        </form>
      </div>

      {/* Plant Search & Change Modal */}
      {showSearchModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel p-6 rounded-2xl max-w-md w-full space-y-4 border border-slate-700">
            <div className="flex justify-between items-center">
              <h3 className="text-base font-bold text-white">{t('assistant.type_select_plant') || 'Select Crop for Advisory'}</h3>
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
