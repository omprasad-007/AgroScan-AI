import React, { useState, useEffect, useRef } from 'react';
import { 
  Bot, Send, X, Sparkles, MessageCircle, Maximize2, 
  RotateCcw, Download, Mic, MicOff, Volume2, 
  ChevronDown, HelpCircle, Sprout, ArrowUpRight
} from 'lucide-react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguage } from '../../context/LanguageContext';
import { FormattedAIMessage } from './FormattedAIMessage';
import api from '../../services/api';

/**
 * FloatingAIChatbot
 * Persistent, global floating AI Agronomist chatbot widget.
 * Available across all pages for instant farming advice, crop diagnosis questions,
 * organic remedies, pesticide dosages, and weather guidance in English and Marathi.
 */
export const FloatingAIChatbot = () => {
  const { lang, setLang, t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  if (location.pathname === '/assistant') {
    return null;
  }

  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [hasUnread, setHasUnread] = useState(false);
  
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

  // Initial Welcome Greeting
  useEffect(() => {
    if (messages.length === 0) {
      const welcomeMsg = lang === 'mr'
        ? `**नमस्कार शेतकरी बंधूंनो!** मी तुमचा **ॲग्रोस्कॅन AI कृषी सल्लागार** आहे.\n\nतुम्ही मला पिकांचे रोग, सेंद्रिय औषधोपचार, खत व्यवस्थापन, किंवा फवारणीच्या प्रमाणाबद्दल काहीही विचारू शकता. खालीलपैकी एका प्रश्नावर क्लिक करा किंवा खाली थेट टाईप करा:`
        : `**Hello Farmer!** I am your **AgroScan AI Agronomist**.\n\nAsk me anything about plant disease diagnosis, organic remedies, chemical dosages, irrigation schedules, or crop nutrition. Tap a quick question below or type your inquiry:`;

      setMessages([{
        sender: 'assistant',
        content: welcomeMsg,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    }
  }, [lang]);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    if (isOpen && !isMinimized) {
      chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen, isMinimized]);

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

  // Send Message
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
        language: lang
      });

      const botReply = res.data?.answer || res.data?.content || (
        lang === 'mr' 
          ? "माहिती यशस्वीरीत्या प्राप्त झाली. पिकाचे नियमित निरीक्षण करा." 
          : "Guidance retrieved. Continue regular crop monitoring."
      );

      setMessages(prev => [...prev, {
        sender: 'assistant',
        content: botReply,
        sources: res.data?.sources || [],
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } catch (err) {
      setMessages(prev => [...prev, {
        sender: 'assistant',
        content: lang === 'mr'
          ? "माफ करा, सर्व्हर तात्पुरता व्यस्त आहे. कृपया काही क्षणांनंतर पुन्हा प्रयत्न करा."
          : "The agronomy service is momentarily busy. Please try again in a few moments.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } finally {
      setLoading(false);
    }
  };

  // Quick Action Chips
  const quickQuestions = lang === 'mr' ? [
    'टोमॅटो करपा रोगावर सेंद्रिय उपाय काय?',
    'निंबोळी अर्क (Neem Oil) फवारणीचे योग्य प्रमाण',
    'कपाशीवरील पांढऱ्या माशीवर नियंत्रण कसे करावे?',
    'ऊस तांबेरा व लाल कुज रोगाची लक्षणे',
    'ठिबक सिंचनाने पाणी देण्याचे वेळापत्रक'
  ] : [
    'How to cure tomato early blight organically?',
    'What is the correct Neem Oil spray ratio (ppm)?',
    'Quick organic remedy for cotton whiteflies',
    'Sugarcane red rot symptoms and control',
    'Optimal drip irrigation schedule for vegetables'
  ];

  // Export full chat transcript
  const handleExportChat = () => {
    if (messages.length === 0) return;
    const dateStr = new Date().toISOString().split('T')[0];
    let md = `# AgroScan AI — Field Advisory Transcript\n\n`;
    md += `**Date**: ${dateStr}\n`;
    md += `**Language**: ${lang === 'mr' ? 'मराठी' : 'English'}\n`;
    md += `==============================================\n\n`;

    messages.forEach((msg) => {
      const label = msg.sender === 'user' ? (lang === 'mr' ? 'शेतकरी' : 'Farmer') : (lang === 'mr' ? 'ॲग्रोस्कॅन AI कृषी सल्लागार' : 'AgroScan AI Agronomist');
      md += `### ${label} (${msg.timestamp || ''})\n${msg.content}\n\n`;
    });

    const blob = new Blob(["\uFEFF" + md], { type: 'text/markdown;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `agroscan-advisory-${dateStr}.md`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Reset conversation
  const handleResetChat = () => {
    const welcomeMsg = lang === 'mr'
      ? `**नमस्कार!** नवा सल्ला सत्र सुरू झाले आहे. पिकांच्या कोणत्याही समस्येबाबत विचारा:`
      : `**Hello!** New consultation session started. Ask any question about crop health:`;

    setMessages([{
      sender: 'assistant',
      content: welcomeMsg,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }]);
  };

  return (
    <>
      {/* 1. Floating Action Button (FAB) */}
      {!isOpen && (
        <div className="fixed bottom-20 md:bottom-8 right-5 md:right-8 z-50 flex items-center gap-3">
          {/* Pulsing Hint Pill */}
          <div 
            onClick={() => { setIsOpen(true); setHasUnread(false); }}
            className="hidden sm:flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-white/95 dark:bg-slate-900/90 text-slate-800 dark:text-slate-100 border border-slate-200 dark:border-emerald-500/40 shadow-xl backdrop-blur-md cursor-pointer hover:border-emerald-500 transition group animate-fade-in"
          >
            <Sparkles className="w-4 h-4 text-emerald-500 dark:text-emerald-400 group-hover:rotate-12 transition-transform" />
            <span className="text-xs font-bold tracking-wide">
              {lang === 'mr' ? 'AI कृषी सल्लागार' : 'Ask AI Agronomist'}
            </span>
            <span className="w-2 h-2 rounded-full bg-agro-primary animate-pulse" />
          </div>

          {/* Glowing Circular FAB */}
          <button
            type="button"
            onClick={() => { setIsOpen(true); setHasUnread(false); }}
            className="relative w-14 h-14 rounded-full bg-gradient-to-tr from-agro-primary via-[#C94427] to-agro-accent text-white flex items-center justify-center shadow-2xl shadow-orange-glow hover:scale-105 active:scale-95 transition-all border-2 border-white/20 group"
            title={lang === 'mr' ? 'AI कृषी सल्लागार उघडा' : 'Open AI Agronomist Chat'}
          >
            <Bot className="w-7 h-7 text-white group-hover:scale-110 transition-transform" />
            <span className="absolute -top-1 -right-1 flex h-4 w-4">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-agro-highlight opacity-75" />
              <span className="relative inline-flex rounded-full h-4 w-4 bg-agro-highlight border-2 border-white dark:border-agro-card" />
            </span>
          </button>
        </div>
      )}

      {/* 2. Floating Chat Drawer / Window */}
      {isOpen && (
        <div 
          className={`fixed bottom-20 md:bottom-8 right-4 md:right-8 z-50 w-[94vw] sm:w-[460px] md:w-[500px] flex flex-col rounded-3xl overflow-hidden shadow-2xl border border-agro-border bg-agro-card text-agro-cream backdrop-blur-2xl transition-all duration-300 animate-slide-up ${
            isMinimized ? 'h-16' : 'h-[640px] max-h-[85vh]'
          }`}
        >
          {/* Header */}
          <div className="p-4 bg-gradient-to-r from-agro-primary via-[#C94427] to-agro-accent border-b border-agro-border flex items-center justify-between shrink-0 select-none text-white">
            <div className="flex items-center gap-3">
              <div className="relative w-9 h-9 rounded-2xl bg-white/20 text-white flex items-center justify-center shadow-md border border-white/30">
                <Bot className="w-5 h-5 text-white" />
                <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-agro-highlight border-2 border-agro-primary animate-pulse" />
              </div>
              <div>
                <h3 className="font-heading text-sm font-extrabold flex items-center gap-2 text-white">
                  <span>{lang === 'mr' ? 'ॲग्रोस्कॅन AI कृषी सल्लागार' : 'AgroScan AI Agronomist'}</span>
                  <span className="px-2 py-0.5 rounded-full bg-white/20 text-white border border-white/30 text-[10px] font-bold uppercase tracking-wider">
                    {lang === 'mr' ? 'थेट' : 'Live'}
                  </span>
                </h3>
                <p className="text-[11px] text-white/80">
                  {lang === 'mr' ? 'पिकांचे रोग, खते व फवारणी सल्ला' : 'Crop pathology, dosages & farm remedies'}
                </p>
              </div>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-1.5">
              {/* Language Switcher */}
              <div className="flex bg-black/20 dark:bg-black/40 rounded-xl p-0.5 border border-white/20 text-[10px] font-bold">
                <button
                  type="button"
                  onClick={() => setLang('en')}
                  className={`px-2 py-0.5 rounded-lg transition ${lang === 'en' ? 'bg-white text-emerald-800 font-extrabold dark:bg-emerald-500 dark:text-white' : 'text-white/80 hover:text-white'}`}
                >
                  EN
                </button>
                <button
                  type="button"
                  onClick={() => setLang('mr')}
                  className={`px-2 py-0.5 rounded-lg transition ${lang === 'mr' ? 'bg-white text-emerald-800 font-extrabold dark:bg-emerald-500 dark:text-white' : 'text-white/80 hover:text-white'}`}
                >
                  मराठी
                </button>
              </div>

              {/* Fullpage View */}
              <button
                type="button"
                onClick={() => { setIsOpen(false); navigate('/assistant'); }}
                className="p-1.5 rounded-xl hover:bg-white/20 text-white transition"
                title={lang === 'mr' ? 'संपूर्ण स्क्रीनवर उघडा' : 'Expand to full page'}
              >
                <Maximize2 className="w-4 h-4" />
              </button>

              {/* Reset Session */}
              <button
                type="button"
                onClick={handleResetChat}
                className="p-1.5 rounded-xl hover:bg-white/20 text-white transition"
                title={lang === 'mr' ? 'नवे सत्र सुरू करा' : 'New consultation session'}
              >
                <RotateCcw className="w-4 h-4" />
              </button>

              {/* Minimize / Expand Toggle */}
              <button
                type="button"
                onClick={() => setIsMinimized(prev => !prev)}
                className="p-1.5 rounded-xl hover:bg-white/20 text-white transition"
                title={isMinimized ? 'Expand' : 'Minimize'}
              >
                <ChevronDown className={`w-4 h-4 transition-transform ${isMinimized ? 'rotate-180' : ''}`} />
              </button>

              {/* Close */}
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-xl hover:bg-rose-500/30 text-white hover:text-rose-200 transition"
                title="Close"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Body (Messages Feed + Quick Prompts) */}
          {!isMinimized && (
            <>
              {/* Message Feed */}
              <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-agro-surface">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex gap-3 max-w-[92%] ${msg.sender === 'user' ? 'ml-auto justify-end' : ''}`}
                  >
                    {msg.sender === 'assistant' && (
                      <div className="w-8 h-8 rounded-2xl bg-agro-accent/15 text-agro-accent flex items-center justify-center shrink-0 border border-agro-accent/30 shadow-sm mt-0.5">
                        <Bot className="w-4 h-4" />
                      </div>
                    )}

                    <div className={`flex flex-col gap-1 ${msg.sender === 'user' ? 'items-end' : ''}`}>
                      <div
                        className={`p-4 rounded-3xl text-xs sm:text-sm leading-relaxed shadow-md ${
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

                {/* Animated Thinking State */}
                {loading && (
                  <div className="flex items-center gap-3 p-3 rounded-2xl bg-agro-surface border border-agro-border text-agro-primary text-xs font-semibold animate-pulse w-fit">
                    <Sparkles className="w-4 h-4 animate-spin text-agro-primary" />
                    <span>{lang === 'mr' ? 'कृषी सल्लागार विश्लेषण करत आहे...' : 'AI Agronomist is analyzing remedies & dosages...'}</span>
                  </div>
                )}

                <div ref={chatEndRef} />
              </div>

              {/* Quick Prompt Carousel */}
              <div className="px-3 py-2 bg-white dark:bg-slate-900/80 border-t border-slate-200 dark:border-white/[0.06] flex items-center gap-2 overflow-x-auto hide-scrollbar">
                <span className="text-[10px] font-bold text-emerald-600 dark:text-emerald-400 uppercase tracking-wider shrink-0 flex items-center gap-1">
                  <Sprout className="w-3 h-3" />
                  {lang === 'mr' ? 'सुचवलेले:' : 'Quick:'}
                </span>
                {quickQuestions.map((q, qIdx) => (
                  <button
                    key={qIdx}
                    type="button"
                    onClick={() => handleSendMessage(q)}
                    className="whitespace-nowrap px-3 py-1 rounded-full bg-slate-100 dark:bg-slate-800 hover:bg-emerald-50 dark:hover:bg-emerald-500/20 border border-slate-200 dark:border-white/[0.08] text-[11px] text-slate-700 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400 transition shrink-0 font-medium"
                  >
                    {q}
                  </button>
                ))}
              </div>

              {/* Input Area */}
              <div className="p-3 bg-white dark:bg-slate-900 border-t border-slate-200 dark:border-white/[0.06]">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    handleSendMessage();
                  }}
                  className="flex items-center gap-2"
                >
                  {/* Voice Dictation Button */}
                  <button
                    type="button"
                    onClick={toggleListening}
                    className={`w-10 h-10 rounded-2xl flex items-center justify-center shrink-0 border transition ${
                      isListening
                        ? 'bg-rose-500/20 text-rose-500 border-rose-500 animate-pulse'
                        : 'bg-slate-100 dark:bg-slate-800/80 text-slate-600 dark:text-slate-300 hover:text-emerald-600 dark:hover:text-emerald-400 border-slate-200 dark:border-white/[0.08]'
                    }`}
                    title={isListening ? 'Stop listening' : 'Speak your question'}
                  >
                    {isListening ? <MicOff className="w-4 h-4 text-rose-500" /> : <Mic className="w-4 h-4" />}
                  </button>

                  {/* Text Input */}
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder={
                      isListening
                        ? (lang === 'mr' ? 'ऐकत आहे... बोला' : 'Listening... Speak now')
                        : (lang === 'mr' ? 'पिकांबद्दल काहीही विचारा (उदा. खते, रोग, फवारणी)...' : 'Ask about crop care, organic sprays, dosages...')
                    }
                    className="flex-1 h-10 px-4 rounded-2xl bg-agro-surface border border-agro-border text-xs sm:text-sm text-agro-cream focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary transition placeholder:text-agro-muted"
                  />

                  {/* Send Button */}
                  <button
                    type="submit"
                    disabled={!input.trim() || loading}
                    className="w-10 h-10 rounded-2xl bg-agro-primary hover:bg-agro-primaryHover text-white flex items-center justify-center shrink-0 shadow-md shadow-orange-glow disabled:opacity-40 transition-all active:scale-95"
                    title="Send"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </form>

                {/* Subtitle / Disclaimer */}
                <div className="flex items-center justify-between mt-2 px-1 text-[10px] text-agro-muted">
                  <span className="flex items-center gap-1">
                    <Sparkles className="w-3 h-3 text-agro-highlight" />
                    <span>{lang === 'mr' ? 'कृषी तज्ज्ञ संदर्भयुक्त AI' : 'Expert Grounded Agricultural AI'}</span>
                  </span>
                  <button
                    type="button"
                    onClick={handleExportChat}
                    className="hover:text-agro-primary transition underline"
                  >
                    {lang === 'mr' ? 'संवाद सेव्ह करा' : 'Save Transcript'}
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      )}
    </>
  );
};
