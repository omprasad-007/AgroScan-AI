import React, { createContext, useCallback, useContext, useEffect, useState } from 'react';
import api, { clearStoredSession } from '../services/api';

const AuthContext = createContext(null);

const toClientUser = (user) => {
  if (!user) return null;
  const fullName = user.full_name || user.displayName || user.email?.split('@')[0] || 'Farmer';
  return {
    ...user,
    uid: user.id,
    id: user.id,
    full_name: fullName,
    displayName: fullName,
    role: user.role || 'farmer',
  };
};

const messageFromError = (error, fallback) => {
  const detail = error.response?.data?.detail;
  if (typeof detail === 'string') return detail;
  if (detail?.message) return detail.message;
  return fallback;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const clearSession = useCallback(() => {
    clearStoredSession();
    setUser(null);
  }, []);

  const saveSession = useCallback((payload) => {
    if (!payload?.access_token || !payload?.user) {
      throw new Error('The server did not return a valid sign-in session. Please try again.');
    }
    const clientUser = toClientUser(payload.user);
    localStorage.setItem('agroscan_token', payload.access_token);
    localStorage.setItem('agroscan_user', JSON.stringify(clientUser));
    setUser(clientUser);
    return clientUser;
  }, []);

  useEffect(() => {
    let mounted = true;
    const restoreSession = async () => {
      const token = localStorage.getItem('agroscan_token');
      if (!token) {
        if (mounted) setLoading(false);
        return;
      }

      try {
        const response = await api.get('/auth/me');
        if (mounted) {
          const clientUser = toClientUser(response.data);
          localStorage.setItem('agroscan_user', JSON.stringify(clientUser));
          setUser(clientUser);
        }
      } catch {
        clearStoredSession();
        if (mounted) setUser(null);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    const onSessionExpired = () => {
      if (mounted) clearSession();
    };

    window.addEventListener('agroscan:session-expired', onSessionExpired);
    restoreSession();
    return () => {
      mounted = false;
      window.removeEventListener('agroscan:session-expired', onSessionExpired);
    };
  }, [clearSession]);

  const register = async (email, password, fullName = '') => {
    setLoading(true);
    try {
      const response = await api.post('/auth/register', {
        email: email.trim(),
        password,
        full_name: fullName.trim() || email.trim().split('@')[0],
        role: 'farmer',
      });
      return saveSession(response.data);
    } catch (error) {
      throw new Error(messageFromError(error, 'Could not create your account. Please try again.'));
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    setLoading(true);
    try {
      const response = await api.post('/auth/login', { email: email.trim(), password });
      return saveSession(response.data);
    } catch (error) {
      throw new Error(messageFromError(error, 'Could not sign you in. Check your email and password.'));
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    clearSession();
    sessionStorage.removeItem('agroscan_login_marker');
  };

  const resetPassword = async () => {
    throw new Error('Password reset email is not configured yet. Please contact the project administrator to reset your password.');
  };

  return (
    <AuthContext.Provider value={{
      user,
      loading,
      isAuthenticated: Boolean(user && localStorage.getItem('agroscan_token')),
      register,
      login,
      logout,
      resetPassword,
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
