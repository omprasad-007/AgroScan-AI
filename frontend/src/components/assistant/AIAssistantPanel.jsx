import React, { useState, useEffect, useRef } from 'react';
import { 
  Bot, Send, Download, Sparkles, BookOpen, Maximize2, 
  Minimize2, Mic, MicOff, RotateCcw, Sprout, ArrowUpRight
} from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import { FormattedAIMessage } from './FormattedAIMessage';
import api from '../../services/api';

/**
 * AIAssistantPanel
 * Full-featured, spacious AI Agronomist consultation panel.
 * Embedded directly in scan results and diagnosis dashboards with 
 * context awareness, rich markdown formatting, and bilingual speech/audio.
 */
export const AIAssistantPanel = ({ scanData, predictionId, autoOpen = true }) => {
  const { lang, setLang, t, translateCrop, translateDisease } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [isListening, setIsListening] = useState(false);

  const chatEndRef = useRef(null);
  const recognitionRef = useRef(null);

  // Initialize Speech Recognition once
  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recognition = new SpeechRecognition();
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = lang === 'mr' ? 'mr-IN' : 'en-US';

      recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        if (transcript) {
          setInput(prev => (prev ? `${prev} ${transcript}` : transcript));
        }
        setIsListening(false);
      };

      recognition.onerror = () => setIsListening(false);
      recognition.onend = () => setIsListening(false);
      recognitionRef.current = recognition;
    }
  }, [lang]);

  // Initial Pre-seeded Context Greeting
  useEffect(() => {
    if (scanData) {
      const rawCrop = scanData.crop_detected || scanData.plant || 'Crop';
      const rawDisease = scanData.disease_name || scanData.disease || 'Healthy';
      const plant = translateCrop(rawCrop);
      const disease = translateDisease(rawDisease);
      const isHealthy = rawDisease.toLowerCase().includes('healthy') || rawDisease.toLowerCase().includes('no disease') || scanData.status === 'HEALTHY' || Boolean(scanData.healthy_status);

      let greeting = '';
      if (lang === 'mr') {
        greeting = isHealthy
          ? `मी पाहत आहे की हे **${plant}** चे झाड निरोगी आहे (कोणताही रोग आढळला नाही). खत व्यवस्थापन, पाणी देणे किंवा पिकाच्या काळजीबद्दल काहीही विचारा.`
          : `मी पाहत आहे की **${plant}** वर **${disease}** चे लक्षण आढळले आहे. सेंद्रिय उपचार, फवारणीचे प्रमाण किंवा प्रतिबंधात्मक उपायांबद्दल विचारू शकता.`;
      } else {
        greeting = isHealthy
          ? `I see this is **${plant}** with no disease detected — ask me anything about care, watering, or fertilizing.`
          : `I see this is **${plant}** with **${disease}** detected — ask me anything about organic remedies, chemical options, or prevention.`;
      }

      setMessages([{ 
        sender: 'assistant', 
        content: greeting, 
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      }]);
    } else {
      const welcome = lang === 'mr' 
        ? "नमस्कार! मी तुमचा ॲग्रोस्कॅन AI कृषी सल्लागार आहे. पिकांच्या आरोग्याबद्दल किंवा रोगाबद्दल प्रश्न विचारा."
        : "Hello! I am your AgroScan AI Agronomist. Ask me anything about crop diseases, remedies, or farming guidance.";
      setMessages([{ 
        sender: 'assistant', 
        content: welcome, 
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      }]);
    }
  }, [scanData, lang, translateCrop, translateDisease]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle Speech Recognition Toggle
  const toggleListening = () => {
    if (!recognitionRef.current) {
      alert(lang === 'mr' ? 'आपल्या ब्राउझरमध्ये व्हॉइस इनपुट उपलब्ध नाही.' : 'Voice recognition is not supported in this browser.');
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      recognitionRef.current.lang = lang === 'mr' ? 'mr-IN' : 'en-US';
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch {
        setIsListening(false);
      }
    }
  };

  const handleSendMessage = async (textToSend) => {
    const query = (textToSend || input).trim();
    if (!query || loading) return;

    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setInput('');
    setMessages(prev => [...prev, { sender: 'user', content: query, timestamp: timeStr }]);
    setLoading(true);

    try {
      const res = await api.post('/chat', {
        message: query,
        prediction_id: predictionId || (scanData ? scanData.id : undefined),
        language: lang
      });

      const botContent = res.data?.answer || res.data?.content || (
        lang === 'mr'
          ? "माहिती प्राप्त झाली. पिकाचे नियमित निरीक्षण ठेवा."
          : "Consultation response generated. Please scout your foliage regularly."
      );

      setMessages(prev => [...prev, { 
        sender: 'assistant', 
        content: botContent,
        sources: res.data?.sources || [],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      }]);
    } catch (err) {
      setMessages(prev => [...prev, { 
        sender: 'assistant', 
        content: lang === 'mr' 
          ? "माफ करा, सेवा सध्या व्यस्त आहे. कृपया पुन्हा प्रयत्न करा." 
          : "Service is temporarily unavailable. Please try again shortly.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) 
      }]);
    } finally {
      setLoading(false);
    }
  };

  // Export Chat with UTF-8 BOM to guarantee zero mojibake in Marathi
  const handleExportChat = () => {
    if (messages.length === 0) return;

    const plantName = scanData?.crop_detected || scanData?.plant || 'Crop';
    const diseaseName = scanData?.disease_name || scanData?.disease || 'N/A';
    const confidence = scanData?.confidence_score ? `${(scanData.confidence_score * 100).toFixed(1)}%` : 'N/A';
    const dateStr = new Date().toISOString().split('T')[0];

    let md = `# AgroScan AI — Field Chat & Advisory Report\n\n`;
    md += `**Date**: ${dateStr}\n`;
    md += `**Plant**: ${plantName}\n`;
    md += `**Disease / Status**: ${diseaseName}\n`;
    md += `**Confidence**: ${confidence}\n`;
    md += `**Language**: ${lang === 'mr' ? 'मराठी' : 'English'}\n`;
    md += `--------------------------------------------------\n\n`;

    messages.forEach((msg) => {
      const label = msg.sender === 'user' ? (lang === 'mr' ? 'शेतकरी' : 'Farmer') : (lang === 'mr' ? 'AgroScan AI कृषी सल्लागार' : 'AgroScan AI Agronomist');
      md += `### ${label} (${msg.timestamp || 'N/A'})\n${msg.content}\n\n`;
    });

    const blob = new Blob(["\uFEFF" + md], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    const cleanPlant = plantName.toLowerCase().replace(/[^a-z0-9]/g, '_');
    link.href = url;
    link.setAttribute('download', `agroscan-chat-${cleanPlant}-${dateStr}.md`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const getQuickReplies = () => {
    if (scanData) {
      const rawCrop = scanData.crop_detected || scanData.plant || 'Crop';
      const rawDisease = scanData.disease_name || scanData.disease || '';
      const plant = translateCrop(rawCrop);
      const disease = translateDisease(rawDisease);
      const isHealthy = rawDisease.toLowerCase().includes('healthy');

      if (lang === 'mr') {
        if (isHealthy) {
          return [
            `${plant} ची काळजी कशी घ्यावी?`,
            `${plant} साठी सर्वोत्तम सेंद्रिय खत कोणते?`,
            `${plant} साठी पाणी देण्याचे वेळापत्रक`,
            `रोग प्रतिबंधक उपाय`
          ];
        }
        return [
          `${disease} ची लक्षणे व तीव्रता`,
          `${disease} वर सेंद्रिय उपाय काय आहेत?`,
          `${disease} साठी रासायनिक फवारणी व प्रमाण`,
          `हा रोग इतर झाडांवर पसरू नये म्हणून काय करावे?`
        ];
      }

      if (isHealthy) {
        return [
          `How to care for ${rawCrop}?`,
          `Best organic fertilizers for ${rawCrop}`,
          `Watering schedule for ${rawCrop}`,
          `Prevent common ${rawCrop} diseases`
        ];
      }
      return [
        `Symptoms of ${rawDisease}`,
        `Organic treatment for ${rawDisease}`,
        `Chemical spray & dosage for ${rawDisease}`,
        `How to prevent ${rawDisease} spread`
      ];
    }

    if (lang === 'mr') {
      return [
        "टोमॅटो करपा रोगावर सेंद्रिय फवारणी कोणती?",
        "निंबोळी अर्क (Neem Oil) वापरण्याचे प्रमाण किती?",
        "कपाशीवरील कीड नियंत्रणासाठी उपाय",
        "ऊस पिकासाठी ठिबक सिंचन वेळापत्रक"
      ];
    }

    return [
      "Organic cure for tomato early blight",
      "Correct Neem Oil spray dilution (ppm)",
      "Pest control tips for cotton crops",
      "Drip irrigation schedule for sugarcane"
    ];
  };

  return (
    <div 
      className={`agro-panel rounded-3xl border border-agro-border shadow-2xl overflow-hidden flex flex-col bg-agro-card backdrop-blur-xl transition-all duration-300 ${
        isExpanded ? 'min-h-[720px] h-[750px]' : 'min-h-[520px] h-[560px]'
      }`}
    >
      
      {/* Panel Header */}
      <div className="bg-gradient-to-r from-agro-primary via-[#C94427] to-agro-accent border-b border-agro-border p-4 sm:p-5 flex items-center justify-between shrink-0 text-white">
        <div className="flex items-center space-x-3">
          <div className="relative w-10 h-10 rounded-2xl bg-white/20 text-white flex items-center justify-center shadow-lg border border-white/30">
            <Bot className="w-5 h-5" />
            <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-agro-highlight border-2 border-agro-primary animate-pulse" />
          </div>
          <div>
            <h3 className="font-heading text-sm sm:text-base font-extrabold text-white flex items-center space-x-2">
              <span>{t('assistant.title') || (lang === 'mr' ? 'ॲग्रोस्कॅन AI कृषी सल्लागार' : 'AgroScan AI Agronomist')}</span>
              <span className="px-2 py-0.5 rounded-full bg-white/20 text-white text-[10px] uppercase font-bold border border-white/30 tracking-wider">
                {lang === 'mr' ? 'थेट AI' : 'Live AI'}
              </span>
            </h3>
            <p className="text-[11px] sm:text-xs text-white/80">
              {lang === 'mr' ? 'भारतीय शेतकऱ्यांसाठी वैज्ञानिक व सेंद्रिय कृषी सल्ला' : 'Contextual agronomic & diagnostic guidance for farmers'}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {/* Export Chat Button */}
          <button
            type="button"
            onClick={handleExportChat}
            disabled={messages.length === 0}
            className="px-3 py-1.5 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-cream text-xs font-bold border border-agro-border flex items-center space-x-1.5 transition disabled:opacity-50"
            title="Export full chat transcript as Markdown (.md)"
          >
            <Download className="w-3.5 h-3.5 text-agro-highlight" />
            <span className="hidden sm:inline">{lang === 'mr' ? 'संवाद जतन करा' : 'Export Chat'}</span>
          </button>

          {/* Expand / Minimize Toggle */}
          <button
            type="button"
            onClick={() => setIsExpanded(prev => !prev)}
            className="p-2 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-cream border border-agro-border transition"
            title={isExpanded ? 'Collapse size' : 'Expand size'}
          >
            {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>

          {/* Language Toggle */}
          <div className="flex bg-agro-surface rounded-xl p-0.5 border border-agro-border text-[11px] font-bold">
            <button
              type="button"
              onClick={() => setLang('en')}
              className={`px-2.5 py-1 rounded-lg transition ${lang === 'en' ? 'bg-agro-primary text-white font-bold' : 'text-agro-muted hover:text-agro-cream'}`}
            >
              EN
            </button>
            <button
              type="button"
              onClick={() => setLang('mr')}
              className={`px-2.5 py-1 rounded-lg transition ${lang === 'mr' ? 'bg-agro-primary text-white font-bold' : 'text-agro-muted hover:text-agro-cream'}`}
            >
              मराठी
            </button>
          </div>
        </div>
      </div>

      {/* Messages Feed */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4 bg-agro-bg">
        {messages.map((msg, i) => (
          <div 
            key={i} 
            className={`flex gap-3 max-w-[92%] sm:max-w-[85%] ${msg.sender === 'user' ? 'ml-auto justify-end' : ''}`}
          >
            {msg.sender === 'assistant' && (
              <div className="w-8 h-8 rounded-2xl bg-agro-accent/15 text-agro-accent flex items-center justify-center shrink-0 border border-agro-accent/30 shadow-sm mt-0.5">
                <Bot className="w-4 h-4" />
              </div>
            )}
            
            <div className={`flex flex-col gap-1 ${msg.sender === 'user' ? 'items-end' : ''}`}>
              <div
                className={`p-4 rounded-3xl text-xs sm:text-sm leading-relaxed shadow-sm ${
                  msg.sender === 'user'
                    ? 'bg-agro-primary text-white font-medium rounded-tr-none shadow-orange-glow'
                    : 'bg-agro-card border border-agro-border text-agro-cream rounded-tl-none'
                }`}
              >
                <FormattedAIMessage
                  content={msg.content}
                  sender={msg.sender}
                  sources={msg.sources}
                  timestamp={msg.timestamp}
                  lang={lang}
                />
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-center space-x-3 p-3 rounded-2xl bg-agro-surface border border-agro-border text-agro-primary text-xs sm:text-sm font-semibold animate-pulse w-fit">
            <Sparkles className="w-4 h-4 animate-spin text-agro-primary" />
            <span>{t('assistant.thinking') || (lang === 'mr' ? 'कृषी सल्लागार विश्लेषण करत आहे...' : 'AI Agronomist is analyzing symptoms & weather data...')}</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Quick Replies & Input */}
      <div className="p-3 sm:p-4 bg-agro-card border-t border-agro-border space-y-3 shrink-0">
        <div className="flex overflow-x-auto gap-2 pb-1 hide-scrollbar">
          <span className="text-[11px] font-bold text-agro-highlight uppercase tracking-wider shrink-0 flex items-center gap-1">
            <Sprout className="w-3.5 h-3.5" />
            {lang === 'mr' ? 'सुचवलेले प्रश्न:' : 'Suggested:'}
          </span>
          {getQuickReplies().map((qr, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSendMessage(qr)}
              className="whitespace-nowrap px-3.5 py-1.5 bg-agro-card border border-agro-border rounded-full text-xs font-medium text-agro-cream hover:bg-agro-primary/20 hover:text-agro-primary transition shrink-0"
            >
              {qr}
            </button>
          ))}
        </div>

        <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(input); }} className="flex gap-2">
          {/* Voice Input Microphone */}
          <button
            type="button"
            onClick={toggleListening}
            className={`w-11 h-11 rounded-2xl flex items-center justify-center shrink-0 border transition ${
              isListening
                ? 'bg-rose-500/20 text-rose-400 border-rose-500 animate-pulse'
                : 'bg-agro-card text-agro-muted hover:text-agro-primary border border-agro-border'
            }`}
            title={isListening ? 'Stop listening' : 'Voice input'}
          >
            {isListening ? <MicOff className="w-4 h-4 text-rose-400" /> : <Mic className="w-4 h-4" />}
          </button>

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t('assistant.placeholder_input') || (lang === 'mr' ? "पिकांबद्दल काहीही विचारा (उदा. औषध प्रमाण, रोग लक्षणे, खत)..." : "Ask AgroScan AI about crop care, dosages, organic remedies...")}
            className="flex-1 h-11 px-4 rounded-2xl bg-agro-surface border border-agro-border text-xs sm:text-sm text-agro-cream focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary placeholder:text-agro-muted transition"
          />

          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="px-5 h-11 rounded-2xl bg-agro-primary hover:bg-agro-primaryHover text-white font-bold text-xs sm:text-sm flex items-center justify-center shrink-0 disabled:opacity-40 transition-all shadow-md shadow-orange-glow active:scale-95"
            title="Send"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

    </div>
  );
};
