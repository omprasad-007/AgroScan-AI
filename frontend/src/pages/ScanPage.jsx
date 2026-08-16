import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Upload, Sparkles, AlertCircle, CheckCircle2, Camera } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { CameraScanner } from '../components/camera/CameraScanner';

export const ScanPage = () => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('camera'); // 'camera' or 'upload'

  const sampleLeaves = [
    { name: 'Tomato Late Blight', crop: 'Tomato', url: 'https://images.unsplash.com/photo-1592417817098-8f3d6eb16431?w=400&q=80' },
    { name: 'Potato Late Blight', crop: 'Potato', url: 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=400&q=80' },
    { name: 'Healthy Leaf', crop: 'General', url: 'https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=400&q=80' }
  ];

  const handleFileChange = (file) => {
    if (!file) return;
    if (!['image/jpeg', 'image/png', 'image/webp', 'image/jpg'].includes(file.type)) {
      setError('Please upload a valid image file (JPEG, PNG, or WEBP).');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      setError('Image file size must be less than 10MB.');
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

  const handleSampleSelect = async (sample) => {
    setError('');
    try {
      const response = await fetch(sample.url);
      const blob = await response.blob();
      const file = new File([blob], `${sample.crop.toLowerCase()}_sample.jpg`, { type: 'image/jpeg' });
      setSelectedFile(file);
      setPreviewUrl(sample.url);
    } catch (err) {
      setError('Failed to load sample image.');
    }
  };

  const handleUploadAndAnalyze = (overrideFile = null) => {
    const targetFile = overrideFile || selectedFile;
    if (!targetFile) {
      setError('Please select or capture a leaf photo first.');
      return;
    }
    setIsAnalyzing(true);
    // Navigate to animated Analysis Loading page
    navigate('/analysis', { state: { imageFile: targetFile } });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center space-x-2">
          <span>{t('scan.title')}</span>
          <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-[10px] font-bold text-emerald-400 uppercase tracking-wide">
            Live AI Scanner
          </span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Open your device camera or upload a leaf photo for instant plant identification, disease diagnosis, and complete cultivation advice.
        </p>
      </div>

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
          <span>1. Open Camera</span>
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
          <span>2. Upload File</span>
        </button>
      </div>

      {/* Tab 1: Live Browser Camera Scanner (Primary Feature) */}
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
                alt="Leaf Preview" 
                className="max-h-64 mx-auto rounded-xl shadow-lg border border-slate-700 object-cover" 
              />
              <div className="flex items-center justify-center space-x-3 text-xs text-slate-300">
                <CheckCircle2 className="w-4 h-4 text-agri-400" />
                <span>Image loaded successfully ({selectedFile?.name || 'Sample Leaf'})</span>
              </div>
              <button
                onClick={() => { setSelectedFile(null); setPreviewUrl(null); }}
                className="text-xs text-slate-400 hover:text-red-400 underline"
              >
                Choose different image
              </button>
            </div>
          ) : (
            <div className="space-y-4 py-6">
              <div className="w-16 h-16 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mx-auto border border-primary/20 shadow-inner">
                <Upload className="w-8 h-8" />
              </div>
              <div>
                <p className="text-sm font-semibold text-slate-200">{t('scan.drag_drop')}</p>
                <p className="text-xs text-slate-500 mt-1">{t('scan.supported_formats')}</p>
              </div>
              <button
                onClick={() => fileInputRef.current?.click()}
                className="px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-slate-200 border border-slate-700 transition"
              >
                Browse Local Files
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

      {/* Sample Leaf Selector for Demo Mode */}
      <div className="glass-panel p-6 rounded-2xl space-y-3">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
          {t('scan.sample_picker')}
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {sampleLeaves.map((sample, idx) => (
            <button
              key={idx}
              onClick={() => handleSampleSelect(sample)}
              className="flex items-center space-x-3 p-3 rounded-xl bg-slate-900/60 hover:bg-slate-800 border border-slate-800 text-left transition group"
            >
              <img src={sample.url} alt={sample.name} className="w-12 h-12 rounded-lg object-cover border border-slate-700 group-hover:scale-105 transition" />
              <div>
                <span className="block text-xs font-bold text-slate-200">{sample.name}</span>
                <span className="text-[10px] text-agri-400">{sample.crop}</span>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Action Button for File Upload Mode */}
      {activeTab === 'upload' && (
        <div className="flex justify-end">
          <button
            onClick={() => handleUploadAndAnalyze()}
            disabled={!selectedFile || isAnalyzing}
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-primary hover:bg-agri-700 text-on-primary font-extrabold text-sm transition shadow-lg shadow-primary/25 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Sparkles className="w-4 h-4" />
            <span>{isAnalyzing ? t('scan.analyzing') : t('scan.btn_analyze')}</span>
          </button>
        </div>
      )}

    </div>
  );
};

