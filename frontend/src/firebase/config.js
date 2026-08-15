import { initializeApp } from 'firebase/app';
import { getAuth, browserLocalPersistence, setPersistence } from 'firebase/auth';
import { getAnalytics, isSupported } from 'firebase/analytics';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyBS34qOVv8r2nhwefeTC8Q9Klp5CRnttGI",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "agroscan-ai-07.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "agroscan-ai-07",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "agroscan-ai-07.firebasestorage.app",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "279701842154",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:279701842154:web:cbb8228842360fddf40f93",
  measurementId: import.meta.env.VITE_FIREBASE_MEASUREMENT_ID || "G-DRDQ26J04Y"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

let analytics = null;
if (typeof window !== 'undefined') {
  isSupported().then((supported) => {
    if (supported) {
      analytics = getAnalytics(app);
    }
  }).catch((err) => {
    console.debug("Firebase Analytics unsupported in current environment:", err);
  });
}

// Ensure local persistence across browser refreshes
setPersistence(auth, browserLocalPersistence).catch((error) => {
  console.warn("Firebase persistence error:", error);
});

export { app, auth, analytics };
