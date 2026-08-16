import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Scan, 
  History, 
  CloudSun, 
  Bot, 
  User 
} from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const MobileNav = () => {
  const { t } = useLanguage();

  const links = [
    { to: '/dashboard', label: t('nav.dashboard'), icon: LayoutDashboard },
    { to: '/scan', label: t('nav.scan'), icon: Scan },
    { to: '/history', label: t('nav.history'), icon: History },
    { to: '/weather', label: t('nav.weather'), icon: CloudSun },
    { to: '/assistant', label: t('nav.assistant'), icon: Bot },
    { to: '/profile', label: t('nav.profile'), icon: User },
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 z-50 md:hidden bg-slate-900/95 dark:bg-slate-900/95 light:bg-white/95 backdrop-blur-lg border-t border-slate-800 dark:border-slate-800 light:border-slate-200 px-2 py-1 shadow-2xl">
      <div className="flex items-center justify-around">
        {links.map((link) => {
          const Icon = link.icon;
          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex flex-col items-center py-1 px-2 rounded-xl text-[10px] font-semibold transition-all duration-200 ${
                  isActive
                    ? 'text-emerald-400 dark:text-emerald-400 light:text-emerald-600 font-bold scale-105'
                    : 'text-slate-400 hover:text-slate-200'
                }`
              }
            >
              <Icon className="w-5 h-5 mb-0.5" />
              <span className="truncate max-w-[50px]">{link.label.split(' ')[0]}</span>
            </NavLink>
          );
        })}
      </div>
    </div>
  );
};
