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
    <header className="sticky top-0 z-40 bg-agro-card/95 backdrop-blur-md border-b border-agro-border">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo */}
          <Link
            to={isAuthenticated ? "/dashboard" : "/"}
            className="flex items-center gap-3 group focus-visible:ring-2 focus-visible:ring-agro-primary rounded-xl"
            aria-label="AgroScan AI Home"
          >
            <div className="w-10 h-10 rounded-xl bg-agro-primary/15 border border-agro-primary/30 flex items-center justify-center text-agro-primary group-hover:bg-agro-primary group-hover:text-agro-bg transition-all duration-200">
              <Sprout className="w-5 h-5" aria-hidden="true" />
            </div>
            <div>
              <span className="text-base font-extrabold tracking-tight text-agro-cream block">
                AgroScan <span className="text-agro-primary">AI</span>
              </span>
              <span className="block text-[10px] text-agro-muted tracking-wider font-semibold uppercase">
                {t('subtitle_short') || 'Smart Agriculture & Diagnostics'}
              </span>
            </div>
          </Link>

          {/* Center / Right Actions */}
          <div className="flex items-center gap-2 sm:gap-3">
            
            {/* Primary Action CTA: Scan Plant */}
            <Link
              to="/scan"
              className={`inline-flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-bold transition-all duration-150 ${
                isScanActive
                  ? 'bg-agro-primary text-agro-bg shadow-md shadow-agro-primary/25 ring-2 ring-agro-primary/40'
                  : 'bg-agro-primary hover:bg-agro-primaryHover text-agro-bg shadow-sm shadow-agro-primary/20 active:scale-[0.98]'
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
              className="inline-flex items-center gap-1.5 px-3 py-2 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-cream text-xs font-semibold border border-agro-border transition-colors duration-150"
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
              className="p-2 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-amber border border-agro-border transition-colors duration-150"
              title={theme === 'dark' ? "Switch to warm light theme" : "Switch to dark forest theme"}
              aria-label={theme === 'dark' ? "Switch to light theme" : "Switch to dark theme"}
            >
              {theme === 'dark' ? (
                <Sun className="w-4 h-4 text-agro-amber" aria-hidden="true" />
              ) : (
                <Moon className="w-4 h-4 text-agro-muted" aria-hidden="true" />
              )}
            </button>

            {/* User Session / Auth Links */}
            {isAuthenticated ? (
              <div className="flex items-center gap-2 pl-1 border-l border-agro-border">
                <Link
                  to="/profile"
                  className="hidden md:flex items-center gap-2 px-2.5 py-1.5 rounded-xl hover:bg-agro-surface text-right transition-colors"
                  title="Farmer Profile"
                >
                  <div className="w-7 h-7 rounded-lg bg-agro-surface border border-agro-border flex items-center justify-center text-agro-lime">
                    <User className="w-3.5 h-3.5" aria-hidden="true" />
                  </div>
                  <div className="flex flex-col text-left leading-tight">
                    <span className="text-xs font-bold text-agro-cream truncate max-w-[120px]">
                      {user?.full_name || 'Farmer'}
                    </span>
                    <span className="text-[10px] text-agro-muted truncate max-w-[120px]">
                      {user?.email}
                    </span>
                  </div>
                </Link>

                <button
                  type="button"
                  onClick={handleLogout}
                  className="p-2 rounded-xl bg-agro-surface hover:bg-agro-terracotta/15 text-agro-muted hover:text-agro-terracotta border border-agro-border hover:border-agro-terracotta/30 transition-colors"
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
                  className="px-3 py-1.5 rounded-xl text-xs font-bold text-agro-cream hover:bg-agro-surface border border-transparent hover:border-agro-border transition-colors"
                >
                  {t('nav.login') || 'Sign In'}
                </Link>
                <Link
                  to="/register"
                  className="px-3.5 py-1.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-agro-bg font-extrabold text-xs transition shadow-sm"
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
