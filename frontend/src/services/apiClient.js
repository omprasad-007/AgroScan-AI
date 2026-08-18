import axios from 'axios';

const rawApiUrl = import.meta.env.VITE_API_URL || import.meta.env.VITE_API_BASE_URL || '/api/v1';
const API_BASE_URL = rawApiUrl.endsWith('/api/v1') 
  ? rawApiUrl 
  : (rawApiUrl === '/api/v1' ? rawApiUrl : rawApiUrl.replace(/\/+$/, '') + (rawApiUrl.includes('/api') ? '' : '/api/v1'));

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000, // 15s request timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request Interceptor: Attach Bearer JWT token automatically
apiClient.interceptors.request.use(
  (config) => {
    try {
      const token = localStorage.getItem('agroscan_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (e) {
      console.warn("Storage token read error:", e);
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Standardized Error Handling & Session Expiry Detection
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const status = error.response?.status;
    const detail = error.response?.data?.detail;

    if (status === 401) {
      console.warn("Session expired or unauthenticated. Clearing token.");
      try {
        localStorage.removeItem('agroscan_token');
        localStorage.removeItem('agroscan_user');
      } catch (e) {}
    } else if (status === 403) {
      console.warn("Access denied. Insufficient permissions.");
    } else if (status === 429) {
      console.warn("Rate limit exceeded. Please wait a moment before retrying.");
    } else if (status >= 500) {
      console.error("Server error encountered:", detail || error.message);
    } else if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
      console.warn("API Request timed out after 15 seconds.");
    }

    return Promise.reject(error);
  }
);

export default apiClient;
