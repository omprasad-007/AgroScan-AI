import { en } from './en';
import { mr } from './mr';

const translations = { en, mr };

export const getTranslation = (lang, key, params = {}) => {
  const dictionary = translations[lang] || translations.en;
  let text = dictionary[key] || translations.en[key] || key;

  // Param interpolation e.g. {plant} -> "Mango"
  Object.keys(params).forEach(p => {
    text = text.replace(new RegExp(`{${p}}`, 'g'), params[p]);
  });

  return text;
};
