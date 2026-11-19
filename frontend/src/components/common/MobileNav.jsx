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
      className="fixed bottom-0 left-0 right-0 z-50 md:hidden bg-agro-card/95 backdrop-blur-lg border-t border-agro-border px-2 py-1.5 shadow-2xl safe-area-pb"
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
                  `-mt-5 flex flex-col items-center group focus-visible:outline-none`
                }
                aria-label={t('nav.scan') || 'Scan Plant'}
              >
                {({ isActive }) => (
                  <div className={`w-13 h-13 rounded-2xl flex items-center justify-center shadow-lg transition-transform duration-150 active:scale-95 ${
                    isActive
                      ? 'bg-agro-primary text-agro-bg ring-4 ring-agro-primary/20 scale-105'
                      : 'bg-agro-primary text-agro-bg hover:bg-agro-primaryHover'
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
                `flex flex-col items-center justify-center min-w-[48px] min-h-[44px] py-1 px-1.5 rounded-xl text-[10px] font-semibold transition-colors duration-150 ${
                  isActive
                    ? 'text-agro-primary font-bold'
                    : 'text-agro-muted hover:text-agro-cream'
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
