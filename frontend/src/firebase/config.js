import { initializeApp } from 'firebase/app';
import { getAuth, browserLocalPersistence, setPersistence } from 'firebase/auth';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY || "AIzaSyAgroScanAI07MockKeyForDevOnly",
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN || "agroscan-ai-07.firebaseapp.com",
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID || "agroscan-ai-07",
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET || "agroscan-ai-07.appspot.com",
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID || "1026781866088",
  appId: import.meta.env.VITE_FIREBASE_APP_ID || "1:1026781866088:web:agroscan07app"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Ensure local persistence across browser refreshes
setPersistence(auth, browserLocalPersistence).catch((error) => {
  console.warn("Firebase persistence error:", error);
});

export { app, auth };
