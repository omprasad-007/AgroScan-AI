import React, { createContext, useContext, useState, useEffect } from 'react';
import {
  subscribeToAuthState,
  registerUser,
  loginUser,
  logoutUser,
  resetPassword as firebaseResetPassword
} from '../firebase/auth';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('agroscan_user');
    return saved ? JSON.parse(saved) : null;
  });
  const [loading, setLoading] = useState(true);

  const syncBackendUser = async (email, password = null, fullName = 'Farmer User') => {
    const existingToken = localStorage.getItem('agroscan_token');
    if (existingToken && !password) {
      return JSON.parse(localStorage.getItem('agroscan_user') || 'null');
    }

    try {
      let res;
      if (password) {
        try {
          res = await api.post('/auth/login', { email, password });
        } catch (err) {
          res = await api.post('/auth/firebase-login', { email, full_name: fullName });
        }
      } else {
        res = await api.post('/auth/firebase-login', { email, full_name: fullName });
      }

      if (res.data?.access_token) {
        localStorage.setItem('agroscan_token', res.data.access_token);
      }
      return res.data?.user;
    } catch (err) {
      return null;
    }
  };

  useEffect(() => {
    const unsubscribe = subscribeToAuthState(async (firebaseUser) => {
      if (firebaseUser) {
        const deriveName = (email, inputName) => {
          if (inputName && inputName.trim()) return inputName.trim();
          if (email) {
            const prefix = email.split('@')[0];
            return prefix.charAt(0).toUpperCase() + prefix.slice(1);
          }
          return 'Farmer User';
        };

        const role = firebaseUser.email?.includes('admin') ? 'admin' : 'farmer';
        const name = deriveName(firebaseUser.email, firebaseUser.displayName);
        const userObj = {
          uid: firebaseUser.uid,
          id: firebaseUser.uid,
          email: firebaseUser.email,
          displayName: name,
          full_name: name,
          photoURL: firebaseUser.photoURL || null,
          emailVerified: firebaseUser.emailVerified,
          role: role
        };
        setUser(userObj);
        localStorage.setItem('agroscan_user', JSON.stringify(userObj));
        await syncBackendUser(firebaseUser.email, null, userObj.displayName);
      } else {
        const savedUser = localStorage.getItem('agroscan_user');
        if (!savedUser) {
          setUser(null);
        }
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const register = async (email, password, fullName = '') => {
    setLoading(true);
    const cleanEmail = email.trim();
    const cleanName = fullName.trim() || cleanEmail.split('@')[0];

    try {
      let backendUser = null;
      let token = null;

      // 1. Register with Backend API
      try {
        const res = await api.post('/auth/register', {
          email: cleanEmail,
          password: password,
          full_name: cleanName,
          role: cleanEmail.includes('admin') ? 'admin' : 'farmer',
          city: 'Pune',
          state: 'Maharashtra'
        });
        if (res.data?.access_token) {
          token = res.data.access_token;
          localStorage.setItem('agroscan_token', token);
        }
        backendUser = res.data?.user;
      } catch (apiErr) {
        if (apiErr.response?.data?.detail?.toLowerCase().includes('already registered')) {
          throw new Error('An account with this email address already exists. Please sign in instead.');
        }
        console.warn("Backend API register notice:", apiErr);
      }

      // 2. Register with Firebase Authentication
      let fbUser = null;
      try {
        fbUser = await registerUser(cleanEmail, password, cleanName);
      } catch (fbErr) {
        if (fbErr.message?.toLowerCase().includes('already in use')) {
          throw new Error('An account with this email address already exists. Please sign in instead.');
        }
        console.warn("Firebase Auth Register note:", fbErr.message);
      }

      // If backend was sleeping or didn't return token during registration, sync via firebase-login
      if (!token) {
        try {
          const syncRes = await api.post('/auth/firebase-login', {
            email: cleanEmail,
            full_name: cleanName
          });
          if (syncRes.data?.access_token) {
            token = syncRes.data.access_token;
            localStorage.setItem('agroscan_token', token);
          }
          if (!backendUser) backendUser = syncRes.data?.user;
        } catch (syncErr) {
          console.warn("Token recovery sync notice:", syncErr);
        }
      }

      // Ensure fallback token is present
      if (!token) {
        const fallbackToken = `token_${Date.now()}_${btoa(cleanEmail)}`;
        localStorage.setItem('agroscan_token', fallbackToken);
      }

      const role = backendUser?.role || (cleanEmail.includes('admin') ? 'admin' : 'farmer');
      const userObj = {
        uid: backendUser?.id || fbUser?.uid || `user_${Date.now()}`,
        id: backendUser?.id || fbUser?.uid || `user_${Date.now()}`,
        email: cleanEmail,
        displayName: cleanName,
        full_name: cleanName,
        role: role
      };

      setUser(userObj);
      localStorage.setItem('agroscan_user', JSON.stringify(userObj));
      return userObj;
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    setLoading(true);
    const cleanEmail = email.trim();

    try {
      let backendUser = null;
      let token = null;
      let backendError = null;

      // 1. Primary Backend API Verification
      try {
        const res = await api.post('/auth/login', { email: cleanEmail, password });
        if (res.data?.access_token) {
          token = res.data.access_token;
          localStorage.setItem('agroscan_token', token);
        }
        backendUser = res.data?.user;
      } catch (err) {
        backendError = err;
      }

      // 2. Firebase Authentication Verification
      let fbUser = null;
      let fbError = null;
      try {
        fbUser = await loginUser(cleanEmail, password);
      } catch (err) {
        fbError = err;
      }

      // If backend login succeeded with credentials
      if (backendUser && token) {
        const role = backendUser.role || (cleanEmail.includes('admin') ? 'admin' : 'farmer');
        const userDisplayName = backendUser.full_name || cleanEmail.split('@')[0];
        const userObj = {
          uid: backendUser.id,
          id: backendUser.id,
          email: backendUser.email || cleanEmail,
          displayName: userDisplayName,
          full_name: userDisplayName,
          role: role
        };
        setUser(userObj);
        localStorage.setItem('agroscan_user', JSON.stringify(userObj));
        return userObj;
      }

      // If Firebase verified the credentials but backend user record was absent (e.g. Render restart)
      if (fbUser) {
        try {
          const syncRes = await api.post('/auth/firebase-login', {
            email: cleanEmail,
            full_name: fbUser.displayName || cleanEmail.split('@')[0]
          });
          if (syncRes.data?.access_token) {
            token = syncRes.data.access_token;
            localStorage.setItem('agroscan_token', token);
          }
          backendUser = syncRes.data?.user;
        } catch (syncErr) {
          console.warn("Backend sync notice:", syncErr);
        }

        if (!token) {
          const fallbackToken = `token_${Date.now()}_${btoa(cleanEmail)}`;
          localStorage.setItem('agroscan_token', fallbackToken);
        }

        const role = backendUser?.role || (cleanEmail.includes('admin') ? 'admin' : 'farmer');
        const userDisplayName = fbUser.displayName || backendUser?.full_name || cleanEmail.split('@')[0];
        const userObj = {
          uid: fbUser.uid || backendUser?.id || `user_${Date.now()}`,
          id: fbUser.uid || backendUser?.id || `user_${Date.now()}`,
          email: cleanEmail,
          displayName: userDisplayName,
          full_name: userDisplayName,
          role: role
        };
        setUser(userObj);
        localStorage.setItem('agroscan_user', JSON.stringify(userObj));
        return userObj;
      }

      // If both authentication attempts failed, throw the exact relevant error
      if (backendError?.response?.status === 401 || fbError?.message?.toLowerCase().includes('password') || fbError?.message?.toLowerCase().includes('credential')) {
        throw new Error('Incorrect password. Please verify your password and try again.');
      } else if (backendError?.response?.status === 404 || fbError?.message?.toLowerCase().includes('not found')) {
        throw new Error('User account not found. Please click Create Account below to get started.');
      } else {
        const msg = backendError?.response?.data?.detail || fbError?.message || 'Authentication failed. Please check your email and password.';
        throw new Error(msg);
      }
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    try {
      try {
        await logoutUser();
      } catch (err) {
        console.warn("Firebase logout warning:", err);
      }
      setUser(null);
      localStorage.removeItem('agroscan_user');
      localStorage.removeItem('agroscan_token');
      sessionStorage.clear();
    } finally {
      setLoading(false);
    }
  };

  const resetPassword = async (email) => {
    return await firebaseResetPassword(email);
  };

  const value = {
    user,
    loading,
    isAuthenticated: !!user,
    register,
    login,
    logout,
    resetPassword
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
