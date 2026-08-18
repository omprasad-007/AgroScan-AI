import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Sparkles, AlertCircle, CheckCircle2, Camera, RefreshCw, Home, MapPin } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { CameraScanner } from '../components/camera/CameraScanner';
import api from '../services/api';

export const ScanPage = () => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('camera'); // 'camera' or 'upload'

  const [farms, setFarms] = useState([]);
  const [selectedFarmId, setSelectedFarmId] = useState('');

  useEffect(() => {
    api.get('/farms')
      .then(res => {
        const list = Array.isArray(res.data) ? res.data : [];
        setFarms(list);
        if (list.length > 0) setSelectedFarmId(list[0].id);
      })
      .catch(() => setFarms([]));
  }, []);

  const selectedFarm = farms.find(f => f.id === selectedFarmId);

  const handleFileChange = (file) => {
    if (!file) return;
    if (!['image/jpeg', 'image/png', 'image/webp', 'image/jpg'].includes(file.type)) {
      setError(t('scan.err_invalid_type') || 'Please upload a valid image file (JPEG, PNG, or WEBP).');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError(t('scan.err_max_size') || 'Image file size must be less than 10MB.');
      return;
    }
    setError('');
    setSelectedFile(file);
    setPreviewUrl(URL.createObjectURL(file));
  };

  const handleCameraCaptured = (file, dataUrl) => {
    setSelectedFile(file);
    setPreviewUrl(dataUrl);
    handleUploadAndAnalyze(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileChange(e.dataTransfer.files[0]);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setError('');
  };

  const handleUploadAndAnalyze = (overrideFile = null) => {
    const targetFile = overrideFile || selectedFile;
    if (!targetFile) {
      setError(t('scan.err_no_photo') || 'Please select or capture a leaf photo first.');
      return;
    }
    setIsAnalyzing(true);
    // Navigate to animated Analysis Loading page
    navigate('/analysis', { state: { imageFile: targetFile, farmId: selectedFarmId } });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center space-x-2">
          <span>{t('scan.title') || 'Scan Plant'}</span>
          <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-[10px] font-bold text-emerald-400 uppercase tracking-wide">
            {t('scan.live_scanner') || 'Live AI Scanner'}
          </span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          {t('scan.subtitle') || 'Open your device camera or upload a plant photo for instant identification and disease analysis.'}
        </p>
      </div>

      {/* Target Farm & Location Selector */}
      {farms.length > 0 && (
        <div className="glass-panel p-4 rounded-2xl space-y-2 border border-slate-800">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <label className="text-xs font-bold text-slate-200 flex items-center space-x-2">
              <Home className="w-4 h-4 text-agri-400" />
              <span>{t('scan.select_farm') || 'Select Target Farm / Location'}</span>
            </label>
            <select
              value={selectedFarmId}
              onChange={(e) => setSelectedFarmId(e.target.value)}
              className="px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-semibold text-white focus:outline-none focus:border-agri-500"
            >
              {farms.map((f) => (
                <option key={f.id} value={f.id}>{f.name} ({f.village || ''}, {f.district || ''})</option>
              ))}
            </select>
          </div>
          {selectedFarm && (
            <div className="flex items-center space-x-2 text-[11px] text-slate-400 pt-1 border-t border-slate-800/60">
              <MapPin className="w-3.5 h-3.5 text-slate-500 shrink-0" />
              <span>{t('profile.location') || 'Location'}: <strong>{selectedFarm.village || ''}, {selectedFarm.taluka || ''}, {selectedFarm.district || ''}, {selectedFarm.state || ''} {selectedFarm.pincode ? `(PIN: ${selectedFarm.pincode})` : ''}</strong></span>
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center space-x-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Mode Switcher Tabs */}
      <div className="flex p-1.5 rounded-xl bg-slate-900 border border-slate-800 max-w-xs mx-auto text-xs font-bold">
        <button
          type="button"
          onClick={() => setActiveTab('camera')}
          className={`flex-1 py-2 rounded-lg flex items-center justify-center space-x-2 transition ${
            activeTab === 'camera'
              ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Camera className="w-3.5 h-3.5" />
          <span>{t('scan.tab_camera') || '1. Open Camera'}</span>
        </button>

        <button
          type="button"
          onClick={() => setActiveTab('upload')}
          className={`flex-1 py-2 rounded-lg flex items-center justify-center space-x-2 transition ${
            activeTab === 'upload'
              ? 'bg-emerald-500 text-slate-950 shadow-md shadow-emerald-500/20'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          <Upload className="w-3.5 h-3.5" />
          <span>{t('scan.tab_upload') || '2. Upload File'}</span>
        </button>
      </div>

      {/* Tab 1: Live Browser Camera Scanner */}
      {activeTab === 'camera' && (
        <CameraScanner
          onImageCaptured={handleCameraCaptured}
          onFallbackUpload={() => setActiveTab('upload')}
          isAnalyzing={isAnalyzing}
        />
      )}

      {/* Tab 2: Secondary Device File Upload */}
      {activeTab === 'upload' && (
        <div 
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleDrop}
          className={`glass-panel p-8 rounded-2xl text-center border-2 border-dashed transition-all duration-300 ${
            previewUrl ? 'border-primary/50 bg-primary/5' : 'border-slate-800 hover:border-slate-700'
          }`}
        >
          {previewUrl ? (
            <div className="space-y-4">
              <img 
                src={previewUrl} 
                alt="Plant Preview" 
                className="max-h-64 mx-auto rounded-xl shadow-lg border border-slate-700 object-cover" 
              />
              <div className="flex items-center justify-center space-x-3 text-xs text-slate-300">
                <CheckCircle2 className="w-4 h-4 text-agri-400" />
                <span>{t('scan.img_loaded') || 'Image loaded successfully'} ({selectedFile?.name})</span>
              </div>
              <div className="flex justify-center space-x-3 pt-2">
                <button
                  type="button"
                  onClick={handleReset}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-300 border border-slate-700 flex items-center space-x-1.5 transition"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>{t('scan.btn_retake') || 'Retake / Select Different'}</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="space-y-4 py-6">
              <div className="w-16 h-16 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mx-auto border border-primary/20 shadow-inner">
                <Upload className="w-8 h-8" />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-200">{t('scan.drag_drop') || 'Drag and drop your plant photo here'}</p>
                <p className="text-xs text-slate-500 mt-1">{t('scan.supported_formats') || 'Supports JPEG, PNG, or WEBP (Max 10MB)'}</p>
              </div>
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition"
              >
                {t('scan.btn_browse') || 'Browse Local Files'}
              </button>
            </div>
          )}

          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={(e) => e.target.files?.[0] && handleFileChange(e.target.files[0])}
            accept="image/jpeg,image/png,image/webp" 
            className="hidden" 
          />
        </div>
      )}

      {/* Action Button for File Upload Mode */}
      {activeTab === 'upload' && selectedFile && (
        <div className="flex justify-end">
          <button
            type="button"
            onClick={() => handleUploadAndAnalyze()}
            disabled={!selectedFile || isAnalyzing}
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-primary hover:bg-agri-700 text-on-primary font-extrabold text-sm transition shadow-lg shadow-primary/25 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Sparkles className="w-4 h-4" />
            <span>{isAnalyzing ? (t('scan.analyzing') || 'Analyzing...') : (t('scan.btn_analyze') || 'Analyze Plant')}</span>
          </button>
        </div>
      )}

    </div>
  );
};
