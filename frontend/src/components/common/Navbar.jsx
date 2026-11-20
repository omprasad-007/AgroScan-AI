import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Sprout, Globe, LogOut, Sun, Moon, ScanLine, User } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';
import { useTheme } from '../../context/ThemeContext';

export const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const { lang, toggleLanguage, t } = useLanguage();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isScanActive = location.pathname === '/scan' || location.pathname === '/analysis';

  return (
    <header className="sticky top-0 z-40 bg-white/85 dark:bg-slate-950/80 backdrop-blur-xl border-b border-slate-200/90 dark:border-white/[0.08] shadow-[0_4px_24px_-4px_rgba(0,0,0,0.06)] dark:shadow-[0_4px_24px_-4px_rgba(0,0,0,0.3)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo */}
          <Link
            to={isAuthenticated ? "/dashboard" : "/"}
            className="flex items-center gap-3 group focus-visible:ring-2 focus-visible:ring-emerald-500 rounded-xl"
            aria-label="AgroScan AI Home"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 text-white flex items-center justify-center shadow-lg shadow-emerald-500/25 group-hover:scale-105 transition-all duration-200">
              <Sprout className="w-5 h-5" aria-hidden="true" />
            </div>
            <div>
              <span className="text-base font-extrabold tracking-tight text-slate-900 dark:text-white block">
                AgroScan <span className="text-emerald-500 dark:text-emerald-400">AI</span>
              </span>
              <span className="block text-[10px] text-slate-500 dark:text-slate-400 font-semibold tracking-wider uppercase">
                {t('subtitle_short') || 'Smart Agriculture & Diagnostics'}
              </span>
            </div>
          </Link>

          {/* Center / Right Actions */}
          <div className="flex items-center gap-2 sm:gap-3">
            
            {/* Primary Action CTA: Scan Plant */}
            <Link
              to="/scan"
              className={`inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all duration-200 text-white ${
                isScanActive
                  ? 'bg-emerald-500 shadow-lg shadow-emerald-500/30 ring-2 ring-emerald-400'
                  : 'bg-emerald-500 hover:bg-emerald-600 shadow-md shadow-emerald-500/25 hover:shadow-emerald-500/40 active:scale-[0.98]'
              }`}
              title={t('nav.scan') || 'Scan Plant Leaf'}
              aria-label={t('nav.scan') || 'Scan Plant Leaf'}
            >
              <ScanLine className="w-4 h-4 shrink-0" aria-hidden="true" />
              <span className="hidden sm:inline">{t('nav.scan') || 'Scan Plant'}</span>
            </Link>

            {/* Language Switcher */}
            <button
              type="button"
              onClick={toggleLanguage}
              className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800/80 dark:hover:bg-slate-700/80 text-slate-700 dark:text-slate-200 text-xs font-semibold border border-slate-200 dark:border-slate-700/80 transition-all duration-150 backdrop-blur-md"
              title={lang === 'en' ? 'मराठी मध्ये बदला (Switch to Marathi)' : 'Switch to English'}
              aria-label={lang === 'en' ? 'Switch to Marathi' : 'Switch to English'}
            >
              <Globe className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" aria-hidden="true" />
              <span>{lang === 'en' ? 'मराठी' : 'English'}</span>
            </button>

            {/* Theme Switcher */}
            <button
              type="button"
              onClick={toggleTheme}
              className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-800/80 dark:hover:bg-slate-700/80 text-amber-500 dark:text-amber-400 border border-slate-200 dark:border-slate-700/80 transition-all duration-150 backdrop-blur-md"
              title={theme === 'dark' ? "Switch to light theme" : "Switch to dark theme"}
              aria-label={theme === 'dark' ? "Switch to light theme" : "Switch to dark theme"}
            >
              {theme === 'dark' ? (
                <Sun className="w-4 h-4 text-amber-400" aria-hidden="true" />
              ) : (
                <Moon className="w-4 h-4 text-slate-600" aria-hidden="true" />
              )}
            </button>

            {/* User Session / Auth Links */}
            {isAuthenticated ? (
              <div className="flex items-center gap-2 pl-1 border-l border-slate-200 dark:border-slate-800">
                <Link
                  to="/profile"
                  className="hidden md:flex items-center gap-2 px-2.5 py-1.5 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800/60 text-right transition-colors"
                  title="Farmer Profile"
                >
                  <div className="w-7 h-7 rounded-lg bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
                    <User className="w-3.5 h-3.5" aria-hidden="true" />
                  </div>
                  <div className="flex flex-col text-left leading-tight">
                    <span className="text-xs font-bold text-slate-900 dark:text-white truncate max-w-[120px]">
                      {user?.full_name || 'Farmer'}
                    </span>
                    <span className="text-[10px] text-slate-500 dark:text-slate-400 truncate max-w-[120px]">
                      {user?.email}
                    </span>
                  </div>
                </Link>

                <button
                  type="button"
                  onClick={handleLogout}
                  className="p-2 rounded-xl bg-slate-100 hover:bg-rose-50 dark:bg-slate-800/80 dark:hover:bg-rose-500/20 text-slate-500 hover:text-rose-600 dark:text-slate-400 dark:hover:text-rose-400 border border-slate-200 hover:border-rose-200 dark:border-slate-700/80 dark:hover:border-rose-500/30 transition-colors"
                  title={t('nav.logout') || 'Sign Out'}
                  aria-label={t('nav.logout') || 'Sign Out'}
                >
                  <LogOut className="w-4 h-4" aria-hidden="true" />
                </button>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link
                  to="/login"
                  className="px-3 py-1.5 rounded-xl text-xs font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 border border-transparent hover:border-slate-200 dark:hover:border-slate-700 transition-colors"
                >
                  {t('nav.login') || 'Sign In'}
                </Link>
                <Link
                  to="/register"
                  className="px-3.5 py-1.5 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-white font-extrabold text-xs transition shadow-sm"
                >
                  {t('nav.register') || 'Register'}
                </Link>
              </div>
            )}

          </div>

        </div>
      </div>
    </header>
  );
};
