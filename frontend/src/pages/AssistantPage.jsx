import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

export const AssistantPage = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { lang, setLang, t } = useLanguage();
  const predictionId = searchParams.get('predictionId');

  const [scanContext, setScanContext] = useState({
    crop: 'Tomato',
    disease: 'Early Blight',
    severity: 'Moderate',
    risk: 'High'
  });

  const [messages, setMessages] = useState([
    {
      sender: 'assistant',
      content: "I see you've scanned a Tomato plant showing signs of Early Blight. The weather forecast indicates high humidity over the next 48 hours, which will accelerate the spread.\n\nI recommend taking immediate action. What would you like to know first?",
      actionBtn: "Find Treatment Guides"
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  const quickReplies = [
    "How can I prevent this disease?",
    "Explain this in Marathi",
    "Why is my disease risk high?",
    "Should I monitor again?"
  ];

  useEffect(() => {
    if (predictionId) {
      api.get(`/predictions/${predictionId}`)
        .then(res => {
          const data = res.data;
          setScanContext({
            crop: data.crop_detected || 'Tomato',
            disease: data.disease_name || 'Early Blight',
            severity: data.severity_level || 'Moderate',
            risk: data.weather_risk_level || 'High'
          });
        })
        .catch(err => console.warn('Using default context'));
    }
  }, [predictionId]);

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
        prediction_id: predictionId || undefined
      });
      setMessages(prev => [...prev, { sender: 'assistant', content: res.data.content }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        sender: 'assistant',
        content: 'Immediate Steps for Early Blight:\n• Remove and destroy infected lower leaves immediately to slow the spread.\n• Apply a copper-based fungicide or chlorothalonil spray before the rain begins tomorrow.\n• Ensure good air circulation around the plants by avoiding overcrowding.'
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
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-6rem)] relative overflow-hidden bg-surface rounded-2xl border border-outline-variant shadow-xl">
      
      {/* Context Header */}
      <div className="bg-surface-container-low border-b border-outline-variant p-4 shrink-0 shadow-sm z-10">
        <div className="flex items-center justify-between mb-3">
          <h2 className="text-base font-semibold text-on-surface flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>smart_toy</span>
            <span>Scan Context</span>
          </h2>
          <div className="flex bg-surface rounded-lg p-1 border border-outline-variant">
            <button
              onClick={() => setLang('en')}
              className={`px-3 py-1 text-xs font-semibold rounded-md transition-colors ${
                lang === 'en' ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:bg-surface-container'
              }`}
            >
              EN
            </button>
            <button
              onClick={() => setLang('mr')}
              className={`px-3 py-1 text-xs font-semibold rounded-md transition-colors ${
                lang === 'mr' ? 'bg-primary-container text-on-primary-container' : 'text-on-surface-variant hover:bg-surface-container'
              }`}
            >
              MR
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
          <div className="bg-surface p-2.5 rounded-lg border border-outline-variant flex items-center gap-2">
            <span className="material-symbols-outlined text-primary text-base">yard</span>
            <span className="text-on-surface-variant">Crop: <strong className="text-on-surface">{scanContext.crop}</strong></span>
          </div>

          <div className="bg-error-container/40 p-2.5 rounded-lg border border-error-container flex items-center gap-2">
            <span className="material-symbols-outlined text-error text-base">coronavirus</span>
            <span className="text-on-error-container">Disease: <strong>{scanContext.disease}</strong></span>
          </div>

          <div className="bg-tertiary-container/30 p-2.5 rounded-lg border border-tertiary-container/40 flex items-center gap-2">
            <span className="material-symbols-outlined text-tertiary text-base">warning</span>
            <span className="text-on-tertiary-container">Severity: <strong>{scanContext.severity}</strong></span>
          </div>

          <div className="bg-error-container/40 p-2.5 rounded-lg border border-error-container flex items-center gap-2">
            <span className="material-symbols-outlined text-error text-base">thunderstorm</span>
            <span className="text-on-error-container">Risk: <strong>{scanContext.risk}</strong></span>
          </div>
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
              <div className="w-9 h-9 rounded-full bg-primary-container flex items-center justify-center shrink-0 shadow-sm border border-primary">
                <span className="material-symbols-outlined text-on-primary-container text-lg" style={{ fontVariationSettings: "'FILL' 1" }}>
                  smart_toy
                </span>
              </div>
            )}

            <div className={`flex flex-col gap-1 ${msg.sender === 'user' ? 'items-end' : ''}`}>
              <span className="text-[11px] font-medium text-on-surface-variant">
                {msg.sender === 'user' ? 'You' : 'AgroScan AI Assistant'}
              </span>
              
              <div
                className={`p-4 rounded-xl shadow-sm text-sm leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-primary text-on-primary rounded-tr-none'
                    : 'bg-surface border border-outline-variant text-on-surface rounded-tl-none'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>

                {msg.actionBtn && (
                  <button
                    onClick={() => navigate('/results/pred_001')}
                    className="mt-3 w-full h-11 bg-primary hover:bg-agri-700 text-on-primary rounded-lg font-medium text-xs flex items-center justify-center gap-2 transition-transform active:scale-95 shadow"
                  >
                    <span className="material-symbols-outlined text-base">local_pharmacy</span>
                    <span>{msg.actionBtn}</span>
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex gap-2 text-xs text-primary font-medium items-center animate-pulse p-2">
            <span className="material-symbols-outlined text-base" style={{ fontVariationSettings: "'FILL' 1" }}>smart_toy</span>
            <span>AgroScan AI Assistant is thinking...</span>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Input Area (Fixed at bottom) */}
      <div className="absolute bottom-0 w-full bg-surface-container border-t border-outline-variant p-3 shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.1)]">
        {/* Suggested Quick Replies */}
        <div className="flex overflow-x-auto gap-2 pb-2.5 hide-scrollbar">
          {quickReplies.map((qr, i) => (
            <button
              key={i}
              onClick={() => sendMessage(qr)}
              className="whitespace-nowrap px-3.5 py-1.5 bg-surface border border-outline-variant rounded-full text-xs font-medium text-on-surface hover:bg-surface-container-high transition-colors active:scale-95 shrink-0"
            >
              {qr}
            </button>
          ))}
        </div>

        <form onSubmit={handleFormSubmit} className="flex items-center gap-2">
          <div className="flex-1 relative">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask AI Assistant..."
              className="w-full h-12 pl-4 pr-10 rounded-xl bg-surface border border-outline text-xs text-on-surface focus:ring-2 focus:ring-primary focus:border-primary placeholder:text-on-surface-variant"
            />
            <button
              type="button"
              className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 flex items-center justify-center text-primary hover:bg-surface-container-high rounded-full transition-transform"
            >
              <span className="material-symbols-outlined text-xl">mic</span>
            </button>
          </div>

          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="w-12 h-12 rounded-xl bg-primary hover:bg-agri-700 text-on-primary flex items-center justify-center shadow-md active:scale-95 transition-transform shrink-0 disabled:opacity-50"
          >
            <span className="material-symbols-outlined text-xl" style={{ fontVariationSettings: "'FILL' 1" }}>send</span>
          </button>
        </form>
      </div>

    </div>
  );
};
