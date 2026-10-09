import axios from 'axios';

const getApiBaseUrl = () => {
  const envUrl = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL;

  // If accessing from local Wi-Fi / LAN (e.g. mobile phone browsing http://172.16.x.x:5173 or 192.168.x.x:5173)
  if (typeof window !== 'undefined' && window.location) {
    const hostname = window.location.hostname;
    const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1';
    const isVercel = hostname.endsWith('.vercel.app');

    if (!isLocalhost && !isVercel && (!envUrl || envUrl.includes('localhost') || envUrl.includes('127.0.0.1'))) {
      return `http://${hostname}:8000/api/v1`;
    }
  }

  const rawApiUrl = envUrl || 'http://localhost:8000/api/v1';
  return rawApiUrl.endsWith('/api/v1') 
    ? rawApiUrl 
    : rawApiUrl.replace(/\/+$/, '') + (rawApiUrl.includes('/api') ? '' : '/api/v1');
};

const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 60000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach Authorization Bearer Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('agroscan_token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Clean error handling without fake mock data substitutions
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // If backend returns a structured error, propagate it cleanly
    return Promise.reject(error);
  }
);

export default api;
