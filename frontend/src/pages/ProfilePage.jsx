import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { User, Mail, MapPin, Plus, LogOut, CheckCircle, Sprout, Home, Edit2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { LocationPickerModal } from '../components/location/LocationPickerModal';
import api from '../services/api';

export const ProfilePage = () => {
  const { user, logout } = useAuth();
  const { lang, setLang, t } = useLanguage();
  const navigate = useNavigate();

  const [farms, setFarms] = useState([]);
  const [showAddFarmModal, setShowAddFarmModal] = useState(false);

  // Location Modal State
  const [showLocationPicker, setShowLocationPicker] = useState(false);
  const [locationPickerTarget, setLocationPickerTarget] = useState(null); // 'user' or farm object

  // User Profile Location State
  const [userLoc, setUserLoc] = useState({
    village: user?.village || '',
    taluka: user?.taluka || '',
    district: user?.district || '',
    state: user?.state || (lang === 'mr' ? 'महाराष्ट्र' : 'Maharashtra'),
    pincode: user?.pincode || '',
    latitude: user?.latitude || null,
    longitude: user?.longitude || null,
    location_source: 'GPS'
  });

  // New Farm State
  const [newFarm, setNewFarm] = useState({
    name: '',
    village: '',
    taluka: '',
    district: '',
    state: lang === 'mr' ? 'महाराष्ट्र' : 'Maharashtra',
    pincode: '',
    latitude: null,
    longitude: null,
    location_source: 'MANUAL',
    crop_types: 'Tomato, Potato, Sugarcane',
    area_acres: 2.5,
    irrigation_type: 'Drip Irrigation'
  });

  useEffect(() => {
    // Load farms
    api.get('/farms')
      .then(res => setFarms(Array.isArray(res.data) ? res.data : []))
      .catch(() => setFarms([]));

    // Load current user's profile location
    api.get('/auth/me')
      .then(res => {
        const u = res.data;
        if (u && (u.village || u.district || u.latitude)) {
          setUserLoc(prev => ({
            ...prev,
            village: u.village || prev.village,
            taluka: u.taluka || prev.taluka,
            district: u.district || prev.district,
            state: u.state || prev.state,
            pincode: u.pincode || prev.pincode,
            latitude: u.latitude || prev.latitude,
            longitude: u.longitude || prev.longitude,
            location_source: u.latitude ? 'GPS' : 'MANUAL'
          }));
        }
      })
      .catch(() => {});
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleOpenUserLocPicker = () => {
    setLocationPickerTarget('user');
    setShowLocationPicker(true);
  };

  const handleOpenFarmLocPicker = (farm) => {
    setLocationPickerTarget(farm);
    setShowLocationPicker(true);
  };

  const handleLocationSaved = (savedLoc) => {
    if (locationPickerTarget === 'user') {
      setUserLoc(prev => ({ ...prev, ...savedLoc }));
      api.patch('/user/profile', savedLoc).catch(() => {});
    } else if (locationPickerTarget && typeof locationPickerTarget === 'object') {
      const updatedFarm = { ...locationPickerTarget, ...savedLoc };
      api.patch(`/farms/${locationPickerTarget.id}`, updatedFarm)
        .then(res => setFarms(prev => prev.map(f => f.id === locationPickerTarget.id ? res.data : f)))
        .catch(() => setFarms(prev => prev.map(f => f.id === locationPickerTarget.id ? updatedFarm : f)));
    }
  };

  const handleAddFarm = (e) => {
    e.preventDefault();
    if (!newFarm.name.trim()) return;
    api.post('/farms', newFarm)
      .then(res => {
        setFarms(prev => [...prev, res.data]);
        setShowAddFarmModal(false);
      })
      .catch(() => {
        setFarms(prev => [...prev, { id: `farm_${Date.now()}`, ...newFarm }]);
        setShowAddFarmModal(false);
      });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-agro-cream tracking-tight">
            {t('profile.title') || 'Farmer Profile & Lands'}
          </h1>
          <p className="text-xs sm:text-sm text-agro-muted mt-1">
            {t('profile.subtitle') || 'Manage verified farm locations, crops under cultivation, and regional microclimate settings.'}
          </p>
        </div>
        <button
          onClick={handleLogout}
          className="px-4 py-2.5 rounded-xl bg-agro-terracotta/15 hover:bg-agro-terracotta/25 text-agro-terracotta text-xs font-bold border border-agro-terracotta/30 flex items-center space-x-2 transition"
        >
          <LogOut className="w-4 h-4" />
          <span>{t('nav.logout') || 'Log Out'}</span>
        </button>
      </div>

      {/* User Info Card */}
      <div className="agro-panel p-6 rounded-2xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            {user?.photoURL ? (
              <img src={user.photoURL} alt={user.displayName} className="w-16 h-16 rounded-full object-cover border-2 border-agro-primary" />
            ) : (
              <div className="w-16 h-16 rounded-full bg-agro-primary/20 text-agro-primary border border-agro-primary/30 flex items-center justify-center font-bold text-2xl">
                {user?.displayName ? user.displayName.charAt(0).toUpperCase() : 'F'}
              </div>
            )}

            <div className="space-y-1">
              <h2 className="text-lg font-bold text-agro-cream flex items-center space-x-2">
                <span>{user?.displayName || user?.full_name || t('header.role_farmer')}</span>
                <span className="px-2.5 py-0.5 rounded-full bg-agro-primary/15 text-agro-primary border border-agro-primary/30 text-[10px] font-bold uppercase tracking-wide">
                  {user?.role || t('header.role_farmer')}
                </span>
              </h2>
              <div className="flex items-center space-x-4 text-xs text-agro-muted">
                <span className="flex items-center space-x-1">
                  <Mail className="w-3.5 h-3.5 text-agro-muted" />
                  <span>{user?.email}</span>
                </span>
                <span className="flex items-center space-x-1">
                  <MapPin className="w-3.5 h-3.5 text-agro-primary" />
                  <span>{userLoc.village || ''}{userLoc.district ? `, ${userLoc.district}` : ''}{userLoc.state ? `, ${userLoc.state}` : ''}</span>
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={handleOpenUserLocPicker}
            className="px-3.5 py-2.5 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-cream font-bold text-xs flex items-center space-x-1.5 border border-agro-border transition shrink-0"
          >
            <Edit2 className="w-3.5 h-3.5 text-agro-primary" />
            <span>{t('profile.edit_location') || 'Edit Location'}</span>
          </button>
        </div>

        {/* Structured Indian Agricultural Location Details */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 text-xs">
          <div className="p-3.5 rounded-xl bg-agro-surface border border-agro-border space-y-1">
            <span className="text-agro-muted text-[10px] block uppercase font-bold flex items-center justify-between">
              <span>{t('profile.location') || 'Location'}</span>
              <span className="text-agro-primary font-mono text-[9px] font-bold">
                {lang === 'mr' ? 'स्रोत' : 'Source'}: {userLoc.location_source || 'MANUAL'}
              </span>
            </span>
            <span className="font-semibold text-agro-cream block">
              {t('profile.village') || 'Village'}: {userLoc.village || 'N/A'} | {t('profile.taluka') || 'Taluka'}: {userLoc.taluka || 'N/A'}
            </span>
            <span className="text-agro-muted block text-[11px]">
              {t('profile.district') || 'District'}: {userLoc.district || 'N/A'}, {userLoc.state || ''} ({userLoc.pincode || 'N/A'})
            </span>
          </div>

          <div className="p-3.5 rounded-xl bg-agro-surface border border-agro-border space-y-1">
            <span className="text-agro-muted text-[10px] block uppercase font-bold">{t('profile.status') || 'Account Status'}</span>
            <div className="flex items-center space-x-1.5 text-agro-primary font-semibold">
              <CheckCircle className="w-4 h-4" />
              <span>{lang === 'mr' ? 'सक्रिय नोंदणीकृत शेतकरी' : 'Active Verified Farmer'}</span>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-agro-surface border border-agro-border space-y-1">
            <span className="text-agro-muted text-[10px] block uppercase font-bold">{t('profile.language') || 'Language'}</span>
            <div className="flex items-center justify-between">
              <span className="text-agro-cream font-semibold">{lang === 'en' ? 'English (EN)' : 'मराठी (MR)'}</span>
              <button 
                onClick={() => setLang(lang === 'en' ? 'mr' : 'en')}
                className="text-[11px] text-agro-primary hover:text-agro-lime font-bold transition"
              >
                {t('header.toggle_lang') || 'Switch'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Farms List */}
      <div className="agro-panel p-6 rounded-2xl space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-base font-bold text-agro-cream">{t('profile.farms') || 'Farm Lands & Plots'}</h2>
            <p className="text-xs text-agro-muted">
              {lang === 'mr' ? 'शेताचे प्लॉट व्यवस्थापित करा व शेताचे स्थान बदला' : 'Manage agricultural land plots and edit individual farm locations'}
            </p>
          </div>
          <button
            onClick={() => setShowAddFarmModal(true)}
            className="px-3.5 py-2.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white font-bold text-xs flex items-center space-x-1.5 transition shadow-md shadow-agro-primary/20 active:scale-95"
          >
            <Plus className="w-4 h-4" />
            <span>{t('profile.add_farm') || 'Add Farm Plot'}</span>
          </button>
        </div>

        {farms.length === 0 ? (
          <div className="py-10 text-center text-xs text-agro-muted bg-agro-surface/60 rounded-xl border border-agro-border p-4 space-y-2">
            <Sprout className="w-8 h-8 mx-auto text-agro-primary/60" />
            <p>{t('profile.no_farms') || 'No farm plots added yet. Register your agricultural plots to enable localized crop advisory.'}</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {farms.map((f) => (
              <div key={f.id} className="p-4 rounded-xl bg-agro-surface border border-agro-border space-y-2.5">
                <div className="flex justify-between items-start">
                  <h3 className="text-sm font-bold text-agro-cream flex items-center space-x-1.5">
                    <Home className="w-4 h-4 text-agro-primary" />
                    <span>{f.name}</span>
                  </h3>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleOpenFarmLocPicker(f)}
                      className="px-2 py-1 rounded-lg bg-agro-bg hover:bg-agro-hover text-agro-primary font-bold text-[10px] flex items-center space-x-1 transition border border-agro-border"
                    >
                      <Edit2 className="w-3 h-3" />
                      <span>{t('profile.location') || 'Location'}</span>
                    </button>
                    <span className="px-2 py-0.5 rounded-lg bg-agro-primary/10 text-agro-primary border border-agro-primary/20 text-[10px] font-bold">
                      {f.area_acres} {lang === 'mr' ? 'एकर' : 'Acres'}
                    </span>
                  </div>
                </div>
                <p className="text-xs text-agro-muted">
                  {lang === 'mr' ? 'मुख्य पिके' : 'Primary Crops'}: <strong className="text-agro-cream">{f.crop_types}</strong>
                </p>
                <p className="text-xs text-agro-muted">
                  {lang === 'mr' ? 'स्थान' : 'Location'}: <strong className="text-agro-cream">{f.village || ''}, {f.taluka || ''}, {f.district || ''}, {f.state || ''} {f.pincode ? `(${f.pincode})` : ''}</strong>
                </p>
                <div className="flex justify-between items-center text-xs text-agro-muted pt-2 border-t border-agro-border font-mono text-[10px]">
                  <span>{lang === 'mr' ? 'स्रोत' : 'Source'}: {f.location_source || 'MANUAL'}</span>
                  <span>PIN: {f.pincode || '416216'}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 3-Method Location Picker Modal */}
      <LocationPickerModal
        isOpen={showLocationPicker}
        onClose={() => setShowLocationPicker(false)}
        onSave={handleLocationSaved}
        initialData={locationPickerTarget === 'user' ? userLoc : (locationPickerTarget || userLoc)}
      />

      {/* Add Farm Modal */}
      {showAddFarmModal && (
        <div className="fixed inset-0 z-50 bg-agro-bg/85 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="agro-panel p-6 rounded-2xl max-w-lg w-full space-y-4 border border-agro-border max-h-[90vh] overflow-y-auto shadow-2xl">
            <h3 className="text-lg font-bold text-agro-cream">
              {lang === 'mr' ? 'नवीन शेत व जमिनीची माहिती नोंदवा' : 'Register Farm Plot & Land Info'}
            </h3>
            <form onSubmit={handleAddFarm} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.farm_name') || 'Farm Name'}</label>
                <input
                  type="text"
                  value={newFarm.name}
                  onChange={(e) => setNewFarm({ ...newFarm, name: e.target.value })}
                  placeholder="Sunrise Organic Farm"
                  className="w-full px-3.5 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream placeholder:text-agro-muted/60 focus:outline-none focus:border-agro-primary"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.village') || 'Village'}</label>
                  <input
                    type="text"
                    value={newFarm.village}
                    onChange={(e) => setNewFarm({ ...newFarm, village: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.taluka') || 'Taluka'}</label>
                  <input
                    type="text"
                    value={newFarm.taluka}
                    onChange={(e) => setNewFarm({ ...newFarm, taluka: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.district') || 'District'}</label>
                  <input
                    type="text"
                    value={newFarm.district}
                    onChange={(e) => setNewFarm({ ...newFarm, district: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.state') || 'State'}</label>
                  <input
                    type="text"
                    value={newFarm.state}
                    onChange={(e) => setNewFarm({ ...newFarm, state: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.pin') || 'PIN Code'}</label>
                  <input
                    type="text"
                    value={newFarm.pincode}
                    onChange={(e) => setNewFarm({ ...newFarm, pincode: e.target.value })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-agro-muted mb-1">{t('profile.area') || 'Land Area (Acres)'}</label>
                  <input
                    type="number"
                    step="0.5"
                    value={newFarm.area_acres}
                    onChange={(e) => setNewFarm({ ...newFarm, area_acres: parseFloat(e.target.value) || 1 })}
                    className="w-full px-3.5 py-2.5 rounded-xl bg-agro-bg border border-agro-border text-xs text-agro-cream focus:outline-none focus:border-agro-primary"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-2 pt-3 border-t border-agro-border">
                <button
                  type="button"
                  onClick={() => setShowAddFarmModal(false)}
                  className="px-4 py-2 rounded-xl bg-agro-surface hover:bg-agro-hover border border-agro-border text-xs text-agro-cream transition"
                >
                  {t('common.cancel') || 'Cancel'}
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-xs font-bold text-white shadow transition active:scale-95"
                >
                  {t('profile.save') || 'Save Plot'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
