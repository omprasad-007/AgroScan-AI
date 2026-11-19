import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  ScanLine, 
  History, 
  CloudSun, 
  MessageCircle, 
  User 
} from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const MobileNav = () => {
  const { t } = useLanguage();

  const links = [
    { to: '/dashboard', label: t('nav.dashboard') || 'Home', icon: LayoutDashboard },
    { to: '/history', label: t('nav.history') || 'History', icon: History },
    { to: '/scan', label: t('nav.scan') || 'Scan', icon: ScanLine, isCenterCta: true },
    { to: '/weather', label: t('nav.weather') || 'Weather', icon: CloudSun },
    { to: '/assistant', label: t('nav.assistant') || 'AI Chat', icon: MessageCircle },
    { to: '/profile', label: t('nav.profile') || 'Profile', icon: User },
  ];

  return (
    <nav
      className="fixed bottom-0 left-0 right-0 z-50 md:hidden bg-slate-900/80 dark:bg-slate-950/80 light:bg-white/85 backdrop-blur-xl border-t border-slate-800/80 dark:border-white/[0.08] light:border-slate-200/90 px-2 py-1.5 shadow-[0_-8px_30px_rgba(0,0,0,0.15)] safe-area-pb"
      aria-label="Mobile Navigation"
    >
      <div className="flex items-center justify-around max-w-md mx-auto">
        {links.map((link) => {
          const Icon = link.icon;

          if (link.isCenterCta) {
            return (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `-mt-6 flex flex-col items-center group focus-visible:outline-none`
                }
                aria-label={t('nav.scan') || 'Scan Plant'}
              >
                {({ isActive }) => (
                  <div className={`w-14 h-14 rounded-2xl flex items-center justify-center shadow-xl transition-all duration-200 active:scale-95 ${
                    isActive
                      ? 'bg-gradient-to-tr from-emerald-500 to-teal-400 text-slate-950 ring-4 ring-emerald-500/30 scale-105 shadow-emerald-500/40'
                      : 'bg-gradient-to-tr from-emerald-500 to-teal-500 text-slate-950 hover:brightness-110 shadow-emerald-500/25'
                  }`}>
                    <ScanLine className="w-6 h-6 shrink-0" aria-hidden="true" />
                  </div>
                )}
              </NavLink>
            );
          }

          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex flex-col items-center justify-center min-w-[48px] min-h-[44px] py-1 px-1.5 rounded-xl text-[10px] font-semibold transition-all duration-150 ${
                  isActive
                    ? 'text-emerald-500 font-bold scale-105'
                    : 'text-slate-400 hover:text-white dark:hover:text-white light:hover:text-slate-900'
                }`
              }
            >
              <Icon className="w-5 h-5 mb-0.5 shrink-0" aria-hidden="true" />
              <span className="truncate max-w-[56px] leading-tight">{link.label.split(' ')[0]}</span>
            </NavLink>
          );
        })}
      </div>
    </nav>
  );
};
