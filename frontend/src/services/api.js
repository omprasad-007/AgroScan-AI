import axios from 'axios';

const LIVE_BACKEND_URL = 'https://agroscan-ai-backend-6ppw.onrender.com/api/v1';

export const getApiBaseUrl = () => {
  let envUrl = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL;

  if (envUrl && envUrl.includes('agroscan-ai-backend.onrender.com') && !envUrl.includes('agroscan-ai-backend-6ppw')) {
    envUrl = envUrl.replace('agroscan-ai-backend.onrender.com', 'agroscan-ai-backend-6ppw.onrender.com');
  }

  if (typeof window !== 'undefined' && window.location) {
    const hostname = window.location.hostname;
    const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1';
    const isVercel = hostname.endsWith('.vercel.app');
    if (!isLocalhost && !isVercel && envUrl && (envUrl.includes('localhost') || envUrl.includes('127.0.0.1'))) {
      return 'http://' + hostname + ':8000/api/v1';
    }
  }

  const rawApiUrl = envUrl || LIVE_BACKEND_URL;
  return rawApiUrl.endsWith('/api/v1')
    ? rawApiUrl
    : rawApiUrl.replace(/\/+$/, '') + (rawApiUrl.includes('/api') ? '' : '/api/v1');
};

export const clearStoredSession = () => {
  localStorage.removeItem('agroscan_token');
  localStorage.removeItem('agroscan_user');
  localStorage.removeItem('agroscan_user_email');
  localStorage.removeItem('agroscan_login_marker');
};

const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 90000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('agroscan_token');
  if (token) {
    config.headers.Authorization = 'Bearer ' + token;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;
    const requestUrl = error.config?.url || '';
    const isAuthRequest = requestUrl.startsWith('/auth/');

    if (status === 401 && !isAuthRequest) {
      clearStoredSession();
      window.dispatchEvent(new CustomEvent('agroscan:session-expired'));
    }

    return Promise.reject(error);
  },
);

export default api;
