import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Filter, Search, ArrowRight, Trash2, RotateCcw, Leaf, AlertTriangle } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { SeverityBadge, WeatherRiskBadge } from '../components/common/Badge';
import api from '../services/api';

const STORAGE_KEY = 'agroscan_scans_v1';

export const HistoryPage = () => {
  const { t, translateCrop, translateDisease, formatDate } = useLanguage();
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [cropFilter, setCropFilter] = useState('All');
  const [showClearModal, setShowClearModal] = useState(false);

  const fetchHistory = useCallback(async () => {
    try {
      // 1. Read local storage
      let localScans = [];
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) localScans = JSON.parse(raw);
        if (!Array.isArray(localScans)) localScans = [];
      } catch (e) {
        console.warn('LocalStorage error in history:', e);
      }

      // 2. Fetch backend
      let backendScans = [];
      try {
        const res = await api.get('/predictions/history?limit=100');
        backendScans = Array.isArray(res.data) ? res.data : [];
      } catch (err) {
        console.warn('Backend history fetch notice:', err);
      }

      // 3. Merge
      const map = new Map();
      localScans.forEach(item => { if (item && item.id) map.set(item.id, item); });
      backendScans.forEach(item => { if (item && item.id && !map.has(item.id)) map.set(item.id, item); });

      const merged = Array.from(map.values()).sort((a, b) => {
        const dateA = new Date(a.created_at || a.timestamp || 0).getTime();
        const dateB = new Date(b.created_at || b.timestamp || 0).getTime();
        return dateB - dateA;
      });

      setHistory(merged);
    } catch (err) {
      console.error('Failed to load history:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchHistory();
    const handleScanEvent = () => fetchHistory();
    window.addEventListener('agroscan_scan_completed', handleScanEvent);
    return () => window.removeEventListener('agroscan_scan_completed', handleScanEvent);
  }, [fetchHistory]);

  const handleDeleteItem = (id) => {
    try {
      const updated = history.filter(item => item.id !== id);
      setHistory(updated);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      window.dispatchEvent(new Event('agroscan_scan_completed'));
    } catch (e) {
      console.error('Failed to delete item:', e);
    }
  };

  const handleClearAll = () => {
    try {
      localStorage.removeItem(STORAGE_KEY);
      setHistory([]);
      setShowClearModal(false);
      window.dispatchEvent(new Event('agroscan_scan_completed'));
    } catch (e) {
      console.error('Failed to clear history:', e);
    }
  };

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
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">
            {t('history.title') || 'Scan History & Diagnostic Logs'}
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            {t('history.subtitle') || 'Historical log of past leaf disease predictions, severity percentages, and weather risk levels.'}
          </p>
        </div>

        {safeHistory.length > 0 && (
          <button
            onClick={() => setShowClearModal(true)}
            className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-slate-800/80 hover:bg-red-500/20 text-slate-300 hover:text-red-400 border border-slate-700/60 hover:border-red-500/30 text-xs font-semibold transition shrink-0"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>{t('dashboard.reset_data')}</span>
          </button>
        )}
      </div>

      {/* Filter & Search Bar */}
      <div className="glass-panel p-4 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-4 border border-slate-800/80">
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
            <option value="Cotton">{translateCrop('Cotton')}</option>
            <option value="Rice">{translateCrop('Rice')}</option>
            <option value="Wheat">{translateCrop('Wheat')}</option>
            <option value="Chilli">{translateCrop('Chilli')}</option>
            <option value="Onion">{translateCrop('Onion')}</option>
            <option value="General Crop">{translateCrop('General Crop')}</option>
          </select>
        </div>
      </div>

      {/* History Table */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800/80">
        {loading ? (
          <div className="py-12 text-center text-xs text-slate-400 animate-pulse">
            {t('history.loading') || 'Loading scan history...'}
          </div>
        ) : filteredHistory.length === 0 ? (
          <div className="py-14 text-center space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-slate-900 border border-slate-800 text-slate-500 flex items-center justify-center mx-auto">
              <Leaf className="w-6 h-6" />
            </div>
            <p className="text-slate-400 text-xs font-semibold">
              {t('history.empty') || 'No scan history matching filters found.'}
            </p>
            <Link
              to="/scan"
              className="inline-flex items-center space-x-2 mt-2 px-4 py-2 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-semibold transition"
            >
              <Leaf className="w-3.5 h-3.5" />
              <span>{t('dashboard.blank_cta')}</span>
            </Link>
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
                  <th className="py-3 px-3 text-right">{t('history.col_report') || 'Action'}</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filteredHistory.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-800/30 transition group">
                    <td className="py-3.5 px-3 text-slate-400 font-mono text-[11px]">
                      {formatDate(item.created_at || item.timestamp || new Date())}
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
                      <WeatherRiskBadge level={item.weather_risk_level || item.risk || 'Low'} />
                    </td>
                    <td className="py-3.5 px-3 font-mono text-agri-400">
                      {(((Number(item.confidence_score ?? item.confidence)) || 0.9) * 100).toFixed(1)}%
                    </td>
                    <td className="py-3.5 px-3 text-right">
                      <div className="inline-flex items-center space-x-2">
                        <Link
                          to={`/results/${item.id}`}
                          className="text-xs font-semibold text-agri-400 hover:underline inline-flex items-center space-x-1"
                        >
                          <span>{t('history.view_report') || 'View'}</span>
                          <ArrowRight className="w-3 h-3" />
                        </Link>
                        <button
                          onClick={() => handleDeleteItem(item.id)}
                          className="p-1 rounded text-slate-500 hover:text-red-400 hover:bg-red-500/10 transition opacity-0 group-hover:opacity-100"
                          title="Delete scan"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Clear Modal */}
      {showClearModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
          <div className="glass-panel max-w-md w-full p-6 rounded-3xl border border-red-500/30 space-y-4 shadow-2xl">
            <div className="flex items-center space-x-3 text-red-400">
              <div className="p-2 rounded-xl bg-red-500/10 border border-red-500/20">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-white">{t('dashboard.reset_data')}</h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {t('dashboard.reset_confirm')}
            </p>
            <div className="flex items-center justify-end space-x-3 pt-2">
              <button
                onClick={() => setShowClearModal(false)}
                className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300 transition"
              >
                Cancel
              </button>
              <button
                onClick={handleClearAll}
                className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-500 text-xs font-bold text-white transition shadow-lg shadow-red-600/20"
              >
                Confirm Clear
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
