import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { Mail, ArrowLeft, CheckCircle2, AlertCircle } from 'lucide-react';

export const ForgotPasswordPage = () => {
  const { resetPassword } = useAuth();
  const { t } = useLanguage();

  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!email.trim()) {
      setErrorMsg(t('login.err_required') || 'Please enter your email address.');
      return;
    }

    setLoading(true);
    setErrorMsg('');
    setSuccessMsg('');

    try {
      await resetPassword(email.trim());
      setSuccessMsg(t('forgot.success') || 'Password reset email sent! Check your inbox for reset instructions.');
      setEmail('');
    } catch (err) {
      setErrorMsg(err.message || 'Failed to send password reset email.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto py-12 px-4 space-y-6">
      <Link to="/login" className="inline-flex items-center space-x-2 text-xs font-semibold text-agro-muted hover:text-agro-cream transition">
        <ArrowLeft className="w-4 h-4" />
        <span>{t('forgot.back_to_login') || 'Back to Sign In'}</span>
      </Link>

      <div className="agro-panel p-6 sm:p-8 rounded-3xl space-y-6 shadow-2xl">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 rounded-2xl bg-agro-primary/10 text-agro-primary flex items-center justify-center mx-auto border border-agro-primary/25 shadow-inner">
            <Mail className="w-6 h-6" />
          </div>
          <h1 className="text-2xl font-bold text-agro-cream tracking-tight">{t('forgot.title') || 'Reset Your Password'}</h1>
          <p className="text-xs text-agro-muted">
            {t('forgot.subtitle') || 'Enter your registered email address and we will send you a link to reset your password.'}
          </p>
        </div>

        {successMsg && (
          <div className="p-4 rounded-xl bg-agro-primary/15 border border-agro-primary/30 text-agro-primary text-xs flex items-center space-x-2">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>{successMsg}</span>
          </div>
        )}

        {errorMsg && (
          <div className="p-4 rounded-xl bg-agro-terracotta/15 border border-agro-terracotta/30 text-agro-cream text-xs flex items-center space-x-2">
            <AlertCircle className="w-4 h-4 shrink-0 text-agro-terracotta" />
            <span>{errorMsg}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-agro-cream/90 mb-1.5">
              {t('login.email') || 'Email Address'}
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="farmer@agroscan.ai"
              className="w-full px-4 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream placeholder-agro-muted/60 focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary transition"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-agro-primary hover:bg-agro-primary-hover text-agro-bg font-extrabold text-xs transition shadow-lg shadow-agro-primary/20 disabled:opacity-50 cursor-pointer"
          >
            {loading ? (t('common.loading') || 'Sending Link...') : (t('forgot.submit') || 'Send Reset Link')}
          </button>
        </form>

        <div className="text-center pt-2">
          <Link to="/login" className="text-xs text-agro-primary hover:text-agro-lime font-semibold transition">
            {t('forgot.back_to_login') || 'Back to Sign In'}
          </Link>
        </div>
      </div>
    </div>
  );
};
