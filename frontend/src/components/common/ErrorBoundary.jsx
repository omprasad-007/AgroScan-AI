import React from 'react';

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
        <div className="min-h-screen flex items-center justify-center bg-slate-950 p-6 text-slate-100 font-sans">
          <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-2xl p-6 sm:p-8 shadow-2xl text-center space-y-6">
            <div className="w-16 h-16 bg-red-500/10 border border-red-500/20 rounded-full flex items-center justify-center mx-auto text-red-400">
              <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            
            <div>
              <h2 className="text-xl font-bold text-slate-100">
                {isMarathi ? 'सत्र सुरक्षितपणे पुनर्प्राप्त केले' : 'Session Recovered'}
              </h2>
              <p className="text-slate-400 text-xs sm:text-sm mt-2">
                {isMarathi
                  ? 'AgroScan AI ने ॲप्लिकेशन सुरक्षित ठेवले आहे. पुन्हा लोड करण्यासाठी खालील बटण दाबा.'
                  : 'AgroScan AI protected your application from a session error. Tap below to reload or reset session.'
                }
              </p>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
              <button
                onClick={this.handleReset}
                className="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded-xl transition border border-slate-700"
              >
                {isMarathi ? 'पुन्हा प्रयत्न करा' : 'Try Again'}
              </button>
              <button
                onClick={this.handleReload}
                className="px-4 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded-xl transition shadow-lg shadow-emerald-900/30"
              >
                {isMarathi ? 'ॲप पुन्हा लोड करा' : 'Reload App'}
              </button>
            </div>

            <div className="pt-2 border-t border-slate-800">
              <button
                onClick={this.handleClearStorage}
                className="text-xs text-slate-400 hover:text-red-400 underline transition"
              >
                {isMarathi ? 'कॅशे साफ करा आणि रीसेट करा' : 'Clear Cache & Reset Session'}
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
