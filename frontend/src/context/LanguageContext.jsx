import React, { createContext, useContext, useState } from 'react';
import en from '../i18n/en.json';
import mr from '../i18n/mr.json';

const translations = { en, mr };

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [lang, setLang] = useState('en');

  const toggleLanguage = () => {
    setLang(prev => (prev === 'en' ? 'mr' : 'en'));
  };

  const t = (path) => {
    const keys = path.split('.');
    let current = translations[lang];
    for (const key of keys) {
      if (!current || current[key] === undefined) {
        // Fallback to English
        let fallback = translations['en'];
        for (const fKey of keys) {
          if (!fallback) return path;
          fallback = fallback[fKey];
        }
        return fallback || path;
      }
      current = current[key];
    }
    return current;
  };

  return (
    <LanguageContext.Provider value={{ lang, setLang, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
