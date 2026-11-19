import React, { useState } from 'react';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { UserPlus, AlertCircle } from 'lucide-react';

export const RegisterPage = () => {
  const { register } = useAuth();
  const { lang, setLang, t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  const searchParams = new URLSearchParams(location.search);
  const redirectTarget = searchParams.get('redirect') || '/dashboard';

  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    password: '',
    confirmPassword: '',
    city: 'Pune',
    preferredLanguage: lang
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.fullName.trim() || !formData.email.trim() || !formData.password) {
      setError(t('register.err_required') || 'Please fill in all required fields.');
      return;
    }

    if (formData.password.length < 6) {
      setError(t('register.password') || 'Password must be at least 6 characters long.');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError(t('register.err_match') || 'Passwords do not match. Please verify and try again.');
      return;
    }

    setLoading(true);
    try {
      if (formData.preferredLanguage !== lang) {
        setLang(formData.preferredLanguage);
      }
      await register(formData.email.trim(), formData.password, formData.fullName.trim());
      navigate(redirectTarget, { replace: true });
    } catch (err) {
      setError(err.message || t('login.err_failed') || 'Registration failed. Email may already be registered.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto py-12 px-4 space-y-6">
      <div className="agro-panel p-6 sm:p-8 rounded-3xl space-y-6 shadow-2xl">
        
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-agro-primary/10 text-agro-primary flex items-center justify-center mx-auto border border-agro-primary/25 shadow-inner">
            <UserPlus className="w-6 h-6" />
          </div>
          <h1 className="text-2xl font-bold text-agro-cream tracking-tight">{t('register.title') || 'Create Farmer Account'}</h1>
          <p className="text-xs text-agro-muted">
            {t('register.subtitle') || 'Create your farmer account for disease diagnostics & weather alerts'}
          </p>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-agro-terracotta/15 border border-agro-terracotta/30 text-agro-cream text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-agro-terracotta" />
            <span className="font-semibold">{error}</span>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-agro-cream/90 mb-1.5">
              {t('register.full_name') || 'Full Name'} *
            </label>
            <input
              type="text"
              name="fullName"
              value={formData.fullName}
              onChange={handleChange}
              placeholder="Ramesh Patil"
              className="w-full px-4 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream placeholder-agro-muted/60 focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary transition"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-agro-cream/90 mb-1.5">
              {t('register.email') || 'Email Address'} *
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="name@gmail.com"
              className="w-full px-4 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream placeholder-agro-muted/60 focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary transition"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-agro-cream/90 mb-1.5">
                {t('register.password') || 'Password'} *
              </label>
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="••••••••"
                className="w-full px-4 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream placeholder-agro-muted/60 focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary transition"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-agro-cream/90 mb-1.5">
                {t('register.confirm_password') || 'Confirm Password'} *
              </label>
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="••••••••"
                className="w-full px-4 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream placeholder-agro-muted/60 focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary transition"
                required
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-agro-cream/90 mb-1.5">
                {t('profile.district') || 'District / City'}
              </label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleChange}
                placeholder="Pune"
                className="w-full px-4 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream placeholder-agro-muted/60 focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary transition"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-agro-cream/90 mb-1.5">
                {t('profile.language') || 'Preferred Language'}
              </label>
              <select
                name="preferredLanguage"
                value={formData.preferredLanguage}
                onChange={handleChange}
                className="w-full px-4 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary font-semibold transition cursor-pointer"
              >
                <option value="en">English (EN)</option>
                <option value="mr">मराठी (MR)</option>
              </select>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-agro-primary hover:bg-agro-primary-hover text-agro-bg font-extrabold text-xs transition shadow-lg shadow-agro-primary/20 flex items-center justify-center space-x-2 disabled:opacity-50 cursor-pointer"
          >
            <UserPlus className="w-4 h-4" />
            <span>{loading ? (t('register.registering') || 'Creating Account...') : (t('register.submit') || 'Register Account')}</span>
          </button>
        </form>

        <div className="text-center pt-2">
          <p className="text-xs text-agro-muted">
            {t('register.have_account') || 'Already have an account?'}{' '}
            <Link to="/login" className="text-agro-primary hover:text-agro-lime font-semibold transition">
              {t('register.sign_in') || 'Login'}
            </Link>
          </p>
        </div>

      </div>
    </div>
  );
};
