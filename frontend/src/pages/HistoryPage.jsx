import React, { useState, useEffect, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { Filter, Search, ArrowRight, Trash2, RotateCcw, Sprout, AlertTriangle, ScanLine } from 'lucide-react';
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
    const handleClearEvent = () => {
      setHistory([]);
      try {
        localStorage.setItem(STORAGE_KEY, '[]');
      } catch {
        // storage fallback
      }
    };
    window.addEventListener('agroscan_scan_completed', handleScanEvent);
    window.addEventListener('agroscan_history_cleared', handleClearEvent);
    return () => {
      window.removeEventListener('agroscan_scan_completed', handleScanEvent);
      window.removeEventListener('agroscan_history_cleared', handleClearEvent);
    };
  }, [fetchHistory]);

  const handleDeleteItem = async (id) => {
    try {
      const updated = history.filter(item => item.id !== id);
      setHistory(updated);
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      } catch {
        // storage fallback
      }
      await api.delete('/predictions/' + id).catch(() => {});
    } catch (e) {
      console.error('Failed to delete item:', e);
    }
  };

  const handleClearAll = async () => {
    try {
      setLoading(true);
      setShowClearModal(false);
      setHistory([]);
      try {
        localStorage.removeItem(STORAGE_KEY);
        localStorage.setItem(STORAGE_KEY, '[]');
      } catch {
        // storage fallback
      }

      try {
        await api.delete('/predictions/history?scope=all');
      } catch (apiErr) {
        console.warn('Backend clear history notification:', apiErr);
      }

      setHistory([]);
      window.dispatchEvent(new Event('agroscan_history_cleared'));
    } catch (e) {
      console.error('Failed to clear history:', e);
    } finally {
      setLoading(false);
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
          <h1 className="text-2xl sm:text-3xl font-extrabold text-agro-cream tracking-tight font-heading">
            {t('history.title') || 'Scan History & Diagnostic Logs'}
          </h1>
          <p className="text-xs sm:text-sm text-agro-muted mt-1">
            {t('history.subtitle') || 'Historical log of past leaf disease predictions, severity percentages, and weather risk levels.'}
          </p>
        </div>

        <div className="flex items-center space-x-3 shrink-0">
          <Link
            to="/scan"
            className="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-bold transition shadow-md shadow-orange-glow active:scale-95"
          >
            <ScanLine className="w-4 h-4" />
            <span>{t('nav.scan') || 'Start New Scan'}</span>
          </Link>

          {safeHistory.length > 0 && (
            <button
              onClick={() => setShowClearModal(true)}
              className="inline-flex items-center space-x-1.5 px-3.5 py-2.5 rounded-xl bg-agro-surface hover:bg-agro-primary/10 text-agro-muted hover:text-agro-primary border border-agro-border hover:border-agro-primary/40 text-xs font-semibold transition"
              title="Clear all saved scan history"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>{t('dashboard.reset_data') || 'Reset Scans'}</span>
            </button>
          )}
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="agro-panel bg-agro-card p-4 rounded-2xl border border-agro-border flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-agro-muted" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder={t('history.search_placeholder') || 'Search crop or disease...'}
            className="w-full pl-10 pr-3.5 py-2.5 rounded-xl bg-agro-surface border border-agro-border text-xs text-agro-cream placeholder-agro-muted focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary transition"
          />
        </div>

        <div className="flex items-center space-x-2.5 w-full sm:w-auto">
          <Filter className="w-4 h-4 text-agro-muted shrink-0" />
          <select
            value={cropFilter}
            onChange={(e) => setCropFilter(e.target.value)}
            className="w-full sm:w-auto px-3.5 py-2.5 rounded-xl bg-agro-surface border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary focus:ring-1 focus:ring-agro-primary font-semibold transition cursor-pointer"
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

      {/* History Container */}
      <div className="agro-panel bg-agro-card p-4 sm:p-6 rounded-2xl border border-agro-border overflow-hidden">
        {loading ? (
          <div className="py-14 text-center text-xs text-agro-muted animate-pulse">
            {t('history.loading') || 'Loading scan history...'}
          </div>
        ) : filteredHistory.length === 0 ? (
          <div className="py-14 text-center space-y-4">
            <div className="w-14 h-14 rounded-2xl bg-agro-surface border border-agro-border text-agro-muted flex items-center justify-center mx-auto">
              <Sprout className="w-7 h-7 text-agro-primary" />
            </div>
            <div className="space-y-1">
              <p className="text-agro-cream text-sm font-bold">
                {t('history.empty') || 'No scan history matching filters found.'}
              </p>
              <p className="text-agro-muted text-xs">
                {t('history.empty_sub') || 'Scan plant leaves using your camera or upload an image to start logging diagnostics.'}
              </p>
            </div>
            <Link
              to="/scan"
              className="inline-flex items-center space-x-2 mt-2 px-4 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-bold transition shadow-md shadow-orange-glow active:scale-95"
            >
              <ScanLine className="w-4 h-4" />
              <span>{t('dashboard.blank_cta') || 'Scan Your First Plant Leaf'}</span>
            </Link>
          </div>
        ) : (
          <>
            {/* Mobile Cards (Visible only on < md) */}
            <div className="block md:hidden space-y-3">
              {filteredHistory.map((item) => (
                <div
                  key={item.id}
                  className="p-4 rounded-xl bg-agro-surface border border-agro-border space-y-2.5 transition-all shadow-sm"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-agro-cream text-sm">
                      {translateCrop(item.crop_detected || item.plant)}
                    </span>
                    <span className="text-[11px] text-agro-muted font-mono">
                      {formatDate(item.created_at || item.timestamp || new Date())}
                    </span>
                  </div>

                  <div className="text-xs text-agro-cream/90 font-medium">
                    {translateDisease(item.disease_name || item.disease)}
                  </div>

                  <div className="flex flex-wrap items-center gap-2 pt-1">
                    <SeverityBadge level={item.severity_level || item.severity} />
                    <WeatherRiskBadge level={item.weather_risk_level || item.risk || 'Low'} />
                    <span className="font-mono text-xs font-bold text-agro-primary ml-auto">
                      {(((Number(item.confidence_score ?? item.confidence)) || 0.9) * 100).toFixed(1)}%
                    </span>
                  </div>

                  <div className="flex items-center justify-between pt-2 border-t border-agro-border">
                    <button
                      onClick={() => handleDeleteItem(item.id)}
                      className="p-1.5 rounded-lg text-agro-muted hover:text-agro-primary hover:bg-agro-primary/10 transition"
                      title="Delete scan"
                      aria-label="Delete scan record"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                    <Link
                      to={`/results/${item.id}`}
                      className="text-xs font-bold text-white bg-agro-primary hover:bg-agro-primaryHover px-3 py-1.5 rounded-lg inline-flex items-center space-x-1 transition shadow-sm"
                    >
                      <span>{t('history.view_report') || 'View Full Report'}</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>

            {/* Desktop Table (Visible on >= md) */}
            <div className="hidden md:block overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-agro-border text-agro-muted font-semibold tracking-wide uppercase text-[11px]">
                    <th className="py-3 px-3">{t('history.col_date') || 'Date'}</th>
                    <th className="py-3 px-3">{t('history.col_crop') || 'Crop'}</th>
                    <th className="py-3 px-3">{t('history.col_disease') || 'Disease Identified'}</th>
                    <th className="py-3 px-3">{t('history.col_severity') || 'Severity'}</th>
                    <th className="py-3 px-3">{t('history.col_risk') || 'Weather Risk'}</th>
                    <th className="py-3 px-3">{t('history.col_confidence') || 'Confidence'}</th>
                    <th className="py-3 px-3 text-right">{t('history.col_report') || 'Action'}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-agro-border">
                  {filteredHistory.map((item) => (
                    <tr key={item.id} className="hover:bg-agro-surface/60 transition group">
                      <td className="py-3.5 px-3 text-agro-muted font-mono text-[11px]">
                        {formatDate(item.created_at || item.timestamp || new Date())}
                      </td>
                      <td className="py-3.5 px-3 font-semibold text-agro-cream">
                        {translateCrop(item.crop_detected || item.plant)}
                      </td>
                      <td className="py-3.5 px-3 text-agro-cream/90">
                        {translateDisease(item.disease_name || item.disease)}
                      </td>
                      <td className="py-3.5 px-3">
                        <SeverityBadge level={item.severity_level || item.severity} />
                      </td>
                      <td className="py-3.5 px-3">
                        <WeatherRiskBadge level={item.weather_risk_level || item.risk || 'Low'} />
                      </td>
                      <td className="py-3.5 px-3 font-mono font-bold text-agro-primary">
                        {(((Number(item.confidence_score ?? item.confidence)) || 0.9) * 100).toFixed(1)}%
                      </td>
                      <td className="py-3.5 px-3 text-right">
                        <div className="inline-flex items-center space-x-2">
                          <Link
                            to={`/results/${item.id}`}
                            className="text-xs font-bold text-agro-primary hover:text-agro-primaryHover inline-flex items-center space-x-1 transition"
                          >
                            <span>{t('history.view_report') || 'View Full Report'}</span>
                            <ArrowRight className="w-3.5 h-3.5" />
                          </Link>
                          <button
                            onClick={() => handleDeleteItem(item.id)}
                            className="p-1.5 rounded-lg text-agro-muted hover:text-agro-primary hover:bg-agro-primary/10 transition opacity-80 group-hover:opacity-100"
                            title="Delete scan"
                            aria-label="Delete scan record"
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
          </>
        )}
      </div>

      {/* Clear Modal */}
      {showClearModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-agro-bg/80 backdrop-blur-sm">
          <div className="agro-panel bg-agro-card max-w-md w-full p-6 rounded-3xl border border-agro-primary/40 space-y-4 shadow-2xl">
            <div className="flex items-center space-x-3 text-agro-primary">
              <div className="p-2.5 rounded-xl bg-agro-primary/15 border border-agro-primary/30">
                <AlertTriangle className="w-5 h-5 text-agro-primary" />
              </div>
              <h3 className="text-base font-bold text-agro-cream font-heading">{t('dashboard.reset_data') || 'Reset Scans'}</h3>
            </div>
            <p className="text-xs text-agro-muted leading-relaxed">
              {t('dashboard.reset_confirm') || 'Are you sure you want to clear your scan history? All past diagnoses and health logs will be permanently deleted.'}
            </p>
            <div className="flex items-center justify-end space-x-3 pt-2">
              <button
                onClick={() => setShowClearModal(false)}
                className="px-4 py-2 rounded-xl bg-agro-surface hover:bg-agro-hover border border-agro-border text-xs font-semibold text-agro-cream transition"
              >
                {t('common.cancel') || 'Cancel'}
              </button>
              <button
                onClick={handleClearAll}
                className="px-4 py-2 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-xs font-bold text-white transition shadow-lg shadow-orange-glow"
              >
                {t('common.confirm') || 'Confirm Clear'}
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};
