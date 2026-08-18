import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Filter, Search, ArrowRight } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { SeverityBadge, WeatherRiskBadge } from '../components/common/Badge';
import api from '../services/api';

export const HistoryPage = () => {
  const { t, translateCrop, translateDisease, formatDate } = useLanguage();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [cropFilter, setCropFilter] = useState('All');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get('/predictions/history?limit=100');
        setHistory(res.data);
      } catch (err) {
        console.error('Failed to load history:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  const safeHistory = Array.isArray(history) ? history : [];
  const filteredHistory = safeHistory.filter((item) => {
    const diseaseName = item.disease_name || item.disease || '';
    const cropName = item.crop_detected || item.plant || '';
    const matchesSearch = diseaseName.toLowerCase().includes(search.toLowerCase()) ||
                          cropName.toLowerCase().includes(search.toLowerCase());
    const matchesCrop = cropFilter === 'All' || cropName === cropFilter;
    return matchesSearch && matchesCrop;
  });

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
          {t('history.title') || 'Scan History & Diagnostic Logs'}
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          {t('history.subtitle') || 'Historical log of past leaf disease predictions, severity percentages, and weather risk levels.'}
        </p>
      </div>

      {/* Filter & Search Bar */}
      <div className="glass-panel p-4 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-72">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t('history.search_placeholder') || 'Search crop or disease...'}
            className="w-full pl-9 pr-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-agri-500"
          />
        </div>

        <div className="flex items-center space-x-2 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={cropFilter}
            onChange={(e) => setCropFilter(e.target.value)}
            className="px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-200 focus:outline-none focus:border-agri-500 font-semibold"
          >
            <option value="All">{t('history.filter_all') || 'All Crops'}</option>
            <option value="Tomato">{translateCrop('Tomato')}</option>
            <option value="Potato">{translateCrop('Potato')}</option>
            <option value="Corn (Maize)">{translateCrop('Corn (Maize)')}</option>
            <option value="Mango">{translateCrop('Mango')}</option>
            <option value="Sugarcane">{translateCrop('Sugarcane')}</option>
            <option value="General Crop">{translateCrop('General Crop')}</option>
          </select>
        </div>
      </div>

      {/* History Table */}
      <div className="glass-panel p-6 rounded-2xl">
        {loading ? (
          <div className="py-12 text-center text-xs text-slate-400 animate-pulse">
            {t('history.loading') || 'Loading scan history...'}
          </div>
        ) : filteredHistory.length === 0 ? (
          <div className="py-12 text-center text-xs text-slate-500">
            {t('history.empty') || 'No scan history matching filters found.'}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 font-semibold">
                  <th className="py-3 px-3">{t('history.col_date') || 'Date'}</th>
                  <th className="py-3 px-3">{t('history.col_crop') || 'Crop'}</th>
                  <th className="py-3 px-3">{t('history.col_disease') || 'Disease Identified'}</th>
                  <th className="py-3 px-3">{t('history.col_severity') || 'Severity'}</th>
                  <th className="py-3 px-3">{t('history.col_risk') || 'Weather Risk'}</th>
                  <th className="py-3 px-3">{t('history.col_confidence') || 'Confidence'}</th>
                  <th className="py-3 px-3 text-right">{t('history.col_report') || 'Report'}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filteredHistory.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3.5 px-3 text-slate-400 font-mono text-[11px]">
                      {formatDate(item.created_at)}
                    </td>
                    <td className="py-3.5 px-3 font-semibold text-white">
                      {translateCrop(item.crop_detected || item.plant)}
                    </td>
                    <td className="py-3.5 px-3 text-slate-300">
                      {translateDisease(item.disease_name || item.disease)}
                    </td>
                    <td className="py-3.5 px-3">
                      <SeverityBadge level={item.severity_level || item.severity} />
                    </td>
                    <td className="py-3.5 px-3">
                      <WeatherRiskBadge level={item.weather_risk_level || item.risk} />
                    </td>
                    <td className="py-3.5 px-3 font-mono text-agri-400">
                      {((item.confidence_score || item.confidence || 0.9) * 100).toFixed(1)}%
                    </td>
                    <td className="py-3.5 px-3 text-right">
                      <Link
                        to={`/results/${item.id}`}
                        className="text-xs font-semibold text-agri-400 hover:underline inline-flex items-center space-x-1"
                      >
                        <span>{t('history.view_report') || 'View'}</span>
                        <ArrowRight className="w-3 h-3" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
};
