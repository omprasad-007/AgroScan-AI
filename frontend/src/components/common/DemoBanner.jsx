import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const DemoBanner = () => {
  const { t } = useLanguage();

  return (
    <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-2 text-xs md:text-sm font-medium text-amber-400 flex items-center justify-between shadow-inner">
      <div className="flex items-center space-x-2 max-w-7xl mx-auto w-full">
        <AlertTriangle className="w-4 h-4 shrink-0 text-amber-400 animate-pulse" />
        <span>{t('demo_banner')}</span>
      </div>
      <span className="hidden sm:inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-amber-500/20 text-amber-300">
        Demo Mode
      </span>
    </div>
  );
};
