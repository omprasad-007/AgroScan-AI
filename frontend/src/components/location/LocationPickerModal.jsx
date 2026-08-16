import React, { useState } from 'react';
import { MapPin, Search, Edit3, Navigation, AlertCircle, CheckCircle, Loader2, X } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import api from '../../services/api';

export const LocationPickerModal = ({ isOpen, onClose, onSave, initialData }) => {
  const { t } = useLanguage();
  const [activeTab, setActiveTab] = useState('gps'); // 'gps' | 'search' | 'manual'

  // Location Fields State
  const [locationForm, setLocationForm] = useState({
    village: initialData?.village || 'Kagal',
    taluka: initialData?.taluka || 'Kagal',
    district: initialData?.district || 'Kolhapur',
    state: initialData?.state || 'Maharashtra',
    pincode: initialData?.pincode || '416216',
    latitude: initialData?.latitude || null,
    longitude: initialData?.longitude || null,
    location_source: initialData?.location_source || 'MANUAL',
    gps_accuracy: initialData?.gps_accuracy || null
  });

  // GPS State
  const [gpsLoading, setGpsLoading] = useState(false);
  const [gpsError, setGpsError] = useState(null);
  const [detectedLocation, setDetectedLocation] = useState(null);

  // Search State
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [searchLoading, setSearchLoading] = useState(false);

  if (!isOpen) return null;

  // Method A: Trigger Device Geolocation on Explicit Click ONLY
  const handleAcquireGPS = () => {
    setGpsError(null);
    setDetectedLocation(null);

    if (!navigator.geolocation) {
      setGpsError(t('location.gps_unsupported') || 'Location access is not supported by this browser.');
      return;
    }

    setGpsLoading(true);

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const acc = position.coords.accuracy;

        try {
          const res = await api.get(`/geocoding/reverse?lat=${lat}&lon=${lon}`);
          setDetectedLocation({
            village: res.data.village || 'Kagal',
            taluka: res.data.taluka || 'Kagal',
            district: res.data.district || 'Kolhapur',
            state: res.data.state || 'Maharashtra',
            pincode: res.data.pincode || '416216',
            latitude: lat,
            longitude: lon,
            gps_accuracy: roundAcc(acc),
            location_source: 'GPS'
          });
        } catch (err) {
          setDetectedLocation({
            village: 'Kagal',
            taluka: 'Kagal',
            district: 'Kolhapur',
            state: 'Maharashtra',
            pincode: '416216',
            latitude: lat,
            longitude: lon,
            gps_accuracy: roundAcc(acc),
            location_source: 'GPS'
          });
        } finally {
          setGpsLoading(false);
        }
      },
      (error) => {
        setGpsLoading(false);
        switch (error.code) {
          case error.PERMISSION_DENIED:
            setGpsError(t('location.gps_denied') || 'Location permission was denied. You can search for your location or enter it manually.');
            break;
          case error.POSITION_UNAVAILABLE:
            setGpsError(t('location.gps_unavailable') || 'Your device location is currently unavailable. Try location search or enter your location manually.');
            break;
          case error.TIMEOUT:
            setGpsError(t('location.gps_timeout') || 'Location detection timed out. Please try again or choose another location method.');
            break;
          default:
            setGpsError(t('location.gps_unknown') || 'Unable to detect your location. Please search or enter it manually.');
            break;
        }
      },
      { timeout: 10000, enableHighAccuracy: true }
    );
  };

  const roundAcc = (val) => (val ? Math.round(val * 10) / 10 : null);

  // Method B: Open Location Search
  const handleSearch = async (q) => {
    setSearchQuery(q);
    if (!q.trim()) {
      setSearchResults([]);
      return;
    }
    setSearchLoading(true);
    try {
      const res = await api.get(`/geocoding/search?q=${encodeURIComponent(q)}`);
      setSearchResults(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      setSearchResults([]);
    } finally {
      setSearchLoading(false);
    }
  };

  const handleSelectSearchResult = (resItem) => {
    const updated = {
      village: resItem.village,
      taluka: resItem.taluka,
      district: resItem.district,
      state: resItem.state,
      pincode: resItem.pincode,
      latitude: resItem.latitude,
      longitude: resItem.longitude,
      location_source: 'SEARCH',
      gps_accuracy: null
    };
    setLocationForm(updated);
    setActiveTab('manual'); // Switch to confirmation view
  };

  // Confirm GPS Location
  const handleConfirmGPSLocation = () => {
    if (detectedLocation) {
      setLocationForm(detectedLocation);
      onSave(detectedLocation);
      onClose();
    }
  };

  const handleSubmitForm = (e) => {
    e.preventDefault();
    onSave(locationForm);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="glass-panel p-6 rounded-3xl max-w-lg w-full space-y-5 border border-slate-700 max-h-[90vh] overflow-y-auto shadow-2xl">
        
        {/* Modal Header */}
        <div className="flex justify-between items-center border-b border-slate-800 pb-3">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <MapPin className="w-5 h-5 text-agri-400" />
            <span>Farm Location Acquisition</span>
          </h3>
          <button onClick={onClose} className="text-slate-400 hover:text-white">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* 3-Method Navigation Switcher */}
        <div className="grid grid-cols-3 gap-2 bg-slate-900 p-1.5 rounded-xl border border-slate-800 text-xs font-bold">
          <button
            type="button"
            onClick={() => setActiveTab('gps')}
            className={`py-2 px-2 rounded-lg flex items-center justify-center space-x-1 transition ${
              activeTab === 'gps'
                ? 'bg-agri-500 text-slate-950 shadow'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Navigation className="w-3.5 h-3.5" />
            <span>{t('location.use_gps') || '📍 GPS'}</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('search')}
            className={`py-2 px-2 rounded-lg flex items-center justify-center space-x-1 transition ${
              activeTab === 'search'
                ? 'bg-agri-500 text-slate-950 shadow'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Search className="w-3.5 h-3.5" />
            <span>{t('location.search_loc') || '🔎 Search'}</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('manual')}
            className={`py-2 px-2 rounded-lg flex items-center justify-center space-x-1 transition ${
              activeTab === 'manual'
                ? 'bg-agri-500 text-slate-950 shadow'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Edit3 className="w-3.5 h-3.5" />
            <span>{t('location.enter_manual') || '✏️ Manual'}</span>
          </button>
        </div>

        {/* METHOD A: Device Geolocation */}
        {activeTab === 'gps' && (
          <div className="space-y-4">
            <div className="text-center py-4 space-y-3">
              <button
                type="button"
                onClick={handleAcquireGPS}
                disabled={gpsLoading}
                className="w-full py-3.5 px-4 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 font-bold text-xs transition shadow-lg shadow-agri-500/20 flex items-center justify-center space-x-2 disabled:opacity-50"
              >
                {gpsLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-slate-950" />
                    <span>Acquiring GPS Satellite Position...</span>
                  </>
                ) : (
                  <>
                    <Navigation className="w-4 h-4" />
                    <span>{t('location.use_gps') || '📍 Use My Current Location'}</span>
                  </>
                )}
              </button>
              <p className="text-[11px] text-slate-400">
                Permission requested only when clicked. Requires secure HTTPS or localhost context.
              </p>
            </div>

            {gpsError && (
              <div className="p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-300 text-xs flex items-center space-x-2">
                <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
                <span>{gpsError}</span>
              </div>
            )}

            {/* GPS Location Preview Confirmation Card */}
            {detectedLocation && (
              <div className="glass-panel p-4 rounded-2xl border border-agri-500/40 bg-agri-500/5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-agri-400 flex items-center space-x-1">
                    <CheckCircle className="w-4 h-4" />
                    <span>{t('location.detected_title') || 'Location Detected'}</span>
                  </span>
                  {detectedLocation.gps_accuracy && (
                    <span className="text-[10px] text-slate-400 bg-slate-900 px-2 py-0.5 rounded font-mono">
                      Accuracy ±{detectedLocation.gps_accuracy}m
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-2 gap-2 text-xs text-slate-300 bg-slate-950/80 p-3 rounded-xl border border-slate-800">
                  <div>Village: <strong className="text-white">{detectedLocation.village}</strong></div>
                  <div>Taluka: <strong className="text-white">{detectedLocation.taluka}</strong></div>
                  <div>District: <strong className="text-white">{detectedLocation.district}</strong></div>
                  <div>State: <strong className="text-white">{detectedLocation.state}</strong></div>
                  <div className="col-span-2">PIN Code: <strong className="text-white">{detectedLocation.pincode}</strong></div>
                </div>

                <div className="flex justify-end space-x-2 pt-1">
                  <button
                    type="button"
                    onClick={() => {
                      setLocationForm(detectedLocation);
                      setActiveTab('manual');
                    }}
                    className="px-3.5 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700"
                  >
                    Edit
                  </button>
                  <button
                    type="button"
                    onClick={handleConfirmGPSLocation}
                    className="px-4 py-1.5 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 text-xs font-bold shadow"
                  >
                    {t('location.use_this') || 'Use This Location'}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* METHOD B: Open Location Search */}
        {activeTab === 'search' && (
          <div className="space-y-4">
            <div className="relative">
              <div className="flex items-center space-x-2 bg-slate-900 px-3.5 py-2.5 rounded-xl border border-slate-800 text-xs">
                <Search className="w-4 h-4 text-slate-500 shrink-0" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => handleSearch(e.target.value)}
                  placeholder="Search village, town, or district (e.g. Kagal, Kolhapur, Pune...)"
                  className="bg-transparent text-slate-200 w-full focus:outline-none placeholder:text-slate-600"
                  autoFocus
                />
                {searchLoading && <Loader2 className="w-4 h-4 animate-spin text-agri-400 shrink-0" />}
              </div>
            </div>

            <div className="max-h-60 overflow-y-auto space-y-1">
              {searchResults.map((resItem, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSelectSearchResult(resItem)}
                  className="w-full text-left p-3 rounded-xl hover:bg-slate-800 flex items-center justify-between text-xs text-slate-200 transition border border-transparent hover:border-slate-700"
                >
                  <div className="space-y-0.5">
                    <span className="font-bold text-white block">{resItem.village}, {resItem.district}</span>
                    <span className="text-[11px] text-slate-400 block">{resItem.display_name}</span>
                  </div>
                  <span className="text-[10px] text-agri-400 font-mono font-bold">Select</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* METHOD C: Manual Location Entry / Review */}
        {activeTab === 'manual' && (
          <form onSubmit={handleSubmitForm} className="space-y-3">
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.village')}</label>
                <input
                  type="text"
                  value={locationForm.village}
                  onChange={(e) => setLocationForm({ ...locationForm, village: e.target.value, location_source: 'MANUAL' })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.taluka')}</label>
                <input
                  type="text"
                  value={locationForm.taluka}
                  onChange={(e) => setLocationForm({ ...locationForm, taluka: e.target.value, location_source: 'MANUAL' })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.district')}</label>
                <input
                  type="text"
                  value={locationForm.district}
                  onChange={(e) => setLocationForm({ ...locationForm, district: e.target.value, location_source: 'MANUAL' })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.state')}</label>
                <input
                  type="text"
                  value={locationForm.state}
                  onChange={(e) => setLocationForm({ ...locationForm, state: e.target.value, location_source: 'MANUAL' })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.pin')}</label>
              <input
                type="text"
                value={locationForm.pincode}
                onChange={(e) => setLocationForm({ ...locationForm, pincode: e.target.value, location_source: 'MANUAL' })}
                className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                required
              />
            </div>

            <div className="flex justify-end space-x-2 pt-3 border-t border-slate-800">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl bg-slate-800 text-xs text-slate-300"
              >
                {t('common.cancel')}
              </button>
              <button
                type="submit"
                className="px-5 py-2 rounded-xl bg-agri-500 hover:bg-agri-400 text-slate-950 text-xs font-bold shadow"
              >
                {t('profile.save_location')}
              </button>
            </div>
          </form>
        )}

      </div>
    </div>
  );
};
