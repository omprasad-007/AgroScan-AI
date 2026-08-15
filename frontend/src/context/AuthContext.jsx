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
        const role = firebaseUser.email?.includes('admin') ? 'admin' : 'farmer';
        const userObj = {
          uid: firebaseUser.uid,
          id: firebaseUser.uid,
          email: firebaseUser.email,
          displayName: firebaseUser.displayName || (role === 'admin' ? 'Dr. Agro Admin' : 'Kisan Ramesh Patil'),
          full_name: firebaseUser.displayName || (role === 'admin' ? 'Dr. Agro Admin' : 'Kisan Ramesh Patil'),
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
      let fbUser = null;
      try {
        fbUser = await registerUser(email, password, fullName);
      } catch (fbErr) {
        console.warn("Firebase Auth Register warning:", fbErr.message);
      }

      // Sync with backend API
      let backendUser = null;
      try {
        const res = await api.post('/auth/register', {
          email,
          password,
          full_name: fullName || 'Farmer',
          role: email.includes('admin') ? 'admin' : 'farmer',
          city: 'Pune',
          state: 'Maharashtra'
        });
        if (res.data?.access_token) {
          localStorage.setItem('agroscan_token', res.data.access_token);
          backendUser = res.data.user;
        }
      } catch (apiErr) {
        console.warn("Backend Register fallback:", apiErr);
      }

      const role = email.includes('admin') ? 'admin' : 'farmer';
      const userObj = {
        uid: fbUser?.uid || backendUser?.id || `user_${Date.now()}`,
        id: fbUser?.uid || backendUser?.id || `user_${Date.now()}`,
        email: email,
        displayName: fullName || fbUser?.displayName || (role === 'admin' ? 'Dr. Agro Admin' : 'Kisan Ramesh Patil'),
        full_name: fullName || (role === 'admin' ? 'Dr. Agro Admin' : 'Kisan Ramesh Patil'),
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
    try {
      let fbUser = null;
      try {
        fbUser = await loginUser(email, password);
      } catch (fbErr) {
        console.warn("Firebase Auth Login warning:", fbErr.message);
        // If user is not yet created in Firebase (e.g. demo accounts), auto-create in Firebase
        if (fbErr.message.includes('Incorrect email') || fbErr.message.includes('invalid-credential') || fbErr.message.includes('user-not-found')) {
          try {
            fbUser = await registerUser(email, password, email.includes('admin') ? 'Dr. Agro Admin' : 'Kisan Ramesh Patil');
          } catch (createErr) {
            console.warn("Firebase auto-register fallback warning:", createErr.message);
          }
        }
      }

      // Sync with Backend API
      const backendUser = await syncBackendUser(email, password, email.includes('admin') ? 'Dr. Agro Admin' : 'Kisan Ramesh Patil');

      const role = email.includes('admin') ? 'admin' : 'farmer';
      const userObj = {
        uid: fbUser?.uid || backendUser?.id || `user_${Date.now()}`,
        id: fbUser?.uid || backendUser?.id || `user_${Date.now()}`,
        email: email,
        displayName: fbUser?.displayName || backendUser?.full_name || (role === 'admin' ? 'Dr. Agro Admin' : 'Kisan Ramesh Patil'),
        full_name: fbUser?.displayName || backendUser?.full_name || (role === 'admin' ? 'Dr. Agro Admin' : 'Kisan Ramesh Patil'),
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
