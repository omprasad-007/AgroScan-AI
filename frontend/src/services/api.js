import axios from 'axios';

const LIVE_BACKEND_URL = 'https://agroscan-ai-backend-6ppw.onrender.com/api/v1';

const getApiBaseUrl = () => {
  let envUrl = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL;

  // Auto-heal outdated Render domain if baked in from previous Vercel deployment or stale build cache
  if (envUrl && envUrl.includes('agroscan-ai-backend.onrender.com') && !envUrl.includes('agroscan-ai-backend-6ppw')) {
    envUrl = envUrl.replace('agroscan-ai-backend.onrender.com', 'agroscan-ai-backend-6ppw.onrender.com');
  }

  // If accessing from local Wi-Fi / LAN (e.g. mobile phone browsing http://172.16.x.x:5173 or 192.168.x.x:5173)
  if (typeof window !== 'undefined' && window.location) {
    const hostname = window.location.hostname;
    const isLocalhost = hostname === 'localhost' || hostname === '127.0.0.1';
    const isVercel = hostname.endsWith('.vercel.app');

    // Only route to local port 8000 if explicitly running with localhost in development
    if (!isLocalhost && !isVercel && (envUrl && (envUrl.includes('localhost') || envUrl.includes('127.0.0.1')))) {
      return `http://${hostname}:8000/api/v1`;
    }
  }

  const rawApiUrl = envUrl || LIVE_BACKEND_URL;
  return rawApiUrl.endsWith('/api/v1') 
    ? rawApiUrl 
    : rawApiUrl.replace(/\/+$/, '') + (rawApiUrl.includes('/api') ? '' : '/api/v1');
};

const api = axios.create({
  baseURL: getApiBaseUrl(),
  timeout: 90000, // 90s timeout to tolerate Render free-tier cold starts
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
