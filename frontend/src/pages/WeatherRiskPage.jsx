import React, { useState, useEffect, useCallback } from 'react';
import { 
  CloudSun, HelpCircle, MapPin, Navigation, Search, CheckCircle2, 
  ShieldCheck, Thermometer, Droplets, CloudRain, Wind, AlertTriangle, 
  Calendar, Info, RefreshCw, Compass
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { WeatherRiskBadge } from '../components/common/Badge';
import { 
  detectLocalWeather, 
  fetchCityWeather, 
  fetchWeatherForecast,
  getSavedFarmDistrict,
  setSavedFarmDistrict
} from '../services/weather';
import api from '../services/api';

const MAHARASHTRA_DISTRICTS = [
  { id: 'Kolhapur', name_en: 'Kolhapur', name_mr: 'कोल्हापूर' },
  { id: 'Pune', name_en: 'Pune', name_mr: 'पुणे' },
  { id: 'Sangli', name_en: 'Sangli', name_mr: 'सांगली' },
  { id: 'Satara', name_en: 'Satara', name_mr: 'सातारा' },
  { id: 'Solapur', name_en: 'Solapur', name_mr: 'सोलापूर' },
  { id: 'Nashik', name_en: 'Nashik', name_mr: 'नाशिक' },
  { id: 'Ahmednagar', name_en: 'Ahmednagar / Ahilyanagar', name_mr: 'अहमदनगर / अहिल्यानगर' },
  { id: 'Jalgaon', name_en: 'Jalgaon', name_mr: 'जळगाव' },
  { id: 'Chhatrapati Sambhajinagar', name_en: 'Chhatrapati Sambhajinagar', name_mr: 'छत्रपती संभाजीनगर' },
  { id: 'Nagpur', name_en: 'Nagpur', name_mr: 'नागपूर' },
  { id: 'Amravati', name_en: 'Amravati', name_mr: 'अमरावती' },
  { id: 'Nanded', name_en: 'Nanded', name_mr: 'नांदेड' },
  { id: 'Latur', name_en: 'Latur', name_mr: 'लातूर' },
  { id: 'Dhule', name_en: 'Dhule', name_mr: 'धुळे' },
  { id: 'Ratnagiri', name_en: 'Ratnagiri', name_mr: 'रत्नागिरी' },
  { id: 'Sindhudurg', name_en: 'Sindhudurg', name_mr: 'सिंधुदुर्ग' },
  { id: 'Baramati', name_en: 'Baramati (Pune Hub)', name_mr: 'बारामती (पुणे)' },
  { id: 'Kagal', name_en: 'Kagal (Kolhapur Hub)', name_mr: 'कागल (कोल्हापूर)' },
  { id: 'Karad', name_en: 'Karad (Satara Hub)', name_mr: 'कराड (सातारा)' },
  { id: 'Pandharpur', name_en: 'Pandharpur (Solapur Hub)', name_mr: 'पंढरपूर (सोलापूर)' },
  { id: 'Beed', name_en: 'Beed', name_mr: 'बीड' },
  { id: 'Parbhani', name_en: 'Parbhani', name_mr: 'परभणी' },
  { id: 'Jalna', name_en: 'Jalna', name_mr: 'जालना' },
  { id: 'Dharashiv', name_en: 'Dharashiv / Osmanabad', name_mr: 'धाराशिव / उस्मानाबाद' },
  { id: 'Buldhana', name_en: 'Buldhana', name_mr: 'बुलढाणा' },
  { id: 'Akola', name_en: 'Akola', name_mr: 'अकोला' },
  { id: 'Yavatmal', name_en: 'Yavatmal', name_mr: 'यवतमाळ' },
  { id: 'Washim', name_en: 'Washim', name_mr: 'वाशीम' },
  { id: 'Wardha', name_en: 'Wardha', name_mr: 'वर्धा' },
  { id: 'Chandrapur', name_en: 'Chandrapur', name_mr: 'चंद्रपूर' },
  { id: 'Gadchiroli', name_en: 'Gadchiroli', name_mr: 'गडचिरोली' },
  { id: 'Gondia', name_en: 'Gondia', name_mr: 'गोंदिया' },
  { id: 'Bhandara', name_en: 'Bhandara', name_mr: 'भंडारा' },
  { id: 'Thane', name_en: 'Thane', name_mr: 'ठाणे' },
  { id: 'Palghar', name_en: 'Palghar', name_mr: 'पालघर' },
  { id: 'Raigad', name_en: 'Raigad', name_mr: 'रायगड' },
];

export const WeatherRiskPage = () => {
  const { t, translateCrop, lang } = useLanguage();
  const [temp, setTemp] = useState(25.5);
  const [humidity, setHumidity] = useState(45.0);
  const [rainfall, setRainfall] = useState(0.0);
  const [windSpeed, setWindSpeed] = useState(6.0);
  const [crop, setCrop] = useState('Tomato');
  const [riskResult, setRiskResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [weatherMeta, setWeatherMeta] = useState(null);
  const [forecastList, setForecastList] = useState([]);
  const [detectingGps, setDetectingGps] = useState(false);
  const [gpsErrorMsg, setGpsErrorMsg] = useState('');
  const [cityInput, setCityInput] = useState('');
  const [selectedDistrict, setSelectedDistrict] = useState(() => getSavedFarmDistrict());

  const availableCrops = [
    'Tomato', 'Potato', 'Rice', 'Wheat', 'Cotton',
    'Soybean', 'Maize', 'Chilli', 'Onion', 'Sugarcane',
    'Grapes', 'Pomegranate', 'Banana', 'Mango'
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

  const loadWeatherForLocation = useCallback(async (locationQuery = null, lat = null, lon = null) => {
    setDetectingGps(true);
    setGpsErrorMsg('');
    try {
      let live = null;
      if (lat && lon) {
        live = await detectLocalWeather(lang, true, true);
      } else {
        const target = locationQuery || selectedDistrict || 'Kolhapur';
        live = await fetchCityWeather(target, lang);
      }

      if (live) {
        setWeatherMeta(live);
        setTemp(live.temperature_c);
        setHumidity(live.humidity_pct);
        setRainfall(live.rainfall_mm);
        setWindSpeed(live.wind_speed_kmh || 6.0);
        evaluateRisk(live.temperature_c, live.humidity_pct, live.rainfall_mm, crop);
      }

      // Load 5-day forecast
      const fcData = await fetchWeatherForecast(locationQuery || selectedDistrict, lat, lon, lang);
      if (fcData && fcData.forecast) {
        setForecastList(fcData.forecast);
      }
    } catch (err) {
      console.warn('Weather detection error:', err);
      if (err.message === 'PERMISSION_DENIED') {
        setGpsErrorMsg(
          lang === 'mr'
            ? 'मोबाईल/ब्राउझरमध्ये GPS परवानगी बंद आहे. कृपया खाली दिलेल्या ड्रॉपडाउनमधून तुमचा जिल्हा निवडा.'
            : 'GPS permission denied or unavailable on this device. Please select your farm district below.'
        );
      } else {
        setGpsErrorMsg(
          lang === 'mr'
            ? 'हवामान तपासताना अडचण आली. कृपया जिल्हा निवडा किंवा गावाचे नाव शोधा.'
            : 'Unable to reach GPS. Please select your farm district from the list below.'
        );
      }
    } finally {
      setDetectingGps(false);
    }
  }, [crop, evaluateRisk, lang, selectedDistrict]);

  useEffect(() => {
    loadWeatherForLocation(selectedDistrict);
  }, []); // Initial load on mount

  const handleDistrictChange = (e) => {
    const newDistrict = e.target.value;
    setSelectedDistrict(newDistrict);
    setSavedFarmDistrict(newDistrict);
    loadWeatherForLocation(newDistrict);
  };

  const handleCitySearch = async (e) => {
    e.preventDefault();
    if (!cityInput.trim()) return;
    const query = cityInput.trim();
    setSelectedDistrict(query);
    setSavedFarmDistrict(query);
    await loadWeatherForLocation(query);
    setCityInput('');
  };

  const handleTriggerGps = () => {
    loadWeatherForLocation(null, 1, 1);
  };

  const handleEvaluate = (e) => {
    if (e) e.preventDefault();
    evaluateRisk(temp, humidity, rainfall, crop);
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-28">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-2xl sm:text-3xl font-extrabold text-agro-cream tracking-tight font-heading">
              {t('weather.title') || 'Weather Outbreak Risk Simulator'}
            </h1>
            <span className="px-2.5 py-0.5 rounded-full bg-agro-primary/10 border border-agro-primary/30 text-[10px] font-bold text-agro-primary uppercase tracking-wide">
              {lang === 'mr' ? 'थेट कृषी हवामान' : 'Live Microclimate'}
            </span>
          </div>
          <p className="text-xs sm:text-sm text-agro-muted mt-1 max-w-2xl">
            {t('weather.subtitle') || 'Evaluate ambient weather parameters against crop-specific pathogen germination thresholds to forecast outbreak probability and explain WHY.'}
          </p>
        </div>

        {/* GPS Trigger Button */}
        <button
          type="button"
          onClick={handleTriggerGps}
          disabled={detectingGps}
          className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-bold transition shadow-md shadow-orange-glow active:scale-95 disabled:opacity-50 shrink-0 self-start sm:self-auto"
          title="Detect exact coordinates via device GPS"
        >
          <Navigation className={`w-4 h-4 ${detectingGps ? 'animate-spin' : ''}`} />
          <span>{detectingGps ? (lang === 'mr' ? 'GPS शोधत आहे...' : 'Locating GPS...') : (lang === 'mr' ? 'शेताचे थेट GPS घ्या' : 'Detect Farm GPS')}</span>
        </button>
      </div>

      {/* GPS Error Notification banner if GPS denied */}
      {gpsErrorMsg && (
        <div className="p-4 rounded-2xl bg-agro-highlight/15 border border-agro-highlight/35 text-agro-cream text-xs flex items-center gap-3">
          <AlertTriangle className="w-5 h-5 shrink-0 text-agro-highlight" />
          <div className="flex-1">
            <p className="font-bold">{lang === 'mr' ? 'GPS माहिती' : 'Farm Location Notice'}</p>
            <p className="text-[11px] mt-0.5 leading-relaxed text-agro-muted">{gpsErrorMsg}</p>
          </div>
        </div>
      )}

      {/* 1. Primary Live Farm Location & Microclimate Selector Card */}
      <div className="agro-panel p-5 sm:p-6 rounded-3xl border border-agro-border shadow-xl space-y-5 bg-agro-card">
        
        {/* Farm District Selector & Village Search Bar */}
        <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4 pb-4 border-b border-agro-border">
          
          {/* District Dropdown Selector */}
          <div className="flex items-center gap-2.5 flex-1">
            <div className="w-9 h-9 rounded-xl bg-agro-primary/10 border border-agro-primary/25 flex items-center justify-center text-agro-primary shrink-0">
              <MapPin className="w-5 h-5" />
            </div>
            <div className="flex-1">
              <label htmlFor="farm-district" className="block text-[11px] font-bold text-agro-muted mb-1">
                {lang === 'mr' ? 'तुमचा शेती जिल्हा निवडा:' : 'Select Your Farm District:'}
              </label>
              <select
                id="farm-district"
                value={selectedDistrict}
                onChange={handleDistrictChange}
                className="w-full px-3.5 py-2 rounded-xl bg-agro-surface border border-agro-border text-xs font-bold text-agro-cream focus-visible:ring-2 focus-visible:ring-agro-primary cursor-pointer shadow-sm"
              >
                {MAHARASHTRA_DISTRICTS.map((d) => (
                  <option key={d.id} value={d.id}>
                    {lang === 'mr' ? `${d.name_mr} (${d.name_en})` : `${d.name_en} (${d.name_mr})`}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Quick Village / Taluka Search */}
          <form onSubmit={handleCitySearch} className="flex items-center gap-2 flex-1">
            <div className="relative flex-1">
              <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-agro-muted" />
              <input
                type="text"
                value={cityInput}
                onChange={(e) => setCityInput(e.target.value)}
                placeholder={lang === 'mr' ? 'गाव, तालुका किंवा पिनकोड शोधा...' : 'Search any village, taluka or PIN...'}
                className="w-full pl-9 pr-3 py-2 rounded-xl bg-agro-surface border border-agro-border text-xs text-agro-cream placeholder-agro-muted focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary transition shadow-sm"
              />
            </div>
            <button
              type="submit"
              disabled={detectingGps || !cityInput.trim()}
              className="px-4 py-2 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-bold transition shadow-sm disabled:opacity-40"
            >
              {lang === 'mr' ? 'शोधा' : 'Search'}
            </button>
          </form>

        </div>

        {/* Current Weather Snapshot Banner */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="p-3.5 rounded-2xl bg-agro-surface border border-agro-border flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-agro-primary/10 text-agro-primary flex items-center justify-center shrink-0">
              <Thermometer className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-agro-muted block uppercase">
                {lang === 'mr' ? 'तापमान' : 'Temperature'}
              </span>
              <span className="text-lg font-black text-agro-cream font-mono">
                {temp}°C
              </span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-agro-surface border border-agro-border flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-agro-accent/15 text-agro-accent flex items-center justify-center shrink-0">
              <Droplets className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-agro-muted block uppercase">
                {lang === 'mr' ? 'सापेक्ष आर्द्रता' : 'Humidity'}
              </span>
              <span className="text-lg font-black text-agro-cream font-mono">
                {humidity}%
              </span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-agro-surface border border-agro-border flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-agro-highlight/15 text-agro-highlight flex items-center justify-center shrink-0">
              <CloudRain className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-agro-muted block uppercase">
                {lang === 'mr' ? 'पाऊस' : '24h Rainfall'}
              </span>
              <span className="text-lg font-black text-agro-cream font-mono">
                {rainfall} mm
              </span>
            </div>
          </div>

          <div className="p-3.5 rounded-2xl bg-agro-surface border border-agro-border flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-agro-surface text-agro-muted border border-agro-border flex items-center justify-center shrink-0">
              <Wind className="w-5 h-5" />
            </div>
            <div>
              <span className="text-[10px] font-bold text-agro-muted block uppercase">
                {lang === 'mr' ? 'वाऱ्याचा वेग' : 'Wind Speed'}
              </span>
              <span className="text-lg font-black text-agro-cream font-mono">
                {windSpeed} km/h
              </span>
            </div>
          </div>
        </div>

        {/* Active Location & Spray Advisory Ribbon */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-2xl bg-agro-surface border border-agro-border">
          <div className="flex items-center gap-2.5">
            <span className="w-2.5 h-2.5 rounded-full bg-agro-primary animate-ping" />
            <span className="text-xs font-bold text-agro-cream">
              {lang === 'mr' ? 'सक्रिय शेती हवामान:' : 'Active Farm Weather:'} <strong className="text-agro-primary">{weatherMeta?.location || selectedDistrict}</strong> ({weatherMeta?.condition || 'Clear sky'})
            </span>
          </div>

          {/* Spraying Advisory Tag */}
          {weatherMeta?.spraying_advisory && (
            <div className="flex items-center gap-2">
              <span className={`px-3 py-1 rounded-full text-xs font-extrabold flex items-center gap-1.5 shadow-sm ${
                weatherMeta.spraying_advisory.status === 'SAFE'
                  ? 'bg-agro-accent text-white'
                  : weatherMeta.spraying_advisory.status === 'CAUTION'
                  ? 'bg-agro-highlight text-[#39332F]'
                  : 'bg-agro-primary text-white'
              }`}>
                <ShieldCheck className="w-3.5 h-3.5" />
                <span>{weatherMeta.spraying_advisory.headline}</span>
              </span>
            </div>
          )}
        </div>

        {/* Spraying Advisory Detail Explanation */}
        {weatherMeta?.spraying_advisory && (
          <p className="text-xs text-agro-cream/90 px-1 leading-relaxed">
            🌾 <strong>{lang === 'mr' ? 'फवारणी सल्ला:' : 'Spraying Advisory:'}</strong> {weatherMeta.spraying_advisory.reason}
          </p>
        )}

        {/* 1-Tap Popular Maharashtra Agricultural Districts */}
        <div className="flex items-center gap-1.5 flex-wrap pt-2 border-t border-agro-border text-[11px] text-agro-muted">
          <span className="font-bold text-agro-cream">
            {lang === 'mr' ? 'जलद जिल्हे:' : 'Quick Districts:'}
          </span>
          {['Kolhapur', 'Pune', 'Sangli', 'Satara', 'Solapur', 'Nashik', 'Ahmednagar', 'Jalgaon', 'Nagpur', 'Amravati'].map((cName) => (
            <button
              key={cName}
              type="button"
              onClick={() => {
                setSelectedDistrict(cName);
                setSavedFarmDistrict(cName);
                loadWeatherForLocation(cName);
              }}
              className={`px-2.5 py-1 rounded-lg border transition-all text-[11px] font-semibold cursor-pointer ${
                selectedDistrict.toLowerCase() === cName.toLowerCase()
                  ? 'bg-agro-primary text-white border-agro-primary shadow-sm'
                  : 'bg-agro-surface hover:bg-agro-hover border-agro-border text-agro-cream'
              }`}
            >
              {cName}
            </button>
          ))}
        </div>

      </div>

      {/* 2. 5-Day Agricultural Weather & Foliar Spray Forecast */}
      {forecastList.length > 0 && (
        <section className="agro-panel p-5 sm:p-6 rounded-3xl border border-agro-border shadow-sm space-y-4 bg-agro-card">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-bold text-agro-cream flex items-center gap-2 font-heading">
              <Calendar className="w-4 h-4 text-agro-primary" />
              <span>{lang === 'mr' ? '५ दिवसांचा शेती हवामान व फवारणी अंदाज' : '5-Day Agricultural Weather & Spray Forecast'}</span>
            </h3>
            <span className="text-[11px] text-agro-muted font-medium">
              {weatherMeta?.location || selectedDistrict}
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-5 gap-3">
            {forecastList.map((dayItem, idx) => (
              <div 
                key={idx}
                className="p-3.5 rounded-2xl bg-agro-surface border border-agro-border space-y-2 text-center"
              >
                <div className="border-b border-agro-border pb-1.5">
                  <span className="block text-xs font-black text-agro-cream">
                    {dayItem.day_name}
                  </span>
                  <span className="text-[10px] text-agro-muted font-semibold">
                    {dayItem.date_display}
                  </span>
                </div>

                <div className="py-1">
                  <span className="block text-base font-extrabold text-agro-cream font-mono">
                    {dayItem.temp_max}° / <span className="text-agro-muted text-xs font-normal">{dayItem.temp_min}°C</span>
                  </span>
                  <span className="text-[11px] text-agro-muted font-medium block truncate mt-0.5">
                    {dayItem.condition}
                  </span>
                </div>

                <div className="text-[10px] text-agro-muted space-y-0.5 font-medium border-t border-agro-border pt-1.5">
                  <div className="flex justify-between">
                    <span>{lang === 'mr' ? 'आर्द्रता:' : 'Humidity:'}</span>
                    <strong className="text-agro-cream">{dayItem.humidity_pct}%</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>{lang === 'mr' ? 'पाऊस:' : 'Rain %:'}</span>
                    <strong className="text-agro-cream">{dayItem.rain_probability_pct}%</strong>
                  </div>
                </div>

                {/* Day Spray Badge */}
                {dayItem.spraying_advisory && (
                  <div className={`mt-2 py-1 px-2 rounded-lg text-[10px] font-extrabold truncate ${
                    dayItem.spraying_advisory.status === 'SAFE'
                      ? 'bg-agro-accent/15 text-agro-accent border border-agro-accent/30'
                      : dayItem.spraying_advisory.status === 'CAUTION'
                      ? 'bg-agro-highlight/15 text-agro-highlight border border-agro-highlight/30'
                      : 'bg-agro-primary/15 text-agro-primary border border-agro-primary/30'
                  }`}>
                    {dayItem.spraying_advisory.headline.split('—')[0]}
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* 3. Crop Pathogen Outbreak Risk Simulator */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Input Controls */}
        <form onSubmit={handleEvaluate} className="agro-panel p-6 rounded-3xl border border-agro-border shadow-xl space-y-5 bg-agro-card">
          <div className="flex items-center justify-between border-b border-agro-border pb-3">
            <h3 className="text-sm font-bold text-agro-cream flex items-center space-x-2 font-heading">
              <CloudSun className="w-4 h-4 text-agro-primary" />
              <span>{t('weather.card_params') || 'Weather & Crop Parameters'}</span>
            </h3>
            <span className="text-[11px] text-agro-primary font-bold">
              {lang === 'mr' ? 'थेट हवामानाशी समक्रमित' : 'Synced with Live Weather'}
            </span>
          </div>

          <div>
            <label className="block text-xs font-bold text-agro-cream mb-1.5">
              {t('weather.target_crop') || 'Target Crop'}
            </label>
            <select
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl bg-agro-surface border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary font-bold transition cursor-pointer shadow-sm"
            >
              {availableCrops.map((c) => (
                <option key={c} value={c}>{translateCrop(c)}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="text-xs font-bold text-agro-cream mb-1.5 flex justify-between">
              <span className="flex items-center space-x-1.5">
                <Thermometer className="w-3.5 h-3.5 text-agro-primary" />
                <span>{t('weather.temp') || 'Ambient Temperature (°C)'}</span>
              </span>
              <strong className="text-agro-primary font-mono text-sm">{temp}°C</strong>
            </label>
            <input
              type="range"
              min="5"
              max="45"
              step="0.5"
              value={temp}
              onChange={(e) => setTemp(e.target.value)}
              className="w-full accent-brand-orange-light dark:accent-brand-orange-dark cursor-pointer"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-agro-cream mb-1.5 flex justify-between">
              <span className="flex items-center space-x-1.5">
                <Droplets className="w-3.5 h-3.5 text-agro-accent" />
                <span>{t('weather.humidity') || 'Relative Humidity (%)'}</span>
              </span>
              <strong className="text-agro-accent font-mono text-sm">{humidity}%</strong>
            </label>
            <input
              type="range"
              min="15"
              max="100"
              step="1"
              value={humidity}
              onChange={(e) => setHumidity(e.target.value)}
              className="w-full accent-brand-orange-light dark:accent-brand-orange-dark cursor-pointer"
            />
          </div>

          <div>
            <label className="text-xs font-bold text-agro-cream mb-1.5 flex justify-between">
              <span className="flex items-center space-x-1.5">
                <CloudRain className="w-3.5 h-3.5 text-agro-highlight" />
                <span>{t('weather.rainfall') || '24h Rainfall (mm)'}</span>
              </span>
              <strong className="text-agro-highlight font-mono text-sm">{rainfall} mm</strong>
            </label>
            <input
              type="range"
              min="0"
              max="50"
              step="0.5"
              value={rainfall}
              onChange={(e) => setRainfall(e.target.value)}
              className="w-full accent-brand-orange-light dark:accent-brand-orange-dark cursor-pointer"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white font-extrabold text-xs transition shadow-lg shadow-orange-glow flex items-center justify-center space-x-2 active:scale-95"
          >
            <ShieldCheck className="w-4 h-4" />
            <span>{loading ? (t('weather.simulating') || 'Evaluating Model...') : (t('weather.simulate_btn') || 'Calculate Outbreak Risk')}</span>
          </button>
        </form>

        {/* Risk Output & Scientific "Explain WHY" Display */}
        <div className="agro-panel p-6 rounded-3xl border border-agro-border shadow-xl flex flex-col justify-between space-y-4 bg-agro-card">
          {riskResult ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-agro-border pb-3">
                <div>
                  <span className="text-xs font-bold text-agro-muted block">{t('weather.outbreak_risk') || 'Outbreak Risk Index'}</span>
                  <span className="text-xs text-agro-cream font-bold">Target Pathogen: <strong className="text-agro-primary">{riskResult.pathogen}</strong></span>
                </div>
                <WeatherRiskBadge level={riskResult.risk_level} />
              </div>

              <div className="text-center py-4 bg-agro-surface rounded-2xl border border-agro-border">
                <span className="text-5xl font-black text-agro-cream font-mono">{riskResult.risk_score}</span>
                <span className="text-xs text-agro-muted block mt-1 font-semibold">
                  {lang === 'mr' ? '१०० पैकी जोखीम गुण (Risk Score)' : 'out of 100 Pathogen Infection Potential'}
                </span>
              </div>

              {/* Scientific "Explain WHY" Breakdown */}
              <div className="bg-agro-surface p-4 rounded-2xl border border-agro-border space-y-2">
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

              <div className="text-xs text-agro-cream bg-agro-highlight/15 p-4 rounded-2xl border border-agro-highlight/35 leading-relaxed font-semibold">
                🌾 {riskResult.advice}
              </div>
            </div>
          ) : (
            <div className="text-center py-16 text-agro-muted text-xs">
              {lang === 'mr' 
                ? 'पीक निवडा, हवामान घटक तपासा आणि रोग प्रादुर्भावाचा वैज्ञानिक अंदाज पाहण्यासाठी "रोग प्रादुर्भाव धोका तपासा" वर क्लिक करा.'
                : 'Select a crop, adjust parameters, and click "Calculate Outbreak Risk" to view scientific pathogen transmission forecasts.'
              }
            </div>
          )}

          <p className="text-[11px] text-agro-muted italic pt-3 border-t border-agro-border">
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
