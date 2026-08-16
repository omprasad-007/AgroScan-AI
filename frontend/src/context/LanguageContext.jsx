import React, { createContext, useContext, useState, useEffect } from 'react';
import { getTranslation } from '../i18n';

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

  useEffect(() => {
    document.documentElement.lang = lang;
  }, [lang]);

  return (
    <LanguageContext.Provider value={{ lang, setLang, toggleLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
