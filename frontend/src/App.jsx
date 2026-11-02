import React from 'react';
import { BrowserRouter as Router, Navigate, Route, Routes, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';
import { ThemeProvider } from './context/ThemeContext';
import { ErrorBoundary } from './components/common/ErrorBoundary';
import { MobileNav } from './components/common/MobileNav';
import { Navbar } from './components/common/Navbar';
import { Sidebar } from './components/common/Sidebar';
import { ProtectedRoute } from './components/ProtectedRoute';
import { AdminDashboardPage } from './pages/AdminDashboardPage';
import { AnalysisPage } from './pages/AnalysisPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { AssistantPage } from './pages/AssistantPage';
import { DashboardPage } from './pages/DashboardPage';
import { ForgotPasswordPage } from './pages/ForgotPasswordPage';
import { HistoryPage } from './pages/HistoryPage';
import { LandingPage } from './pages/LandingPage';
import { LoginPage } from './pages/LoginPage';
import { ProfilePage } from './pages/ProfilePage';
import { RegisterPage } from './pages/RegisterPage';
import { ResultPage } from './pages/ResultPage';
import { ScanPage } from './pages/ScanPage';
import { WeatherRiskPage } from './pages/WeatherRiskPage';

const AppLayout = () => {
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  const isGuestFlow = location.pathname === '/scan'
    || location.pathname === '/analysis'
    || location.pathname.startsWith('/results/');
  const isPublicPage = ['/', '/login', '/register', '/forgot-password'].includes(location.pathname) || isGuestFlow;
  const showWorkspaceNavigation = isAuthenticated && !isPublicPage;

  return (
    <div className="min-h-screen flex flex-col font-sans transition-colors duration-300">
      {location.pathname !== '/' && <Navbar />}
      <div className="flex-1 flex w-full">
        {showWorkspaceNavigation && <Sidebar />}
        <main className={showWorkspaceNavigation ? 'flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto w-full pb-20 md:pb-8' : 'w-full'}>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/forgot-password" element={<ForgotPasswordPage />} />

            <Route path="/scan" element={<ScanPage />} />
            <Route path="/analysis" element={<AnalysisPage />} />
            <Route path="/results/:scanId" element={<ResultPage />} />

            <Route path="/dashboard" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
            <Route path="/history" element={<ProtectedRoute><HistoryPage /></ProtectedRoute>} />
            <Route path="/analytics" element={<ProtectedRoute><AnalyticsPage /></ProtectedRoute>} />
            <Route path="/weather" element={<ProtectedRoute><WeatherRiskPage /></ProtectedRoute>} />
            <Route path="/assistant" element={<ProtectedRoute><AssistantPage /></ProtectedRoute>} />
            <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
            <Route path="/admin" element={<ProtectedRoute adminOnly><AdminDashboardPage /></ProtectedRoute>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
      {showWorkspaceNavigation && <MobileNav />}
    </div>
  );
};

export default function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <Router future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
          <AuthProvider>
            <LanguageProvider>
              <AppLayout />
            </LanguageProvider>
          </AuthProvider>
        </Router>
      </ThemeProvider>
    </ErrorBoundary>
  );
}
