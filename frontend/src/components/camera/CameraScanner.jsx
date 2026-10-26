import React, { useState, useRef, useEffect } from 'react';
import { CameraPreview } from './CameraPreview';
import { ImagePreview } from './ImagePreview';
import { CameraError } from './CameraError';
import { Camera, Upload, Smartphone } from 'lucide-react';
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

  // Handle native camera or file input capture (works 100% on any mobile or desktop browser)
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

  // Start browser camera stream with progressive fallback for mobile and low-spec webcams
  const startCamera = async (targetFacingMode = facingMode) => {
    setErrorInfo(null);
    stopCameraStream();

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setErrorInfo({
        type: 'NotSupported',
        message: 'Live browser viewfinder requires HTTPS or localhost. Tap "Use Device Camera" below to use your native phone/laptop camera.'
      });
      return;
    }

    let mediaStream = null;

    // Attempt 1: High-definition ideal rear camera
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
      // Attempt 2: Flexible basic constraint (guaranteed to work across older phones & tablets)
      try {
        mediaStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: targetFacingMode },
          audio: false
        });
      } catch (err2) {
        // Attempt 3: Any video device available
        try {
          mediaStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
          });
        } catch (err3) {
          console.error('All camera access attempts failed:', err3);
          let msg = 'Failed to open camera.';
          if (err3.name === 'NotAllowedError' || err3.name === 'PermissionDeniedError') {
            msg = t('scan.camera_denied') || 'Camera permission was denied. Please grant camera access in browser settings or tap "Use Device Camera" below.';
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

  // Switch between Rear/Front Camera
  const handleSwitchCamera = () => {
    const nextMode = facingMode === 'environment' ? 'user' : 'environment';
    startCamera(nextMode);
  };

  // Capture canvas snapshot frame from video feed
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

    // Stop live stream after capture
    stopCameraStream();
    setIsCameraActive(false);
  };

  // Retake photo
  const handleRetake = () => {
    setCapturedDataUrl(null);
    setCapturedFile(null);
    startCamera(facingMode);
  };

  // Close camera modal / inline view
  const handleCloseCamera = () => {
    stopCameraStream();
    setIsCameraActive(false);
    setErrorInfo(null);
  };

  // Confirm photo usage and start analysis
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
      {/* Hidden Native Device Camera Input (100% works on Android, iOS Safari, Windows, Mac) */}
      <input
        ref={nativeCameraInputRef}
        type="file"
        accept="image/*"
        capture="environment"
        className="hidden"
        onChange={handleNativeFileChange}
      />

      {/* 1. Camera Error Display with Direct Native Trigger */}
      {errorInfo && (
        <CameraError
          errorType={errorInfo.type}
          message={errorInfo.message}
          onRetry={() => startCamera(facingMode)}
          onNativeCapture={triggerNativeCamera}
          onFallbackUpload={onFallbackUpload}
        />
      )}

      {/* 2. Captured Image Preview & AI Confirmation */}
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
        <div className="p-6 sm:p-8 rounded-3xl bg-gradient-to-br from-emerald-950/40 via-slate-900 to-slate-950 border border-emerald-500/30 text-center space-y-4 shadow-2xl">
          <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto shadow-inner">
            <Camera className="w-8 h-8" />
          </div>

          <div className="space-y-1">
            <h3 className="text-lg font-extrabold text-slate-100">{t('scan.title') || 'Live Camera Leaf Scanner'}</h3>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              {t('scan.subtitle') || 'Capture a clear photo of the plant leaf using your phone camera or laptop webcam for instant identification and health analysis.'}
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
            <button
              type="button"
              onClick={() => startCamera('environment')}
              className="px-6 py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider transition shadow-lg shadow-emerald-500/30 flex items-center justify-center space-x-2"
            >
              <Camera className="w-4 h-4" />
              <span>{t('scan.camera_start') || 'Open Camera Scanner'}</span>
            </button>

            <button
              type="button"
              onClick={triggerNativeCamera}
              className="px-5 py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-300 font-bold text-xs border border-emerald-500/30 transition flex items-center justify-center space-x-2 shadow-sm"
            >
              <Smartphone className="w-4 h-4 text-emerald-400" />
              <span>Use Device Camera</span>
            </button>

            <button
              type="button"
              onClick={onFallbackUpload}
              className="px-5 py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs border border-slate-700 transition flex items-center justify-center space-x-2"
            >
              <Upload className="w-4 h-4" />
              <span>{t('scan.tab_upload') || 'Upload Photo'}</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
