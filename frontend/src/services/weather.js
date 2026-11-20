import api from './api';

const WEATHER_CACHE_KEY = 'agroscan_local_weather_cache';
const FARM_DISTRICT_KEY = 'agroscan_farm_district';
const CACHE_TTL_MS = 5 * 60 * 1000; // 5 minutes cache

export const getSavedFarmDistrict = () => {
  try {
    return localStorage.getItem(FARM_DISTRICT_KEY) || 'Kolhapur';
  } catch {
    return 'Kolhapur';
  }
};

export const setSavedFarmDistrict = (districtName) => {
  try {
    if (districtName) {
      localStorage.setItem(FARM_DISTRICT_KEY, districtName);
    }
  } catch {
    // LocalStorage error
  }
};

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
 * Detects local weather for the farmer:
 * 1. If GPS is specifically requested, queries HTML5 Geolocation.
 * 2. If user has a saved farm district, uses their selected district (never forces Pune).
 * 3. Falls back to backend location lookup.
 */
export const detectLocalWeather = async (lang = 'en', forceRefresh = false, useGps = false) => {
  if (forceRefresh) {
    clearWeatherCache();
  } else {
    const cached = getCachedWeather();
    if (cached && !useGps) return cached;
  }

  const weatherLang = lang === 'mr' ? 'mr' : 'en';

  // 1. Try Browser HTML5 GPS Geolocation if requested or available
  if (useGps && typeof navigator !== 'undefined' && navigator.geolocation) {
    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(
          resolve,
          reject,
          { timeout: 7000, maximumAge: 30000, enableHighAccuracy: true }
        );
      });

      const { latitude, longitude } = position.coords;
      const res = await api.get('/weather/current', {
        params: { lat: latitude, lon: longitude, lang: weatherLang },
      });

      const weatherData = {
        location: res.data.location || 'Local Farm GPS',
        temperature_c: Number(res.data.temperature_c ?? 26.5),
        humidity_pct: Number(res.data.humidity_pct ?? 55.0),
        rainfall_mm: Number(res.data.rainfall_mm ?? 0.0),
        condition: res.data.condition || 'Clear sky',
        wind_speed_kmh: Number(res.data.wind_speed_kmh ?? 8.0),
        latitude: Number(res.data.latitude ?? latitude),
        longitude: Number(res.data.longitude ?? longitude),
        isGpsDetected: true,
        detectionMethod: 'device_gps',
        spraying_advisory: res.data.spraying_advisory || null,
        liveApi: res.data.live_api ?? true,
        detectedAt: new Date().toISOString(),
      };

      setCachedWeather(weatherData);
      return weatherData;
    } catch (gpsErr) {
      console.warn("GPS Geolocation notice:", gpsErr);
      throw new Error(gpsErr.code === 1 ? 'PERMISSION_DENIED' : 'GPS_UNAVAILABLE');
    }
  }

  // 2. Check farmer's saved farm district first (defaults to Kolhapur agro-hub, NOT false Pune)
  const targetDistrict = getSavedFarmDistrict();
  try {
    const res = await api.get('/weather/current', {
      params: { city: targetDistrict, lang: weatherLang },
    });

    const weatherData = {
      location: res.data.location || targetDistrict,
      temperature_c: Number(res.data.temperature_c ?? 26.5),
      humidity_pct: Number(res.data.humidity_pct ?? 55.0),
      rainfall_mm: Number(res.data.rainfall_mm ?? 0.0),
      condition: res.data.condition || 'Clear sky',
      wind_speed_kmh: Number(res.data.wind_speed_kmh ?? 8.0),
      latitude: Number(res.data.latitude ?? 16.705),
      longitude: Number(res.data.longitude ?? 74.243),
      isGpsDetected: false,
      detectionMethod: res.data.detection_method || 'district_select',
      spraying_advisory: res.data.spraying_advisory || null,
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
  const cleanName = cityName.trim();
  const res = await api.get('/weather/current', {
    params: { city: cleanName, lang: weatherLang },
  });

  const data = {
    location: res.data.location || cleanName,
    temperature_c: Number(res.data.temperature_c ?? 26.5),
    humidity_pct: Number(res.data.humidity_pct ?? 55.0),
    rainfall_mm: Number(res.data.rainfall_mm ?? 0.0),
    condition: res.data.condition || 'Clear sky',
    wind_speed_kmh: Number(res.data.wind_speed_kmh ?? 8.0),
    latitude: Number(res.data.latitude ?? 16.705),
    longitude: Number(res.data.longitude ?? 74.243),
    isGpsDetected: res.data.is_gps ?? false,
    detectionMethod: res.data.detection_method || 'city_query',
    spraying_advisory: res.data.spraying_advisory || null,
    liveApi: res.data.live_api ?? true,
    detectedAt: new Date().toISOString(),
  };

  setSavedFarmDistrict(cleanName);
  setCachedWeather(data);
  return data;
};

/**
 * Fetch 5-day daily agricultural forecast including foliar spraying advisory
 */
export const fetchWeatherForecast = async (cityName = null, lat = null, lon = null, lang = 'en') => {
  const weatherLang = lang === 'mr' ? 'mr' : 'en';
  const params = { lang: weatherLang };
  if (lat && lon) {
    params.lat = lat;
    params.lon = lon;
  } else {
    params.city = (cityName || getSavedFarmDistrict()).trim();
  }

  const res = await api.get('/weather/forecast', { params });
  return res.data;
};
