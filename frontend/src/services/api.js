import axios from 'axios';
import { 
  MOCK_USER, 
  MOCK_ADMIN, 
  MOCK_FARMS, 
  MOCK_PREDICTIONS, 
  MOCK_RECOMMENDATIONS, 
  MOCK_DASHBOARD_ANALYTICS 
} from './mockData';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('agroscan_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Fallback Mock Interceptor for 100% Standalone Frontend Execution
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const url = error.config?.url || '';
    const method = (error.config?.method || 'get').toLowerCase();

    console.warn(`API Server offline/unreachable at ${url}. Returning Standalone Mock Data.`);

    // Mock Route Handling
    if (url.includes('/auth/login')) {
      const body = JSON.parse(error.config.data || '{}');
      const isPass = body.password === 'password123' || body.password === 'admin123';
      if (!isPass) {
        return Promise.reject({ response: { data: { detail: 'Incorrect email or password' } } });
      }
      const user = body.email.includes('admin') ? MOCK_ADMIN : MOCK_USER;
      return { data: { access_token: 'mock_jwt_token_123', token_type: 'bearer', user } };
    }

    if (url.includes('/auth/register')) {
      const body = JSON.parse(error.config.data || '{}');
      const user = { ...MOCK_USER, email: body.email, full_name: body.full_name, city: body.city || 'Pune' };
      return { data: { access_token: 'mock_jwt_token_123', token_type: 'bearer', user } };
    }

    if (url.includes('/analytics/dashboard')) {
      return { data: MOCK_DASHBOARD_ANALYTICS };
    }

    if (url.includes('/predictions/history')) {
      return { data: MOCK_PREDICTIONS };
    }

    if (url.includes('/predictions/analyze')) {
      const newPred = {
        id: `pred_${Date.now()}`,
        crop_detected: "Tomato",
        disease_name: "Tomato Late Blight",
        disease_code: "tomato_late_blight",
        confidence_score: 0.942,
        severity_percentage: 22.5,
        severity_level: "Moderate",
        affected_area_cm2: 11.25,
        ambient_temp_c: 26.5,
        humidity_pct: 82.0,
        rainfall_mm: 5.0,
        weather_risk_score: 82.5,
        weather_risk_level: "High",
        is_demo: true,
        created_at: new Date().toISOString(),
        image_url: "https://images.unsplash.com/photo-1592417817098-8f3d6eb16431?w=600&q=80"
      };
      MOCK_PREDICTIONS.unshift(newPred);
      return { data: newPred };
    }

    if (url.includes('/predictions/')) {
      const id = url.split('/predictions/')[1];
      const found = MOCK_PREDICTIONS.find(p => p.id === id) || MOCK_PREDICTIONS[0];
      return { data: found };
    }

    if (url.includes('/recommendations/')) {
      return { data: { id: "rec_101", prediction_id: "pred_001", ...MOCK_RECOMMENDATIONS.tomato_late_blight } };
    }

    if (url.includes('/weather/risk')) {
      const body = JSON.parse(error.config.data || '{}');
      return {
        data: {
          risk_score: 82.5,
          risk_level: "High",
          contributing_factors: [
            `Optimal thermal range for spore germination (${body.temperature_c || 26.5}°C)`,
            `Elevated humidity level (${body.humidity_pct || 82}%) promoting leaf wetness`
          ],
          advice: "Favorable weather for fungal outbreak. Apply preventive organic/copper spray every 5-7 days."
        }
      };
    }

    if (url.includes('/chat')) {
      const body = JSON.parse(error.config.data || '{}');
      return {
        data: {
          id: `msg_${Date.now()}`,
          sender: "assistant",
          content: `**AgroScan AI Agronomist (Mock Mode)**:\n\nRegarding your question: "${body.message}"\n\n- **Organic Remedy**: Spray neem oil (5ml/L) or copper octanoate soap solution every 7-10 days.\n- **Prevention**: Avoid overhead watering during evening hours to keep leaves dry.\n- **Note**: Always follow local product label guidelines.`,
          created_at: new Date().toISOString()
        }
      };
    }

    if (url.includes('/farms') && method === 'get') {
      return { data: MOCK_FARMS };
    }

    if (url.includes('/farms') && method === 'post') {
      const body = JSON.parse(error.config.data || '{}');
      const newFarm = { id: `farm_${Date.now()}`, ...body, user_id: MOCK_USER.id, created_at: new Date().toISOString() };
      MOCK_FARMS.push(newFarm);
      return { data: newFarm };
    }

    if (url.includes('/admin/users')) {
      return { data: [MOCK_USER, MOCK_ADMIN] };
    }

    if (url.includes('/admin/analytics')) {
      return {
        data: {
          system_status: "Operational",
          total_users: 2,
          total_scans: 50,
          demo_scans: 50,
          ml_scans: 0
        }
      };
    }

    return Promise.reject(error);
  }
);

export default api;
