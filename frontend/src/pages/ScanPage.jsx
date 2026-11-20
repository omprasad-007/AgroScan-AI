import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Upload, 
  Sparkles, 
  AlertCircle, 
  CheckCircle2, 
  Camera, 
  RefreshCw, 
  Home, 
  MapPin, 
  Sprout, 
  ScanLine, 
  SunMedium, 
  Maximize2,
  FileText,
  CloudSun
} from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import { useAuth } from '../context/AuthContext';
import { CameraScanner } from '../components/camera/CameraScanner';
import { detectLocalWeather } from '../services/weather';
import api from '../services/api';

const AVAILABLE_CROPS = [
  { id: "auto", name: "Auto-Detect Plant Species (Multi-Crop Vision)" },
  { id: "mango", name: "Mango (आम / आंबा)" },
  { id: "cotton", name: "Cotton (कपास / कापूस)" },
  { id: "sugarcane", name: "Sugarcane (गन्ना / ऊस)" },
  { id: "rice", name: "Rice / Paddy (धान / भात)" },
  { id: "wheat", name: "Wheat (गेहूं / गहू)" },
  { id: "soybean", name: "Soybean (सोयाबीन)" },
  { id: "chilli", name: "Chilli / Pepper (मिर्च / मिरची)" },
  { id: "tomato", name: "Tomato (टमाटर / टोमॅटो)" },
  { id: "potato", name: "Potato (आलू / बटाटा)" },
  { id: "grapes", name: "Grapes (अंगूर / द्राक्षे)" },
  { id: "corn", name: "Corn / Maize (मक्का / मका)" },
  { id: "onion", name: "Onion (प्याज / कांदा)" },
  { id: "pomegranate", name: "Pomegranate (अनार / डाळिंब)" },
  { id: "banana", name: "Banana (केला / केळी)" },
  { id: "citrus", name: "Citrus / Lemon (नींबू / लिंबू)" },
  { id: "rose", name: "Rose (गुलाब)" },
  { id: "papaya", name: "Papaya (पपीता / पपई)" },
  { id: "other", name: "Other Field Plant / Horticulture" }
];

export const ScanPage = () => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const fileInputRef = useRef(null);

  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [error, setError] = useState('');
  const [activeTab, setActiveTab] = useState('camera'); // 'camera' or 'upload'
  const [selectedCrop, setSelectedCrop] = useState('auto');
  const [localWeather, setLocalWeather] = useState(null);

  const [farms, setFarms] = useState([]);
  const [selectedFarmId, setSelectedFarmId] = useState('');

  useEffect(() => () => {
    if (previewUrl?.startsWith('blob:')) URL.revokeObjectURL(previewUrl);
  }, [previewUrl]);

  useEffect(() => {
    detectLocalWeather()
      .then(w => { if (w) setLocalWeather(w); })
      .catch(() => {});
  }, []);

  useEffect(() => {
    api.get('/health').catch(() => {});
    if (!isAuthenticated) {
      setFarms([]);
      setSelectedFarmId('');
      return;
    }

    api.get('/farms')
      .then((res) => {
        const list = Array.isArray(res.data) ? res.data : [];
        setFarms(list);
        if (list.length > 0) setSelectedFarmId(list[0].id);
      })
      .catch(() => setFarms([]));
  }, [isAuthenticated]);

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
    navigate('/analysis', {
      state: {
        imageFile: targetFile,
        farmId: selectedFarmId,
        targetCrop: selectedCrop,
        weather: localWeather
      }
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-28">
      
      {/* Header */}
      <div className="space-y-1.5">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-emerald-500/10 dark:bg-emerald-500/20 border border-emerald-500/30 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
            <ScanLine className="w-4 h-4" aria-hidden="true" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">
            {t('scan.title') || 'Scan Plant Leaf'}
          </h1>
          <span className="hidden sm:inline-flex items-center px-2.5 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-[10px] font-extrabold text-emerald-700 dark:text-emerald-300 uppercase tracking-wide">
            Live AI Vision
          </span>
        </div>
        <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-2xl leading-relaxed">
          {t('scan.subtitle') || 'Capture or upload a plant photo for instant species identification, disease severity quantification, and organic/chemical remedies.'}
        </p>
      </div>

      {/* Sleek Step Progress Indicator */}
      <div className="px-4 py-3 rounded-2xl bg-white dark:bg-slate-900/80 border border-slate-200 dark:border-slate-800 shadow-sm">
        <div className="flex items-center justify-between text-xs font-semibold">
          <div className="flex items-center gap-2 text-emerald-600 dark:text-emerald-400 font-bold">
            <span className="w-5 h-5 rounded-full bg-emerald-500 text-white flex items-center justify-center text-[10px] font-black shadow-sm">1</span>
            <span>Capture / Upload</span>
          </div>
          <div className="h-0.5 flex-1 mx-3 sm:mx-6 bg-slate-200 dark:bg-slate-800"></div>
          <div className="flex items-center gap-2 text-slate-400 dark:text-slate-500">
            <span className="w-5 h-5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 flex items-center justify-center text-[10px] font-bold">2</span>
            <span>AI Pathology Analysis</span>
          </div>
          <div className="h-0.5 flex-1 mx-3 sm:mx-6 bg-slate-200 dark:bg-slate-800"></div>
          <div className="flex items-center gap-2 text-slate-400 dark:text-slate-500">
            <span className="w-5 h-5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 flex items-center justify-center text-[10px] font-bold">3</span>
            <span>Prescription & Remedies</span>
          </div>
        </div>
      </div>

      {/* Primary Action Section: Camera & Upload Hero Card */}
      <section className="agro-panel p-5 sm:p-7 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-xl space-y-6">
        
        {/* Context Controls: Crop Species & Field Context */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 pb-4 border-b border-slate-100 dark:border-slate-800/80">
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2 min-w-0">
              <Sprout className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" aria-hidden="true" />
              <label htmlFor="target-crop" className="text-xs font-bold text-slate-700 dark:text-slate-200 whitespace-nowrap">
                Crop Species:
              </label>
              <select
                id="target-crop"
                value={selectedCrop}
                onChange={(e) => setSelectedCrop(e.target.value)}
                className="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-semibold text-slate-900 dark:text-slate-100 focus-visible:ring-2 focus-visible:ring-emerald-500 cursor-pointer"
              >
                {AVAILABLE_CROPS.map((c) => (
                  <option key={c.id} value={c.id} className="bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100">
                    {c.name}
                  </option>
                ))}
              </select>
            </div>

            {farms.length > 0 && (
              <div className="flex items-center gap-2">
                <label htmlFor="target-farm" className="text-xs font-bold text-slate-700 dark:text-slate-200 whitespace-nowrap">
                  Farm Plot:
                </label>
                <select
                  id="target-farm"
                  value={selectedFarmId}
                  onChange={(e) => setSelectedFarmId(e.target.value)}
                  className="px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-semibold text-slate-900 dark:text-slate-100 focus-visible:ring-2 focus-visible:ring-emerald-500 cursor-pointer"
                >
                  {farms.map((f) => (
                    <option key={f.id} value={f.id} className="bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100">
                      {f.name}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          {/* Mode Switcher Tabs */}
          <div
            role="tablist"
            aria-label="Capture Mode"
            className="inline-flex p-1 rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-bold shrink-0 self-start sm:self-auto"
          >
            <button
              type="button"
              role="tab"
              aria-selected={activeTab === 'camera'}
              onClick={() => setActiveTab('camera')}
              className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-lg transition-all ${
                activeTab === 'camera'
                  ? 'bg-emerald-600 text-white shadow font-extrabold'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <Camera className="w-3.5 h-3.5" aria-hidden="true" />
              <span>Camera</span>
            </button>

            <button
              type="button"
              role="tab"
              aria-selected={activeTab === 'upload'}
              onClick={() => setActiveTab('upload')}
              className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-lg transition-all ${
                activeTab === 'upload'
                  ? 'bg-emerald-600 text-white shadow font-extrabold'
                  : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
              }`}
            >
              <Upload className="w-3.5 h-3.5" aria-hidden="true" />
              <span>Upload Photo</span>
            </button>
          </div>
        </div>

        {/* Local Weather Status Pill (if available) */}
        {localWeather && (
          <div className="flex items-center justify-between px-3.5 py-2 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-800 dark:text-amber-300">
            <div className="flex items-center gap-2">
              <CloudSun className="w-4 h-4 text-amber-500" aria-hidden="true" />
              <span className="font-semibold">Local Agro-Climate: {localWeather.location}</span>
            </div>
            <div className="flex items-center gap-3 font-medium">
              <span>{localWeather.temperature_c}°C</span>
              <span>•</span>
              <span>{localWeather.humidity_percent}% Humidity</span>
            </div>
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-800 text-rose-700 dark:text-rose-300 text-xs flex items-center gap-2.5">
            <AlertCircle className="w-4 h-4 shrink-0" aria-hidden="true" />
            <span className="font-semibold">{error}</span>
          </div>
        )}

        {/* Active Tab 1: Live Camera View */}
        {activeTab === 'camera' && (
          <CameraScanner
            onImageCaptured={handleCameraCaptured}
            onFallbackUpload={() => setActiveTab('upload')}
            isAnalyzing={isAnalyzing}
          />
        )}

        {/* Active Tab 2: File Upload Dropzone */}
        {activeTab === 'upload' && (
          <div className="text-center space-y-5">
            {!previewUrl ? (
              <div
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-slate-300 dark:border-slate-700 hover:border-emerald-500 dark:hover:border-emerald-400 bg-slate-50/60 dark:bg-slate-800/40 hover:bg-emerald-50/20 dark:hover:bg-slate-800/70 rounded-3xl p-8 sm:p-14 transition-all cursor-pointer space-y-4 group shadow-inner"
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  className="hidden"
                  onChange={(e) => handleFileChange(e.target.files?.[0])}
                />
                
                <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/25 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mx-auto group-hover:scale-105 transition-transform shadow-sm">
                  <Upload className="w-8 h-8" aria-hidden="true" />
                </div>

                <div className="space-y-1.5">
                  <h3 className="text-base sm:text-lg font-bold text-slate-900 dark:text-white">
                    Drop your leaf photo here, or <span className="text-emerald-600 dark:text-emerald-400 underline underline-offset-2">browse files</span>
                  </h3>
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Supports high-resolution JPEG, PNG, or WEBP up to 10MB
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="relative max-w-sm mx-auto rounded-3xl overflow-hidden border border-emerald-500/40 shadow-2xl bg-slate-100 dark:bg-slate-900">
                  <img
                    src={previewUrl}
                    alt="Selected leaf preview"
                    className="w-full h-80 object-cover"
                  />
                  <div className="absolute top-3 right-3 px-3 py-1 rounded-full bg-white/90 dark:bg-slate-900/90 backdrop-blur-md border border-emerald-500/40 text-[11px] font-extrabold text-emerald-700 dark:text-emerald-400 flex items-center gap-1.5 shadow">
                    <CheckCircle2 className="w-3.5 h-3.5" aria-hidden="true" />
                    <span>Photo Ready</span>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row gap-3.5 justify-center pt-2">
                  <button
                    type="button"
                    onClick={handleReset}
                    className="px-6 py-3.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-100 text-xs font-bold flex items-center justify-center gap-2 transition"
                  >
                    <RefreshCw className="w-4 h-4 text-slate-500 dark:text-slate-400" aria-hidden="true" />
                    <span>Choose Another Photo</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => handleUploadAndAnalyze()}
                    disabled={isAnalyzing}
                    className="px-8 py-3.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-black flex items-center justify-center gap-2 transition shadow-xl shadow-emerald-600/30 active:scale-[0.98] disabled:opacity-50"
                  >
                    <Sparkles className="w-4 h-4" aria-hidden="true" />
                    <span>{isAnalyzing ? 'Analyzing Plant with AI...' : 'Diagnose Plant Leaf Now'}</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </section>

      {/* Photo Quality Guidelines (3 High-Contrast Cards) */}
      <section className="agro-panel p-5 sm:p-6 rounded-3xl border border-slate-200 dark:border-slate-800 shadow-sm">
        <h3 className="text-xs font-bold text-slate-900 dark:text-white mb-3.5 flex items-center gap-2">
          <SunMedium className="w-4 h-4 text-emerald-600 dark:text-emerald-400" aria-hidden="true" />
          <span>Foliage Photography Quality Standard for 98%+ AI Accuracy</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 text-left">
          <div className="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
            <span className="block text-xs font-bold text-slate-900 dark:text-white mb-1">Natural Daylight</span>
            <span className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">Even daylight without hard reflective flash or shadow glare.</span>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
            <span className="block text-xs font-bold text-slate-900 dark:text-white mb-1">Macro Venation Focus</span>
            <span className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">Keep the affected spots and leaf vein structure sharply focused.</span>
          </div>
          <div className="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
            <span className="block text-xs font-bold text-slate-900 dark:text-white mb-1">Frame Single Leaf</span>
            <span className="text-[11px] text-slate-500 dark:text-slate-400 leading-relaxed">Fill at least 40% of the frame with the affected leaf blade.</span>
          </div>
        </div>
      </section>

    </div>
  );
};
