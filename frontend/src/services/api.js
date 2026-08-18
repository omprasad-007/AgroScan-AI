import axios from 'axios';

const rawApiUrl = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';
// Ensure base URL points to /api/v1 without duplicate trailing paths
const normalizedBaseUrl = rawApiUrl.endsWith('/api/v1') 
  ? rawApiUrl 
  : rawApiUrl.replace(/\/+$/, '') + (rawApiUrl.includes('/api') ? '' : '/api/v1');

const api = axios.create({
  baseURL: normalizedBaseUrl,
  timeout: 15000,
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
