import React from 'react';
import { AlertTriangle, RotateCcw, Home } from 'lucide-react';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error("AgroScan AI UI Error Caught:", error, errorInfo);
    this.setState({ errorInfo });
  }

  handleReload = () => {
    window.location.reload();
  };

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  handleClearStorage = () => {
    try {
      localStorage.clear();
      sessionStorage.clear();
    } catch (e) {}
    window.location.href = '/';
  };

  render() {
    if (this.state.hasError) {
      const isMarathi = typeof window !== 'undefined' && localStorage.getItem('agroscan_language') === 'mr';

      return (
        <div className="min-h-screen flex items-center justify-center bg-agro-bg p-6 text-agro-cream font-sans">
          <div className="max-w-md w-full bg-agro-card border border-agro-border rounded-3xl p-6 sm:p-8 shadow-2xl text-center space-y-6">
            <div className="w-16 h-16 bg-agro-terracotta/15 border border-agro-terracotta/30 rounded-2xl flex items-center justify-center mx-auto text-agro-terracotta">
              <AlertTriangle className="w-8 h-8" aria-hidden="true" />
            </div>
            
            <div className="space-y-2">
              <h1 className="text-xl font-extrabold text-agro-cream">
                {isMarathi ? 'सत्र सुरक्षितपणे पुनर्प्राप्त केले' : 'Interface Recovery'}
              </h1>
              <p className="text-agro-muted text-xs sm:text-sm leading-relaxed">
                {isMarathi
                  ? 'AgroScan AI ने ॲप्लिकेशन सुरक्षित ठेवले आहे. पुन्हा लोड करण्यासाठी खालील बटण दाबा.'
                  : 'AgroScan AI encountered a render notice. You can safely reload or return to the dashboard.'
                }
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
              <button
                type="button"
                onClick={this.handleReload}
                className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-bold transition shadow-md active:scale-95"
              >
                <RotateCcw className="w-3.5 h-3.5" aria-hidden="true" />
                <span>{isMarathi ? 'पुन्हा लोड करा' : 'Reload Page'}</span>
              </button>
              
              <button
                type="button"
                onClick={this.handleClearStorage}
                className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-agro-surface hover:bg-agro-hover border border-agro-border text-agro-muted hover:text-agro-cream text-xs font-semibold transition"
              >
                <Home className="w-3.5 h-3.5" aria-hidden="true" />
                <span>{isMarathi ? 'मुख्यपृष्ठावर जा' : 'Reset to Home'}</span>
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
