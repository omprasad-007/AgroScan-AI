import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Sprout,
  ScanLine,
  ShieldAlert,
  Bot,
  ArrowRight,
  CheckCircle2,
  Globe,
  MapPin,
  History,
  Sparkles,
  Menu,
  X,
  Zap,
  Leaf,
  ShieldCheck,
  CloudSun,
  Sun,
  Moon,
  Layers,
  Cpu,
  Activity,
  Thermometer,
  Droplets,
  Wind,
  Check
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';

// Crop dataset for the Interactive Diagnostic Simulator (Vibrant Orange + Harvest Yellow + Royal Purple)
const SAMPLE_SIMULATION_CROPS = [
  {
    id: 'cotton',
    cropNameEn: 'Cotton',
    cropNameMr: 'कापूस',
    scientific: 'Gossypium hirsutum',
    diseaseEn: 'Bacterial Blight',
    diseaseMr: 'जिवाणू करपा',
    severity: 'Moderate',
    severityPercent: 28,
    confidence: '95.4%',
    pathogen: 'Xanthomonas citri pv. malvacearum',
    latency: '34ms',
    imageUrl: 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?auto=format&fit=crop&w=900&q=80',
    organicProtocolEn: 'Spray cold-pressed Neem Oil (1500 ppm @ 4 ml/L) or Copper Oxychloride 50% WP (2.5 g/L). Ensure proper furrow drainage.',
    organicProtocolMr: 'थंड दाबाचे कडुनिंब तेल (१५०० ppm @ ४ मि.ली./लिटर) किंवा कॉपर ऑक्सिक्लोराईड फवारावे. मुळांशी साचलेले पाणी काढून टाका.',
    chemicalProtocolEn: 'Streptocycline (0.5 g/L) combined with Copper Hydroxide (2 g/L) at 12-day intervals.',
    chemicalProtocolMr: 'स्ट्रेप्टोसायक्लिन (०.५ ग्रॅम/लिटर) + कॉपर हायड्रॉक्साइड (२ ग्रॅम/लिटर) १२ दिवसांच्या अंतराने फवारावे.'
  },
  {
    id: 'tomato',
    cropNameEn: 'Tomato',
    cropNameMr: 'टोमॅटो',
    scientific: 'Solanum lycopersicum',
    diseaseEn: 'Early Blight',
    diseaseMr: 'लवकर येणारा करपा',
    severity: 'High',
    severityPercent: 44,
    confidence: '97.2%',
    pathogen: 'Alternaria solani',
    latency: '31ms',
    imageUrl: 'https://images.unsplash.com/photo-1592841200221-a6898f307baa?auto=format&fit=crop&w=900&q=80',
    organicProtocolEn: 'Prune infected lower foliage immediately. Spray Trichoderma viride bio-fungicide (5 g/L) in cool evening hours.',
    organicProtocolMr: 'रोगट झालेली खालची पाने तात्काळ छाटून टाका. संध्याकाळी ट्रायकोडर्मा व्हिरिडी (५ ग्रॅम/लिटर) फवारावे.',
    chemicalProtocolEn: 'Apply Mancozeb 75% WP (2.5 g/L) or Azoxystrobin 23% SC (1 ml/L) to prevent spore transmission.',
    chemicalProtocolMr: 'मॅन्कोझेब ७५% WP (२.५ ग्रॅम/लिटर) किंवा ॲझॉक्सीस्ट्रोबिन २३% SC (१ मि.ली./लिटर) फवारावे.'
  },
  {
    id: 'mango',
    cropNameEn: 'Mango',
    cropNameMr: 'आंबा',
    scientific: 'Mangifera indica',
    diseaseEn: 'Powdery Mildew',
    diseaseMr: 'भुरी रोग (पांढरी बुरशी)',
    severity: 'Moderate',
    severityPercent: 22,
    confidence: '96.1%',
    pathogen: 'Oidium mangiferae',
    latency: '38ms',
    imageUrl: 'https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=900&q=80',
    organicProtocolEn: 'Dust wettable sulfur 80% WP (2 g/L) during cool morning hours. Apply Dashparni ark (20 ml/L) for canopy protection.',
    organicProtocolMr: 'सकाळच्या थंड हवेत विद्राव्य गंधक ८०% WP (२ ग्रॅम/लिटर) किंवा दशपर्णी अर्क (२० मि.ली./लिटर) फवारावे.',
    chemicalProtocolEn: 'Hexaconazole 5% EC (1 ml/L) or Dinocap 48% EC (1 ml/L) at flower panicle initiation.',
    chemicalProtocolMr: 'मोहर येण्याच्या काळात हेक्साकोनाझोल ५% EC (१ मि.ली./लिटर) फवारावे.'
  },
  {
    id: 'rice',
    cropNameEn: 'Rice / Paddy',
    cropNameMr: 'भात / धान',
    scientific: 'Oryza sativa',
    diseaseEn: 'Rice Blast',
    diseaseMr: 'तांदळावरील करपा (ब्लास्ट)',
    severity: 'Critical',
    severityPercent: 62,
    confidence: '94.8%',
    pathogen: 'Magnaporthe oryzae',
    latency: '42ms',
    imageUrl: 'https://images.unsplash.com/photo-1536657464919-892534f60d6e?auto=format&fit=crop&w=900&q=80',
    organicProtocolEn: 'Apply Pseudomonas fluorescens (10 g/L). Avoid excess chemical nitrogen fertilizer application.',
    organicProtocolMr: 'स्यूडोमोनास फ्लोरोसेन्स (१० ग्रॅम/लिटर) वापरा. जास्त युरिया (नायट्रोजन) खताचा वापर टाळा.',
    chemicalProtocolEn: 'Spray Tricyclazole 75% WP (0.6 g/L) or Isoprothiolane 40% EC (1.5 ml/L) at panicle emergence.',
    chemicalProtocolMr: 'लोंबी भरण्याच्या वेळी ट्रायसायक्लॅझोल ७५% WP (०.६ ग्रॅम/लिटर) फवारावे.'
  },
  {
    id: 'sugarcane',
    cropNameEn: 'Sugarcane',
    cropNameMr: 'ऊस',
    scientific: 'Saccharum officinarum',
    diseaseEn: 'Red Rot',
    diseaseMr: 'लाल कुजव्या',
    severity: 'High',
    severityPercent: 51,
    confidence: '98.1%',
    pathogen: 'Colletotrichum falcatum',
    latency: '36ms',
    imageUrl: 'https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=900&q=80',
    organicProtocolEn: 'Rotate crop with leguminous pulses; treat sets with Trichoderma viride (10 g/L) prior to planting.',
    organicProtocolMr: 'कडधान्य पिकांसोबत फेरपालट करा; लागवडीपूर्वी बेणे ट्रायकोडर्मा (१० ग्रॅम/लिटर) मध्ये प्रक्रिया करा.',
    chemicalProtocolEn: 'Carbendazim 50% WP (1 g/L) set dipping for 15 minutes before furrow placement.',
    chemicalProtocolMr: 'कार्बेन्डाझिम ५०% WP (१ ग्रॅम/लिटर) द्रावणात बेणे १५ मिनिटे बुडवून लागवड करा.'
  }
];

export const LandingPage = () => {
  const { lang, toggleLanguage } = useLanguage();
  const { isAuthenticated } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [selectedCrop, setSelectedCrop] = useState(SAMPLE_SIMULATION_CROPS[0]);
  const [treatmentTab, setTreatmentTab] = useState('organic'); // 'organic' | 'chemical'
  const [activeFaqQuery, setActiveFaqQuery] = useState(0);

  const handleScanClick = () => navigate('/scan');

  const scrollToSection = (id) => {
    setMobileMenuOpen(false);
    const element = document.getElementById(id);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Sample Interactive Agronomist Consultations
  const sampleFaqs = [
    {
      qEn: "How to prevent early blight from destroying tomato crops in humid weather?",
      qMr: "दमट हवामानात टोमॅटोवरील करपा रोगाचा प्रसार कसा रोखावा?",
      aEn: "Early Blight (Alternaria solani) thrives when relative humidity exceeds 80%. Immediately prune infected bottom leaves (defoliate up to 25cm from soil). Spray Trichoderma viride (5g/L) during mornings or apply Mancozeb 75% WP (2.5g/L). Avoid overhead sprinkler irrigation to keep leaf surfaces dry.",
      aMr: "करपा (Alternaria solani) हवेतील आर्द्रता ८०% पेक्षा जास्त असताना वेगाने पसरतो. जमिनीलगतची संसर्ग झालेली पाने तात्काळ छाटून नष्ट करा. सकाळी ट्रायकोडर्मा व्हिरिडी (५ ग्रॅम/लिटर) किंवा मॅन्कोझेब ७५% WP (२.५ ग्रॅम/लिटर) फवारावे. वरून पाणी देणे टाळा."
    },
    {
      qEn: "What is the certified dosage of cold-pressed Neem Oil for crop protection?",
      qMr: "पिकांच्या संरक्षणासाठी कडुनिंब तेलाचे प्रमाणित प्रमाण किती असावे?",
      aEn: "For preventive protection against aphids, thrips, and fungal spores, use 1500 ppm cold-pressed Neem Oil at 4 to 5 ml per liter of water. Always mix with 1 ml of neutral organic soap or liquid surfactant to emulsify properly before foliar application.",
      aMr: "मावा, तुडतुडे आणि बुरशीच्या बीजाणूंपासून संरक्षणासाठी १५०० ppm कडुनिंब तेल ४ ते ५ मि.ली. प्रति लिटर पाण्यात वापरा. फवारणीपूर्वी द्रावण व्यवस्थित मिसळण्यासाठी १ मि.ली. साबणाचे पाणी किंवा सर्फॅक्टंट एकत्र करावे."
    },
    {
      qEn: "Can I combine copper fungicide with systemic insecticide in one tank?",
      qMr: "कॉपर बुरशीनाशक आणि कीटकनाशक एकाच टाकीत एकत्र फवारता येते का?",
      aEn: "Caution: Never mix Copper Oxychloride or Bordeaux mixtures with organophosphates or acidic systemic chemicals, as it causes severe phytotoxicity (leaf scorch) and neutralizes efficacy. Keep a minimum 5-to-7 day gap between copper sprays and other agrochemicals.",
      aMr: "सावधगिरी: कॉपर ऑक्सिक्लोराईड किंवा बोर्डो मिश्रण इतर रासायनिक कीटकनाशकांमध्ये एकत्र करू नका; यामुळे पानांवर जळल्यासारखे डाग पडतात आणि औषधाची कार्यक्षमता नष्ट होते. दोन्ही फवारणीमध्ये किमान ५ ते ७ दिवसांचे अंतर ठेवा."
    }
  ];

  return (
    <div className="min-h-screen bg-agro-bg text-agro-cream flex flex-col justify-between selection:bg-agro-primary/20 selection:text-agro-primary transition-colors duration-200">

      {/* =========================================================
       * 1. TOP APP BAR (Vibrant Orange + Harvest Yellow + Royal Purple)
       * ======================================================= */}
      <header className="sticky top-0 z-50 bg-agro-card/90 backdrop-blur-xl border-b border-agro-border transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16 sm:h-20">

            {/* Brand Logo with Engine Badge */}
            <Link to="/" className="flex items-center gap-3 group focus-visible:outline-none">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-agro-primary via-[#C94427] to-agro-accent text-white flex items-center justify-center shadow-md shadow-agro-primary/25 group-hover:scale-105 transition-transform duration-200">
                <Sprout className="w-5 h-5 text-white" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-heading text-lg font-extrabold tracking-tight text-agro-cream">
                    AgroScan <span className="text-agro-primary">AI</span>
                  </span>
                  <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold bg-agro-highlight/15 text-agro-highlight border border-agro-highlight/30">
                    {theme === 'dark' ? 'DARK MODE' : 'LIGHT MODE'}
                  </span>
                </div>
                <span className="block text-supporting-text text-agro-muted font-medium tracking-wider uppercase">
                  SMART PLANT HEALTH MONITORING
                </span>
              </div>
            </Link>

            {/* Desktop Navigation Links */}
            <nav className="hidden lg:flex items-center gap-7 text-label-text font-semibold text-agro-muted">
              <button
                onClick={() => scrollToSection('simulator')}
                className="hover:text-agro-primary transition-colors cursor-pointer flex items-center gap-1.5"
              >
                <Activity className="w-3.5 h-3.5 text-agro-primary" />
                <span>{lang === 'mr' ? 'थेट सिम्युलेटर' : 'Crop Insights'}</span>
              </button>
              <button
                onClick={() => scrollToSection('features')}
                className="hover:text-agro-primary transition-colors cursor-pointer flex items-center gap-1.5"
              >
                <Layers className="w-3.5 h-3.5 text-agro-highlight" />
                <span>{lang === 'mr' ? 'फील्ड इंटेलिजन्स' : 'Field Intelligence'}</span>
              </button>
              <button
                onClick={() => scrollToSection('workflow')}
                className="hover:text-agro-primary transition-colors cursor-pointer flex items-center gap-1.5"
              >
                <Zap className="w-3.5 h-3.5 text-agro-primary" />
                <span>{lang === 'mr' ? 'कसे कार्य करते' : 'AI Analysis'}</span>
              </button>
              <button
                onClick={() => scrollToSection('ai-advisor')}
                className="hover:text-agro-primary transition-colors cursor-pointer flex items-center gap-1.5"
              >
                <Bot className="w-3.5 h-3.5 text-agro-accent" />
                <span>{lang === 'mr' ? 'AI सल्लागार' : 'AI Agronomist'}</span>
              </button>
            </nav>

            {/* Right Action Tools */}
            <div className="hidden sm:flex items-center gap-2.5">
              
              {/* Language Switcher */}
              <button
                type="button"
                onClick={toggleLanguage}
                className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-cream text-label-text font-semibold border border-agro-border transition-all duration-150"
                title={lang === 'en' ? 'मराठी मध्ये बदला' : 'Switch to English'}
              >
                <Globe className="w-3.5 h-3.5 text-agro-primary" />
                <span>{lang === 'en' ? 'मराठी' : 'English'}</span>
              </button>

              {/* Theme Toggle Button */}
              <button
                type="button"
                onClick={toggleTheme}
                className="p-2.5 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-highlight border border-agro-border transition-all duration-150"
                title={theme === 'dark' ? "Switch to light theme" : "Switch to dark theme"}
              >
                {theme === 'dark' ? (
                  <Sun className="w-4 h-4 text-agro-highlight" />
                ) : (
                  <Moon className="w-4 h-4 text-agro-accent" />
                )}
              </button>

              {/* Sign In / Dashboard */}
              {isAuthenticated ? (
                <Link
                  to="/dashboard"
                  className="px-3.5 py-2 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-cream text-label-text font-semibold border border-agro-border transition-all"
                >
                  {lang === 'mr' ? 'डॅशबोर्ड' : 'Dashboard'}
                </Link>
              ) : (
                <Link
                  to="/login"
                  className="px-3 py-2 rounded-xl text-label-text font-semibold text-agro-muted hover:text-agro-cream transition-colors"
                >
                  {lang === 'mr' ? 'साइन इन' : 'Sign In'}
                </Link>
              )}

              {/* Primary Button: Start New Scan (15px) */}
              <button
                onClick={handleScanClick}
                className="px-4 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white font-bold text-button-text transition-all duration-150 shadow-md shadow-orange-glow flex items-center gap-2 active:scale-95"
              >
                <ScanLine className="w-4 h-4" />
                <span>{lang === 'mr' ? 'नवीन स्कॅन सुरू करा' : 'Start New Scan'}</span>
              </button>
            </div>

            {/* Mobile Nav Toggle */}
            <div className="flex sm:hidden items-center gap-1.5">
              <button
                type="button"
                onClick={toggleTheme}
                className="p-2 rounded-lg bg-agro-surface border border-agro-border text-agro-highlight"
              >
                {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4 text-agro-accent" />}
              </button>
              <button
                type="button"
                onClick={toggleLanguage}
                className="p-2 rounded-lg bg-agro-surface border border-agro-border text-label-text font-bold text-agro-cream"
              >
                {lang === 'en' ? 'मराठी' : 'EN'}
              </button>
              <button
                type="button"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="p-2 rounded-xl bg-agro-surface border border-agro-border text-agro-cream"
              >
                {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </button>
            </div>

          </div>
        </div>

        {/* Mobile Navigation Dropdown */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              className="sm:hidden border-b border-agro-border bg-agro-card px-4 py-4 space-y-3"
            >
              <button
                onClick={() => scrollToSection('simulator')}
                className="block w-full text-left py-2 text-body-text font-semibold text-agro-cream"
              >
                {lang === 'mr' ? 'थेट सिम्युलेटर' : 'Crop Insights'}
              </button>
              <button
                onClick={() => scrollToSection('features')}
                className="block w-full text-left py-2 text-body-text font-semibold text-agro-cream"
              >
                {lang === 'mr' ? 'फील्ड इंटेलिजन्स' : 'Field Intelligence'}
              </button>
              <button
                onClick={() => scrollToSection('workflow')}
                className="block w-full text-left py-2 text-body-text font-semibold text-agro-cream"
              >
                {lang === 'mr' ? 'कसे कार्य करते' : 'AI Analysis'}
              </button>
              <button
                onClick={() => scrollToSection('ai-advisor')}
                className="block w-full text-left py-2 text-body-text font-semibold text-agro-cream"
              >
                {lang === 'mr' ? 'AI सल्लागार' : 'AI Agronomist'}
              </button>
              <div className="pt-3 border-t border-agro-border flex flex-col gap-2">
                <button
                  onClick={handleScanClick}
                  className="w-full py-2.5 rounded-xl bg-agro-primary text-white font-bold text-button-text flex items-center justify-center gap-2"
                >
                  <ScanLine className="w-4 h-4" />
                  <span>{lang === 'mr' ? 'नवीन स्कॅन सुरू करा' : 'Start New Scan'}</span>
                </button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </header>

      {/* =========================================================
       * 2. HERO SECTION — VIBRANT ORANGE & MANROPE TYPOGRAPHY
       * ======================================================= */}
      <section className="relative overflow-hidden pt-12 sm:pt-20 pb-16 sm:pb-24">
        {/* Warm Ambient Orbs (GPU Layered) */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-[450px] bg-gradient-to-b from-agro-primary/10 via-agro-highlight/5 to-transparent blur-2xl pointer-events-none [transform:translateZ(0)]" />
        <div className="absolute top-1/4 right-10 w-72 h-72 bg-agro-accent/5 rounded-full blur-2xl pointer-events-none [transform:translateZ(0)]" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">

          {/* Subheading Badge */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-agro-surface border border-agro-border text-agro-cream text-label-text font-semibold mb-6 shadow-sm"
          >
            <span className="w-2 h-2 rounded-full bg-agro-primary animate-ping shrink-0" />
            <span className="font-heading font-bold text-agro-primary">SMART PLANT HEALTH MONITORING</span>
            <span className="text-agro-muted">·</span>
            <span className="font-sans text-supporting-text text-agro-muted">35+ Crop Classes</span>
          </motion.div>

          {/* Main Headline: Grow smarter. (36px, Manrope 800) */}
          <motion.h1
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="font-heading text-main-heading sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-agro-cream max-w-4xl mx-auto leading-tight"
          >
            {lang === 'mr' ? (
              <>
                हुशारीने पीक वाढवा.{' '}
                <span className="text-agro-primary">
                  Grow smarter.
                </span>
              </>
            ) : (
              <>
                Grow smarter.{' '}
                <span className="text-agro-primary">
                  Intelligent Plant Disease Detection
                </span>{' '}
                and Crop Monitoring.
              </>
            )}
          </motion.h1>

          {/* Subtitle / Body text (16px) */}
          <motion.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="mt-6 text-body-text text-agro-muted max-w-2xl mx-auto leading-relaxed font-normal"
          >
            {lang === 'mr' ? (
              'पानाचा एक फोटो अपलोड करा किंवा थेट कॅमेऱ्याने काढा. आमचे मॉडेल त्वरित रोग, संसर्ग पातळी आणि प्रमाणित सेंद्रिय-रासायनिक उपाय सांगते.'
            ) : (
              'Intelligent plant disease detection and real-time crop monitoring. Receive instant botanical identification, leaf lesion segmentation, and certified remedial protocols.'
            )}
          </motion.p>

          {/* Hero Action Buttons (15px) */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3.5 max-w-md mx-auto"
          >
            {/* Primary Button: Start New Scan */}
            <button
              onClick={handleScanClick}
              className="w-full sm:w-auto px-7 py-3.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white font-bold text-button-text transition-all duration-150 shadow-md shadow-orange-glow flex items-center justify-center gap-2 group active:scale-95"
            >
              <ScanLine className="w-5 h-5" />
              <span>{lang === 'mr' ? 'नवीन स्कॅन सुरू करा' : 'Start New Scan'}</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>

            {/* Secondary Button: Crop Insights */}
            <button
              onClick={() => scrollToSection('simulator')}
              className="w-full sm:w-auto px-7 py-3.5 rounded-xl bg-agro-card hover:bg-agro-surface text-agro-cream font-semibold text-button-text border border-agro-border transition-all duration-150 shadow-sm flex items-center justify-center gap-2"
            >
              <Activity className="w-4 h-4 text-agro-highlight" />
              <span>{lang === 'mr' ? 'पीक माहिती पहा' : 'Crop Insights'}</span>
            </button>
          </motion.div>

          {/* Trust Metric Strip (13px Supporting Text) */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="mt-12 pt-8 border-t border-agro-border grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto text-left"
          >
            <div className="flex items-center gap-3 p-3.5 rounded-2xl bg-agro-card border border-agro-border">
              <div className="w-9 h-9 rounded-xl bg-agro-primary/10 text-agro-primary flex items-center justify-center shrink-0">
                <Cpu className="w-4 h-4" />
              </div>
              <div>
                <span className="text-label-text font-bold text-agro-cream block">&lt;45ms Latency</span>
                <span className="text-supporting-text text-agro-muted block">Local CPU Inference</span>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3.5 rounded-2xl bg-agro-card border border-agro-border">
              <div className="w-9 h-9 rounded-xl bg-agro-highlight/15 text-agro-highlight flex items-center justify-center shrink-0">
                <ShieldCheck className="w-4 h-4" />
              </div>
              <div>
                <span className="text-label-text font-bold text-agro-cream block">35+ Pathologies</span>
                <span className="text-supporting-text text-agro-muted block">Cotton, Rice, Mango</span>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3.5 rounded-2xl bg-agro-card border border-agro-border">
              <div className="w-9 h-9 rounded-xl bg-agro-accent/15 text-agro-accent flex items-center justify-center shrink-0">
                <Activity className="w-4 h-4" />
              </div>
              <div>
                <span className="text-label-text font-bold text-agro-cream block">94.6% Accuracy</span>
                <span className="text-supporting-text text-agro-muted block">Neural Verification</span>
              </div>
            </div>

            <div className="flex items-center gap-3 p-3.5 rounded-2xl bg-agro-card border border-agro-border">
              <div className="w-9 h-9 rounded-xl bg-agro-primary/10 text-agro-primary flex items-center justify-center shrink-0">
                <Zap className="w-4 h-4" />
              </div>
              <div>
                <span className="text-label-text font-bold text-agro-cream block">100% Offline</span>
                <span className="text-supporting-text text-agro-muted block">Farmland Ready</span>
              </div>
            </div>
          </motion.div>

        </div>
      </section>

      {/* =========================================================
       * 3. INTERACTIVE DIAGNOSTIC SIMULATOR (Crop Insights & AI Analysis)
       * ======================================================= */}
      <section id="simulator" className="py-16 sm:py-24 bg-agro-surface border-y border-agro-border relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

          {/* Section Heading (26px, Manrope 700) */}
          <div className="text-center max-w-3xl mx-auto mb-12">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-agro-highlight/15 text-agro-highlight font-bold text-supporting-text border border-agro-highlight/30 mb-3">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Smart Monitoring & AI Analysis</span>
            </div>
            <h2 className="font-heading text-section-heading font-bold text-agro-cream tracking-tight">
              {lang === 'mr' ? 'थेट रोगाचे नमुने तपासा' : 'Crop Insights & Real-Time Disease Detection'}
            </h2>
            <p className="text-body-text text-agro-muted mt-2">
              {lang === 'mr'
                ? 'खालील पिकांवर क्लिक करा आणि न्यूरल मॉडेलचे रिअल-टाइम पृथक्करण आणि औषधोपचार पहा.'
                : 'Select any crop leaf below to observe live bounding box targeting, latency telemetry, and certified remedial protocols.'}
            </p>

            {/* Crop Selector Tabs */}
            <div className="mt-8 flex flex-wrap items-center justify-center gap-2">
              {SAMPLE_SIMULATION_CROPS.map((crop) => {
                const isSelected = selectedCrop.id === crop.id;
                return (
                  <button
                    key={crop.id}
                    onClick={() => setSelectedCrop(crop)}
                    className={`px-4 py-2.5 rounded-xl text-label-text font-semibold transition-all duration-150 border flex items-center gap-2 ${
                      isSelected
                        ? 'bg-agro-primary text-white border-agro-primary shadow-md shadow-orange-glow scale-105'
                        : 'bg-agro-card hover:bg-agro-hover text-agro-cream border-agro-border'
                    }`}
                  >
                    <Leaf className="w-3.5 h-3.5" />
                    <span>{lang === 'mr' ? crop.cropNameMr : crop.cropNameEn}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Simulator Viewport Card */}
          <div className="max-w-5xl mx-auto agro-panel p-4 sm:p-7 rounded-3xl shadow-xl">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">

              {/* Left: Simulated Leaf Viewport HUD (5 Cols) */}
              <div className="lg:col-span-5 relative rounded-2xl overflow-hidden bg-brand-dark-bg aspect-[4/3] sm:aspect-auto sm:min-h-[380px] border border-agro-border flex flex-col justify-between p-4 group">
                {/* Background image */}
                <img
                  src={selectedCrop.imageUrl}
                  alt={selectedCrop.cropNameEn}
                  loading="lazy"
                  decoding="async"
                  className="absolute inset-0 w-full h-full object-cover transition-transform duration-700 group-hover:scale-105 opacity-85"
                />

                {/* Reticle Overlay & Orange Laser Sweep */}
                <div className="absolute inset-0 bg-gradient-to-t from-brand-dark-bg/85 via-transparent to-brand-dark-bg/40 pointer-events-none" />
                <div className="absolute inset-x-0 h-0.5 bg-gradient-to-r from-transparent via-agro-primary to-transparent shadow-[0_0_12px_#E96747] animate-laser-sweep pointer-events-none" />

                {/* Bounding Box on Lesion (Vibrant Orange HUD) */}
                <div className="absolute top-[28%] left-[24%] w-[52%] h-[44%] border-2 border-agro-primary rounded-lg bg-agro-primary/10 backdrop-blur-[1px] pointer-events-none flex flex-col justify-between p-1.5 shadow-[0_0_15px_rgba(233,103,71,0.35)]">
                  <div className="flex justify-between items-center text-[10px] font-mono font-bold text-white bg-brand-dark-card/90 px-1.5 py-0.5 rounded border border-agro-border">
                    <span>HOTSPOT #01</span>
                    <span className="text-agro-highlight">{selectedCrop.confidence}</span>
                  </div>
                  <div className="text-right text-[9px] font-mono font-bold text-agro-highlight bg-brand-dark-card/90 px-1 rounded self-end">
                    AREA: {selectedCrop.severityPercent}%
                  </div>
                </div>

                {/* HUD Top Bar */}
                <div className="relative z-10 flex items-center justify-between text-supporting-text font-mono text-agro-highlight bg-brand-dark-card/90 backdrop-blur-md px-3 py-1.5 rounded-lg border border-agro-border">
                  <span className="flex items-center gap-1.5 font-bold">
                    <span className="w-2 h-2 rounded-full bg-agro-primary animate-pulse" />
                    LIVE_INFERENCE
                  </span>
                  <span className="text-agro-muted">{selectedCrop.latency}</span>
                </div>

                {/* HUD Bottom Label */}
                <div className="relative z-10 bg-brand-dark-card/95 backdrop-blur-md p-3.5 rounded-xl border border-agro-border">
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="text-supporting-text font-bold text-agro-highlight uppercase tracking-wider block">
                        {selectedCrop.scientific}
                      </span>
                      <h4 className="font-heading text-card-heading font-bold text-brand-dark-text">
                        {lang === 'mr' ? selectedCrop.cropNameMr : selectedCrop.cropNameEn}
                      </h4>
                    </div>
                    <span className="px-2.5 py-1 rounded-md text-supporting-text font-bold bg-agro-primary/20 text-agro-primary border border-agro-primary/30">
                      {selectedCrop.severity} Risk
                    </span>
                  </div>
                </div>
              </div>

              {/* Right: Real-time Telemetry & Prescription (7 Cols) */}
              <div className="lg:col-span-7 flex flex-col justify-between space-y-5">

                {/* Diagnosis Header Card */}
                <div className="p-5 rounded-2xl bg-agro-card border border-agro-border">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-agro-border pb-3 mb-3">
                    <div>
                      <span className="text-supporting-text font-bold text-agro-muted uppercase tracking-wider block">
                        Detected Pathology
                      </span>
                      <h3 className="font-heading text-card-heading font-bold text-agro-cream">
                        {lang === 'mr' ? selectedCrop.diseaseMr : selectedCrop.diseaseEn}
                      </h3>
                      <span className="text-supporting-text text-agro-muted italic">
                        Pathogen: {selectedCrop.pathogen}
                      </span>
                    </div>
                    <div className="text-left sm:text-right">
                      <span className="font-heading text-2xl font-extrabold text-agro-primary">
                        {selectedCrop.confidence}
                      </span>
                      <span className="text-supporting-text text-agro-muted block font-medium">
                        Confidence Score
                      </span>
                    </div>
                  </div>

                  {/* Progress Gauge */}
                  <div>
                    <div className="flex justify-between items-center text-label-text font-semibold text-agro-cream mb-1.5">
                      <span>Lesion Spread & Severity</span>
                      <span className="text-agro-primary font-bold">{selectedCrop.severityPercent}% Foliar Area</span>
                    </div>
                    <div className="w-full bg-agro-surface h-2.5 rounded-full overflow-hidden border border-agro-border">
                      <motion.div
                        key={selectedCrop.id}
                        initial={{ width: 0 }}
                        animate={{ width: `${selectedCrop.severityPercent}%` }}
                        transition={{ duration: 0.6 }}
                        className="bg-gradient-to-r from-agro-highlight via-agro-primary to-agro-accent h-full rounded-full"
                      />
                    </div>
                  </div>
                </div>

                {/* Treatment Advisory Tabs */}
                <div className="p-5 rounded-2xl bg-agro-card border border-agro-border flex-1 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center gap-2 mb-3">
                      <button
                        onClick={() => setTreatmentTab('organic')}
                        className={`px-3 py-1.5 rounded-lg text-label-text font-semibold transition-colors ${
                          treatmentTab === 'organic'
                            ? 'bg-agro-primary text-white shadow-sm'
                            : 'bg-agro-surface text-agro-muted hover:text-agro-cream'
                        }`}
                      >
                        {lang === 'mr' ? 'सेंद्रिय उपाय (Organic)' : 'Organic Protocol'}
                      </button>
                      <button
                        onClick={() => setTreatmentTab('chemical')}
                        className={`px-3 py-1.5 rounded-lg text-label-text font-semibold transition-colors ${
                          treatmentTab === 'chemical'
                            ? 'bg-agro-accent text-white shadow-sm'
                            : 'bg-agro-surface text-agro-muted hover:text-agro-cream'
                        }`}
                      >
                        {lang === 'mr' ? 'रासायनिक उपाय (Chemical)' : 'Chemical Fungicide'}
                      </button>
                    </div>

                    <div className="p-3.5 rounded-xl bg-agro-surface border border-agro-border text-supporting-text leading-relaxed text-agro-cream">
                      {treatmentTab === 'organic' ? (
                        <p>{lang === 'mr' ? selectedCrop.organicProtocolMr : selectedCrop.organicProtocolEn}</p>
                      ) : (
                        <p>{lang === 'mr' ? selectedCrop.chemicalProtocolMr : selectedCrop.chemicalProtocolEn}</p>
                      )}
                    </div>
                  </div>

                  {/* Action Link to Full Scan */}
                  <div className="pt-4 mt-3 border-t border-agro-border flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <span className="text-supporting-text text-agro-muted flex items-center gap-1.5">
                      <ShieldCheck className="w-4 h-4 text-agro-primary shrink-0" />
                      <span>ICAR & KVK Certified Agronomy</span>
                    </span>
                    <button
                      onClick={handleScanClick}
                      className="px-4 py-2 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-button-text font-bold flex items-center justify-center gap-1.5 shadow-md shadow-orange-glow active:scale-95 transition-all"
                    >
                      <ScanLine className="w-4 h-4" />
                      <span>{lang === 'mr' ? 'स्वतःचे पीक तपासा' : 'Start New Scan'}</span>
                    </button>
                  </div>

                </div>

              </div>

            </div>
          </div>

        </div>
      </section>

      {/* =========================================================
       * 4. FIELD INTELLIGENCE BENTO GRID
       * ======================================================= */}
      <section id="features" className="py-16 sm:py-24 relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

          {/* Section Heading (26px, Manrope 700) */}
          <div className="text-center max-w-2xl mx-auto mb-16">
            <span className="text-supporting-text font-bold text-agro-primary uppercase tracking-widest block">
              AgroScan Intelligence
            </span>
            <h2 className="font-heading text-section-heading font-bold text-agro-cream mt-2 tracking-tight">
              {lang === 'mr' ? 'सर्वसमावेशक फील्ड इंटेलिजन्स प्लॅटफॉर्म' : 'Intelligent Crop Monitoring & Disease Detection'}
            </h2>
            <p className="text-body-text text-agro-muted mt-2">
              {lang === 'mr'
                ? 'कृषी विज्ञान आणि डीप लर्निंगचे एकत्रीकरण, शेतात तात्काळ निर्णय घेण्यासाठी.'
                : 'Built with production-grade neural networks, weather telematics, and localized agricultural knowledge.'}
            </p>
          </div>

          {/* Asymmetric Bento Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-[minmax(240px,auto)]">

            {/* Bento Card 1: Microclimate Outbreak Radar (Span 2) */}
            <div className="md:col-span-2 agro-panel p-6 sm:p-8 rounded-3xl relative overflow-hidden group flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 rounded-2xl bg-agro-primary/10 text-agro-primary flex items-center justify-center border border-agro-primary/25">
                    <CloudSun className="w-6 h-6" />
                  </div>
                  <span className="px-3 py-1 rounded-full text-supporting-text font-bold bg-agro-highlight/15 text-agro-highlight border border-agro-highlight/30">
                    Live Telematics
                  </span>
                </div>

                <h3 className="font-heading text-card-heading font-bold text-agro-cream mb-2">
                  {lang === 'mr' ? 'हवामान जोखीम आणि बुरशी प्रादुर्भाव अंदाज' : 'Microclimate Outbreak Risk Radar'}
                </h3>
                <p className="text-body-text text-agro-muted leading-relaxed max-w-xl">
                  {lang === 'mr'
                    ? 'स्थानिक तापमान, हवेतील आर्द्रता आणि पावसाच्या शक्यतेचे विश्लेषण करून बुरशी बीजाणूंचा धोका आगाऊ ओळखा.'
                    : 'Correlates ambient temperature, relative humidity, and rainfall probability to forecast fungal spore germination before visible lesions emerge.'}
                </p>
              </div>

              {/* Mini weather widget */}
              <div className="mt-6 pt-5 border-t border-agro-border grid grid-cols-3 gap-3">
                <div className="p-3.5 rounded-xl bg-agro-surface border border-agro-border">
                  <span className="text-supporting-text font-semibold text-agro-muted block flex items-center gap-1">
                    <Thermometer className="w-3.5 h-3.5 text-agro-primary" /> Temp
                  </span>
                  <span className="font-heading text-lg font-bold text-agro-cream mt-0.5 block">28.4°C</span>
                </div>
                <div className="p-3.5 rounded-xl bg-agro-surface border border-agro-border">
                  <span className="text-supporting-text font-semibold text-agro-muted block flex items-center gap-1">
                    <Droplets className="w-3.5 h-3.5 text-agro-highlight" /> Humidity
                  </span>
                  <span className="font-heading text-lg font-bold text-agro-cream mt-0.5 block">82%</span>
                </div>
                <div className="p-3.5 rounded-xl bg-agro-surface border border-agro-border">
                  <span className="text-supporting-text font-semibold text-agro-muted block flex items-center gap-1">
                    <Wind className="w-3.5 h-3.5 text-agro-accent" /> Spore Risk
                  </span>
                  <span className="font-heading text-lg font-bold text-agro-primary mt-0.5 block">Moderate</span>
                </div>
              </div>
            </div>

            {/* Bento Card 2: Neural Ensemble (Span 1) */}
            <div className="agro-panel p-6 sm:p-8 rounded-3xl flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-agro-accent/10 text-agro-accent flex items-center justify-center border border-agro-accent/25 mb-4">
                  <Cpu className="w-6 h-6" />
                </div>
                <h3 className="font-heading text-card-heading font-bold text-agro-cream mb-2">
                  {lang === 'mr' ? 'ड्युअल न्यूरल नेटवर्क' : 'Dual Neural Ensemble'}
                </h3>
                <p className="text-body-text text-agro-muted leading-relaxed">
                  {lang === 'mr'
                    ? 'दोन टप्प्यांत तपासणी: आधी वनस्पती पडताळणी आणि नंतर रोगाचे वर्गीकरण.'
                    : 'Stage 1 validates leaf morphology via DINOv2 vision; Stage 2 segments pathology lesions via MobileNetV2.'}
                </p>
              </div>

              <div className="mt-6 space-y-2 text-supporting-text font-mono text-agro-muted">
                <div className="flex justify-between items-center p-2.5 rounded-lg bg-agro-surface border border-agro-border">
                  <span>Botanical ID</span>
                  <span className="text-agro-primary font-bold">Passed (98.6%)</span>
                </div>
                <div className="flex justify-between items-center p-2.5 rounded-lg bg-agro-surface border border-agro-border">
                  <span>Inference Latency</span>
                  <span className="text-agro-highlight font-bold">~34ms Edge</span>
                </div>
              </div>
            </div>

            {/* Bento Card 3: Multilingual Agronomist (Span 1) */}
            <div className="agro-panel p-6 sm:p-8 rounded-3xl flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-agro-highlight/15 text-agro-highlight flex items-center justify-center border border-agro-highlight/30 mb-4">
                  <Globe className="w-6 h-6" />
                </div>
                <h3 className="font-heading text-card-heading font-bold text-agro-cream mb-2">
                  {lang === 'mr' ? 'मराठी व इंग्रजी संवाद' : 'Bilingual Native Speech'}
                </h3>
                <p className="text-body-text text-agro-muted leading-relaxed">
                  {lang === 'mr'
                    ? 'संपूर्ण माहिती मराठीत उपलब्ध. तांत्रिक शब्द सोप्या शेती भाषेत समजावून सांगितले जातात.'
                    : '100% native localization in Marathi (मराठी) and English, supporting voice speech recognition and audio readout.'}
                </p>
              </div>

              <div className="mt-6 p-3 rounded-xl bg-agro-surface border border-agro-border flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-agro-primary shrink-0" />
                <span className="text-label-text font-semibold text-agro-cream">मराठी कृषी ज्ञानकोश समाविष्ट</span>
              </div>
            </div>

            {/* Bento Card 4: Historical Field Plot Mapping (Span 2) */}
            <div className="md:col-span-2 agro-panel p-6 sm:p-8 rounded-3xl flex flex-col justify-between">
              <div>
                <div className="w-12 h-12 rounded-2xl bg-agro-primary/10 text-agro-primary flex items-center justify-center border border-agro-primary/25 mb-4">
                  <History className="w-6 h-6" />
                </div>
                <h3 className="font-heading text-card-heading font-bold text-agro-cream mb-2">
                  {lang === 'mr' ? 'शेताचा इतिहास आणि आरोग्य नोंदी' : 'Farm Health Timeline & Diagnostic Logs'}
                </h3>
                <p className="text-body-text text-agro-muted leading-relaxed max-w-xl">
                  {lang === 'mr'
                    ? 'मागील सर्व स्कॅनचे रेकॉर्ड ठेवा, रोगातून पिकांची रिकव्हरी ट्रॅक करा आणि सल्लागार नोट्स मिळवा.'
                    : 'Maintain immutable diagnostic records across seasonal cycles. Compare leaf lesion progression over 14-day intervals to verify fungicide efficacy.'}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-agro-border flex flex-wrap items-center gap-3">
                <span className="px-3 py-1.5 rounded-lg text-supporting-text font-semibold bg-agro-surface border border-agro-border text-agro-cream flex items-center gap-1.5">
                  <Check className="w-3.5 h-3.5 text-agro-primary" /> Export Advisory Notes
                </span>
                <span className="px-3 py-1.5 rounded-lg text-supporting-text font-semibold bg-agro-surface border border-agro-border text-agro-cream flex items-center gap-1.5">
                  <Check className="w-3.5 h-3.5 text-agro-highlight" /> Plot Recovery Index
                </span>
                <span className="px-3 py-1.5 rounded-lg text-supporting-text font-semibold bg-agro-surface border border-agro-border text-agro-cream flex items-center gap-1.5">
                  <Check className="w-3.5 h-3.5 text-agro-accent" /> Multi-District Sync
                </span>
              </div>
            </div>

          </div>

        </div>
      </section>

      {/* =========================================================
       * 5. DIAGNOSTIC PIPELINE (HOW IT WORKS — 4 STEPS)
       * ======================================================= */}
      <section id="workflow" className="py-16 sm:py-24 bg-agro-surface border-y border-agro-border relative">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

          {/* Section Heading (26px, Manrope 700) */}
          <div className="text-center max-w-2xl mx-auto mb-16">
            <span className="text-supporting-text font-bold text-agro-primary uppercase tracking-widest block">
              Workflow Mechanics
            </span>
            <h2 className="font-heading text-section-heading font-bold text-agro-cream mt-2 tracking-tight">
              {lang === 'mr' ? '४ सोप्या पायऱ्यांमध्ये संपूर्ण प्रक्रिया' : 'Diagnostic Pipeline in 4 Steps'}
            </h2>
            <p className="text-body-text text-agro-muted mt-2">
              {lang === 'mr'
                ? 'शेतातून मोबाईलद्वारे थेट वापरा, एका मिनिटात अचूक निकाल.'
                : 'Engineered for simplicity in outdoor daylight conditions with high computational precision.'}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">

            {/* Step 1 */}
            <div className="agro-panel p-6 rounded-2xl space-y-3 relative">
              <div className="w-10 h-10 rounded-xl bg-agro-primary/10 text-agro-primary font-heading font-extrabold flex items-center justify-center border border-agro-primary/25 text-label-text">
                01
              </div>
              <h3 className="font-heading text-card-heading font-bold text-agro-cream">
                {lang === 'mr' ? '१. फोटो काढा किंवा निवडा' : '1. Capture Leaf'}
              </h3>
              <p className="text-supporting-text text-agro-muted leading-relaxed">
                {lang === 'mr'
                  ? 'मोबाईल कॅमेऱ्याने बाधित पानाचा फोटो घ्या किंवा गॅलरीतून इमेज फाइल अपलोड करा.'
                  : 'Take a clear photo of the symptomatic foliage in daylight or upload an existing image.'}
              </p>
            </div>

            {/* Step 2 */}
            <div className="agro-panel p-6 rounded-2xl space-y-3 relative">
              <div className="w-10 h-10 rounded-xl bg-agro-highlight/15 text-agro-highlight font-heading font-extrabold flex items-center justify-center border border-agro-highlight/30 text-label-text">
                02
              </div>
              <h3 className="font-heading text-card-heading font-bold text-agro-cream">
                {lang === 'mr' ? '२. वनस्पती पडताळणी' : '2. Botanical Check'}
              </h3>
              <p className="text-supporting-text text-agro-muted leading-relaxed">
                {lang === 'mr'
                  ? 'मॉडेल पडताळते की फोटो वनस्पतीचाच आहे आणि पिकाची प्रजाती अचूक ओळखते.'
                  : 'DINOv2 vision verifies genuine plant tissue, rejecting random objects or non-crop foliage.'}
              </p>
            </div>

            {/* Step 3 */}
            <div className="agro-panel p-6 rounded-2xl space-y-3 relative">
              <div className="w-10 h-10 rounded-xl bg-agro-accent/15 text-agro-accent font-heading font-extrabold flex items-center justify-center border border-agro-accent/30 text-label-text">
                03
              </div>
              <h3 className="font-heading text-card-heading font-bold text-agro-cream">
                {lang === 'mr' ? '३. रोग व तीव्रता विश्लेषण' : '3. Lesion Inference'}
              </h3>
              <p className="text-supporting-text text-agro-muted leading-relaxed">
                {lang === 'mr'
                  ? 'न्यूरल नेटवर्क बुरशी, जिवाणू किंवा कीड शोधते आणि संसर्गाची टक्केवारी काढते.'
                  : 'Local MobileNetV2 classifies pathogens, computes confidence %, and quantifies lesion spread.'}
              </p>
            </div>

            {/* Step 4 */}
            <div className="agro-panel p-6 rounded-2xl space-y-3 relative">
              <div className="w-10 h-10 rounded-xl bg-agro-primary/10 text-agro-primary font-heading font-extrabold flex items-center justify-center border border-agro-primary/25 text-label-text">
                04
              </div>
              <h3 className="font-heading text-card-heading font-bold text-agro-cream">
                {lang === 'mr' ? '४. औषधोपचार सल्ला' : '4. Certified Treatment'}
              </h3>
              <p className="text-supporting-text text-agro-muted leading-relaxed">
                {lang === 'mr'
                  ? 'सेंद्रिय आणि रासायनिक उपाय त्वरित मिळवा आणि AI कृषी सल्लागाराशी थेट बोला.'
                  : 'Receive dosage recommendations, spray intervals, and consult the AI agronomist.'}
              </p>
            </div>

          </div>

        </div>
      </section>

      {/* =========================================================
       * 6. INTERACTIVE AI AGRONOMIST CONSULTATION TERMINAL
       * ======================================================= */}
      <section id="ai-advisor" className="py-16 sm:py-24 relative">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">

          {/* Section Heading (26px, Manrope 700) */}
          <div className="text-center max-w-2xl mx-auto mb-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-agro-accent/15 text-agro-accent font-bold text-supporting-text border border-agro-accent/30 mb-3">
              <Bot className="w-3.5 h-3.5" />
              <span>Conversational Agronomy</span>
            </div>
            <h2 className="font-heading text-section-heading font-bold text-agro-cream tracking-tight">
              {lang === 'mr' ? 'AI कृषी सल्लागाराशी संवाद साधा' : 'Consult the AgroScan AI Agronomist'}
            </h2>
            <p className="text-body-text text-agro-muted mt-2">
              {lang === 'mr'
                ? 'खालील प्रश्नांवर क्लिक करा किंवा थेट आपले पीक स्कॅन करून सल्ला विचारा.'
                : 'Select an agronomic query below to evaluate our verified recommendations.'}
            </p>
          </div>

          {/* Interactive Chat Console Card */}
          <div className="agro-panel p-6 sm:p-8 rounded-3xl space-y-6">

            {/* Query Chips */}
            <div className="flex flex-wrap gap-2 pb-2 border-b border-agro-border">
              {sampleFaqs.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => setActiveFaqQuery(idx)}
                  className={`px-3.5 py-2 rounded-xl text-label-text font-semibold transition-all ${
                    activeFaqQuery === idx
                      ? 'bg-agro-primary text-white shadow-sm'
                      : 'bg-agro-surface hover:bg-agro-hover text-agro-muted border border-agro-border'
                  }`}
                >
                  {lang === 'mr' ? item.qMr.substring(0, 32) + '...' : item.qEn.substring(0, 32) + '...'}
                </button>
              ))}
            </div>

            {/* Conversation Flow */}
            <div className="space-y-4">
              {/* User Bubble */}
              <div className="flex items-start justify-end gap-3">
                <div className="bg-agro-primary text-white p-4 rounded-2xl rounded-tr-none text-body-text font-medium max-w-lg shadow-md shadow-orange-glow">
                  {lang === 'mr' ? sampleFaqs[activeFaqQuery].qMr : sampleFaqs[activeFaqQuery].qEn}
                </div>
                <div className="w-8 h-8 rounded-full bg-agro-surface text-agro-cream font-bold text-supporting-text flex items-center justify-center shrink-0 border border-agro-border">
                  You
                </div>
              </div>

              {/* Assistant Bubble */}
              <div className="flex items-start gap-3">
                <div className="w-8 h-8 rounded-full bg-agro-accent/15 text-agro-accent font-bold text-supporting-text flex items-center justify-center shrink-0 border border-agro-accent/30">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="bg-agro-surface border border-agro-border p-4 sm:p-5 rounded-2xl rounded-tl-none text-body-text text-agro-cream max-w-xl space-y-2 leading-relaxed">
                  <div className="flex items-center justify-between pb-2 border-b border-agro-border">
                    <span className="font-heading font-bold text-agro-primary text-label-text flex items-center gap-1.5">
                      <Sparkles className="w-3.5 h-3.5" />
                      AgroScan AI Agronomist
                    </span>
                    <span className="text-supporting-text text-agro-muted">ICAR Standard</span>
                  </div>
                  <p>{lang === 'mr' ? sampleFaqs[activeFaqQuery].aMr : sampleFaqs[activeFaqQuery].aEn}</p>
                </div>
              </div>
            </div>

            {/* Bottom Call to Action */}
            <div className="pt-4 border-t border-agro-border flex flex-col sm:flex-row items-center justify-between gap-4">
              <span className="text-supporting-text text-agro-muted text-center sm:text-left">
                {lang === 'mr'
                  ? 'तुमच्या शेतातील पानाचा फोटो जोडून थेट वैयक्तिकृत सल्ला विचारा.'
                  : 'Have a specific farm inquiry? Attach your leaf scan for context-aware diagnosis.'}
              </span>
              <button
                onClick={handleScanClick}
                className="w-full sm:w-auto px-6 py-3 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white font-bold text-button-text transition-all shadow-md shadow-orange-glow flex items-center justify-center gap-2 active:scale-95"
              >
                <ScanLine className="w-4 h-4" />
                <span>{lang === 'mr' ? 'फोटो जोडून विचारा' : 'Start New Scan'}</span>
              </button>
            </div>

          </div>

        </div>
      </section>

      {/* =========================================================
       * 7. FOOTER
       * ======================================================= */}
      <footer className="border-t border-agro-border bg-agro-card py-12 text-agro-muted text-supporting-text">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">

          {/* Logo Brand */}
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-agro-primary/10 text-agro-primary flex items-center justify-center border border-agro-primary/25">
              <Sprout className="w-4 h-4" />
            </div>
            <div>
              <span className="font-heading text-body-text font-bold text-agro-cream block">AgroScan AI</span>
              <span className="text-supporting-text text-agro-muted">Grow smarter. Intelligent plant disease detection.</span>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="flex items-center gap-6 text-label-text font-medium">
            <button onClick={() => scrollToSection('simulator')} className="hover:text-agro-cream transition">
              {lang === 'mr' ? 'पीक माहिती' : 'Crop Insights'}
            </button>
            <button onClick={() => scrollToSection('features')} className="hover:text-agro-cream transition">
              {lang === 'mr' ? 'वैशिष्ट्ये' : 'Field Intelligence'}
            </button>
            <button onClick={() => scrollToSection('workflow')} className="hover:text-agro-cream transition">
              {lang === 'mr' ? 'प्रक्रिया' : 'AI Analysis'}
            </button>
            <button onClick={() => scrollToSection('ai-advisor')} className="hover:text-agro-cream transition">
              {lang === 'mr' ? 'AI सल्लागार' : 'AI Agronomist'}
            </button>
          </div>

          <p className="text-supporting-text text-agro-muted">
            © 2026 AgroScan AI. Empowering Farmers with Artificial Intelligence.
          </p>

        </div>
      </footer>

    </div>
  );
};
