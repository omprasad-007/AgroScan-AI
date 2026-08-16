import React from 'react';
import { AlertTriangle } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const DemoBanner = () => {
  const { t } = useLanguage();

  return (
    <div className="bg-emerald-500/10 border-b border-emerald-500/20 px-4 py-1.5 text-xs md:text-sm font-medium text-emerald-400 flex items-center justify-between shadow-inner">
      <div className="flex items-center space-x-2 max-w-7xl mx-auto w-full">
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping shrink-0"></span>
        <span className="text-[11px] font-semibold text-emerald-300">
          AGROSCAN AI ENGINE ONLINE — Multi-Model Plant Disease Detection & Cultivation Knowledge Active
        </span>
      </div>
      <span className="hidden sm:inline-block px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-emerald-500/20 text-emerald-300">
        Live Active
      </span>
    </div>
  );
};
