import React, { useState } from 'react';
import { CloudSun, ShieldAlert, Thermometer, Droplets, CloudRain, CheckCircle2 } from 'lucide-react';
import { WeatherRiskBadge } from '../components/common/Badge';
import api from '../services/api';

export const WeatherRiskPage = () => {
  const [temp, setTemp] = useState(26.5);
  const [humidity, setHumidity] = useState(82.0);
  const [rainfall, setRainfall] = useState(5.0);
  const [crop, setCrop] = useState('Tomato');
  const [disease, setDisease] = useState('Late Blight');
  const [riskResult, setRiskResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleEvaluate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post('/weather/risk', {
        temperature_c: parseFloat(temp),
        humidity_pct: parseFloat(humidity),
        rainfall_mm: parseFloat(rainfall),
        crop,
        disease
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
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">Weather Disease Risk Simulator</h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Evaluate weather parameters (temperature, relative humidity, rainfall) against crop pathogen germination thresholds.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Input Controls */}
        <form onSubmit={handleEvaluate} className="glass-panel p-6 rounded-2xl space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center space-x-2">
            <CloudSun className="w-4 h-4 text-agri-400" />
            <span>Weather & Crop Inputs</span>
          </h3>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Target Crop</label>
            <select
              value={crop}
              onChange={(e) => setCrop(e.target.value)}
              className="w-full px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-agri-500"
            >
              <option value="Tomato">Tomato</option>
              <option value="Potato">Potato</option>
              <option value="Corn (Maize)">Corn (Maize)</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1">Temperature (°C): {temp}°C</label>
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
            <label className="block text-xs font-medium text-slate-300 mb-1">Relative Humidity (%): {humidity}%</label>
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
            <label className="block text-xs font-medium text-slate-300 mb-1">24h Rainfall (mm): {rainfall} mm</label>
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
            className="w-full py-3 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 font-bold text-xs transition shadow-lg shadow-agri-500/20"
          >
            {loading ? 'Evaluating Model...' : 'Simulate Weather Outbreak Risk'}
          </button>
        </form>

        {/* Risk Output Display */}
        <div className="glass-panel p-6 rounded-2xl flex flex-col justify-between">
          {riskResult ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs text-slate-400">Risk Score</span>
                <WeatherRiskBadge level={riskResult.risk_level} />
              </div>

              <div className="text-center py-4">
                <span className="text-4xl font-extrabold text-white">{riskResult.risk_score}</span>
                <span className="text-xs text-slate-400 block mt-1">out of 100 Risk Index</span>
              </div>

              <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 space-y-2">
                <span className="text-xs font-bold text-slate-300 block">Contributing Factors:</span>
                <ul className="space-y-1.5 text-xs text-slate-400">
                  {riskResult.contributing_factors.map((f, i) => (
                    <li key={i} className="flex items-start space-x-2">
                      <span className="text-agri-400 font-bold">•</span>
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>
              </div>

              <p className="text-xs text-amber-300 bg-amber-500/10 p-3 rounded-xl border border-amber-500/20">
                {riskResult.advice}
              </p>
            </div>
          ) : (
            <div className="text-center py-16 text-slate-500 text-xs">
              Adjust parameters and click "Simulate Weather Outbreak Risk" to view rule-based disease forecast models.
            </div>
          )}

          <p className="text-[11px] text-slate-500 italic mt-4 pt-3 border-t border-slate-800">
            Note: Baseline transparent rule-based engine. Replaceable by trained ML weather outbreak models.
          </p>
        </div>

      </div>

    </div>
  );
};
