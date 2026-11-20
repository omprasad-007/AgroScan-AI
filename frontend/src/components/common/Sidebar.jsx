import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  ScanLine, 
  History, 
  BarChart3, 
  CloudSun, 
  MessageCircle, 
  ShieldCheck, 
  User,
  Sparkles
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';

export const Sidebar = () => {
  const { user } = useAuth();
  const { t } = useLanguage();

  const links = [
    { to: '/dashboard', label: t('nav.dashboard') || 'Dashboard', icon: LayoutDashboard },
    { to: '/scan', label: t('nav.scan') || 'Start New Scan', icon: ScanLine, isPrimary: true },
    { to: '/history', label: t('nav.history') || 'Diagnostic History', icon: History },
    { to: '/analytics', label: t('nav.analytics') || 'Crop Insights', icon: BarChart3 },
    { to: '/weather', label: t('nav.weather') || 'Weather Outbreak', icon: CloudSun },
    { to: '/assistant', label: t('nav.assistant') || 'AI Agronomist', icon: MessageCircle },
    { to: '/profile', label: t('nav.profile') || 'Farmer Profile', icon: User },
  ];

  if (user?.role === 'admin') {
    links.push({ to: '/admin', label: t('nav.admin') || 'Admin Panel', icon: ShieldCheck });
  }

  return (
    <aside className="w-64 bg-agro-card/90 backdrop-blur-xl border-r border-agro-border shrink-0 hidden md:block min-h-[calc(100vh-4rem)] p-4 flex flex-col justify-between transition-colors duration-200">
      <nav className="space-y-1.5" aria-label="Main navigation">
        {links.map((link) => {
          const Icon = link.icon;
          const isPrimary = link.isPrimary;

          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => {
                if (isPrimary) {
                  return `flex items-center justify-between px-3.5 py-3 rounded-xl font-bold text-button-text transition-all duration-200 mb-2.5 ${
                    isActive
                      ? 'bg-agro-primary text-white shadow-md shadow-orange-glow ring-2 ring-agro-highlight/50'
                      : 'bg-agro-primary/10 text-agro-primary hover:bg-agro-primary hover:text-white border border-agro-primary/25 shadow-sm'
                  }`;
                }
                return `flex items-center space-x-3 px-3.5 py-2.5 rounded-xl font-medium text-label-text transition-all duration-150 ${
                  isActive
                    ? 'bg-agro-surface text-agro-cream font-bold border border-agro-border shadow-sm'
                    : 'text-agro-muted hover:text-agro-cream hover:bg-agro-surface border border-transparent'
                }`;
              }}
            >
              {({ isActive }) => (
                <>
                  <div className="flex items-center space-x-3">
                    <Icon className="w-4 h-4 shrink-0" aria-hidden="true" />
                    <span>{link.label}</span>
                  </div>
                  {isPrimary && (
                    <span className={`text-[10px] uppercase tracking-wider font-extrabold px-1.5 py-0.5 rounded-md ${
                      isActive ? 'bg-white/20 text-white' : 'bg-agro-highlight/20 text-agro-highlight'
                    }`}>
                      Live
                    </span>
                  )}
                </>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Helpful Quick Prompt Card */}
      <div className="mt-6 p-4 rounded-2xl agro-panel space-y-2">
        <div className="flex items-center gap-2 text-label-text font-bold text-agro-highlight">
          <Sparkles className="w-4 h-4 text-agro-highlight" aria-hidden="true" />
          <span>AgroScan Intelligence</span>
        </div>
        <p className="text-supporting-text text-agro-muted leading-relaxed">
          Intelligent plant disease detection and real-time crop monitoring.
        </p>
      </div>
    </aside>
  );
};
