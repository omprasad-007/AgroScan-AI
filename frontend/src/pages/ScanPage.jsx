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
    <div className="max-w-4xl mx-auto space-y-6">
      
      {/* Header */}
      <div className="space-y-1.5">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-agro-primary/15 border border-agro-primary/30 flex items-center justify-center text-agro-primary">
            <ScanLine className="w-4 h-4" aria-hidden="true" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-agro-cream tracking-tight">
            {t('scan.title') || 'Scan Plant Leaf'}
          </h1>
          <span className="hidden sm:inline-flex items-center px-2.5 py-0.5 rounded-full bg-agro-primary/15 border border-agro-primary/30 text-[10px] font-extrabold text-agro-primary uppercase tracking-wide">
            Live AI Vision
          </span>
        </div>
        <p className="text-xs sm:text-sm text-agro-muted max-w-2xl leading-relaxed">
          {t('scan.subtitle') || 'Capture or upload a plant photo for instant species identification, disease severity quantification, and organic/chemical remedies.'}
        </p>
      </div>

      {/* 4-Step Simplified Workflow Indicator */}
      <nav aria-label="Scan Workflow Steps" className="agro-panel p-3 rounded-2xl border border-agro-border">
        <ol className="grid grid-cols-2 md:grid-cols-4 gap-2 text-left">
          <li className="flex items-center gap-2.5 p-2 rounded-xl bg-agro-surface/60 border border-agro-border">
            <span className="w-6 h-6 rounded-lg bg-agro-primary text-agro-bg flex items-center justify-center text-xs font-black shrink-0">
              1
            </span>
            <div className="min-w-0 leading-tight">
              <span className="block text-xs font-bold text-agro-cream truncate">Crop Context</span>
              <span className="text-[10px] text-agro-muted truncate block">Auto or select crop</span>
            </div>
          </li>

          <li className="flex items-center gap-2.5 p-2 rounded-xl bg-agro-surface/60 border border-agro-primary/30">
            <span className="w-6 h-6 rounded-lg bg-agro-primary text-agro-bg flex items-center justify-center text-xs font-black shrink-0">
              2
            </span>
            <div className="min-w-0 leading-tight">
              <span className="block text-xs font-bold text-agro-cream truncate">Leaf Photo</span>
              <span className="text-[10px] text-agro-muted truncate block">Camera or upload</span>
            </div>
          </li>

          <li className="flex items-center gap-2.5 p-2 rounded-xl bg-agro-surface/30">
            <span className="w-6 h-6 rounded-lg bg-agro-surface text-agro-muted flex items-center justify-center text-xs font-bold shrink-0">
              3
            </span>
            <div className="min-w-0 leading-tight">
              <span className="block text-xs font-semibold text-agro-muted truncate">AI Analysis</span>
              <span className="text-[10px] text-agro-mutedDark truncate block">Vision consensus</span>
            </div>
          </li>

          <li className="flex items-center gap-2.5 p-2 rounded-xl bg-agro-surface/30">
            <span className="w-6 h-6 rounded-lg bg-agro-surface text-agro-muted flex items-center justify-center text-xs font-bold shrink-0">
              4
            </span>
            <div className="min-w-0 leading-tight">
              <span className="block text-xs font-semibold text-agro-muted truncate">Prescription</span>
              <span className="text-[10px] text-agro-mutedDark truncate block">Remedies & dosage</span>
            </div>
          </li>
        </ol>
      </nav>

      {/* Step 1: Optional Context (Crop & Farm & Weather) */}
      <section className="agro-panel p-5 rounded-2xl border border-agro-border space-y-4">
        <div className="flex items-center justify-between border-b border-agro-border pb-3">
          <div className="flex items-center gap-2">
            <Sprout className="w-4 h-4 text-agro-lime" aria-hidden="true" />
            <h2 className="text-sm font-bold text-agro-cream">Step 1: Crop & Field Context</h2>
          </div>
          {localWeather && (
            <div className="flex items-center gap-1.5 text-[11px] text-agro-muted">
              <CloudSun className="w-3.5 h-3.5 text-agro-amber" aria-hidden="true" />
              <span>{localWeather.location}: <strong>{localWeather.temperature_c}°C</strong></span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="target-crop" className="block text-xs font-bold text-agro-cream mb-1.5">
              Plant / Crop Species <span className="font-normal text-agro-muted">(Optional)</span>
            </label>
            <select
              id="target-crop"
              value={selectedCrop}
              onChange={(e) => setSelectedCrop(e.target.value)}
              className="w-full px-3.5 py-2.5 rounded-xl bg-agro-surface border border-agro-border text-xs font-bold text-agro-cream focus-visible:ring-2 focus-visible:ring-agro-primary focus-visible:border-transparent transition-colors"
            >
              {AVAILABLE_CROPS.map((c) => (
                <option key={c.id} value={c.id} className="bg-agro-card text-agro-cream">
                  {c.name}
                </option>
              ))}
            </select>
            <p className="text-[11px] text-agro-muted mt-1 leading-normal">
              Select your crop for species-tuned pathology or leave as <strong>Auto-Detect</strong>.
            </p>
          </div>

          {farms.length > 0 && (
            <div>
              <label htmlFor="target-farm" className="block text-xs font-bold text-agro-cream mb-1.5">
                Target Farm Plot
              </label>
              <select
                id="target-farm"
                value={selectedFarmId}
                onChange={(e) => setSelectedFarmId(e.target.value)}
                className="w-full px-3.5 py-2.5 rounded-xl bg-agro-surface border border-agro-border text-xs font-semibold text-agro-cream focus-visible:ring-2 focus-visible:ring-agro-primary transition-colors"
              >
                {farms.map((f) => (
                  <option key={f.id} value={f.id} className="bg-agro-card text-agro-cream">
                    {f.name} ({f.village || ''}, {f.district || ''})
                  </option>
                ))}
              </select>
              {selectedFarm && (
                <p className="text-[11px] text-agro-muted mt-1">
                  Location: {selectedFarm.village || ''}, {selectedFarm.district || ''}
                </p>
              )}
            </div>
          )}
        </div>
      </section>

      {/* Error Alert if any */}
      {error && (
        <div className="p-4 rounded-xl bg-agro-terracotta/15 border border-agro-terracotta/35 text-agro-terracotta text-xs flex items-center gap-2.5">
          <AlertCircle className="w-4 h-4 shrink-0" aria-hidden="true" />
          <span className="font-semibold">{error}</span>
        </div>
      )}

      {/* Step 2: Camera or Upload Tabs */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Camera className="w-4 h-4 text-agro-primary" aria-hidden="true" />
            <h2 className="text-sm font-bold text-agro-cream">Step 2: Add Leaf Photograph</h2>
          </div>

          <div
            role="tablist"
            aria-label="Capture Mode"
            className="inline-flex p-1 rounded-xl bg-agro-surface border border-agro-border text-xs font-bold"
          >
            <button
              type="button"
              role="tab"
              aria-selected={activeTab === 'camera'}
              onClick={() => setActiveTab('camera')}
              className={`inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg transition-colors ${
                activeTab === 'camera'
                  ? 'bg-agro-primary text-agro-bg shadow-sm'
                  : 'text-agro-muted hover:text-agro-cream'
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
              className={`inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg transition-colors ${
                activeTab === 'upload'
                  ? 'bg-agro-primary text-agro-bg shadow-sm'
                  : 'text-agro-muted hover:text-agro-cream'
              }`}
            >
              <Upload className="w-3.5 h-3.5" aria-hidden="true" />
              <span>Upload</span>
            </button>
          </div>
        </div>

        {/* Tab 1: Live Camera View */}
        {activeTab === 'camera' && (
          <CameraScanner
            onImageCaptured={handleCameraCaptured}
            onFallbackUpload={() => setActiveTab('upload')}
            isAnalyzing={isAnalyzing}
          />
        )}

        {/* Tab 2: File Upload View */}
        {activeTab === 'upload' && (
          <div className="agro-panel p-6 sm:p-8 rounded-3xl border border-agro-border text-center space-y-5">
            {!previewUrl ? (
              <div
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className="border-2 border-dashed border-agro-border hover:border-agro-primary/50 bg-agro-surface/40 hover:bg-agro-surface/80 rounded-2xl p-8 sm:p-12 transition-all cursor-pointer space-y-4 group"
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  className="hidden"
                  onChange={(e) => handleFileChange(e.target.files?.[0])}
                />
                
                <div className="w-16 h-16 rounded-2xl bg-agro-primary/10 border border-agro-primary/25 text-agro-primary flex items-center justify-center mx-auto group-hover:scale-105 transition-transform">
                  <Upload className="w-8 h-8" aria-hidden="true" />
                </div>

                <div className="space-y-1">
                  <h3 className="text-base font-bold text-agro-cream">
                    Drop your leaf photo here, or <span className="text-agro-primary underline">browse</span>
                  </h3>
                  <p className="text-xs text-agro-muted">
                    Supports JPEG, PNG, or WEBP up to 10MB
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-5">
                <div className="relative max-w-sm mx-auto rounded-2xl overflow-hidden border border-agro-primary/40 shadow-xl bg-agro-bg">
                  <img
                    src={previewUrl}
                    alt="Selected leaf preview"
                    className="w-full h-72 object-cover"
                  />
                  <div className="absolute top-3 right-3 px-3 py-1 rounded-full bg-agro-card/90 backdrop-blur-md border border-agro-primary/40 text-[11px] font-bold text-agro-primary flex items-center gap-1.5 shadow">
                    <CheckCircle2 className="w-3.5 h-3.5" aria-hidden="true" />
                    <span>Photo Selected</span>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
                  <button
                    type="button"
                    onClick={handleReset}
                    className="px-5 py-3 rounded-xl bg-agro-surface hover:bg-agro-hover border border-agro-border text-agro-cream text-xs font-bold flex items-center justify-center gap-2 transition"
                  >
                    <RefreshCw className="w-4 h-4 text-agro-muted" aria-hidden="true" />
                    <span>Choose Another</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => handleUploadAndAnalyze()}
                    disabled={isAnalyzing}
                    className="px-7 py-3 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-agro-bg text-xs font-extrabold flex items-center justify-center gap-2 transition shadow-lg shadow-agro-primary/25 active:scale-[0.98] disabled:opacity-50"
                  >
                    <Sparkles className="w-4 h-4" aria-hidden="true" />
                    <span>{isAnalyzing ? 'Analyzing...' : 'Diagnose Plant Leaf Now'}</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </section>

      {/* Photo Quality Guidelines */}
      <section className="agro-panel p-5 rounded-2xl border border-agro-border">
        <h3 className="text-xs font-bold text-agro-cream mb-3 flex items-center gap-2">
          <SunMedium className="w-4 h-4 text-agro-lime" aria-hidden="true" />
          <span>Foliage Photography Quality Standard for 98%+ AI Accuracy</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-left">
          <div className="p-3 rounded-xl bg-agro-surface/60 border border-agro-border">
            <span className="block text-xs font-bold text-agro-cream mb-0.5">Natural Daylight</span>
            <span className="text-[11px] text-agro-muted">Even daylight without hard reflective flash or shadow glare.</span>
          </div>
          <div className="p-3 rounded-xl bg-agro-surface/60 border border-agro-border">
            <span className="block text-xs font-bold text-agro-cream mb-0.5">Macro Venation Focus</span>
            <span className="text-[11px] text-agro-muted">Keep the affected spots and leaf vein structure sharply focused.</span>
          </div>
          <div className="p-3 rounded-xl bg-agro-surface/60 border border-agro-border">
            <span className="block text-xs font-bold text-agro-cream mb-0.5">Frame Single Leaf</span>
            <span className="text-[11px] text-agro-muted">Fill at least 40% of the frame with the affected leaf blade.</span>
          </div>
        </div>
      </section>

    </div>
  );
};
