import api from './api';

const WEATHER_CACHE_KEY = 'agroscan_local_weather_cache';
const CACHE_TTL_MS = 15 * 60 * 1000; // 15 minutes

export const getCachedWeather = () => {
  try {
    const raw = sessionStorage.getItem(WEATHER_CACHE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (Date.now() - parsed.timestamp < CACHE_TTL_MS) {
      return parsed.data;
    }
  } catch {
    // Ignore cache parse error
  }
  return null;
};

export const setCachedWeather = (data) => {
  try {
    sessionStorage.setItem(WEATHER_CACHE_KEY, JSON.stringify({
      data,
      timestamp: Date.now(),
    }));
  } catch {
    // SessionStorage may be disabled
  }
};

/**
 * Automatically detects the farmer's live location via device GPS / HTML5 Geolocation,
 * fetches real-time ambient temperature, humidity, rainfall, wind speed, and weather condition,
 * and falls back gracefully to city/district detection if permission is not granted.
 */
export const detectLocalWeather = async (lang = 'en', forceRefresh = false) => {
  if (!forceRefresh) {
    const cached = getCachedWeather();
    if (cached) return cached;
  }

  const weatherLang = lang === 'mr' ? 'mr' : 'en';

  // 1. Try Browser HTML5 GPS Geolocation
  if (typeof navigator !== 'undefined' && navigator.geolocation) {
    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          resolve,
          reject,
          { timeout: 7000, maximumAge: 300000, enableHighAccuracy: true }
        );
      });

      const { latitude, longitude } = position.coords;
      const res = await api.get('/weather/current', {
        params: { lat: latitude, lon: longitude, lang: weatherLang },
      });

      const weatherData = {
        location: res.data.location || 'Local Farm',
        temperature_c: Number(res.data.temperature_c ?? 26.5),
        humidity_pct: Number(res.data.humidity_pct ?? 75.0),
        rainfall_mm: Number(res.data.rainfall_mm ?? 0.0),
        condition: res.data.condition || 'Clear sky',
        wind_speed_kmh: Number(res.data.wind_speed_kmh ?? 12.0),
        latitude,
        longitude,
        isGpsDetected: true,
        detectedAt: new Date().toISOString(),
      };

      setCachedWeather(weatherData);
      return weatherData;
    } catch {
      // Geolocation denied, unavailable, or timed out - seamlessly fall back to IP/District
    }
  }

  // 2. Fallback: Query default agricultural district / Pune
  try {
    const res = await api.get('/weather/current', {
      params: { city: 'Pune', lang: weatherLang },
    });

    const fallbackData = {
      location: res.data.location || 'Pune District',
      temperature_c: Number(res.data.temperature_c ?? 26.5),
      humidity_pct: Number(res.data.humidity_pct ?? 75.0),
      rainfall_mm: Number(res.data.rainfall_mm ?? 0.0),
      condition: res.data.condition || 'Clear sky',
      wind_speed_kmh: Number(res.data.wind_speed_kmh ?? 12.0),
      latitude: res.data.latitude || 18.5204,
      longitude: res.data.longitude || 73.8567,
      isGpsDetected: false,
      detectedAt: new Date().toISOString(),
    };

    setCachedWeather(fallbackData);
    return fallbackData;
  } catch (err) {
    // Ultimate offline fallback
    return {
      location: 'Pune District',
      temperature_c: 26.5,
      humidity_pct: 75.0,
      rainfall_mm: 0.0,
      condition: 'Partly Cloudy',
      wind_speed_kmh: 12.0,
      latitude: 18.5204,
      longitude: 73.8567,
      isGpsDetected: false,
      detectedAt: new Date().toISOString(),
    };
  }
};

/**
 * Fetch live weather for a specific city or district entered by the user.
 */
export const fetchCityWeather = async (cityName, lang = 'en') => {
  const weatherLang = lang === 'mr' ? 'mr' : 'en';
  const res = await api.get('/weather/current', {
    params: { city: cityName, lang: weatherLang },
  });

  const data = {
    location: res.data.location || cityName,
    temperature_c: Number(res.data.temperature_c ?? 26.5),
    humidity_pct: Number(res.data.humidity_pct ?? 75.0),
    rainfall_mm: Number(res.data.rainfall_mm ?? 0.0),
    condition: res.data.condition || 'Clear sky',
    wind_speed_kmh: Number(res.data.wind_speed_kmh ?? 12.0),
    latitude: res.data.latitude,
    longitude: res.data.longitude,
    isGpsDetected: false,
    detectedAt: new Date().toISOString(),
  };

  setCachedWeather(data);
  return data;
};
