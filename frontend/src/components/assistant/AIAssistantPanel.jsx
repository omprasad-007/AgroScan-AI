import React, { useState, useEffect, useRef } from 'react';
import { Bot, Send, Download, Sparkles, RefreshCw } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import api from '../../services/api';

export const AIAssistantPanel = ({ scanData, predictionId, autoOpen = true }) => {
  const { lang, setLang, t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  // Initial Pre-seeded Context Greeting
  useEffect(() => {
    if (scanData) {
      const plant = scanData.crop_detected || scanData.plant || 'Crop';
      const disease = scanData.disease_name || scanData.disease || 'Healthy';
      const isHealthy = disease.toLowerCase().includes('healthy') || disease.toLowerCase().includes('no disease');

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

      setMessages([{ sender: 'assistant', content: greeting, timestamp: new Date().toLocaleTimeString() }]);
    } else {
      const welcome = lang === 'mr' 
        ? "नमस्कार! मी तुमचा ॲग्रोस्कॅन AI कृषी सल्लागार आहे. पिकांच्या आरोग्याबद्दल किंवा रोगाबद्दल प्रश्न विचारा."
        : "Hello! I am your AgroScan AI Agronomist. Ask me anything about crop diseases, remedies, or farming guidance.";
      setMessages([{ sender: 'assistant', content: welcome, timestamp: new Date().toLocaleTimeString() }]);
    }
  }, [scanData, lang]);

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

      setMessages(prev => [...prev, { 
        sender: 'assistant', 
        content: res.data.content, 
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

  // Phase 10: Export Chat as Markdown (.md)
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
    md += `--------------------------------------------------\n\n`;

    messages.forEach((msg) => {
      const label = msg.sender === 'user' ? 'You' : 'AgroScan AI Agronomist';
      md += `### ${label} (${msg.timestamp || 'N/A'})\n${msg.content}\n\n`;
    });

    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8;' });
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
      const plant = scanData.crop_detected || scanData.plant || 'Crop';
      const disease = scanData.disease_name || scanData.disease || '';
      const isHealthy = disease.toLowerCase().includes('healthy');

      if (isHealthy) {
        return [
          `How to care for ${plant}?`,
          `Best organic fertilizers for ${plant}`,
          `Watering schedule for ${plant}`,
          `Prevent common ${plant} diseases`
        ];
      }
      return [
        `Symptoms of ${disease}`,
        `Organic treatment for ${disease}`,
        `Chemical options for ${disease}`,
        `How to prevent ${disease}`
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
    <div className="glass-panel rounded-2xl border border-slate-800 shadow-2xl overflow-hidden flex flex-col">
      
      {/* Panel Header */}
      <div className="bg-slate-900/90 border-b border-slate-800 p-4 flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center border border-emerald-500/30">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white flex items-center space-x-2">
              <span>AgroScan AI Agronomist</span>
              <span className="px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-[10px] uppercase font-bold">Live AI</span>
            </h3>
            <p className="text-[11px] text-slate-400">Contextual guidance for Indian smallholder farmers</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {/* Export Chat Button (Phase 10) */}
          <button
            type="button"
            onClick={handleExportChat}
            disabled={messages.length === 0}
            className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 flex items-center space-x-1.5 transition disabled:opacity-50"
            title="Export full chat transcript as Markdown (.md)"
          >
            <Download className="w-3.5 h-3.5 text-emerald-400" />
            <span>Export Chat</span>
          </button>

          {/* Language Toggle */}
          <div className="flex bg-slate-950 rounded-lg p-1 border border-slate-800 text-[11px] font-bold">
            <button
              type="button"
              onClick={() => setLang('en')}
              className={`px-2 py-0.5 rounded transition ${lang === 'en' ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400'}`}
            >
              EN
            </button>
            <button
              type="button"
              onClick={() => setLang('mr')}
              className={`px-2 py-0.5 rounded transition ${lang === 'mr' ? 'bg-emerald-500 text-slate-950 font-bold' : 'text-slate-400'}`}
            >
              मराठी
            </button>
          </div>
        </div>
      </div>

      {/* Messages Feed */}
      <div className="p-4 space-y-4 max-h-96 overflow-y-auto bg-slate-950/40">
        {messages.map((msg, i) => (
          <div key={i} className={`flex gap-3 max-w-[90%] ${msg.sender === 'user' ? 'ml-auto justify-end' : ''}`}>
            {msg.sender === 'assistant' && (
              <div className="w-7 h-7 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0 border border-emerald-500/30">
                <Bot className="w-4 h-4" />
              </div>
            )}
            <div className={`flex flex-col gap-1 ${msg.sender === 'user' ? 'items-end' : ''}`}>
              <div
                className={`p-3.5 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-emerald-500 text-slate-950 font-semibold rounded-tr-none'
                    : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-none'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex items-center space-x-2 text-xs text-emerald-400 font-semibold animate-pulse">
            <Sparkles className="w-4 h-4 animate-spin" />
            <span>Thinking...</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Quick Replies & Input */}
      <div className="p-3 bg-slate-900 border-t border-slate-800 space-y-2">
        <div className="flex overflow-x-auto gap-2 pb-1 hide-scrollbar">
          {getQuickReplies().map((qr, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => handleSendMessage(qr)}
              className="whitespace-nowrap px-3 py-1 bg-slate-950 border border-slate-800 rounded-full text-xs font-medium text-slate-300 hover:bg-slate-800 hover:text-white transition shrink-0"
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
            placeholder={lang === 'mr' ? "पिकांबद्दल काहीही विचारा..." : "Ask AgroScan AI about crop care, dosage, or remedies..."}
            className="flex-1 h-10 px-3.5 rounded-xl bg-slate-950 border border-slate-800 text-xs text-white focus:outline-none focus:border-emerald-500 placeholder:text-slate-500"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="px-4 h-10 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs flex items-center justify-center shrink-0 disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>

    </div>
  );
};
