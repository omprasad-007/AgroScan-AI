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
    <aside className="w-64 bg-white/85 dark:bg-slate-950/70 backdrop-blur-xl border-r border-slate-200/90 dark:border-white/[0.08] shrink-0 hidden md:block min-h-[calc(100vh-4rem)] p-4 flex flex-col justify-between transition-colors duration-300">
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
                  return `flex items-center justify-between px-3.5 py-3 rounded-xl font-bold text-sm transition-all duration-200 mb-2.5 ${
                    isActive
                      ? 'bg-gradient-to-r from-emerald-500 to-teal-500 text-white shadow-lg shadow-emerald-500/25 ring-2 ring-emerald-400/50'
                      : 'bg-emerald-500/10 text-emerald-700 dark:text-emerald-400 hover:bg-emerald-500 hover:text-white border border-emerald-500/25 shadow-sm'
                  }`;
                }
                return `flex items-center space-x-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-150 ${
                  isActive
                    ? 'bg-slate-100 dark:bg-slate-800/90 text-slate-900 dark:text-white font-bold border border-slate-300/80 dark:border-slate-700 shadow-sm'
                    : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800/50 border border-transparent'
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
                      isActive ? 'bg-white/20 text-white' : 'bg-emerald-500/20 text-emerald-700 dark:text-emerald-400'
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
      <div className="mt-6 p-4 rounded-2xl glass-card space-y-2">
        <div className="flex items-center gap-2 text-xs font-bold text-emerald-600 dark:text-emerald-400">
          <Sparkles className="w-4 h-4 text-emerald-600 dark:text-emerald-400" aria-hidden="true" />
          <span>Multi-Crop Vision AI</span>
        </div>
        <p className="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
          Capture close-up leaf photos with natural daylight for highest diagnostic accuracy.
        </p>
      </div>
    </aside>
  );
};
