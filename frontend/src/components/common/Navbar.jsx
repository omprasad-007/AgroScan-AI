import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sprout, Globe, LogOut, Sun, Moon } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { useTheme } from '../../context/ThemeContext';

export const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const { lang, toggleLanguage, t } = useLanguage();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-40 bg-slate-900/90 dark:bg-slate-900/90 light:bg-white/90 backdrop-blur-md border-b border-slate-800 dark:border-slate-800 light:border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo */}
          <Link to={isAuthenticated ? "/dashboard" : "/"} className="flex items-center space-x-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-emerald-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform">
              <Sprout className="w-6 h-6 text-slate-950" />
            </div>
            <div>
              <span className="text-lg font-bold text-emerald-400">
                AgroScan AI
              </span>
              <span className="block text-[10px] text-slate-400 tracking-wider font-medium uppercase">
                {t('subtitle_short')}
              </span>
            </div>
          </Link>

          {/* Right Header Actions */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            
            {/* Light / Dark Theme Switcher */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-amber-400 dark:text-amber-400 light:text-slate-700 text-xs font-semibold border border-slate-700 transition"
              title={theme === 'dark' ? "Switch to Light Bright Theme" : "Switch to Dark Sleek Theme"}
            >
              {theme === 'dark' ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-indigo-600" />}
            </button>

            {/* Language Switcher */}
            <button
              onClick={toggleLanguage}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition"
              title="Toggle English / Marathi"
            >
              <Globe className="w-3.5 h-3.5 text-emerald-400" />
              <span>{lang === 'en' ? 'मराठी' : 'English'}</span>
            </button>

            {/* Auth Buttons or User Profile */}
            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <div className="hidden md:flex flex-col text-right">
                  <span className="text-xs font-semibold text-white">{user?.full_name}</span>
                  <span className="text-[10px] text-emerald-400 font-mono">{user?.email}</span>
                </div>
                <button
                  onClick={handleLogout}
                  className="p-2 rounded-lg bg-slate-800 hover:bg-red-500/10 text-slate-400 hover:text-red-400 border border-slate-700 hover:border-red-500/30 transition"
                  title={t('nav.logout')}
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <Link
                  to="/login"
                  className="px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition"
                >
                  {t('nav.login')}
                </Link>
                <Link
                  to="/register"
                  className="px-3.5 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs transition shadow-md shadow-emerald-600/20"
                >
                  {t('nav.register')}
                </Link>
              </div>
            )}
          </div>

        </div>
      </div>
    </header>
  );
};
