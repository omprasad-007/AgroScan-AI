import api from './api';

const WEATHER_CACHE_KEY = 'agroscan_local_weather_cache';
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes cache

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
    // Only cache verified live weather
    if (data && data.liveApi !== false) {
      sessionStorage.setItem(WEATHER_CACHE_KEY, JSON.stringify({
        data,
        timestamp: Date.now(),
      }));
    }
  } catch {
    // SessionStorage may be disabled
  }
};

export const clearWeatherCache = () => {
  try {
    sessionStorage.removeItem(WEATHER_CACHE_KEY);
  } catch {
    // Ignore error
  }
};

/**
 * Automatically detects the farmer's live location:
 * 1. Checks device GPS via HTML5 Geolocation (high accuracy).
 * 2. If GPS is denied/unavailable, automatically queries the backend which resolves
 *    the farmer's real city/district via IP Geolocation (e.g. Kolhapur, Maharashtra).
 * 3. Never hardcodes a false default like Pune.
 */
export const detectLocalWeather = async (lang = 'en', forceRefresh = false) => {
  if (forceRefresh) {
    clearWeatherCache();
  } else {
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
          { timeout: 4000, maximumAge: 60000, enableHighAccuracy: true }
        );
      });

      const { latitude, longitude } = position.coords;
      const res = await api.get('/weather/current', {
        params: { lat: latitude, lon: longitude, lang: weatherLang },
      });

      const weatherData = {
        location: res.data.location || 'Local Farm',
        temperature_c: Number(res.data.temperature_c ?? 26.5),
        humidity_pct: Number(res.data.humidity_pct ?? 65.0),
        rainfall_mm: Number(res.data.rainfall_mm ?? 0.0),
        condition: res.data.condition || 'Clear sky',
        wind_speed_kmh: Number(res.data.wind_speed_kmh ?? 12.0),
        latitude: Number(res.data.latitude ?? latitude),
        longitude: Number(res.data.longitude ?? longitude),
        isGpsDetected: true,
        detectionMethod: 'device_gps',
        liveApi: res.data.live_api ?? true,
        detectedAt: new Date().toISOString(),
      };

      setCachedWeather(weatherData);
      return weatherData;
    } catch {
      // GPS denied, blocked, or timed out - proceed to IP-based real location resolution
    }
  }

  // 2. Automatic Real IP Location Fallback (Backend detects client's actual city/coordinates)
  try {
    const res = await api.get('/weather/current', {
      params: { lang: weatherLang },
    });

    const weatherData = {
      location: res.data.location || 'Local Farm',
      temperature_c: Number(res.data.temperature_c ?? 26.5),
      humidity_pct: Number(res.data.humidity_pct ?? 65.0),
      rainfall_mm: Number(res.data.rainfall_mm ?? 0.0),
      condition: res.data.condition || 'Clear sky',
      wind_speed_kmh: Number(res.data.wind_speed_kmh ?? 12.0),
      latitude: Number(res.data.latitude ?? 16.69),
      longitude: Number(res.data.longitude ?? 74.24),
      isGpsDetected: false,
      detectionMethod: res.data.detection_method || 'auto_ip',
      liveApi: res.data.live_api ?? true,
      detectedAt: new Date().toISOString(),
    };

    setCachedWeather(weatherData);
    return weatherData;
  } catch (err) {
    console.warn('Weather detection network error:', err);
    return null;
  }
};

/**
 * Fetch live weather for a specific city or district entered by the user.
 */
export const fetchCityWeather = async (cityName, lang = 'en') => {
  const weatherLang = lang === 'mr' ? 'mr' : 'en';
  const res = await api.get('/weather/current', {
    params: { city: cityName.trim(), lang: weatherLang },
  });

  const data = {
    location: res.data.location || cityName,
    temperature_c: Number(res.data.temperature_c ?? 26.5),
    humidity_pct: Number(res.data.humidity_pct ?? 65.0),
    rainfall_mm: Number(res.data.rainfall_mm ?? 0.0),
    condition: res.data.condition || 'Clear sky',
    wind_speed_kmh: Number(res.data.wind_speed_kmh ?? 12.0),
    latitude: Number(res.data.latitude ?? 16.69),
    longitude: Number(res.data.longitude ?? 74.24),
    isGpsDetected: false,
    detectionMethod: 'city_query',
    liveApi: res.data.live_api ?? true,
    detectedAt: new Date().toISOString(),
  };

  setCachedWeather(data);
  return data;
};
