import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Sprout, Globe, LogOut, User, ShieldCheck } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useLanguage } from '../../context/LanguageContext';

export const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const { lang, toggleLanguage, t } = useLanguage();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="sticky top-0 z-40 bg-slate-900/80 backdrop-blur-md border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          
          {/* Brand Logo */}
          <Link to={isAuthenticated ? "/dashboard" : "/"} className="flex items-center space-x-3 group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-agri-600 to-agri-400 flex items-center justify-center shadow-lg shadow-agri-500/20 group-hover:scale-105 transition-transform">
              <Sprout className="w-6 h-6 text-slate-950" />
            </div>
            <div>
              <span className="text-lg font-bold bg-gradient-to-r from-white via-slate-200 to-agri-400 bg-clip-text text-transparent">
                AgroScan AI
              </span>
              <span className="block text-[10px] text-slate-400 tracking-wider font-medium uppercase">
                Smart Agriculture
              </span>
            </div>
          </Link>

          {/* Right Header Actions */}
          <div className="flex items-center space-x-3">
            
            {/* Language Switcher */}
            <button
              onClick={toggleLanguage}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition"
              title="Toggle English / Marathi"
            >
              <Globe className="w-3.5 h-3.5 text-agri-400" />
              <span>{lang === 'en' ? 'मराठी' : 'English'}</span>
            </button>

            {/* Auth Buttons or User Profile */}
            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <div className="hidden md:flex flex-col text-right">
                  <span className="text-xs font-semibold text-slate-200">{user?.full_name}</span>
                  <span className="text-[10px] text-agri-400 capitalize">{user?.role}</span>
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
                  className="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-300 hover:text-white transition"
                >
                  {t('nav.login')}
                </Link>
                <Link
                  to="/register"
                  className="px-3.5 py-1.5 rounded-lg bg-agri-600 hover:bg-agri-500 text-slate-950 font-semibold text-xs transition shadow-md shadow-agri-600/20"
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
