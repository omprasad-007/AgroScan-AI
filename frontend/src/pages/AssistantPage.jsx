import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import { Bot, User, Send, Search, Sparkles, Sprout, AlertCircle, RefreshCw } from 'lucide-react';
import api from '../services/api';

export const AssistantPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { lang, setLang, t } = useLanguage();
  const predictionId = searchParams.get('predictionId');

  // Context States: 'none' | 'manual' | 'scan' | 'no_plant'
  const [contextMode, setContextMode] = useState('none');
  const [scanData, setScanData] = useState(null);
  const [selectedPlant, setSelectedPlant] = useState('');
  const [plantSearch, setPlantSearch] = useState('');

  const availablePlants = [
    'Mango', 'Sugarcane', 'Tomato', 'Neem', 'Rice', 'Wheat',
    'Cotton', 'Potato', 'Chilli', 'Onion', 'Guava', 'Papaya',
    'Banana', 'Soybean', 'Maize', 'Turmeric', 'Ginger', 'Grape'
  ];

  const filteredPlants = availablePlants.filter(p =>
    p.toLowerCase().includes(plantSearch.toLowerCase())
  );

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Initialize Assistant Messages based on Context State
  useEffect(() => {
    if (predictionId) {
      api.get(`/predictions/${predictionId}`)
        .then(res => {
          const data = res.data;
          if (data.is_plant === false || data.disease_code === 'non_plant') {
            setContextMode('no_plant');
            setMessages([{
              sender: 'assistant',
              content: t('assistant.state_d_noplant')
            }]);
          } else {
            setContextMode('scan');
            setScanData(data);
            setMessages([{
              sender: 'assistant',
              content: t('assistant.state_c_scan', {
                crop: data.crop_detected || 'Crop',
                disease: data.disease_name || 'Healthy',
                severity: data.severity_level || 'Normal',
                confidence: Math.round((data.confidence_score || 0.95) * 100)
              })
            }]);
          }
        })
        .catch(() => {
          setContextMode('none');
          setMessages([{ sender: 'assistant', content: t('assistant.state_a_welcome') }]);
        });
    } else {
      setContextMode('none');
      setMessages([{ sender: 'assistant', content: t('assistant.state_a_welcome') }]);
    }
  }, [predictionId, lang]);

  // Handle Manual Plant Selection
  const handleSelectManualPlant = (plantName) => {
    setSelectedPlant(plantName);
    setPlantSearch('');
    setContextMode('manual');
    setMessages([{
      sender: 'assistant',
      content: t('assistant.state_b_manual', { plant: plantName })
    }]);
  };

  // Dynamic Suggested Questions based on Active Context
  const getDynamicQuickReplies = () => {
    if (contextMode === 'scan' && scanData) {
      return [
        `How to treat ${scanData.disease_name}?`,
        `Preventive measures for ${scanData.crop_detected}`,
        `What fertilizer works best for ${scanData.crop_detected}?`,
        `Explain treatment in Marathi`
      ];
    }
    if (contextMode === 'manual' && selectedPlant) {
      return [
        `What disease affects ${selectedPlant} leaves?`,
        `How much water does ${selectedPlant} need?`,
        `Best soil and climate for ${selectedPlant}`,
        `Pest management for ${selectedPlant}`
      ];
    }
    return [
      "How to prepare organic bio-compost?",
      "What is Integrated Pest Management (IPM)?",
      "Which crops suit Drip Irrigation?",
      "How to prevent fungal leaf spot?"
    ];
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (textToSend) => {
    if (!textToSend.trim() || loading) return;

    const userText = textToSend.trim();
    setInput('');
    setMessages(prev => [...prev, { sender: 'user', content: userText }]);
    setLoading(true);

    try {
      const res = await api.post('/chat', {
        message: userText,
        prediction_id: predictionId || undefined,
        manual_plant: contextMode === 'manual' ? selectedPlant : undefined,
        language: lang
      });
      setMessages(prev => [...prev, { sender: 'assistant', content: res.data.content }]);
    } catch (err) {
      const fallbackTopic = contextMode === 'manual' ? selectedPlant : (scanData?.crop_detected || 'Crop');
      setMessages(prev => [...prev, {
        sender: 'assistant',
        content: `**AgroScan AI Agronomist (${fallbackTopic} Guidance)**:\n\n- **Organic Treatment**: Apply neem oil spray (5ml/L water) or compost tea solution every 7-10 days.\n- **Preventive Care**: Ensure adequate spacing between plants to maintain canopy aeration.\n- **Soil & Moisture**: Irrigate at root zone during morning hours to prevent leaf wetness.`
      }]);
    } finally {
      setLoading(false);
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
              {t('assistant.title')}
            </h2>
            <span className="px-2 py-0.5 rounded-full bg-agri-500/10 border border-agri-500/30 text-[10px] font-bold text-agri-400 uppercase">
              {contextMode === 'scan' ? t('assistant.context_scan') : contextMode === 'manual' ? t('assistant.context_manual') : t('assistant.context_none')}
            </span>
          </div>

          <div className="flex items-center space-x-2">
            {/* Language Switch */}
            <div className="flex bg-slate-950 rounded-xl p-1 border border-slate-800 text-xs font-bold">
              <button
                type="button"
                onClick={() => setLang('en')}
                className={`px-3 py-1 rounded-lg transition ${
                  lang === 'en' ? 'bg-agri-500 text-slate-950 shadow' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                EN
              </button>
              <button
                type="button"
                onClick={() => setLang('mr')}
                className={`px-3 py-1 rounded-lg transition ${
                  lang === 'mr' ? 'bg-agri-500 text-slate-950 shadow' : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                मराठी
              </button>
            </div>
          </div>
        </div>

        {/* Manual Plant Selection Dropdown */}
        <div className="relative">
          <div className="flex items-center space-x-2 bg-slate-950 px-3 py-2 rounded-xl border border-slate-800 text-xs">
            <Search className="w-4 h-4 text-slate-500 shrink-0" />
            <input
              type="text"
              value={plantSearch}
              onChange={(e) => setPlantSearch(e.target.value)}
              placeholder={t('assistant.search_placeholder')}
              className="bg-transparent text-slate-200 w-full focus:outline-none placeholder:text-slate-600"
            />
            {selectedPlant && (
              <span className="px-2 py-0.5 rounded bg-agri-500/20 text-agri-400 font-bold shrink-0">
                Selected: {selectedPlant}
              </span>
            )}
          </div>

          {plantSearch.trim().length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-1 bg-slate-900 border border-slate-800 rounded-xl shadow-2xl z-50 max-h-48 overflow-y-auto">
              {filteredPlants.map((plant) => (
                <button
                  key={plant}
                  type="button"
                  onClick={() => handleSelectManualPlant(plant)}
                  className="w-full text-left px-4 py-2.5 text-xs text-slate-200 hover:bg-slate-800 flex items-center space-x-2 border-b border-slate-800/50"
                >
                  <Sprout className="w-3.5 h-3.5 text-agri-400" />
                  <span>{plant}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Chat Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 pb-36">
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
                {msg.sender === 'user' ? 'You' : 'AgroScan AI Assistant'}
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

        {loading && (
          <div className="flex gap-2 text-xs text-agri-400 font-semibold items-center animate-pulse p-2">
            <Bot className="w-4 h-4 animate-spin" />
            <span>{t('assistant.thinking')}</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Input Area (Fixed at bottom) */}
      <div className="absolute bottom-0 w-full bg-slate-900 border-t border-slate-800 p-3 shadow-2xl">
        {/* Dynamic Quick Reply Suggestions */}
        <div className="flex overflow-x-auto gap-2 pb-2.5 hide-scrollbar">
          {getDynamicQuickReplies().map((qr, i) => (
            <button
              key={i}
              type="button"
              onClick={() => sendMessage(qr)}
              className="whitespace-nowrap px-3.5 py-1.5 bg-slate-950 border border-slate-800 rounded-full text-xs font-semibold text-slate-300 hover:bg-slate-800 hover:text-white transition shrink-0"
            >
              {qr}
            </button>
          ))}
        </div>

        <form onSubmit={handleFormSubmit} className="flex items-center gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t('assistant.placeholder_input')}
            className="flex-1 h-11 px-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-agri-500 placeholder:text-slate-500"
          />

          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="w-11 h-11 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 flex items-center justify-center font-bold shadow-lg shadow-agri-500/20 shrink-0 disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

    </div>
  );
};
