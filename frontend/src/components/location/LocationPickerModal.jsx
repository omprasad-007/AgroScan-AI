import React, { useState, useEffect } from 'react';
import { MapPin, Search, Edit3, Navigation, AlertCircle, CheckCircle2, Loader2, X } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';
import api from '../../services/api';

export const LocationPickerModal = ({ isOpen, onClose, onSave, initialData }) => {
  const { t, lang } = useLanguage();
  const hasGeolocation = typeof navigator !== 'undefined' && 'geolocation' in navigator;
  const [activeTab, setActiveTab] = useState(hasGeolocation ? 'gps' : 'manual');

  // Location Fields State
  const [locationForm, setLocationForm] = useState({
    village: initialData?.village || '',
    taluka: initialData?.taluka || '',
    district: initialData?.district || '',
    state: initialData?.state || (lang === 'mr' ? 'महाराष्ट्र' : 'Maharashtra'),
    pincode: initialData?.pincode || '',
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

  useEffect(() => {
    if (initialData) {
      setLocationForm({
        village: initialData.village || '',
        taluka: initialData.taluka || '',
        district: initialData.district || '',
        state: initialData.state || (lang === 'mr' ? 'महाराष्ट्र' : 'Maharashtra'),
        pincode: initialData.pincode || '',
        latitude: initialData.latitude || null,
        longitude: initialData.longitude || null,
        location_source: initialData.location_source || 'MANUAL',
        gps_accuracy: initialData.gps_accuracy || null
      });
    }
  }, [initialData, lang]);

  if (!isOpen) return null;

  // Method A: Trigger Device Geolocation with High Accuracy and 10s Timeout
  const handleAcquireGPS = () => {
    setGpsError(null);
    setDetectedLocation(null);

    if (!hasGeolocation) {
      setGpsError(t('location.gps_unsupported') || 'Geolocation is not supported by your current browser. Please enter your location manually.');
      setActiveTab('manual');
      return;
    }

    setGpsLoading(true);

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const acc = position.coords.accuracy;

        try {
          const res = await api.get(`/geocoding/reverse?lat=${lat}&lon=${lon}&lang=${lang}`);
          const geo = res.data || {};
          setDetectedLocation({
            village: geo.village || '',
            taluka: geo.taluka || geo.village || '',
            district: geo.district || '',
            state: geo.state || (lang === 'mr' ? 'महाराष्ट्र' : 'Maharashtra'),
            pincode: geo.pincode || '',
            latitude: lat,
            longitude: lon,
            gps_accuracy: roundAcc(acc),
            location_source: 'GPS'
          });
        } catch (err) {
          setDetectedLocation({
            village: '',
            taluka: '',
            district: '',
            state: lang === 'mr' ? 'महाराष्ट्र' : 'Maharashtra',
            pincode: '',
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
            setGpsError(t('location.gps_denied') || 'GPS permission was denied. Please allow location access in your browser settings, or enter your farm location manually below.');
            break;
          case error.POSITION_UNAVAILABLE:
            setGpsError(t('location.gps_unavailable') || 'Device location position is unavailable. Please check your GPS signal or enter your location manually.');
            break;
          case error.TIMEOUT:
            setGpsError(t('location.gps_timeout') || "Couldn't get your location in time — try again or enter it manually.");
            break;
          default:
            setGpsError(t('location.gps_unknown') || 'Unable to detect current GPS location. Please use search or enter it manually.');
            break;
        }
      },
      { timeout: 10000, enableHighAccuracy: true, maximumAge: 0 }
    );
  };

  const roundAcc = (val) => (val ? Math.round(val * 10) / 10 : null);

  // Method B: Location Search
  const handleSearch = async (q) => {
    setSearchQuery(q);
    if (!q.trim()) {
      setSearchResults([]);
      return;
    }
    setSearchLoading(true);
    try {
      const res = await api.get(`/geocoding/search?q=${encodeURIComponent(q)}&lang=${lang}`);
      setSearchResults(Array.isArray(res.data) ? res.data : []);
    } catch (err) {
      setSearchResults([]);
    } finally {
      setSearchLoading(false);
    }
  };

  const handleSelectSearchResult = (resItem) => {
    const updated = {
      village: resItem.village || '',
      taluka: resItem.taluka || '',
      district: resItem.district || '',
      state: resItem.state || (lang === 'mr' ? 'महाराष्ट्र' : 'Maharashtra'),
      pincode: resItem.pincode || '',
      latitude: resItem.latitude || null,
      longitude: resItem.longitude || null,
      location_source: 'SEARCH',
      gps_accuracy: null
    };
    setLocationForm(updated);
    setActiveTab('manual');
  };

  // Confirm GPS Location
  const handleConfirmGPSLocation = () => {
    if (detectedLocation) {
      const finalLoc = { ...detectedLocation };
      setLocationForm(finalLoc);
      onSave(finalLoc);
      onClose();
    }
  };

  const handleSubmitForm = (e) => {
    e.preventDefault();
    onSave(locationForm);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-agro-bg/85 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="agro-panel p-6 rounded-3xl max-w-lg w-full space-y-5 border border-agro-border max-h-[90vh] overflow-y-auto shadow-2xl">
        
        {/* Modal Header */}
        <div className="flex justify-between items-center border-b border-agro-border pb-3">
          <h3 className="text-base font-bold text-agro-cream flex items-center space-x-2">
            <MapPin className="w-5 h-5 text-agro-primary" />
            <span>{t('location.title') || 'Farm Location Acquisition'}</span>
          </h3>
          <button onClick={onClose} className="text-agro-muted hover:text-agro-cream transition" aria-label="Close location modal">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Navigation Switcher */}
        <div className={`grid ${hasGeolocation ? 'grid-cols-3' : 'grid-cols-2'} gap-2 bg-agro-bg p-1.5 rounded-xl border border-agro-border text-xs font-bold`}>
          {hasGeolocation && (
            <button
              type="button"
              onClick={() => setActiveTab('gps')}
              className={`py-2 px-2 rounded-lg flex items-center justify-center space-x-1.5 transition ${
                activeTab === 'gps' ? 'bg-agro-primary text-white shadow font-bold' : 'text-agro-muted hover:text-agro-cream'
              }`}
            >
              <Navigation className="w-3.5 h-3.5" />
              <span>{t('location.use_gps') || 'GPS'}</span>
            </button>
          )}

          <button
            type="button"
            onClick={() => setActiveTab('search')}
            className={`py-2 px-2 rounded-lg flex items-center justify-center space-x-1.5 transition ${
              activeTab === 'search' ? 'bg-agro-primary text-white shadow font-bold' : 'text-agro-muted hover:text-agro-cream'
            }`}
          >
            <Search className="w-3.5 h-3.5" />
            <span>{t('location.search_loc') || 'Search'}</span>
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('manual')}
            className={`py-2 px-2 rounded-lg flex items-center justify-center space-x-1.5 transition ${
              activeTab === 'manual' ? 'bg-agro-primary text-white shadow font-bold' : 'text-agro-muted hover:text-agro-cream'
            }`}
          >
            <Edit3 className="w-3.5 h-3.5" />
            <span>{t('location.enter_manual') || 'Manual'}</span>
          </button>
        </div>

        {/* METHOD A: Device Geolocation */}
        {activeTab === 'gps' && hasGeolocation && (
          <div className="space-y-4">
            <div className="text-center py-4 space-y-3">
              <button
                type="button"
                onClick={handleAcquireGPS}
                disabled={gpsLoading}
                className="w-full py-3.5 px-4 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white font-bold text-xs transition shadow-lg shadow-agro-primary/20 flex items-center justify-center space-x-2 disabled:opacity-50 active:scale-[0.98]"
              >
                {gpsLoading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin text-white" />
                    <span>{t('location.detecting') || 'Acquiring high-accuracy GPS coordinates...'}</span>
                  </>
                ) : (
                  <>
                    <Navigation className="w-4 h-4" />
                    <span>{t('location.use_gps') || 'Use My Current Location'}</span>
                  </>
                )}
              </button>
              <p className="text-[11px] text-agro-muted">
                {lang === 'mr' 
                  ? 'डिव्हाइसच्या GPS हार्डवेअरवरून थेट ताजी भौगोलिक माहिती मागवली जाते.'
                  : 'Fresh coordinates requested from device hardware on click.'
                }
              </p>
            </div>

            {gpsError && (
              <div className="p-3.5 rounded-xl bg-agro-terracotta/15 border border-agro-terracotta/30 text-agro-cream text-xs space-y-2">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="w-4 h-4 text-agro-terracotta shrink-0" />
                  <span>{gpsError}</span>
                </div>
                <div className="flex justify-end pt-1">
                  <button
                    type="button"
                    onClick={() => setActiveTab('manual')}
                    className="px-3 py-1 rounded-lg bg-agro-terracotta/25 hover:bg-agro-terracotta/35 text-agro-cream text-xs font-bold transition"
                  >
                    {t('location.enter_manual') || 'Enter Location Manually'} →
                  </button>
                </div>
              </div>
            )}

            {/* GPS Location Preview Confirmation Card */}
            {detectedLocation && (
              <div className="agro-panel p-4 rounded-2xl border border-agro-primary/40 bg-agro-primary/5 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-agro-primary flex items-center space-x-1.5">
                    <CheckCircle2 className="w-4 h-4" />
                    <span>{t('location.detected_title') || 'Location Detected'}</span>
                  </span>
                  <span className="text-[10px] text-agro-muted bg-agro-bg px-2 py-0.5 rounded font-mono border border-agro-border">
                    {detectedLocation.latitude.toFixed(4)}, {detectedLocation.longitude.toFixed(4)}
                    {detectedLocation.gps_accuracy ? ` (±${detectedLocation.gps_accuracy}m)` : ''}
                  </span>
                </div>

                {/* Editable Detected Fields */}
                <div className="grid grid-cols-2 gap-2 text-xs text-agro-cream bg-agro-surface p-3 rounded-xl border border-agro-border">
                  <div>
                    <label className="text-[10px] text-agro-muted block">{t('location.village') || 'Village / Locality'}</label>
                    <input
                      type="text"
                      value={detectedLocation.village}
                      onChange={(e) => setDetectedLocation({ ...detectedLocation, village: e.target.value })}
                      placeholder="Enter village"
                      className="w-full bg-agro-bg text-agro-cream px-2 py-1 rounded-lg text-xs border border-agro-border mt-0.5 focus:outline-none focus:border-agro-primary"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] text-agro-muted block">{t('location.taluka') || 'Taluka / Tehsil'}</label>
                    <input
                      type="text"
                      value={detectedLocation.taluka}
                      onChange={(e) => setDetectedLocation({ ...detectedLocation, taluka: e.target.value })}
                      placeholder="Enter taluka"
                      className="w-full bg-agro-bg text-agro-cream px-2 py-1 rounded-lg text-xs border border-agro-border mt-0.5 focus:outline-none focus:border-agro-primary"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] text-agro-muted block">{t('location.district') || 'District'}</label>
                    <input
                      type="text"
                      value={detectedLocation.district}
                      onChange={(e) => setDetectedLocation({ ...detectedLocation, district: e.target.value })}
                      placeholder="Enter district"
                      className="w-full bg-agro-bg text-agro-cream px-2 py-1 rounded-lg text-xs border border-agro-border mt-0.5 focus:outline-none focus:border-agro-primary"
                    />
                  </div>
                  <div>
                    <label className="text-[10px] text-agro-muted block">{t('location.state') || 'State'}</label>
                    <input
                      type="text"
                      value={detectedLocation.state}
                      onChange={(e) => setDetectedLocation({ ...detectedLocation, state: e.target.value })}
                      placeholder="Enter state"
                      className="w-full bg-agro-bg text-agro-cream px-2 py-1 rounded-lg text-xs border border-agro-border mt-0.5 focus:outline-none focus:border-agro-primary"
                    />
                  </div>
                  <div className="col-span-2">
                    <label className="text-[10px] text-agro-muted block">{t('location.pincode') || 'PIN Code'}</label>
                    <input
                      type="text"
                      value={detectedLocation.pincode}
                      onChange={(e) => setDetectedLocation({ ...detectedLocation, pincode: e.target.value })}
                      placeholder="e.g. 416216"
                      className="w-full bg-agro-bg text-agro-cream px-2 py-1 rounded-lg text-xs border border-agro-border mt-0.5 focus:outline-none focus:border-agro-primary"
                    />
                  </div>
                </div>

                <div className="flex justify-end space-x-2 pt-1">
                  <button
                    type="button"
                    onClick={() => {
                      setLocationForm(detectedLocation);
                      setActiveTab('manual');
                    }}
                    className="px-3.5 py-1.5 rounded-xl bg-agro-surface hover:bg-agro-hover text-xs font-semibold text-agro-cream border border-agro-border transition"
                  >
                    {t('common.edit') || 'Edit'}
                  </button>
                  <button
                    type="button"
                    onClick={handleConfirmGPSLocation}
                    className="px-4 py-1.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-bold shadow transition active:scale-95"
                  >
                    {t('location.save') || 'Confirm & Save Location'}
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* METHOD B: Location Search */}
        {activeTab === 'search' && (
          <div className="space-y-4">
            <div className="relative">
              <div className="flex items-center space-x-2 bg-agro-bg px-3.5 py-2.5 rounded-xl border border-agro-border text-xs">
                <Search className="w-4 h-4 text-agro-muted shrink-0" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => handleSearch(e.target.value)}
                  placeholder={t('location.search_placeholder') || "Search village, town, district (e.g. Baramati, Nashik)..."}
                  className="bg-transparent text-agro-cream w-full focus:outline-none placeholder:text-agro-muted/60"
                  autoFocus
                />
                {searchLoading && <Loader2 className="w-4 h-4 animate-spin text-agro-primary shrink-0" />}
              </div>
            </div>

            <div className="max-h-60 overflow-y-auto space-y-1">
              {searchResults.map((resItem, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSelectSearchResult(resItem)}
                  className="w-full text-left p-3 rounded-xl hover:bg-agro-surface flex items-center justify-between text-xs text-agro-cream transition border border-transparent hover:border-agro-border"
                >
                  <div className="space-y-0.5">
                    <span className="font-bold text-agro-cream block">{resItem.village || resItem.district}, {resItem.district}</span>
                    <span className="text-[11px] text-agro-muted block">{resItem.display_name}</span>
                  </div>
                  <span className="text-[10px] text-agro-primary font-mono font-bold">
                    {lang === 'mr' ? 'निवडा' : 'Select'}
                  </span>
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
                <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.village') || 'Village / Town'}</label>
                <input
                  type="text"
                  value={locationForm.village}
                  onChange={(e) => setLocationForm({ ...locationForm, village: e.target.value, location_source: 'MANUAL' })}
                  placeholder={t('profile.village') || "Village name"}
                  className="w-full px-3 py-2 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.taluka') || 'Taluka / Block'}</label>
                <input
                  type="text"
                  value={locationForm.taluka}
                  onChange={(e) => setLocationForm({ ...locationForm, taluka: e.target.value, location_source: 'MANUAL' })}
                  placeholder={t('profile.taluka') || "Taluka"}
                  className="w-full px-3 py-2 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                  required
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.district') || 'District'}</label>
                <input
                  type="text"
                  value={locationForm.district}
                  onChange={(e) => setLocationForm({ ...locationForm, district: e.target.value, location_source: 'MANUAL' })}
                  placeholder={t('profile.district') || "District"}
                  className="w-full px-3 py-2 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                  required
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.state') || 'State'}</label>
                <input
                  type="text"
                  value={locationForm.state}
                  onChange={(e) => setLocationForm({ ...locationForm, state: e.target.value, location_source: 'MANUAL' })}
                  placeholder={t('profile.state') || "State"}
                  className="w-full px-3 py-2 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.pin') || 'PIN Code'}</label>
              <input
                type="text"
                value={locationForm.pincode}
                onChange={(e) => setLocationForm({ ...locationForm, pincode: e.target.value, location_source: 'MANUAL' })}
                placeholder="6-digit PIN code"
                className="w-full px-3 py-2 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                required
              />
            </div>

            <div className="flex justify-end space-x-2 pt-3 border-t border-agro-border">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 rounded-xl bg-agro-surface text-xs text-agro-muted hover:text-agro-cream hover:bg-agro-hover transition border border-agro-border"
              >
                {t('common.cancel') || 'Cancel'}
              </button>
              <button
                type="submit"
                className="px-5 py-2 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-bold shadow transition active:scale-95"
              >
                {t('profile.save_location') || 'Save Location'}
              </button>
            </div>
          </form>
        )}

      </div>
    </div>
  );
};
