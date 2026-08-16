import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext';
import { User, Mail, MapPin, Plus, LogOut, CheckCircle, Sprout, Home } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const ProfilePage = () => {
  const { user, logout } = useAuth();
  const { lang, setLang, t } = useLanguage();
  const navigate = useNavigate();

  const [farms, setFarms] = useState([]);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newFarm, setNewFarm] = useState({
    name: '',
    state: 'Maharashtra',
    district: 'Kolhapur',
    taluka: 'Karvir',
    village: '',
    pin_code: '',
    crop_types: 'Tomato',
    area_acres: 2.0,
    irrigation_type: 'Drip Irrigation'
  });

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleAddFarm = (e) => {
    e.preventDefault();
    if (!newFarm.name.trim()) return;
    setFarms(prev => [...prev, { id: `farm_${Date.now()}`, ...newFarm }]);
    setShowAddModal(false);
    setNewFarm({
      name: '',
      state: 'Maharashtra',
      district: 'Kolhapur',
      taluka: 'Karvir',
      village: '',
      pin_code: '',
      crop_types: 'Tomato',
      area_acres: 2.0,
      irrigation_type: 'Drip Irrigation'
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white">{t('profile.title')}</h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Farmer Profile & Registered Land Holdings
          </p>
        </div>
        <button
          onClick={handleLogout}
          className="px-4 py-2 rounded-xl bg-red-500/10 hover:bg-red-500/20 text-red-400 text-xs font-bold border border-red-500/30 flex items-center space-x-2 transition"
        >
          <LogOut className="w-4 h-4" />
          <span>Logout</span>
        </button>
      </div>

      {/* User Info Card */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
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
                <span>Karvir, Kolhapur, Maharashtra</span>
              </span>
            </div>
          </div>
        </div>

        {/* Indian Agricultural Location Details */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 text-xs">
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="text-slate-500 text-[10px] block uppercase font-bold">Agricultural Location</span>
            <span className="font-semibold text-slate-200 block">Taluka: Karvir | District: Kolhapur</span>
          </div>

          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="text-slate-500 text-[10px] block uppercase font-bold">Account Status</span>
            <div className="flex items-center space-x-1 text-emerald-400 font-semibold">
              <CheckCircle className="w-3.5 h-3.5" />
              <span>Active Verified Farmer</span>
            </div>
          </div>

          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 space-y-1">
            <span className="text-slate-500 text-[10px] block uppercase font-bold">Preferred Language</span>
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
            <h2 className="text-base font-bold text-white">Registered Farm Holdings</h2>
            <p className="text-xs text-slate-400">Manage agricultural plots and crop sowing details</p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="px-3.5 py-2 rounded-xl bg-primary hover:bg-agri-700 text-white font-bold text-xs flex items-center space-x-1.5 transition shadow"
          >
            <Plus className="w-4 h-4" />
            <span>Add Farm</span>
          </button>
        </div>

        {farms.length === 0 ? (
          <div className="py-10 text-center text-xs text-slate-500 bg-slate-900/40 rounded-xl border border-slate-800/60 p-4">
            <Sprout className="w-8 h-8 mx-auto text-slate-600 mb-2" />
            <span>No farms registered yet. Click <strong>"Add Farm"</strong> to register your land plot.</span>
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
                  <span className="px-2 py-0.5 rounded bg-agri-500/10 text-agri-400 text-[10px] font-bold">
                    {f.area_acres} Acres
                  </span>
                </div>
                <p className="text-xs text-slate-400">Primary Crops: <strong className="text-slate-200">{f.crop_types}</strong></p>
                <p className="text-xs text-slate-400">Location: <strong className="text-slate-300">{f.village || 'Village'}, {f.taluka}, {f.district}, {f.state}</strong></p>
                <div className="flex justify-between items-center text-xs text-slate-500 pt-2 border-t border-slate-800">
                  <span>Irrigation: {f.irrigation_type}</span>
                  <span>PIN: {f.pin_code || '416001'}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add Farm Modal with Indian Location System */}
      {showAddModal && (
        <div className="fixed inset-0 z-50 bg-slate-950/80 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel p-6 rounded-2xl max-w-lg w-full space-y-4 border border-slate-700 max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-bold text-white">Register Farm Plot & Land Info</h3>
            <form onSubmit={handleAddFarm} className="space-y-3">
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Farm Name</label>
                <input
                  type="text"
                  value={newFarm.name}
                  onChange={(e) => setNewFarm({ ...newFarm, name: e.target.value })}
                  placeholder="Green Acres Organic Farm"
                  className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  required
                />
              </div>

              {/* Indian Agricultural Location Grid */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">State</label>
                  <select
                    value={newFarm.state}
                    onChange={(e) => setNewFarm({ ...newFarm, state: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  >
                    <option value="Maharashtra">Maharashtra</option>
                    <option value="Karnataka">Karnataka</option>
                    <option value="Gujarat">Gujarat</option>
                    <option value="Madhya Pradesh">Madhya Pradesh</option>
                    <option value="Punjab">Punjab</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">District</label>
                  <input
                    type="text"
                    value={newFarm.district}
                    onChange={(e) => setNewFarm({ ...newFarm, district: e.target.value })}
                    placeholder="Kolhapur / Pune"
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Taluka / Tehsil</label>
                  <input
                    type="text"
                    value={newFarm.taluka}
                    onChange={(e) => setNewFarm({ ...newFarm, taluka: e.target.value })}
                    placeholder="Karvir / Haveli"
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Village</label>
                  <input
                    type="text"
                    value={newFarm.village}
                    onChange={(e) => setNewFarm({ ...newFarm, village: e.target.value })}
                    placeholder="Vadgaon / Shirol"
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">PIN Code</label>
                  <input
                    type="text"
                    value={newFarm.pin_code}
                    onChange={(e) => setNewFarm({ ...newFarm, pin_code: e.target.value })}
                    placeholder="416001"
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Farm Area (Acres)</label>
                  <input
                    type="number"
                    step="0.5"
                    value={newFarm.area_acres}
                    onChange={(e) => setNewFarm({ ...newFarm, area_acres: parseFloat(e.target.value) || 1 })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Primary Crops</label>
                  <input
                    type="text"
                    value={newFarm.crop_types}
                    onChange={(e) => setNewFarm({ ...newFarm, crop_types: e.target.value })}
                    placeholder="Tomato, Potato, Sugarcane"
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-300 mb-1">Irrigation Type</label>
                  <select
                    value={newFarm.irrigation_type}
                    onChange={(e) => setNewFarm({ ...newFarm, irrigation_type: e.target.value })}
                    className="w-full px-3 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs text-white"
                  >
                    <option value="Drip Irrigation">Drip Irrigation</option>
                    <option value="Sprinkler System">Sprinkler System</option>
                    <option value="Canal / Flood">Canal / Flood</option>
                    <option value="Rainfed">Rainfed</option>
                  </select>
                </div>
              </div>

              <div className="flex justify-end space-x-2 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setShowAddModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 text-xs text-slate-300"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 rounded-xl bg-primary text-xs font-bold text-white shadow"
                >
                  Save Farm Plot
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
};
