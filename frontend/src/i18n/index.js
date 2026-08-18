import { en } from './en';
import { mr } from './mr';
import {
  translateCropName,
  translateDiseaseName,
  translateSeverityLevel,
  translateRiskLevel,
  CROP_TRANSLATIONS,
  DISEASE_TRANSLATIONS,
  SEVERITY_TRANSLATIONS,
  RISK_TRANSLATIONS
} from './crop_diseases';

const translations = { en, mr };

export const getTranslation = (lang, key, params = {}) => {
  const dictionary = translations[lang] || translations.en;
  let text = dictionary[key] || translations.en[key] || key;

  // Param interpolation e.g. {plant} -> "Mango" or translated
  Object.keys(params).forEach(p => {
    let val = params[p];
    if (p === 'plant' || p === 'crop') {
      val = translateCropName(val, lang);
    } else if (p === 'disease') {
      val = translateDiseaseName(val, lang);
    } else if (p === 'severity') {
      val = translateSeverityLevel(val, lang);
    }
    text = text.replace(new RegExp(`{${p}}`, 'g'), val);
  });

  return text;
};

export {
  translateCropName,
  translateDiseaseName,
  translateSeverityLevel,
  translateRiskLevel,
  CROP_TRANSLATIONS,
  DISEASE_TRANSLATIONS,
  SEVERITY_TRANSLATIONS,
  RISK_TRANSLATIONS
};
