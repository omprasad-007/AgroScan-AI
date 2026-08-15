import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Scan, 
  History, 
  BarChart3, 
  CloudSun, 
  Bot, 
  ShieldCheck, 
  User 
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';

export const Sidebar = () => {
  const { user } = useAuth();
  const { t } = useLanguage();

  const links = [
    { to: '/dashboard', label: t('nav.dashboard'), icon: LayoutDashboard },
    { to: '/scan', label: t('nav.scan'), icon: Scan },
    { to: '/history', label: t('nav.history'), icon: History },
    { to: '/analytics', label: t('nav.analytics'), icon: BarChart3 },
    { to: '/weather', label: t('nav.weather'), icon: CloudSun },
    { to: '/assistant', label: t('nav.assistant'), icon: Bot },
    { to: '/profile', label: t('nav.profile'), icon: User },
  ];

  if (user?.role === 'admin') {
    links.push({ to: '/admin', label: t('nav.admin'), icon: ShieldCheck });
  }

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 shrink-0 hidden md:block min-h-[calc(100vh-4rem)] p-4">
      <nav className="space-y-1.5">
        {links.map((link) => {
          const Icon = link.icon;
          return (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3.5 py-2.5 rounded-xl font-medium text-sm transition-all duration-200 ${
                  isActive
                    ? 'bg-agri-500/10 text-agri-400 border border-agri-500/20 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-4 h-4 shrink-0" />
              <span>{link.label}</span>
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
};
