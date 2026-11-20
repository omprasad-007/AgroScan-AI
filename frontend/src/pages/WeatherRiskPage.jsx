import React, { useState, useEffect, useCallback } from 'react';
import { CloudSun, HelpCircle, MapPin, Navigation, Search, CheckCircle2, ShieldCheck, Thermometer, Droplets, CloudRain } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { WeatherRiskBadge } from '../components/common/Badge';
import { detectLocalWeather, fetchCityWeather } from '../services/weather';
import api from '../services/api';

export const WeatherRiskPage = () => {
  const { t, translateCrop, lang } = useLanguage();
  const [temp, setTemp] = useState(24.5);
  const [humidity, setHumidity] = useState(82.0);
  const [rainfall, setRainfall] = useState(5.0);
  const [crop, setCrop] = useState('Tomato');
  const [riskResult, setRiskResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [weatherMeta, setWeatherMeta] = useState(null);
  const [detectingGps, setDetectingGps] = useState(false);
  const [cityInput, setCityInput] = useState('');

  const availableCrops = [
    'Tomato', 'Potato', 'Rice', 'Wheat', 'Cotton',
    'Soybean', 'Maize', 'Chilli', 'Onion', 'Sugarcane'
  ];

  const evaluateRisk = useCallback(async (tVal, hVal, rVal, cVal) => {
    setLoading(true);
    try {
      const res = await api.post('/weather/risk', {
        temperature_c: parseFloat(tVal),
        humidity_pct: parseFloat(hVal),
        rainfall_mm: parseFloat(rVal),
        crop: cVal,
      });
      setRiskResult(res.data);
    } catch (err) {
      console.error('Failed to compute risk:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleDetectLocation = useCallback(async (force = false) => {
    setDetectingGps(true);
    try {
      const live = await detectLocalWeather(lang, force);
      if (live) {
        setWeatherMeta(live);
        setTemp(live.temperature_c);
        setHumidity(live.humidity_pct);
        setRainfall(live.rainfall_mm);
        evaluateRisk(live.temperature_c, live.humidity_pct, live.rainfall_mm, crop);
      }
    } catch (err) {
      console.warn('Weather detection notice:', err);
    } finally {
      setDetectingGps(false);
    }
  }, [crop, evaluateRisk, lang]);

  useEffect(() => {
    handleDetectLocation(false);
  }, [handleDetectLocation]);

  const handleCitySearch = async (e) => {
    e.preventDefault();
    if (!cityInput.trim()) return;
    setDetectingGps(true);
    try {
      const res = await fetchCityWeather(cityInput.trim(), lang);
      if (res) {
        setWeatherMeta(res);
        setTemp(res.temperature_c);
        setHumidity(res.humidity_pct);
        setRainfall(res.rainfall_mm);
        evaluateRisk(res.temperature_c, res.humidity_pct, res.rainfall_mm, crop);
        setCityInput('');
      }
    } catch (err) {
      console.warn('City weather search failed:', err);
    } finally {
      setDetectingGps(false);
    }
  };

  const handleEvaluate = (e) => {
    if (e) e.preventDefault();
    evaluateRisk(temp, humidity, rainfall, crop);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header */}
      <div>
        <div className="flex items-center space-x-2">
          <h1 className="text-2xl sm:text-3xl font-extrabold text-agro-cream tracking-tight">
            {t('weather.title') || 'Weather Outbreak Risk Simulator'}
          </h1>
          <span className="px-2.5 py-0.5 rounded-full bg-agro-primary/10 border border-agro-primary/30 text-[10px] font-bold text-agro-primary uppercase tracking-wide">
            {t('weather.decision_engine') || 'Scientific Decision Engine'}
          </span>
        </div>
        <p className="text-xs sm:text-sm text-agro-muted mt-1">
          {t('weather.subtitle') || 'Evaluate ambient weather parameters against crop-specific pathogen germination thresholds to forecast outbreak probability and explain WHY.'}
        </p>
      </div>

      {/* Live Farm Weather & GPS Microclimate Detector Card */}
      <div className="agro-panel p-5 rounded-2xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-agro-primary/10 border border-agro-primary/25 flex items-center justify-center text-agro-primary shrink-0">
              <MapPin className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-sm font-extrabold text-agro-cream">
                  {weatherMeta?.location ? weatherMeta.location : 'Detecting Farm Location...'}
                </span>
                <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold ${
                  weatherMeta?.isGpsDetected
                    ? 'bg-agro-primary/15 text-agro-primary border border-agro-primary/30'
                    : 'bg-agro-lime/15 text-agro-lime border border-agro-lime/30'
                }`}>
                  <span className="w-1.5 h-1.5 rounded-full bg-agro-primary animate-ping mr-1.5" />
                  {weatherMeta?.isGpsDetected ? 'Device GPS Microclimate' : 'District Microclimate'}
                </span>
              </div>
              <p className="text-xs text-agro-muted mt-0.5">
                {weatherMeta?.condition || 'Clear sky'} • {temp}°C • {humidity}% Humidity • {rainfall}mm Rain
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2 shrink-0">
            <button
              type="button"
              onClick={() => handleDetectLocation(true)}
              disabled={detectingGps}
              className="inline-flex items-center space-x-1.5 px-3 py-2 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-primary border border-agro-primary/30 text-xs font-semibold transition disabled:opacity-50"
            >
              <Navigation className={`w-3.5 h-3.5 ${detectingGps ? 'animate-spin' : ''}`} />
              <span>{detectingGps ? 'Detecting GPS...' : 'Detect Farm GPS'}</span>
            </button>
          </div>
        </div>

        {/* Quick Search Alternative City or Village */}
        <form onSubmit={handleCitySearch} className="flex items-center gap-2 pt-2 border-t border-agro-border/70">
          <div className="relative flex-1">
            <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-agro-muted" />
            <input
              type="text"
              value={cityInput}
              onChange={(e) => setCityInput(e.target.value)}
              placeholder="Search other district or village (e.g. Kolhapur, Solapur, Nashik)..."
              className="w-full pl-8 pr-3 py-1.5 rounded-xl bg-white dark:bg-slate-900/70 border border-slate-200 dark:border-white/10 text-xs text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary transition"
            />
          </div>
          <button
            type="submit"
            disabled={detectingGps || !cityInput.trim()}
            className="px-3 py-1.5 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-cream text-xs font-semibold border border-agro-border transition disabled:opacity-40"
          >
            Search
          </button>
        </form>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Input Controls */}
        <form onSubmit={handleEvaluate} className="agro-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-sm font-bold text-agro-cream flex items-center space-x-2">
            <CloudSun className="w-4 h-4 text-agro-primary" />
            <span>{t('weather.card_params') || 'Weather & Crop Parameters'}</span>
          </h3>

          <div>
            <label className="block text-xs font-medium text-agro-muted mb-1.5">
              {t('weather.target_crop') || 'Target Crop'}
            </label>
            <select
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl bg-white dark:bg-slate-900/70 border border-slate-200 dark:border-white/10 text-xs text-slate-900 dark:text-slate-100 focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary font-semibold transition cursor-pointer"
            >
              {availableCrops.map((c) => (
                <option key={c} value={c}>{translateCrop(c)}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-agro-muted mb-1.5 flex justify-between">
              <span className="flex items-center space-x-1.5">
                <Thermometer className="w-3.5 h-3.5 text-agro-primary" />
                <span>{t('weather.temp') || 'Ambient Temperature (°C)'}</span>
              </span>
              <strong className="text-agro-primary font-mono">{temp}°C</strong>
            </label>
            <input
              type="range"
              min="5"
              max="45"
              step="0.5"
              value={temp}
              onChange={(e) => setTemp(e.target.value)}
              className="w-full accent-agro-primary cursor-pointer"
            />
          </div>

          <div>
            <label className="text-xs font-medium text-agro-muted mb-1.5 flex justify-between">
              <span className="flex items-center space-x-1.5">
                <Droplets className="w-3.5 h-3.5 text-agro-lime" />
                <span>{t('weather.humidity') || 'Relative Humidity (%)'}</span>
              </span>
              <strong className="text-agro-lime font-mono">{humidity}%</strong>
            </label>
            <input
              type="range"
              min="20"
              max="100"
              step="1"
              value={humidity}
              onChange={(e) => setHumidity(e.target.value)}
              className="w-full accent-agro-primary cursor-pointer"
            />
          </div>

          <div>
            <label className="text-xs font-medium text-agro-muted mb-1.5 flex justify-between">
              <span className="flex items-center space-x-1.5">
                <CloudRain className="w-3.5 h-3.5 text-agro-amber" />
                <span>{t('weather.rainfall') || '24h Rainfall (mm)'}</span>
              </span>
              <strong className="text-agro-amber font-mono">{rainfall} mm</strong>
            </label>
            <input
              type="range"
              min="0"
              max="50"
              step="1"
              value={rainfall}
              onChange={(e) => setRainfall(e.target.value)}
              className="w-full accent-agro-primary cursor-pointer"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white font-extrabold text-xs transition shadow-lg shadow-agro-primary/20 flex items-center justify-center space-x-2"
          >
            <ShieldCheck className="w-4 h-4" />
            <span>{loading ? (t('weather.simulating') || 'Evaluating Model...') : (t('weather.simulate_btn') || 'Calculate Outbreak Risk')}</span>
          </button>
        </form>

        {/* Risk Output & Scientific "Explain WHY" Display */}
        <div className="agro-panel p-6 rounded-2xl flex flex-col justify-between space-y-4">
          {riskResult ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-agro-border pb-3">
                <div>
                  <span className="text-xs text-agro-muted block">{t('weather.outbreak_risk') || 'Outbreak Risk Index'}</span>
                  <span className="text-[11px] text-agro-cream font-mono font-medium">Target: {riskResult.pathogen}</span>
                </div>
                <WeatherRiskBadge level={riskResult.risk_level} />
              </div>

              <div className="text-center py-3 bg-agro-surface rounded-xl border border-agro-border">
                <span className="text-4xl font-extrabold text-agro-cream font-mono">{riskResult.risk_score}</span>
                <span className="text-xs text-agro-muted block mt-0.5">
                  {lang === 'mr' ? '१०० पैकी जोखीम गुण' : 'out of 100 Risk Score'}
                </span>
              </div>

              {/* Scientific "Explain WHY" Breakdown */}
              <div className="bg-agro-surface p-4 rounded-xl border border-agro-border space-y-2">
                <div className="flex items-center space-x-1.5 text-xs font-bold text-agro-primary border-b border-agro-border pb-2">
                  <HelpCircle className="w-4 h-4" />
                  <span>{t('weather.why_this_risk') || 'Scientific Breakdown — Explain WHY'}</span>
                </div>
                <ul className="space-y-2 text-xs text-agro-cream/90 pt-1">
                  {(riskResult.contributing_factors || []).map((f, i) => (
                    <li key={i} className="flex items-start space-x-2 leading-relaxed">
                      <span className="text-agro-primary font-bold shrink-0">•</span>
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <div className="text-xs text-agro-amber bg-agro-amber/10 p-3.5 rounded-xl border border-agro-amber/30 leading-relaxed font-medium">
                {riskResult.advice}
              </div>
            </div>
          ) : (
            <div className="text-center py-16 text-agro-muted text-xs">
              {lang === 'mr' 
                ? 'पीक निवडा, हवामान घटक समायोजित करा आणि रोग प्रादुर्भावाचा वैज्ञानिक अंदाज पाहण्यासाठी "रोग प्रादुर्भाव धोका तपासा" वर क्लिक करा.'
                : 'Select a crop, adjust parameters, and click "Calculate Outbreak Risk" to view scientific pathogen transmission forecasts.'
              }
            </div>
          )}

          <p className="text-[11px] text-agro-muted/70 italic pt-3 border-t border-agro-border">
            {lang === 'mr'
              ? 'टीप: तापमान, सापेक्ष आर्द्रता आणि पाऊस या घटकांवर आधारित पारदर्शक ७-टप्प्यांची मूल्यांकन प्रणाली.'
              : 'Note: Transparent 7-stage risk evaluation pipeline based on temperature, relative humidity, and rainfall germination thresholds.'
            }
          </p>
        </div>

      </div>

    </div>
  );
};
