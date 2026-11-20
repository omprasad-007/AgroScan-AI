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
    <header className="sticky top-0 z-40 bg-agro-card/90 dark:bg-agro-card/90 backdrop-blur-xl border-b border-agro-border transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20">
          
          {/* Brand Logo */}
          <Link
            to={isAuthenticated ? "/dashboard" : "/"}
            className="flex items-center gap-3 group focus-visible:ring-2 focus-visible:ring-agro-primary rounded-xl"
            aria-label="AgroScan AI Home"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-agro-primary via-[#C94427] to-agro-accent text-white flex items-center justify-center shadow-md shadow-agro-primary/25 group-hover:scale-105 transition-all duration-200">
              <Sprout className="w-5 h-5 text-white" aria-hidden="true" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-heading text-lg font-extrabold tracking-tight text-agro-cream block">
                  AgroScan <span className="text-agro-primary">AI</span>
                </span>
                <span className="hidden sm:inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold bg-agro-highlight/15 text-agro-highlight border border-agro-highlight/30">
                  v2.4
                </span>
              </div>
              <span className="block text-supporting-text text-agro-muted font-medium tracking-wider uppercase">
                {t('subtitle_short') || 'Smart Plant Health Monitoring'}
              </span>
            </div>
          </Link>

          {/* Center / Right Actions */}
          <div className="flex items-center gap-2.5 sm:gap-3">
            
            {/* Primary Action CTA: Start New Scan */}
            <Link
              to="/scan"
              className={`inline-flex items-center gap-2 px-4 py-2.5 rounded-xl text-button-text font-bold transition-all duration-200 text-white ${
                isScanActive
                  ? 'bg-agro-primary shadow-lg shadow-agro-primary/30 ring-2 ring-agro-highlight'
                  : 'bg-agro-primary hover:bg-agro-primaryHover shadow-md shadow-agro-primary/25 active:scale-[0.98]'
              }`}
              title={t('nav.scan') || 'Start New Scan'}
              aria-label={t('nav.scan') || 'Start New Scan'}
            >
              <ScanLine className="w-4 h-4 shrink-0" aria-hidden="true" />
              <span className="hidden sm:inline">{t('nav.scan') || 'Start New Scan'}</span>
            </Link>

            {/* Language Switcher */}
            <button
              type="button"
              onClick={toggleLanguage}
              className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-cream text-label-text font-semibold border border-agro-border transition-all duration-150 backdrop-blur-md"
              title={lang === 'en' ? 'मराठी मध्ये बदला (Switch to Marathi)' : 'Switch to English'}
              aria-label={lang === 'en' ? 'Switch to Marathi' : 'Switch to English'}
            >
              <Globe className="w-3.5 h-3.5 text-agro-primary" aria-hidden="true" />
              <span>{lang === 'en' ? 'मराठी' : 'English'}</span>
            </button>

            {/* Theme Switcher */}
            <button
              type="button"
              onClick={toggleTheme}
              className="p-2.5 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-highlight border border-agro-border transition-all duration-150 backdrop-blur-md"
              title={theme === 'dark' ? "Switch to light theme" : "Switch to dark theme"}
              aria-label={theme === 'dark' ? "Switch to light theme" : "Switch to dark theme"}
            >
              {theme === 'dark' ? (
                <Sun className="w-4 h-4 text-agro-highlight" aria-hidden="true" />
              ) : (
                <Moon className="w-4 h-4 text-agro-accent" aria-hidden="true" />
              )}
            </button>

            {/* User Session / Auth Links */}
            {isAuthenticated ? (
              <div className="flex items-center gap-2 pl-2 border-l border-agro-border">
                <Link
                  to="/profile"
                  className="hidden md:flex items-center gap-2.5 px-3 py-1.5 rounded-xl hover:bg-agro-surface text-right transition-colors"
                  title="Farmer Profile"
                >
                  <div className="w-7 h-7 rounded-lg bg-agro-accent/15 border border-agro-accent/30 flex items-center justify-center text-agro-accent">
                    <User className="w-3.5 h-3.5" aria-hidden="true" />
                  </div>
                  <div className="flex flex-col text-left leading-tight">
                    <span className="text-label-text font-bold text-agro-cream truncate max-w-[120px]">
                      {user?.full_name || 'Farmer'}
                    </span>
                    <span className="text-supporting-text text-agro-muted truncate max-w-[120px]">
                      {user?.email}
                    </span>
                  </div>
                </Link>

                <button
                  type="button"
                  onClick={handleLogout}
                  className="p-2 rounded-xl bg-agro-surface hover:bg-agro-primary/10 text-agro-muted hover:text-agro-primary border border-agro-border transition-colors"
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
                  className="px-3 py-2 rounded-xl text-label-text font-semibold text-agro-muted hover:text-agro-cream hover:bg-agro-surface transition-colors"
                >
                  {t('nav.login') || 'Sign In'}
                </Link>
                <Link
                  to="/register"
                  className="px-3.5 py-2 rounded-xl bg-agro-surface hover:bg-agro-hover border border-agro-border text-agro-cream font-bold text-label-text transition"
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
