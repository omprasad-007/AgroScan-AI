import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  sendPasswordResetEmail,
  onAuthStateChanged,
  updateProfile
} from 'firebase/auth';
import { auth } from './config';

/**
 * Converts Firebase error codes into clean, user-friendly messages.
 */
export const getAuthErrorMessage = (errorCode) => {
  switch (errorCode) {
    case 'auth/invalid-email':
      return 'The email address format is invalid. Please check and try again.';
    case 'auth/user-not-found':
    case 'auth/wrong-password':
    case 'auth/invalid-credential':
      return 'Incorrect email or password. Please verify your credentials.';
    case 'auth/email-already-in-use':
      return 'An account with this email address already exists. Please login instead.';
    case 'auth/weak-password':
      return 'Password is too weak. Please use at least 6 characters.';
    case 'auth/too-many-requests':
      return 'Too many failed login attempts. Access temporarily disabled for security.';
    case 'auth/network-request-failed':
      return 'Network connection error. Please check your internet connection.';
    default:
      return 'Authentication failed. Please try again.';
  }
};

/**
 * Register a new user with email and password, updating display name.
 */
export const registerUser = async (email, password, fullName = '') => {
  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    if (fullName && userCredential.user) {
      await updateProfile(userCredential.user, { displayName: fullName });
    }
    return userCredential.user;
  } catch (error) {
    throw new Error(getAuthErrorMessage(error.code || error.message));
  }
};

/**
 * Login user with email and password.
 */
export const loginUser = async (email, password) => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    return userCredential.user;
  } catch (error) {
    throw new Error(getAuthErrorMessage(error.code || error.message));
  }
};

/**
 * Logout current user.
 */
export const logoutUser = async () => {
  try {
    await signOut(auth);
  } catch (error) {
    throw new Error('Failed to logout. Please try again.');
  }
};

/**
 * Send password reset email.
 */
export const resetPassword = async (email) => {
  try {
    await sendPasswordResetEmail(auth, email);
  } catch (error) {
    throw new Error(getAuthErrorMessage(error.code || error.message));
  }
};

/**
 * Get current authenticated Firebase user.
 */
export const getCurrentUser = () => {
  return auth.currentUser;
};

/**
 * Subscribe to Firebase auth state changes.
 */
export const subscribeToAuthState = (callback) => {
  return onAuthStateChanged(auth, callback);
};
