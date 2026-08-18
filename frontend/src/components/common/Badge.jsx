import React from 'react';
import { useLanguage } from '../../context/LanguageContext';

export const SeverityBadge = ({ level }) => {
  const { translateSeverity } = useLanguage();
  const styles = {
    Healthy: 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30',
    Mild: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
    Moderate: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
    Severe: 'bg-red-500/10 text-red-400 border-red-500/30'
  };

  const style = styles[level] || styles.Mild;
  const label = translateSeverity ? translateSeverity(level) : level;

  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold border ${style}`}>
      <span className="w-1.5 h-1.5 rounded-full bg-current mr-1.5 animate-pulse" />
      {label}
    </span>
  );
};

export const WeatherRiskBadge = ({ level }) => {
  const { translateRisk } = useLanguage();
  const styles = {
    Low: 'bg-blue-500/10 text-blue-400 border-blue-500/30',
    Medium: 'bg-yellow-500/10 text-yellow-400 border-yellow-500/30',
    High: 'bg-orange-500/10 text-orange-400 border-orange-500/30',
    Critical: 'bg-red-500/10 text-red-400 border-red-500/30'
  };

  const style = styles[level] || styles.Medium;
  const label = translateRisk ? translateRisk(level) : `${level} Risk`;

  return (
    <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold border ${style}`}>
      {label}
    </span>
  );
};
