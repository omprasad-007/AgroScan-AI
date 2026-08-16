import React, { useState, useRef, useEffect } from 'react';
import { CameraPreview } from './CameraPreview';
import { ImagePreview } from './ImagePreview';
import { CameraError } from './CameraError';
import { Camera, Upload } from 'lucide-react';

export const CameraScanner = ({ onImageCaptured, onFallbackUpload, isAnalyzing }) => {
  const videoRef = useRef(null);
  const [isCameraActive, setIsCameraActive] = useState(false);
  const [stream, setStream] = useState(null);
  const [facingMode, setFacingMode] = useState('environment'); // 'environment' (rear) or 'user' (front)
  const [capturedDataUrl, setCapturedDataUrl] = useState(null);
  const [capturedFile, setCapturedFile] = useState(null);
  const [errorInfo, setErrorInfo] = useState(null);

  // Stop camera tracks safely
  const stopCameraStream = () => {
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      setStream(null);
    }
  };

  // Clean up stream when component unmounts or leaves page
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
        message: 'Browser camera API is not supported on this device or connection. HTTPS or localhost is required for camera access.'
      });
      return;
    }

    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: targetFacingMode },
          width: { ideal: 1920 },
          height: { ideal: 1080 }
        },
        audio: false
      });

      setStream(mediaStream);
      setIsCameraActive(true);
      setFacingMode(targetFacingMode);

      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
    } catch (err) {
      console.error('Camera access error:', err);
      let msg = 'Failed to open camera.';
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        msg = 'Camera permission was denied. Please grant camera access in browser settings.';
      } else if (err.name === 'NotFoundError' || err.name === 'DevicesNotFoundError') {
        msg = 'No camera device found on this system.';
      } else if (err.name === 'NotReadableError' || err.name === 'TrackStartError') {
        msg = 'Camera is already in use by another application.';
      }
      setErrorInfo({ type: err.name || 'CameraError', message: msg });
      setIsCameraActive(false);
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

    canvas.toBlob((blob) => {
      if (blob) {
        const file = new File([blob], `leaf_camera_${Date.now()}.jpg`, { type: 'image/jpeg' });
        setCapturedFile(file);
      }
    }, 'image/jpeg', 0.92);

    // Stop live stream after capture to preserve battery and device resources
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

  // Confirm photo usage
  const handleUsePhoto = () => {
    if (capturedFile && capturedDataUrl) {
      onImageCaptured(capturedFile, capturedDataUrl);
    }
  };

  return (
    <div className="w-full space-y-4">
      {/* 1. Camera Error Display */}
      {errorInfo && (
        <CameraError
          errorType={errorInfo.type}
          message={errorInfo.message}
          onRetry={() => startCamera(facingMode)}
          onFallbackUpload={onFallbackUpload}
        />
      )}

      {/* 2. Captured Image Preview & AI Animation */}
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

      {/* 4. Primary Standby Camera Action Card (When camera is closed & no photo captured) */}
      {!isCameraActive && !capturedDataUrl && !errorInfo && (
        <div className="p-8 rounded-2xl bg-gradient-to-br from-emerald-950/40 via-slate-900 to-slate-950 border border-emerald-500/30 text-center space-y-4 shadow-xl">
          <div className="w-16 h-16 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto shadow-inner">
            <Camera className="w-8 h-8" />
          </div>

          <div className="space-y-1">
            <h3 className="text-lg font-extrabold text-slate-100">Live Camera Leaf Scanner</h3>
            <p className="text-xs text-slate-400 max-w-md mx-auto">
              Capture a clear photo of the affected plant leaf using your phone camera or laptop webcam for instant disease detection.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row gap-3 justify-center pt-2">
            <button
              type="button"
              onClick={() => startCamera('environment')}
              className="px-8 py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs uppercase tracking-wider transition shadow-lg shadow-emerald-500/30 flex items-center justify-center space-x-2"
            >
              <Camera className="w-4 h-4" />
              <span>Open Camera Scanner</span>
            </button>

            <button
              type="button"
              onClick={onFallbackUpload}
              className="px-6 py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs border border-slate-700 transition flex items-center justify-center space-x-2"
            >
              <Upload className="w-4 h-4" />
              <span>Upload From Device</span>
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
