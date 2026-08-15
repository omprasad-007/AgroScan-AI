import React from 'react';
import { Link } from 'react-router-dom';
import { Sprout, Scan, ShieldAlert, BarChart3, Bot, ArrowRight, CheckCircle2 } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';

export const LandingPage = () => {
  const { t } = useLanguage();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col justify-between">
      {/* Hero Section */}
      <div className="relative overflow-hidden pt-12 pb-20">
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-b from-agri-500/10 via-transparent to-transparent blur-3xl pointer-events-none" />
        
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-agri-500/10 border border-agri-500/20 text-agri-400 text-xs font-semibold mb-6">
            <Sprout className="w-3.5 h-3.5" />
            <span>Smart Plant Disease Detection & Crop Health Platform</span>
          </div>

          <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-agri-400 bg-clip-text text-transparent max-w-4xl mx-auto leading-tight">
            Empowering Farmers with AI-Driven Disease Diagnostics & Weather Risk Intelligence
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
            Instantly detect crop diseases, evaluate leaf lesion severity, assess weather outbreak risks, and receive organic treatment protocols.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/register"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 font-bold text-base transition-all duration-200 shadow-lg shadow-agri-500/25 flex items-center justify-center space-x-2"
            >
              <span>Get Started Free</span>
              <ArrowRight className="w-5 h-5" />
            </Link>
            <Link
              to="/login"
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 font-semibold text-base border border-slate-800 transition"
            >
              Sign In to Farm Dashboard
            </Link>
          </div>
        </div>
      </div>

      {/* Feature Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="glass-panel p-6 rounded-2xl">
          <div className="w-12 h-12 rounded-xl bg-agri-500/10 text-agri-400 flex items-center justify-center mb-4 border border-agri-500/20">
            <Scan className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Instant Leaf Scanning</h3>
          <p className="text-sm text-slate-400">
            Upload leaf photos for instant OpenCV pre-processing and AI disease prediction with confidence scores.
          </p>
        </div>

        <div className="glass-panel p-6 rounded-2xl">
          <div className="w-12 h-12 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center mb-4 border border-amber-500/20">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Severity & Weather Risk</h3>
          <p className="text-sm text-slate-400">
            Automated lesion area percentage calculation and real-time weather risk forecasting.
          </p>
        </div>

        <div className="glass-panel p-6 rounded-2xl">
          <div className="w-12 h-12 rounded-xl bg-blue-500/10 text-blue-400 flex items-center justify-center mb-4 border border-blue-500/20">
            <Bot className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white mb-2">Gemini AI Agronomist</h3>
          <p className="text-sm text-slate-400">
            Interactive AI chatbot providing organic remedies, prevention tips, and decision-support guidance.
          </p>
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
        © 2026 AgroScan AI — Smart Plant Disease Detection System. Built for Agricultural Data Science Project.
      </footer>
    </div>
  );
};
