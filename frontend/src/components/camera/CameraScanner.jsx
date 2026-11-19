import React, { useState, useRef, useEffect } from 'react';
import { CameraPreview } from './CameraPreview';
import { ImagePreview } from './ImagePreview';
import { CameraError } from './CameraError';
import { Camera, Upload, Smartphone, ScanLine, SunMedium, Maximize2 } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const CameraScanner = ({ onImageCaptured, onFallbackUpload, isAnalyzing }) => {
  const { t } = useLanguage();
  const videoRef = useRef(null);
  const nativeCameraInputRef = useRef(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [stream, setStream] = useState(null);
  const [facingMode, setFacingMode] = useState('environment'); // 'environment' (rear) or 'user' (front)
  const [capturedDataUrl, setCapturedDataUrl] = useState(null);
  const [capturedFile, setCapturedFile] = useState(null);
  const [errorInfo, setErrorInfo] = useState(null);

  // Helper to convert base64 DataURL to File object synchronously
  const dataURLtoFile = (dataurl, filename) => {
    try {
      const arr = dataurl.split(',');
      const mime = arr[0].match(/:(.*?);/)?.[1] || 'image/jpeg';
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      return new File([u8arr], filename, { type: mime });
    } catch (e) {
      console.warn("dataURLtoFile conversion warning:", e);
      return null;
    }
  };

  // Handle native camera or file input capture
  const handleNativeFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      const dataUrl = URL.createObjectURL(file);
      setCapturedFile(file);
      setCapturedDataUrl(dataUrl);
      setErrorInfo(null);
      stopCameraStream();
      setIsCameraActive(false);
    }
  };

  const triggerNativeCamera = () => {
    if (nativeCameraInputRef.current) {
      nativeCameraInputRef.current.click();
    }
  };

  // Stop camera tracks safely
  const stopCameraStream = () => {
    if (stream) {
      try {
        stream.getTracks().forEach((track) => track.stop());
      } catch (e) {
        console.warn("Track stop warning:", e);
      }
      setStream(null);
    }
  };

  useEffect(() => {
    return () => {
      stopCameraStream();
    };
  }, [stream]);

  // Start browser camera stream
  const startCamera = async (targetFacingMode = facingMode) => {
    setErrorInfo(null);
    stopCameraStream();

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setErrorInfo({
        type: 'NotSupported',
        message: 'Live browser viewfinder requires HTTPS or camera permission. Tap "Use Device Camera" below.'
      });
      return;
    }

    let mediaStream = null;

    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: targetFacingMode },
          width: { ideal: 1280 },
          height: { ideal: 720 }
        },
        audio: false
      });
    } catch (err1) {
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: targetFacingMode },
          audio: false
        });
      } catch (err2) {
        try {
          mediaStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
          });
        } catch (err3) {
          console.error('All camera access attempts failed:', err3);
          let msg = 'Failed to access camera.';
          if (err3.name === 'NotAllowedError' || err3.name === 'PermissionDeniedError') {
            msg = t('scan.camera_denied') || 'Camera permission was denied. Please grant camera access in browser settings or use the upload tab.';
          } else if (err3.name === 'NotFoundError' || err3.name === 'DevicesNotFoundError') {
            msg = 'No camera found on this device.';
          } else if (err3.name === 'NotReadableError' || err3.name === 'TrackStartError') {
            msg = 'Camera is already in use by another app or browser tab.';
          }
          setErrorInfo({ type: err3.name || 'CameraError', message: msg });
          setIsCameraActive(false);
          return;
        }
      }
    }

    if (mediaStream) {
      setStream(mediaStream);
      setIsCameraActive(true);
      setFacingMode(targetFacingMode);

      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    }
  };

  const handleSwitchCamera = () => {
    const nextMode = facingMode === 'environment' ? 'user' : 'environment';
    startCamera(nextMode);
  };

  const handleCapturePhoto = () => {
    if (!videoRef.current) return;
    const video = videoRef.current;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 1280;
    canvas.height = video.videoHeight || 720;
    
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    const dataUrl = canvas.toDataURL('image/jpeg', 0.92);
    setCapturedDataUrl(dataUrl);

    const filename = `leaf_camera_${Date.now()}.jpg`;
    const syncFile = dataURLtoFile(dataUrl, filename);
    if (syncFile) {
      setCapturedFile(syncFile);
    }

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], filename, { type: 'image/jpeg' });
        setCapturedFile(file);
      }
    }, 'image/jpeg', 0.92);

    stopCameraStream();
    setIsCameraActive(false);
  };

  const handleRetake = () => {
    setCapturedDataUrl(null);
    setCapturedFile(null);
    startCamera(facingMode);
  };

  const handleCloseCamera = () => {
    stopCameraStream();
    setIsCameraActive(false);
    setErrorInfo(null);
  };

  const handleUsePhoto = () => {
    if (!capturedDataUrl) return;
    let target = capturedFile;
    if (!target) {
      target = dataURLtoFile(capturedDataUrl, `leaf_scan_${Date.now()}.jpg`);
    }
    if (target) {
      onImageCaptured(target, capturedDataUrl);
    }
  };

  return (
    <div className="w-full space-y-4">
      {/* Hidden Native Device Camera Input */}
      <input
        ref={nativeCameraInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        className="hidden"
        onChange={handleNativeFileChange}
      />

      {/* 1. Camera Error Display */}
      {errorInfo && (
        <CameraError
          errorType={errorInfo.type}
          message={errorInfo.message}
          onRetry={() => startCamera(facingMode)}
          onNativeCapture={triggerNativeCamera}
          onFallbackUpload={onFallbackUpload}
        />
      )}

      {/* 2. Captured Image Preview */}
      {capturedDataUrl && !isCameraActive && (
        <ImagePreview
          imageUrl={capturedDataUrl}
          onRetake={handleRetake}
          onUsePhoto={handleUsePhoto}
          isScanning={isAnalyzing}
        />
      )}

      {/* 3. Live Camera Viewfinder */}
      {isCameraActive && !capturedDataUrl && (
        <CameraPreview
          videoRef={videoRef}
          onCapture={handleCapturePhoto}
          onSwitchCamera={handleSwitchCamera}
          onClose={handleCloseCamera}
          canSwitch={true}
          facingMode={facingMode}
        />
      )}

      {/* 4. Primary Standby Camera Action Card */}
      {!isCameraActive && !capturedDataUrl && !errorInfo && (
        <div className="p-6 sm:p-8 rounded-3xl bg-agro-card border border-agro-border text-center space-y-5 shadow-xl">
          <div className="w-16 h-16 rounded-2xl bg-agro-primary/10 border border-agro-primary/25 text-agro-primary flex items-center justify-center mx-auto shadow-sm">
            <Camera className="w-8 h-8" aria-hidden="true" />
          </div>

          <div className="space-y-1">
            <h3 className="text-lg font-extrabold text-agro-cream">
              {t('scan.camera_card_title') || 'Capture a Clear Leaf Photograph'}
            </h3>
            <p className="text-xs text-agro-muted max-w-md mx-auto leading-relaxed">
              {t('scan.camera_card_description') || 'Position the camera 10–20 cm above the affected leaf in bright, even daylight.'}
            </p>
          </div>

          <div className="grid grid-cols-3 gap-2.5 rounded-2xl border border-agro-border bg-agro-surface/60 p-3.5 text-left max-w-lg mx-auto">
            <div className="min-w-0">
              <SunMedium className="mb-1 h-4 w-4 text-agro-lime" aria-hidden="true" />
              <span className="block text-[11px] font-semibold text-agro-cream">
                {t('scan.tip_light_short') || 'Even Daylight'}
              </span>
            </div>
            <div className="min-w-0">
              <ScanLine className="mb-1 h-4 w-4 text-agro-lime" aria-hidden="true" />
              <span className="block text-[11px] font-semibold text-agro-cream">
                {t('scan.tip_sharp_short') || 'Sharp Focus'}
              </span>
            </div>
            <div className="min-w-0">
              <Maximize2 className="mb-1 h-4 w-4 text-agro-lime" aria-hidden="true" />
              <span className="block text-[11px] font-semibold text-agro-cream">
                {t('scan.tip_frame_short') || 'Fills Frame'}
              </span>
            </div>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2 max-w-md mx-auto">
            <button
              type="button"
              onClick={() => startCamera('environment')}
              className="flex-1 px-6 py-3.5 rounded-xl bg-agro-primary hover:bg-agro-primaryHover text-agro-bg font-extrabold text-xs transition shadow-md shadow-agro-primary/25 flex items-center justify-center gap-2 active:scale-[0.98]"
            >
              <Camera className="w-4 h-4" aria-hidden="true" />
              <span>{t('scan.camera_start') || 'Open Live Camera'}</span>
            </button>

            <button
              type="button"
              onClick={triggerNativeCamera}
              className="px-5 py-3.5 rounded-xl bg-agro-surface hover:bg-agro-hover text-agro-cream font-bold text-xs border border-agro-border transition flex items-center justify-center gap-2 active:scale-[0.98]"
            >
              <Smartphone className="w-4 h-4 text-agro-lime" aria-hidden="true" />
              <span>Use Device Camera</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
