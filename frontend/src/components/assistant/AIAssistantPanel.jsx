import React, { useState, useEffect, useRef } from 'react';
import { Bot, Send, Download, Sparkles, BookOpen } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import api from '../../services/api';

export const AIAssistantPanel = ({ scanData, predictionId, autoOpen = true }) => {
  const { lang, setLang, t, translateCrop, translateDisease } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Initial Pre-seeded Context Greeting
  useEffect(() => {
    if (scanData) {
      const rawCrop = scanData.crop_detected || scanData.plant || 'Crop';
      const rawDisease = scanData.disease_name || scanData.disease || 'Healthy';
      const plant = translateCrop(rawCrop);
      const disease = translateDisease(rawDisease);
      const isHealthy = rawDisease.toLowerCase().includes('healthy') || rawDisease.toLowerCase().includes('no disease');

      let greeting = '';
      if (lang === 'mr') {
        greeting = isHealthy
          ? `मी पाहत आहे की हे **${plant}** चे झाड निरोगी आहे (कोणताही रोग आढळला नाही). खत व्यवस्थापन, पाणी देणे किंवा पिकाच्या काळजीबद्दल काहीही विचारा.`
          : `मी पाहत आहे की **${plant}** वर **${disease}** चे लक्षण आढळले आहे. सेंद्रिय उपचार, फवारणीचे प्रमाण किंवा प्रतिबंधात्मक उपायांबद्दल विचारू शकता.`;
      } else {
        greeting = isHealthy
          ? `I see this is **${rawCrop}** with no disease detected — ask me anything about care, watering, or fertilizing.`
          : `I see this is **${rawCrop}** with **${rawDisease}** detected — ask me anything about organic remedies, chemical options, or prevention.`;
      }

      setMessages([{ sender: 'assistant', content: greeting, timestamp: new Date().toLocaleTimeString() }]);
    } else {
      const welcome = lang === 'mr' 
        ? "नमस्कार! मी तुमचा ॲग्रोस्कॅन AI कृषी सल्लागार आहे. पिकांच्या आरोग्याबद्दल किंवा रोगाबद्दल प्रश्न विचारा."
        : "Hello! I am your AgroScan AI Agronomist. Ask me anything about crop diseases, remedies, or farming guidance.";
      setMessages([{ sender: 'assistant', content: welcome, timestamp: new Date().toLocaleTimeString() }]);
    }
  }, [scanData, lang, translateCrop, translateDisease]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async (textToSend) => {
    if (!textToSend.trim() || loading) return;

    const userText = textToSend.trim();
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    setInput('');
    setMessages(prev => [...prev, { sender: 'user', content: userText, timestamp: timeStr }]);
    setLoading(true);

    try {
      const res = await api.post('/chat', {
        message: userText,
        prediction_id: predictionId || (scanData ? scanData.id : undefined),
        language: lang
      });

      const botContent = res.data.answer || res.data.content;
      setMessages(prev => [...prev, { 
        sender: 'assistant', 
        content: botContent,
        sources: res.data.sources || [],
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

    let md = `# AgroScan AI — Chat & Advisory Report\n\n`;
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
          `${disease} वर सेंद्रिय उपाय`,
          `${disease} साठी रासायनिक फवारणी`,
          `हा रोग कसा रोखावा?`
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
        `Chemical options for ${rawDisease}`,
        `How to prevent ${rawDisease}`
      ];
    }

    if (lang === 'mr') {
      return [
        "सेंद्रिय कंपोस्ट खत कसे बनवावे?",
        "ठिबक सिंचन मार्गदर्शन",
        "कीड नियंत्रण टिप्स",
        "माती परीक्षण माहिती"
      ];
    }

    return [
      "How to make organic compost?",
      "Drip irrigation guidance",
      "Pest control tips",
      "Soil testing advice"
    ];
  };

  return (
    <div className="agro-panel rounded-2xl border border-agro-border shadow-2xl overflow-hidden flex flex-col">
      
      {/* Panel Header */}
      <div className="bg-agro-surface/90 border-b border-agro-border p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-agro-primary/20 text-agro-primary flex items-center justify-center border border-agro-primary/30">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-agro-cream flex items-center space-x-2">
              <span>{t('assistant.title') || 'AgroScan AI Agronomist'}</span>
              <span className="px-2 py-0.5 rounded-full bg-agro-primary/10 text-agro-primary text-[10px] uppercase font-bold border border-agro-primary/20">
                {lang === 'mr' ? 'थेट AI' : 'Live AI'}
              </span>
            </h3>
            <p className="text-[11px] text-agro-muted">
              {lang === 'mr' ? 'भारतीय शेतकऱ्यांसाठी संदर्भयुक्त कृषी मार्गदर्शन' : 'Contextual guidance for Indian smallholder farmers'}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {/* Export Chat Button */}
          <button
            type="button"
            onClick={handleExportChat}
            disabled={messages.length === 0}
            className="px-3 py-1.5 rounded-lg bg-agro-surface hover:bg-agro-hover text-agro-cream text-xs font-bold border border-agro-border flex items-center space-x-1.5 transition disabled:opacity-50"
            title="Export full chat transcript as Markdown (.md)"
          >
            <Download className="w-3.5 h-3.5 text-agro-primary" />
            <span>{lang === 'mr' ? 'संवाद जतन करा' : 'Export Chat'}</span>
          </button>

          {/* Language Toggle */}
          <div className="flex bg-agro-bg rounded-lg p-1 border border-agro-border text-[11px] font-bold">
            <button
              type="button"
              onClick={() => setLang('en')}
              className={`px-2 py-0.5 rounded transition ${lang === 'en' ? 'bg-agro-primary text-white font-bold' : 'text-agro-muted hover:text-agro-cream'}`}
            >
              EN
            </button>
            <button
              type="button"
              onClick={() => setLang('mr')}
              className={`px-2 py-0.5 rounded transition ${lang === 'mr' ? 'bg-agro-primary text-white font-bold' : 'text-agro-muted hover:text-agro-cream'}`}
            >
              मराठी
            </button>
          </div>
        </div>
      </div>

      {/* Messages Feed */}
      <div className="p-4 space-y-4 max-h-96 overflow-y-auto bg-agro-bg/50">
        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-3 max-w-[90%] ${msg.sender === 'user' ? 'ml-auto justify-end' : ''}`}>
            {msg.sender === 'assistant' && (
              <div className="w-7 h-7 rounded-full bg-agro-primary/20 text-agro-primary flex items-center justify-center shrink-0 border border-agro-primary/30">
                <Bot className="w-4 h-4" />
              </div>
            )}
            <div className={`flex flex-col gap-1 ${msg.sender === 'user' ? 'items-end' : ''}`}>
              <div
                className={`p-3.5 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white font-semibold rounded-tr-none shadow-md shadow-emerald-500/20'
                    : 'bg-white dark:bg-slate-900/90 border border-slate-200 dark:border-white/[0.08] text-slate-800 dark:text-slate-100 rounded-tl-none shadow-sm'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>

                {/* Multi-Source Research Citations */}
                {msg.sender === 'assistant' && msg.sources && msg.sources.length > 0 && (
                  <div className="mt-2.5 pt-2 border-t border-slate-200 dark:border-white/[0.08] space-y-1.5">
                    <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 flex items-center gap-1.5">
                      <BookOpen className="w-3 h-3" />
                      <span>{lang === 'mr' ? 'तपासलेले संदर्भ (Sources):' : 'Verified Evidence & Sources:'}</span>
                    </span>
                    <div className="flex flex-col gap-1">
                      {msg.sources.map((src, sIdx) => (
                        <a
                          key={sIdx}
                          href={src.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-[10px] text-slate-600 dark:text-slate-400 hover:text-emerald-600 dark:hover:text-emerald-400 underline truncate transition"
                        >
                          • [{src.source}] {src.title}
                        </a>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex items-center space-x-2 text-xs text-agro-primary font-semibold animate-pulse">
            <Sparkles className="w-4 h-4 animate-spin" />
            <span>{t('assistant.thinking') || 'Thinking...'}</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Quick Replies & Input */}
      <div className="p-3 bg-agro-surface border-t border-agro-border space-y-2">
        <div className="flex overflow-x-auto gap-2 pb-1 hide-scrollbar">
          {getQuickReplies().map((qr, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSendMessage(qr)}
              className="whitespace-nowrap px-3 py-1 bg-agro-bg border border-agro-border rounded-full text-xs font-medium text-agro-muted hover:bg-agro-hover hover:text-agro-cream transition shrink-0"
            >
              {qr}
            </button>
          ))}
        </div>

        <form onSubmit={(e) => { e.preventDefault(); handleSendMessage(input); }} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t('assistant.placeholder_input') || (lang === 'mr' ? "पिकांबद्दल काहीही विचारा..." : "Ask AgroScan AI about crop care, dosage, or remedies...")}
            className="flex-1 h-10 px-3.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary placeholder:text-agro-muted/60 transition"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="px-4 h-10 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white font-bold text-xs flex items-center justify-center shrink-0 disabled:opacity-50 transition shadow-md shadow-agro-primary/20 active:scale-95"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

    </div>
  );
};
