import React, { useState } from 'react';
import { CloudSun, ShieldAlert, Thermometer, Droplets, CloudRain, HelpCircle, CheckCircle2 } from 'lucide-react';
import { WeatherRiskBadge } from '../components/common/Badge';
import api from '../services/api';

export const WeatherRiskPage = () => {
  const [temp, setTemp] = useState(24.5);
  const [humidity, setHumidity] = useState(82.0);
  const [rainfall, setRainfall] = useState(5.0);
  const [crop, setCrop] = useState('Tomato');
  const [riskResult, setRiskResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const availableCrops = [
    'Tomato', 'Potato', 'Rice', 'Wheat', 'Cotton',
    'Soybean', 'Maize', 'Chilli', 'Onion', 'Sugarcane'
  ];

  const handleEvaluate = async (e) => {
    if (e) e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post('/weather/risk', {
        temperature_c: parseFloat(temp),
        humidity_pct: parseFloat(humidity),
        rainfall_mm: parseFloat(rainfall),
        crop
      });
      setRiskResult(res.data);
    } catch (err) {
      console.error('Failed to compute risk:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center space-x-2">
          <span>Weather Outbreak Risk Simulator</span>
          <span className="px-2.5 py-0.5 rounded-full bg-agri-500/10 border border-agri-500/30 text-[10px] font-bold text-agri-400 uppercase tracking-wide">
            Scientific Decision Engine
          </span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Evaluate ambient weather parameters against crop-specific pathogen germination thresholds to forecast outbreak probability and explain WHY.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Input Controls */}
        <form onSubmit={handleEvaluate} className="glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center space-x-2">
            <CloudSun className="w-4 h-4 text-agri-400" />
            <span>Weather & Crop Parameters</span>
          </h3>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Target Crop</label>
            <select
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-agri-500 font-semibold"
            >
              {availableCrops.map((c) => (
                <option key={c} value={c}>{c}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1 flex justify-between">
              <span>Ambient Temperature (°C)</span>
              <strong className="text-agri-400">{temp}°C</strong>
            </label>
            <input
              type="range"
              min="5"
              max="45"
              step="0.5"
              value={temp}
              onChange={(e) => setTemp(e.target.value)}
              className="w-full accent-agri-500"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1 flex justify-between">
              <span>Relative Humidity (%)</span>
              <strong className="text-agri-400">{humidity}%</strong>
            </label>
            <input
              type="range"
              min="20"
              max="100"
              step="1"
              value={humidity}
              onChange={(e) => setHumidity(e.target.value)}
              className="w-full accent-agri-500"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1 flex justify-between">
              <span>24h Rainfall (mm)</span>
              <strong className="text-agri-400">{rainfall} mm</strong>
            </label>
            <input
              type="range"
              min="0"
              max="50"
              step="1"
              value={rainfall}
              onChange={(e) => setRainfall(e.target.value)}
              className="w-full accent-agri-500"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 font-extrabold text-xs transition shadow-lg shadow-agri-500/20"
          >
            {loading ? 'Evaluating Model...' : 'Calculate Outbreak Risk'}
          </button>
        </form>

        {/* Risk Output & Scientific "Explain WHY" Display */}
        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between space-y-4">
          {riskResult ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <span className="text-xs text-slate-400 block">Outbreak Risk Index</span>
                  <span className="text-[10px] text-slate-500 font-mono">Target: {riskResult.pathogen}</span>
                </div>
                <WeatherRiskBadge level={riskResult.risk_level} />
              </div>

              <div className="text-center py-2 bg-slate-900/60 rounded-xl border border-slate-800">
                <span className="text-4xl font-extrabold text-white">{riskResult.risk_score}</span>
                <span className="text-xs text-slate-400 block mt-0.5">out of 100 Risk Score</span>
              </div>

              {/* Scientific "Explain WHY" Breakdown */}
              <div className="bg-slate-900/80 p-4 rounded-xl border border-slate-800 space-y-2">
                <div className="flex items-center space-x-1.5 text-xs font-bold text-agri-400 border-b border-slate-800 pb-2">
                  <HelpCircle className="w-4 h-4" />
                  <span>Scientific Breakdown — Explain WHY</span>
                </div>
                <ul className="space-y-2 text-xs text-slate-300 pt-1">
                  {(riskResult.contributing_factors || []).map((f, i) => (
                    <li key={i} className="flex items-start space-x-2 leading-relaxed">
                      <span className="text-agri-400 font-bold shrink-0">•</span>
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <p className="text-xs text-amber-200 bg-amber-500/10 p-3.5 rounded-xl border border-amber-500/20 leading-relaxed font-medium">
                {riskResult.advice}
              </p>
            </div>
          ) : (
            <div className="text-center py-16 text-slate-500 text-xs">
              Select a crop, adjust parameters, and click <strong>"Calculate Outbreak Risk"</strong> to view scientific pathogen transmission forecasts.
            </div>
          )}

          <p className="text-[11px] text-slate-500 italic pt-3 border-t border-slate-800">
            Note: Transparent 7-stage risk evaluation pipeline based on temperature, relative humidity, and rainfall germination thresholds.
          </p>
        </div>

      </div>

    </div>
  );
};
