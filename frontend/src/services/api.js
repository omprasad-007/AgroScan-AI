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

let pendingAuthPromise = null;

export const ensureAuthToken = async () => {
  let token = localStorage.getItem('agroscan_token');
  if (token && token !== 'null' && token !== 'undefined') {
    return token;
  }

  if (pendingAuthPromise) {
    return pendingAuthPromise;
  }

  pendingAuthPromise = (async () => {
    try {
      const res = await axios.post(getApiBaseUrl() + '/auth/login', {
        email: 'farmer@agroscan.ai',
        password: 'password123',
      }, { timeout: 8000 });

      if (res.data?.access_token) {
        localStorage.setItem('agroscan_token', res.data.access_token);
        if (res.data.user) {
          localStorage.setItem('agroscan_user', JSON.stringify(res.data.user));
        }
        return res.data.access_token;
      }
    } catch {
      // Offline or backend temporarily booting
    } finally {
      pendingAuthPromise = null;
    }
    return null;
  })();

  return pendingAuthPromise;
};

const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 90000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use(async (config) => {
  let token = localStorage.getItem('agroscan_token');
  const isAuthRequest = config.url && (config.url.includes('/auth/login') || config.url.includes('/auth/register'));

  if ((!token || token === 'null' || token === 'undefined') && !isAuthRequest) {
    token = await ensureAuthToken();
  }

  if (token && token !== 'null' && token !== 'undefined') {
    config.headers.Authorization = 'Bearer ' + token;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error.response?.status;
    const originalRequest = error.config;
    const requestUrl = originalRequest?.url || '';
    const isAuthRequest = requestUrl.includes('/auth/login') || requestUrl.includes('/auth/register');

    if (status === 401 && !isAuthRequest && originalRequest && !originalRequest._retry) {
      originalRequest._retry = true;
      localStorage.removeItem('agroscan_token');
      const refreshedToken = await ensureAuthToken();
      if (refreshedToken) {
        originalRequest.headers.Authorization = 'Bearer ' + refreshedToken;
        return api(originalRequest);
      }
      clearStoredSession();
      window.dispatchEvent(new CustomEvent('agroscan:session-expired'));
    }

    return Promise.reject(error);
  },
);

export default api;
