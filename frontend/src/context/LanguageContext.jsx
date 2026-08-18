import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  getTranslation, 
  translateCropName, 
  translateDiseaseName, 
  translateSeverityLevel, 
  translateRiskLevel 
} from '../i18n';

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [lang, setLangState] = useState(() => {
    return localStorage.getItem('agroscan_language') || 'en';
  });

  const setLang = (newLang) => {
    const validLang = newLang === 'mr' ? 'mr' : 'en';
    setLangState(validLang);
    localStorage.setItem('agroscan_language', validLang);
  };

  const toggleLanguage = () => {
    setLang(lang === 'en' ? 'mr' : 'en');
  };

  const t = (key, params = {}) => {
    return getTranslation(lang, key, params);
  };

  const translateCrop = (cropName) => translateCropName(cropName, lang);
  const translateDisease = (diseaseName) => translateDiseaseName(diseaseName, lang);
  const translateSeverity = (level) => translateSeverityLevel(level, lang);
  const translateRisk = (level) => translateRiskLevel(level, lang);

  const formatDate = (dateValue) => {
    if (!dateValue) return '';
    try {
      const d = new Date(dateValue);
      return new Intl.DateTimeFormat(lang === 'mr' ? 'mr-IN' : 'en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }).format(d);
    } catch {
      return String(dateValue);
    }
  };

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  return (
    <LanguageContext.Provider value={{ 
      lang, 
      setLang, 
      toggleLanguage, 
      t,
      translateCrop,
      translateDisease,
      translateSeverity,
      translateRisk,
      formatDate
    }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
