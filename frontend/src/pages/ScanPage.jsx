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
          <div className="w-8 h-8 rounded-lg bg-agro-primary/10 border border-agro-primary/30 flex items-center justify-center text-agro-primary">
            <ScanLine className="w-4 h-4" aria-hidden="true" />
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-agro-cream tracking-tight font-heading">
            {t('scan.title') || 'Scan Plant Leaf'}
          </h1>
          <span className="hidden sm:inline-flex items-center px-2.5 py-0.5 rounded-full bg-agro-highlight/15 border border-agro-highlight/30 text-[10px] font-extrabold text-agro-highlight uppercase tracking-wide">
            Live AI Vision
          </span>
        </div>
        <p className="text-xs sm:text-sm text-agro-muted max-w-2xl leading-relaxed">
          {t('scan.subtitle') || 'Capture or upload a plant photo for instant species identification, disease severity quantification, and organic/chemical remedies.'}
        </p>
      </div>

      {/* Sleek Step Progress Indicator */}
      <div className="px-4 py-3 rounded-2xl bg-agro-card border border-agro-border shadow-sm">
        <div className="flex items-center justify-between text-xs font-semibold">
          <div className="flex items-center gap-2 text-agro-primary font-bold">
            <span className="w-5 h-5 rounded-full bg-agro-primary text-white flex items-center justify-center text-[10px] font-black shadow-sm">1</span>
            <span>Capture / Upload</span>
          </div>
          <div className="h-0.5 flex-1 mx-3 sm:mx-6 bg-agro-border"></div>
          <div className="flex items-center gap-2 text-agro-muted">
            <span className="w-5 h-5 rounded-full bg-agro-surface text-agro-muted flex items-center justify-center text-[10px] font-bold">2</span>
            <span>AI Pathology Analysis</span>
          </div>
          <div className="h-0.5 flex-1 mx-3 sm:mx-6 bg-agro-border"></div>
          <div className="flex items-center gap-2 text-agro-muted">
            <span className="w-5 h-5 rounded-full bg-agro-surface text-agro-muted flex items-center justify-center text-[10px] font-bold">3</span>
            <span>Prescription & Remedies</span>
          </div>
        </div>
      </div>

      {/* Primary Action Section: Camera & Upload Hero Card */}
      <section className="agro-panel bg-agro-card p-5 sm:p-7 rounded-3xl border border-agro-border shadow-xl space-y-6">
        
        {/* Context Controls: Crop Species & Field Context */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 pb-4 border-b border-agro-border">
          <div className="flex flex-wrap items-center gap-3">
            <div className="flex items-center gap-2 min-w-0">
              <Sprout className="w-4 h-4 text-agro-primary shrink-0" aria-hidden="true" />
              <label htmlFor="target-crop" className="text-xs font-bold text-agro-cream whitespace-nowrap">
                Crop Species:
              </label>
              <select
                id="target-crop"
                value={selectedCrop}
                onChange={(e) => setSelectedCrop(e.target.value)}
                className="px-3 py-1.5 rounded-xl bg-agro-surface border border-agro-border text-xs font-semibold text-agro-cream focus-visible:ring-2 focus-visible:ring-agro-primary cursor-pointer"
              >
                {AVAILABLE_CROPS.map((c) => (
                  <option key={c.id} value={c.id} className="bg-agro-card text-agro-cream">
                    {c.name}
                  </option>
                ))}
              </select>
            </div>

            {farms.length > 0 && (
              <div className="flex items-center gap-2">
                <label htmlFor="target-farm" className="text-xs font-bold text-agro-cream whitespace-nowrap">
                  Farm Plot:
                </label>
                <select
                  id="target-farm"
                  value={selectedFarmId}
                  onChange={(e) => setSelectedFarmId(e.target.value)}
                  className="px-3 py-1.5 rounded-xl bg-agro-surface border border-agro-border text-xs font-semibold text-agro-cream focus-visible:ring-2 focus-visible:ring-agro-primary cursor-pointer"
                >
                  {farms.map((f) => (
                    <option key={f.id} value={f.id} className="bg-agro-card text-agro-cream">
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
            className="inline-flex p-1 rounded-xl bg-agro-surface border border-agro-border text-xs font-bold shrink-0 self-start sm:self-auto"
          >
            <button
              type="button"
              role="tab"
              aria-selected={activeTab === 'camera'}
              onClick={() => setActiveTab('camera')}
              className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-lg transition-all ${
                activeTab === 'camera'
                  ? 'bg-agro-primary text-white shadow font-extrabold'
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
              className={`inline-flex items-center gap-1.5 px-4 py-2 rounded-lg transition-all ${
                activeTab === 'upload'
                  ? 'bg-agro-primary text-white shadow font-extrabold'
                  : 'text-agro-muted hover:text-agro-cream'
              }`}
            >
              <Upload className="w-3.5 h-3.5" aria-hidden="true" />
              <span>Upload Photo</span>
            </button>
          </div>
        </div>

        {/* Local Weather Status Pill (if available) */}
        {localWeather && (
          <div className="flex items-center justify-between px-3.5 py-2 rounded-xl bg-agro-highlight/15 border border-agro-highlight/25 text-xs text-agro-cream">
            <div className="flex items-center gap-2">
              <CloudSun className="w-4 h-4 text-agro-highlight" aria-hidden="true" />
              <span className="font-semibold">Local Agro-Climate: {localWeather.location}</span>
            </div>
            <div className="flex items-center gap-3 font-medium text-agro-muted">
              <span>{localWeather.temperature_c}°C</span>
              <span>•</span>
              <span>{localWeather.humidity_pct || localWeather.humidity_percent}% Humidity</span>
            </div>
          </div>
        )}

        {/* Error Alert */}
        {error && (
          <div className="p-4 rounded-xl bg-agro-primary/10 border border-agro-primary/30 text-agro-primary text-xs flex items-center gap-2.5">
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
                className="border-2 border-dashed border-agro-border hover:border-agro-primary bg-agro-surface hover:bg-agro-hover rounded-3xl p-8 sm:p-14 transition-all cursor-pointer space-y-4 group shadow-inner"
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/jpeg,image/png,image/webp"
                  className="hidden"
                  onChange={(e) => handleFileChange(e.target.files?.[0])}
                />
                
                <div className="w-16 h-16 rounded-2xl bg-agro-primary/10 border border-agro-primary/25 text-agro-primary flex items-center justify-center mx-auto group-hover:scale-105 transition-transform shadow-sm">
                  <Upload className="w-8 h-8" aria-hidden="true" />
                </div>

                <div className="space-y-1.5">
                  <h3 className="text-base sm:text-lg font-bold text-agro-cream font-heading">
                    Drop your leaf photo here, or <span className="text-agro-primary underline underline-offset-2">browse files</span>
                  </h3>
                  <p className="text-xs text-agro-muted">
                    Supports high-resolution JPEG, PNG, or WEBP up to 10MB
                  </p>
                </div>
              </div>
            ) : (
              <div className="space-y-6">
                <div className="relative max-w-sm mx-auto rounded-3xl overflow-hidden border border-agro-primary/40 shadow-2xl bg-agro-surface">
                  <img
                    src={previewUrl}
                    alt="Selected leaf preview"
                    className="w-full h-80 object-cover"
                  />
                  <div className="absolute top-3 right-3 px-3 py-1 rounded-full bg-agro-card/90 backdrop-blur-md border border-agro-primary/40 text-[11px] font-extrabold text-agro-primary flex items-center gap-1.5 shadow">
                    <CheckCircle2 className="w-3.5 h-3.5" aria-hidden="true" />
                    <span>Photo Ready</span>
                  </div>
                </div>

                <div className="flex flex-col sm:flex-row gap-3.5 justify-center pt-2">
                  <button
                    type="button"
                    onClick={handleReset}
                    className="px-6 py-3.5 rounded-xl bg-agro-surface hover:bg-agro-hover border border-agro-border text-agro-cream text-xs font-bold flex items-center justify-center gap-2 transition"
                  >
                    <RefreshCw className="w-4 h-4 text-agro-muted" aria-hidden="true" />
                    <span>Choose Another Photo</span>
                  </button>

                  <button
                    type="button"
                    onClick={() => handleUploadAndAnalyze()}
                    disabled={isAnalyzing}
                    className="px-8 py-3.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-white text-xs font-black flex items-center justify-center gap-2 transition shadow-xl shadow-orange-glow active:scale-[0.98] disabled:opacity-50"
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
      <section className="agro-panel bg-agro-card p-5 sm:p-6 rounded-3xl border border-agro-border shadow-sm">
        <h3 className="text-xs font-bold text-agro-cream mb-3.5 flex items-center gap-2 font-heading">
          <SunMedium className="w-4 h-4 text-agro-primary" aria-hidden="true" />
          <span>Foliage Photography Quality Standard for 98%+ AI Accuracy</span>
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 text-left">
          <div className="p-3.5 rounded-2xl bg-agro-surface border border-agro-border">
            <span className="block text-xs font-bold text-agro-cream mb-1">Natural Daylight</span>
            <span className="text-[11px] text-agro-muted leading-relaxed">Even daylight without hard reflective flash or shadow glare.</span>
          </div>
          <div className="p-3.5 rounded-2xl bg-agro-surface border border-agro-border">
            <span className="block text-xs font-bold text-agro-cream mb-1">Macro Venation Focus</span>
            <span className="text-[11px] text-agro-muted leading-relaxed">Keep the affected spots and leaf vein structure sharply focused.</span>
          </div>
          <div className="p-3.5 rounded-2xl bg-agro-surface border border-agro-border">
            <span className="block text-xs font-bold text-agro-cream mb-1">Frame Single Leaf</span>
            <span className="text-[11px] text-agro-muted leading-relaxed">Fill at least 40% of the frame with the affected leaf blade.</span>
          </div>
        </div>
      </section>

    </div>
  );
};
