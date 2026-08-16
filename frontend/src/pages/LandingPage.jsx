import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { 
  Sprout, 
  Scan, 
  ShieldAlert, 
  Bot, 
  ArrowRight, 
  CheckCircle2, 
  Globe, 
  MapPin, 
  History, 
  ChevronRight, 
  MessageSquare, 
  Sparkles, 
  Menu, 
  X,
  FileCheck,
  Zap,
  Leaf
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';

export const LandingPage = () => {
  const { lang, toggleLanguage, t } = useLanguage();
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const handleScanClick = () => {
    if (isAuthenticated) {
      navigate('/scan');
    } else {
      navigate('/login?redirect=/scan');
    }
  };

  const scrollToSection = (id) => {
    setMobileMenuOpen(false);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between selection:bg-emerald-500 selection:text-slate-950">
      
      {/* 1. Header Navigation — Sticky on scroll */}
      <header className="sticky top-0 z-50 bg-slate-950/85 backdrop-blur-md border-b border-slate-800/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 sm:h-20">
            
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 via-emerald-500 to-emerald-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
                <Sprout className="w-6 h-6 text-slate-950" />
              </div>
              <div>
                <span className="text-lg font-bold text-white tracking-tight">
                  AgroScan <span className="text-emerald-400">AI</span>
                </span>
                <span className="block text-[10px] text-slate-400 font-medium tracking-wider uppercase">
                  {lang === 'mr' ? 'स्मार्ट पिके व रोग निदान' : 'Smart Agriculture & Diagnostics'}
                </span>
              </div>
            </Link>

            {/* Desktop Nav Links */}
            <nav className="hidden md:flex items-center space-x-8 text-sm font-semibold text-slate-300">
              <button 
                onClick={() => scrollToSection('how-it-works')} 
                className="hover:text-emerald-400 transition cursor-pointer"
              >
                {lang === 'mr' ? 'हे कसे कार्य करते' : 'How it Works'}
              </button>
              <button 
                onClick={() => scrollToSection('features')} 
                className="hover:text-emerald-400 transition cursor-pointer"
              >
                {lang === 'mr' ? 'वैशिष्ट्ये' : 'Features'}
              </button>
              <button 
                onClick={() => scrollToSection('ai-preview')} 
                className="hover:text-emerald-400 transition cursor-pointer"
              >
                {lang === 'mr' ? 'AI सहाय्यक' : 'AI Assistant'}
              </button>
            </nav>

            {/* Right Header Actions */}
            <div className="hidden md:flex items-center space-x-4">
              <button
                onClick={toggleLanguage}
                className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 text-xs font-semibold border border-slate-800 transition"
              >
                <Globe className="w-4 h-4 text-emerald-400" />
                <span>{lang === 'en' ? 'मराठी' : 'English'}</span>
              </button>

              {isAuthenticated ? (
                <Link
                  to="/dashboard"
                  className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 text-xs font-bold border border-slate-700 transition"
                >
                  {lang === 'mr' ? 'डॅशबोर्डवर जा' : 'Farm Dashboard'}
                </Link>
              ) : (
                <Link
                  to="/login"
                  className="px-4 py-2 rounded-xl text-xs font-bold text-slate-300 hover:text-white transition"
                >
                  {lang === 'mr' ? 'लॉगिन करा' : 'Sign In'}
                </Link>
              )}

              <button
                onClick={handleScanClick}
                className="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs transition shadow-lg shadow-emerald-500/20 flex items-center space-x-1.5"
              >
                <Scan className="w-4 h-4" />
                <span>{lang === 'mr' ? 'पीक स्कॅन करा' : 'Scan Your Plant'}</span>
              </button>
            </div>

            {/* Mobile Hamburger Button */}
            <div className="md:hidden flex items-center space-x-2">
              <button
                onClick={toggleLanguage}
                className="p-2 rounded-lg bg-slate-900 text-slate-300 text-xs font-bold border border-slate-800"
              >
                {lang === 'en' ? 'मराठी' : 'EN'}
              </button>
              <button
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="p-2 rounded-xl bg-slate-900 text-slate-300 border border-slate-800"
              >
                {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>

          </div>
        </div>

        {/* Mobile Menu Dropdown */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-slate-900 border-b border-slate-800 px-4 py-4 space-y-3">
            <button
              onClick={() => scrollToSection('how-it-works')}
              className="block w-full text-left py-2 text-sm font-semibold text-slate-300 hover:text-emerald-400"
            >
              {lang === 'mr' ? 'हे कसे कार्य करते' : 'How it Works'}
            </button>
            <button
              onClick={() => scrollToSection('features')}
              className="block w-full text-left py-2 text-sm font-semibold text-slate-300 hover:text-emerald-400"
            >
              {lang === 'mr' ? 'वैशिष्ट्ये' : 'Features'}
            </button>
            <button
              onClick={() => scrollToSection('ai-preview')}
              className="block w-full text-left py-2 text-sm font-semibold text-slate-300 hover:text-emerald-400"
            >
              {lang === 'mr' ? 'AI सहाय्यक' : 'AI Assistant'}
            </button>
            <div className="pt-2 border-t border-slate-800 flex flex-col gap-2">
              {!isAuthenticated && (
                <Link
                  to="/login"
                  className="w-full text-center py-2.5 rounded-xl bg-slate-800 text-slate-200 text-xs font-bold"
                >
                  {lang === 'mr' ? 'लॉगिन करा' : 'Sign In'}
                </Link>
              )}
              <button
                onClick={handleScanClick}
                className="w-full text-center py-2.5 rounded-xl bg-emerald-500 text-slate-950 font-extrabold text-xs flex items-center justify-center space-x-2"
              >
                <Scan className="w-4 h-4" />
                <span>{lang === 'mr' ? 'पीक स्कॅन करा' : 'Scan Your Plant'}</span>
              </button>
            </div>
          </div>
        )}
      </header>

      {/* 2. Hero Section */}
      <section className="relative overflow-hidden pt-12 sm:pt-20 pb-16 sm:pb-24">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-b from-emerald-500/15 via-emerald-600/5 to-transparent blur-3xl pointer-events-none" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          
          <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold mb-8 shadow-inner">
            <Sparkles className="w-3.5 h-3.5 text-emerald-400 animate-pulse" />
            <span>{lang === 'mr' ? 'कृत्रिम बुद्धिमत्ता आधारित पीक आरोग्य प्लॅटफॉर्म' : 'AI-Powered Plant Disease Diagnostic Platform'}</span>
          </div>

          {/* Headline (One sentence on what product does) */}
          <h1 className="text-4xl sm:text-6xl font-black tracking-tight text-white max-w-4xl mx-auto leading-[1.15]">
            {lang === 'mr' ? (
              <>तुमच्या पिकांवरील रोग आणि आरोग्याचे <span className="bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent">झटपट अचूक निदान</span></>
            ) : (
              <>Instantly Identify Plants & Detect Diseases with <span className="bg-gradient-to-r from-emerald-400 to-teal-300 bg-clip-text text-transparent">AI Diagnostic Precision</span></>
            )}
          </h1>

          {/* Subheadline (One sentence on how) */}
          <p className="mt-6 text-base sm:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed font-normal">
            {lang === 'mr' ? (
              'पानाचा फोटो अपलोड करा, त्वरित रोग निदान मिळवा आणि आपल्या भाषेत सेंद्रिय आणि रासायनिक उपचार मिळवा.'
            ) : (
              'Scan any crop leaf with your phone camera to get instant plant species identification, severity percentage, and practical remedies in your native language.'
            )}
          </p>

          {/* CTAs */}
          <div className="mt-9 flex flex-col sm:flex-row items-center justify-center gap-4 max-w-md mx-auto">
            <button
              onClick={handleScanClick}
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-sm transition-all duration-200 shadow-xl shadow-emerald-500/25 flex items-center justify-center space-x-2 group"
            >
              <Scan className="w-5 h-5" />
              <span>{lang === 'mr' ? 'आत्ताच पीक स्कॅन करा' : 'Scan Your Plant Now'}</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>

            <button
              onClick={() => scrollToSection('how-it-works')}
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 font-bold text-sm border border-slate-800 transition flex items-center justify-center space-x-2"
            >
              <span>{lang === 'mr' ? 'हे कसे कार्य करते पहा' : 'See How It Works'}</span>
            </button>
          </div>

          {/* Hero Visual Mockup — Scan Result Screen */}
          <div className="mt-14 max-w-4xl mx-auto relative rounded-3xl p-3 sm:p-4 bg-slate-900/80 border border-slate-800 shadow-2xl backdrop-blur-xl">
            <div className="rounded-2xl overflow-hidden bg-slate-950 p-6 sm:p-8 text-left border border-slate-800 space-y-6">
              
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center font-extrabold text-xl shrink-0">
                    🥭
                  </div>
                  <div>
                    <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Mangifera indica</span>
                    <h3 className="text-xl sm:text-2xl font-black text-white">Mango (आंबा) — Powdery Mildew</h3>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold">
                    Plant Confidence: 94.8%
                  </span>
                  <span className="px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold">
                    Moderate Risk
                  </span>
                </div>
              </div>

              {/* Sample Result Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-xs text-slate-400 block">Identified Plant</span>
                  <span className="text-lg font-bold text-white mt-0.5 block">Mango Leaf</span>
                </div>
                <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-xs text-slate-400 block">Disease Status</span>
                  <span className="text-lg font-bold text-amber-400 mt-0.5 block">Powdery Mildew</span>
                </div>
                <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-xs text-slate-400 block">Organic Protocol</span>
                  <span className="text-xs text-slate-300 mt-0.5 block line-clamp-2">Spray sulfur (0.2%) or neem oil (5ml/L) at first sign.</span>
                </div>
              </div>

            </div>
          </div>

        </div>
      </section>

      {/* 4. How It Works (4-Step Visual Workflow) */}
      <section id="how-it-works" className="py-16 sm:py-24 bg-slate-900/50 border-y border-slate-900 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center max-w-2xl mx-auto mb-16">
            <span className="text-xs font-extrabold text-emerald-400 uppercase tracking-widest">Simple Step-by-Step</span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white mt-2">
              {lang === 'mr' ? 'फक्त ४ सोप्या पायऱ्यांमध्ये निदान' : 'How AgroScan AI Works in 4 Steps'}
            </h2>
            <p className="text-sm text-slate-400 mt-3">
              {lang === 'mr' ? 'वापरण्यास अत्यंत सोपे, शेतातून थेट मोबाईलद्वारे वापरा.' : 'Designed for smallholder farmers with instant computer-vision diagnostic feedback.'}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">
            
            {/* Step 1 */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 relative space-y-4">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 font-extrabold flex items-center justify-center border border-emerald-500/20 text-sm">
                01
              </div>
              <h3 className="text-lg font-bold text-white">1. Capture / Upload</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Take a photo of any crop leaf using your camera or upload an existing image file (JPG, PNG, WEBP).
              </p>
            </div>

            {/* Step 2 */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 relative space-y-4">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 font-extrabold flex items-center justify-center border border-emerald-500/20 text-sm">
                02
              </div>
              <h3 className="text-lg font-bold text-white">2. AI Identifies Plant</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Botanical AI identifies the plant species and verifies that a valid leaf/plant photo was submitted.
              </p>
            </div>

            {/* Step 3 */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 relative space-y-4">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 font-extrabold flex items-center justify-center border border-emerald-500/20 text-sm">
                03
              </div>
              <h3 className="text-lg font-bold text-white">3. Detects Disease</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Inference algorithms scan for leaf lesions, fungal infections, and calculate severity percentage.
              </p>
            </div>

            {/* Step 4 */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 relative space-y-4">
              <div className="w-10 h-10 rounded-xl bg-emerald-500/10 text-emerald-400 font-extrabold flex items-center justify-center border border-emerald-500/20 text-sm">
                04
              </div>
              <h3 className="text-lg font-bold text-white">4. Get Treatment Advice</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Receive practical organic remedies, chemical options, and chat with the AI Agronomist for custom guidance.
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* 5. Features Grid (6 Core Cards) */}
      <section id="features" className="py-16 sm:py-24 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center max-w-2xl mx-auto mb-16">
            <span className="text-xs font-extrabold text-emerald-400 uppercase tracking-widest">Platform Capabilities</span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-white mt-2">
              {lang === 'mr' ? 'प्रमुख वैशिष्ट्ये' : 'Built for Smart Crop Protection'}
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            
            {/* Card 1 */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition">
              <div className="w-12 h-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mb-4 border border-emerald-500/20">
                <Scan className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-white mb-1.5">Instant Plant ID</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Recognize crop species instantly with scientific name and confidence probability metrics.
              </p>
            </div>

            {/* Card 2 */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition">
              <div className="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center mb-4 border border-amber-500/20">
                <ShieldAlert className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-white mb-1.5">Disease Detection</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Detect fungal, bacterial, and viral diseases with real-time severity level diagnostics.
              </p>
            </div>

            {/* Card 3 */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition">
              <div className="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center mb-4 border border-purple-500/20">
                <Bot className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-white mb-1.5">AI Assistant Chat</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Consult an AI agronomist pre-seeded with your exact scan context and farm location.
              </p>
            </div>

            {/* Card 4 */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition">
              <div className="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center mb-4 border border-blue-500/20">
                <Globe className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-white mb-1.5">Marathi + English Support</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Full Marathi language localization (मराठी) across the interface and AI assistant responses.
              </p>
            </div>

            {/* Card 5 */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition">
              <div className="w-12 h-12 rounded-xl bg-teal-500/10 text-teal-400 flex items-center justify-center mb-4 border border-teal-500/20">
                <MapPin className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-white mb-1.5">Location-Aware Advice</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Incorporate farm village, taluka, district, and weather conditions for tailored advisory.
              </p>
            </div>

            {/* Card 6 */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 hover:border-emerald-500/30 transition">
              <div className="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center mb-4 border border-indigo-500/20">
                <History className="w-6 h-6" />
              </div>
              <h3 className="text-base font-bold text-white mb-1.5">Farm Records & History</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Track past diagnostic scans, export advisory notes, and keep permanent crop health logs.
              </p>
            </div>

          </div>
        </div>
      </section>

      {/* 6. AI Assistant Interactive Chat Preview */}
      <section id="ai-preview" className="py-16 sm:py-24 bg-slate-900/50 border-t border-slate-900">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          
          <div className="text-center max-w-2xl mx-auto mb-12">
            <span className="text-xs font-extrabold text-emerald-400 uppercase tracking-widest">Interactive AI Agronomist</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-white mt-2">
              {lang === 'mr' ? 'AI सहाय्यकाचा नमुना पहा' : 'Try the AI Assistant Preview'}
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-2">
              Ask questions about crop diseases, dosage, or organic remedies.
            </p>
          </div>

          <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-slate-800 shadow-2xl space-y-4">
            
            {/* User Bubble */}
            <div className="flex items-start justify-end space-x-3">
              <div className="bg-emerald-500 text-slate-950 p-4 rounded-2xl rounded-tr-none text-xs sm:text-sm font-semibold max-w-md">
                "Why are my mango leaves curling and showing white powder?"
              </div>
              <div className="w-8 h-8 rounded-full bg-slate-800 text-slate-300 font-bold text-xs flex items-center justify-center shrink-0 border border-slate-700">
                You
              </div>
            </div>

            {/* Assistant Bubble */}
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 rounded-full bg-emerald-500/20 text-emerald-400 font-bold text-xs flex items-center justify-center shrink-0 border border-emerald-500/30">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl rounded-tl-none text-xs sm:text-sm text-slate-200 max-w-lg space-y-2 leading-relaxed">
                <p className="font-bold text-emerald-400">AgroScan AI Agronomist Response (Mango):</p>
                <p>White powder with leaf curling indicates <strong>Powdery Mildew (Oidium mangiferae)</strong>.</p>
                <ul className="list-disc pl-4 space-y-1 text-slate-300">
                  <td><strong>Organic Solution:</strong> Spray Neem Oil (5ml/L) or wettable sulfur (2g/L) during cool morning hours.</td>
                  <td><strong>Prevention:</strong> Ensure good canopy ventilation and avoid overhead watering.</td>
                </ul>
              </div>
            </div>

            <div className="pt-4 text-center">
              <button
                onClick={handleScanClick}
                className="px-6 py-3 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs transition inline-flex items-center space-x-2"
              >
                <Scan className="w-4 h-4" />
                <span>{lang === 'mr' ? 'आपले पीक स्कॅन करून विचारा' : 'Scan Your Crop & Ask AI'}</span>
              </button>
            </div>

          </div>

        </div>
      </section>

      {/* 7. Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 py-12 text-slate-400 text-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">
          
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
              <Sprout className="w-5 h-5" />
            </div>
            <span className="text-sm font-bold text-white">AgroScan AI</span>
          </div>

          <div className="flex items-center space-x-6">
            <button onClick={() => scrollToSection('how-it-works')} className="hover:text-slate-200">How it Works</button>
            <button onClick={() => scrollToSection('features')} className="hover:text-slate-200">Features</button>
            <button onClick={() => scrollToSection('ai-preview')} className="hover:text-slate-200">AI Assistant</button>
            <button onClick={toggleLanguage} className="text-emerald-400 font-bold hover:underline">
              {lang === 'en' ? 'मराठी आवृत्ती' : 'English Version'}
            </button>
          </div>

          <p>© 2026 AgroScan AI — Smart Agricultural Diagnostics.</p>
        </div>
      </footer>

    </div>
  );
};

