import React from 'react';
import { CheckCircle2, AlertTriangle, ShieldCheck } from 'lucide-react';
import { useLanguage } from '../../context/LanguageContext';

export const SeverityBadge = ({ level }) => {
  const { translateSeverity } = useLanguage();
  const normalized = String(level || 'Mild').toLowerCase();

  let style = 'bg-agro-highlight/15 text-agro-highlight border-agro-highlight/30';
  let Icon = AlertTriangle;

  if (normalized.includes('healthy')) {
    style = 'bg-agro-accent/15 text-agro-accent border-agro-accent/30';
    Icon = ShieldCheck;
  } else if (normalized.includes('mild')) {
    style = 'bg-agro-highlight/15 text-agro-highlight border-agro-highlight/30';
    Icon = AlertTriangle;
  } else if (normalized.includes('moderate')) {
    style = 'bg-agro-highlight/20 text-agro-highlight border-agro-highlight/40 font-semibold';
    Icon = AlertTriangle;
  } else if (normalized.includes('severe') || normalized.includes('critical')) {
    style = 'bg-agro-primary/15 text-agro-primary border-agro-primary/40 font-bold';
    Icon = AlertTriangle;
  }

  const label = translateSeverity ? translateSeverity(level) : level;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${style}`}
      role="status"
      aria-label={`Severity: ${label}`}
    >
      <Icon className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
      <span>{label}</span>
    </span>
  );
};

export const WeatherRiskBadge = ({ level }) => {
  const { translateRisk } = useLanguage();
  const normalized = String(level || 'Low').toLowerCase();

  let style = 'bg-agro-accent/15 text-agro-accent border-agro-accent/30';
  let Icon = CheckCircle2;

  if (normalized.includes('low') || normalized.includes('none')) {
    style = 'bg-agro-accent/15 text-agro-accent border-agro-accent/30';
    Icon = CheckCircle2;
  } else if (normalized.includes('medium') || normalized.includes('moderate')) {
    style = 'bg-agro-highlight/15 text-agro-highlight border-agro-highlight/35';
    Icon = AlertTriangle;
  } else if (normalized.includes('high')) {
    style = 'bg-agro-primary/15 text-agro-primary border-agro-primary/40';
    Icon = AlertTriangle;
  } else if (normalized.includes('critical')) {
    style = 'bg-agro-primary/25 text-agro-primary border-agro-primary/50 font-bold';
    Icon = AlertTriangle;
  }

  const label = translateRisk ? translateRisk(level) : `${level} Risk`;

  return (
    <span
      className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${style}`}
      role="status"
      aria-label={`Weather Risk: ${label}`}
    >
      <Icon className="w-3.5 h-3.5 shrink-0" aria-hidden="true" />
      <span>{label}</span>
    </span>
  );
};
