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
    try {
      let res;
      if (password) {
        try {
          res = await api.post('/auth/login', { email, password });
        } catch (err) {
          // If password login fails or user not in backend DB, try firebase-login sync
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
      console.warn("Backend API sync fallback used:", err);
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
    try {
      // 1. Firebase Authentication Primary
      let fbUser = null;
      try {
        fbUser = await registerUser(email, password, fullName);
      } catch (fbErr) {
        console.warn("Firebase Auth Register note:", fbErr.message);
      }

      // 2. Sync with Backend API
      let backendUser = null;
      try {
        const res = await api.post('/auth/register', {
          email,
          password,
          full_name: fullName || email.split('@')[0],
          role: email.includes('admin') ? 'admin' : 'farmer',
          city: 'Pune',
          state: 'Maharashtra'
        });
        if (res.data?.access_token) {
          localStorage.setItem('agroscan_token', res.data.access_token);
        }
        backendUser = res.data?.user;
      } catch (apiErr) {
        console.warn("Backend API sync note:", apiErr);
      }

      const role = backendUser?.role || (email.includes('admin') ? 'admin' : 'farmer');
      const cleanName = fbUser?.displayName || backendUser?.full_name || fullName.trim() || (email ? email.split('@')[0] : 'Farmer');
      const userObj = {
        uid: fbUser?.uid || backendUser?.id || `user_${Date.now()}`,
        id: fbUser?.uid || backendUser?.id || `user_${Date.now()}`,
        email: email,
        displayName: cleanName,
        full_name: cleanName,
        role: role
      };

      setUser(userObj);
      localStorage.setItem('agroscan_user', JSON.stringify(userObj));
      return userObj;
    } catch (err) {
      const msg = err.response?.data?.detail || err.message || 'Registration failed.';
      throw new Error(msg);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    setLoading(true);
    try {
      // 1. Primary Firebase Authentication
      let fbUser = null;
      let fbError = null;
      try {
        fbUser = await loginUser(email, password);
      } catch (err) {
        fbError = err;
      }

      // 2. Backend API Credential Verification
      let backendUser = null;
      let backendError = null;
      try {
        const res = await api.post('/auth/login', { email, password });
        if (res.data?.access_token) {
          localStorage.setItem('agroscan_token', res.data.access_token);
        }
        backendUser = res.data?.user;
      } catch (err) {
        backendError = err;
      }

      // If both Firebase and Backend failed, throw the relevant authentication error
      if (!fbUser && !backendUser) {
        const msg = backendError?.response?.data?.detail || fbError?.message || 'Authentication failed. Please verify credentials.';
        throw new Error(msg);
      }

      const role = backendUser?.role || (email.includes('admin') ? 'admin' : 'farmer');
      const userDisplayName = fbUser?.displayName || backendUser?.full_name || (email ? email.split('@')[0] : 'Farmer');
      const userEmail = fbUser?.email || backendUser?.email || email;

      const userObj = {
        uid: fbUser?.uid || backendUser?.id || `user_${Date.now()}`,
        id: fbUser?.uid || backendUser?.id || `user_${Date.now()}`,
        email: userEmail,
        displayName: userDisplayName,
        full_name: userDisplayName,
        role: role
      };

      setUser(userObj);
      localStorage.setItem('agroscan_user', JSON.stringify(userObj));
      return userObj;
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
