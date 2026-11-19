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
    { to: '/scan', label: t('nav.scan') || 'Scan Plant', icon: ScanLine, isPrimary: true },
    { to: '/history', label: t('nav.history') || 'Diagnostic History', icon: History },
    { to: '/analytics', label: t('nav.analytics') || 'Crop Analytics', icon: BarChart3 },
    { to: '/weather', label: t('nav.weather') || 'Weather Outbreak', icon: CloudSun },
    { to: '/assistant', label: t('nav.assistant') || 'AI Agronomist', icon: MessageCircle },
    { to: '/profile', label: t('nav.profile') || 'Farmer Profile', icon: User },
  ];

  if (user?.role === 'admin') {
    links.push({ to: '/admin', label: t('nav.admin') || 'Admin Panel', icon: ShieldCheck });
  }

  return (
    <aside className="w-64 bg-agro-card border-r border-agro-border shrink-0 hidden md:block min-h-[calc(100vh-4rem)] p-4 flex flex-col justify-between">
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
                  return `flex items-center justify-between px-3.5 py-3 rounded-xl font-bold text-sm transition-all duration-200 mb-2 ${
                    isActive
                      ? 'bg-agro-primary text-agro-bg shadow-md shadow-agro-primary/25 ring-2 ring-agro-primary/50'
                      : 'bg-agro-primary/15 text-agro-primary hover:bg-agro-primary hover:text-agro-bg border border-agro-primary/30 shadow-sm'
                  }`;
                }
                return `flex items-center space-x-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150 ${
                  isActive
                    ? 'bg-agro-surface text-agro-cream font-bold border border-agro-borderStrong shadow-sm'
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
                      isActive ? 'bg-agro-bg text-agro-primary' : 'bg-agro-primary/20 text-agro-primary'
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
      <div className="mt-6 p-3.5 rounded-2xl bg-agro-surface/60 border border-agro-border space-y-2">
        <div className="flex items-center gap-2 text-xs font-bold text-agro-lime">
          <Sparkles className="w-3.5 h-3.5" aria-hidden="true" />
          <span>Multi-Crop Vision AI</span>
        </div>
        <p className="text-[11px] text-agro-muted leading-relaxed">
          Capture close-up leaf photos with natural daylight for highest diagnostic accuracy.
        </p>
      </div>
    </aside>
  );
};
