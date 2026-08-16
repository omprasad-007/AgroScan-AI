import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { User, Mail, MapPin, Plus, LogOut, CheckCircle, Sprout, Home, Edit2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export const ProfilePage = () => {
  const { user, logout } = useAuth();
  const { lang, setLang, t } = useLanguage();
  const navigate = useNavigate();

  const [farms, setFarms] = useState([]);
  const [showAddFarmModal, setShowAddFarmModal] = useState(false);
  const [showEditUserLocModal, setShowEditUserLocModal] = useState(false);
  const [showEditFarmLocModal, setShowEditFarmLocModal] = useState(false);
  const [selectedFarm, setSelectedFarm] = useState(null);

  // User Profile Location State
  const [userLoc, setUserLoc] = useState({
    village: 'Kagal',
    taluka: 'Kagal',
    district: 'Kolhapur',
    state: 'Maharashtra',
    pincode: '416216'
  });

  // Farm State
  const [newFarm, setNewFarm] = useState({
    name: '',
    village: 'Kagal',
    taluka: 'Kagal',
    district: 'Kolhapur',
    state: 'Maharashtra',
    pincode: '416216',
    crop_types: 'Tomato, Potato, Sugarcane',
    area_acres: 2.5,
    irrigation_type: 'Drip Irrigation'
  });

  useEffect(() => {
    api.get('/farms')
      .then(res => setFarms(Array.isArray(res.data) ? res.data : []))
      .catch(() => setFarms([]));
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleSaveUserLocation = (e) => {
    e.preventDefault();
    api.patch('/user/profile', userLoc)
      .catch(() => {});
    setShowEditUserLocModal(false);
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

  const handleOpenEditFarm = (farm) => {
    setSelectedFarm(farm);
    setShowEditFarmLocModal(true);
  };

  const handleSaveFarmLocation = (e) => {
    e.preventDefault();
    if (!selectedFarm) return;
    api.patch(`/farms/${selectedFarm.id}`, selectedFarm)
      .then(res => {
        setFarms(prev => prev.map(f => f.id === selectedFarm.id ? res.data : f));
        setShowEditFarmLocModal(false);
      })
      .catch(() => {
        setFarms(prev => prev.map(f => f.id === selectedFarm.id ? selectedFarm : f));
        setShowEditFarmLocModal(false);
      });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">{t('profile.title')}</h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            {t('profile.subtitle')}
          </p>
        </div>
        <button
          onClick={handleLogout}
          className="px-4 py-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-bold border border-red-500/30 flex items-center space-x-2 transition"
        >
          <LogOut className="w-4 h-4" />
          <span>{t('nav.logout')}</span>
        </button>
      </div>

      {/* User Info Card */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            {user?.photoURL ? (
              <img src={user.photoURL} alt={user.displayName} className="w-16 h-16 rounded-full object-cover border-2 border-primary" />
            ) : (
              <div className="w-16 h-16 rounded-full bg-primary/20 text-primary border border-primary/30 flex items-center justify-center font-bold text-2xl">
                {user?.displayName ? user.displayName.charAt(0).toUpperCase() : 'F'}
              </div>
            )}

            <div className="space-y-1">
              <h2 className="text-lg font-bold text-white flex items-center space-x-2">
                <span>{user?.displayName || user?.full_name || 'Farmer Account'}</span>
                <span className="px-2 py-0.5 rounded-full bg-primary/20 text-agri-400 text-[10px] font-semibold uppercase">
                  {user?.role || 'Farmer'}
                </span>
              </h2>
              <div className="flex items-center space-x-4 text-xs text-slate-400">
                <span className="flex items-center space-x-1">
                  <Mail className="w-3.5 h-3.5 text-slate-500" />
                  <span>{user?.email}</span>
                </span>
                <span className="flex items-center space-x-1">
                  <MapPin className="w-3.5 h-3.5 text-slate-500" />
                  <span>{userLoc.village}, {userLoc.taluka}, {userLoc.district}, {userLoc.state} ({userLoc.pincode})</span>
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={() => setShowEditUserLocModal(true)}
            className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs flex items-center space-x-1.5 border border-slate-700 transition shrink-0"
          >
            <Edit2 className="w-3.5 h-3.5 text-agri-400" />
            <span>{t('profile.edit_location')}</span>
          </button>
        </div>

        {/* Structured Indian Agricultural Location Details */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 text-xs">
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="text-slate-500 text-[10px] block uppercase font-bold">{t('profile.location')}</span>
            <span className="font-semibold text-slate-200 block">Village: {userLoc.village} | Taluka: {userLoc.taluka}</span>
            <span className="text-slate-400 block text-[11px]">District: {userLoc.district}, {userLoc.state} ({userLoc.pincode})</span>
          </div>

          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="text-slate-500 text-[10px] block uppercase font-bold">{t('profile.status')}</span>
            <div className="flex items-center space-x-1 text-emerald-400 font-semibold">
              <CheckCircle className="w-3.5 h-3.5" />
              <span>Active Verified Farmer</span>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="text-slate-500 text-[10px] block uppercase font-bold">{t('profile.language')}</span>
            <div className="flex items-center justify-between">
              <span className="text-slate-200 font-semibold">{lang === 'en' ? 'English (EN)' : 'Marathi (मराठी)'}</span>
              <button 
                onClick={() => setLang(lang === 'en' ? 'mr' : 'en')}
                className="text-[10px] text-agri-400 hover:underline font-bold"
              >
                Switch
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Farms List */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-base font-bold text-white">{t('profile.farms')}</h2>
            <p className="text-xs text-slate-400">Manage agricultural land plots and edit individual farm locations</p>
          </div>
          <button
            onClick={() => setShowAddFarmModal(true)}
            className="px-3.5 py-2 rounded-xl bg-primary hover:bg-agri-700 text-white font-bold text-xs flex items-center space-x-1.5 transition shadow"
          >
            <Plus className="w-4 h-4" />
            <span>{t('profile.add_farm')}</span>
          </button>
        </div>

        {farms.length === 0 ? (
          <div className="py-10 text-center text-xs text-slate-500 bg-slate-900/40 rounded-xl border border-slate-800/60 p-4">
            <Sprout className="w-8 h-8 mx-auto text-slate-600 mb-2" />
            <span>{t('profile.no_farms')}</span>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {farms.map((f) => (
              <div key={f.id} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                <div className="flex justify-between items-start">
                  <h3 className="text-sm font-bold text-white flex items-center space-x-1.5">
                    <Home className="w-4 h-4 text-agri-400" />
                    <span>{f.name}</span>
                  </h3>
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => handleOpenEditFarm(f)}
                      className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-agri-400 transition"
                      title="Edit Farm Location"
                    >
                      <Edit2 className="w-3.5 h-3.5" />
                    </button>
                    <span className="px-2 py-0.5 rounded bg-agri-500/10 text-agri-400 text-[10px] font-bold">
                      {f.area_acres} Acres
                    </span>
                  </div>
                </div>
                <p className="text-xs text-slate-400">Primary Crops: <strong className="text-slate-200">{f.crop_types}</strong></p>
                <p className="text-xs text-slate-400">Location: <strong className="text-slate-300">{f.village || 'Kagal'}, {f.taluka || 'Kagal'}, {f.district || 'Kolhapur'}, {f.state || 'Maharashtra'} ({f.pincode || '416216'})</strong></p>
                <div className="flex justify-between items-center text-xs text-slate-500 pt-2 border-t border-slate-800">
                  <span>Irrigation: {f.irrigation_type || 'Drip Irrigation'}</span>
                  <span>PIN: {f.pincode || '416216'}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Edit User Profile Location Modal */}
      {showEditUserLocModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel p-6 rounded-2xl max-w-md w-full space-y-4 border border-slate-700">
            <h3 className="text-lg font-bold text-white">{t('profile.edit_location')}</h3>
            <form onSubmit={handleSaveUserLocation} className="space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.village')}</label>
                  <input
                    type="text"
                    value={userLoc.village}
                    onChange={(e) => setUserLoc({ ...userLoc, village: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.taluka')}</label>
                  <input
                    type="text"
                    value={userLoc.taluka}
                    onChange={(e) => setUserLoc({ ...userLoc, taluka: e.target.value })}
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
                    value={userLoc.district}
                    onChange={(e) => setUserLoc({ ...userLoc, district: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                    required
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.state')}</label>
                  <input
                    type="text"
                    value={userLoc.state}
                    onChange={(e) => setUserLoc({ ...userLoc, state: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.pin')}</label>
                <input
                  type="text"
                  value={userLoc.pincode}
                  onChange={(e) => setUserLoc({ ...userLoc, pincode: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  required
                />
              </div>

              <div className="flex justify-end space-x-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowEditUserLocModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-xs text-slate-300"
                >
                  {t('common.cancel')}
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-primary text-xs font-bold text-white shadow"
                >
                  {t('profile.save_location')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit Farm Location Modal */}
      {showEditFarmLocModal && selectedFarm && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel p-6 rounded-2xl max-w-md w-full space-y-4 border border-slate-700">
            <h3 className="text-lg font-bold text-white">Edit Farm Location & Plot Info</h3>
            <form onSubmit={handleSaveFarmLocation} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.farm_name')}</label>
                <input
                  type="text"
                  value={selectedFarm.name}
                  onChange={(e) => setSelectedFarm({ ...selectedFarm, name: e.target.value })}
                  className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.village')}</label>
                  <input
                    type="text"
                    value={selectedFarm.village || 'Kagal'}
                    onChange={(e) => setSelectedFarm({ ...selectedFarm, village: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.taluka')}</label>
                  <input
                    type="text"
                    value={selectedFarm.taluka || 'Kagal'}
                    onChange={(e) => setSelectedFarm({ ...selectedFarm, taluka: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.district')}</label>
                  <input
                    type="text"
                    value={selectedFarm.district || 'Kolhapur'}
                    onChange={(e) => setSelectedFarm({ ...selectedFarm, district: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.state')}</label>
                  <input
                    type="text"
                    value={selectedFarm.state || 'Maharashtra'}
                    onChange={(e) => setSelectedFarm({ ...selectedFarm, state: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.pin')}</label>
                  <input
                    type="text"
                    value={selectedFarm.pincode || '416216'}
                    onChange={(e) => setSelectedFarm({ ...selectedFarm, pincode: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.area')}</label>
                  <input
                    type="number"
                    step="0.5"
                    value={selectedFarm.area_acres || 2.5}
                    onChange={(e) => setSelectedFarm({ ...selectedFarm, area_acres: parseFloat(e.target.value) || 1 })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowEditFarmLocModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-xs text-slate-300"
                >
                  {t('common.cancel')}
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-primary text-xs font-bold text-white shadow"
                >
                  {t('profile.save_location')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Add Farm Modal */}
      {showAddFarmModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel p-6 rounded-2xl max-w-lg w-full space-y-4 border border-slate-700 max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-bold text-white">Register Farm Plot & Land Info</h3>
            <form onSubmit={handleAddFarm} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.farm_name')}</label>
                <input
                  type="text"
                  value={newFarm.name}
                  onChange={(e) => setNewFarm({ ...newFarm, name: e.target.value })}
                  placeholder="Sunrise Organic Farm"
                  className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.village')}</label>
                  <input
                    type="text"
                    value={newFarm.village}
                    onChange={(e) => setNewFarm({ ...newFarm, village: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.taluka')}</label>
                  <input
                    type="text"
                    value={newFarm.taluka}
                    onChange={(e) => setNewFarm({ ...newFarm, taluka: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.district')}</label>
                  <input
                    type="text"
                    value={newFarm.district}
                    onChange={(e) => setNewFarm({ ...newFarm, district: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.state')}</label>
                  <input
                    type="text"
                    value={newFarm.state}
                    onChange={(e) => setNewFarm({ ...newFarm, state: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.pin')}</label>
                  <input
                    type="text"
                    value={newFarm.pincode}
                    onChange={(e) => setNewFarm({ ...newFarm, pincode: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">{t('profile.area')}</label>
                  <input
                    type="number"
                    step="0.5"
                    value={newFarm.area_acres}
                    onChange={(e) => setNewFarm({ ...newFarm, area_acres: parseFloat(e.target.value) || 1 })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowAddFarmModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-xs text-slate-300"
                >
                  {t('common.cancel')}
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-primary text-xs font-bold text-white shadow"
                >
                  {t('profile.save')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
