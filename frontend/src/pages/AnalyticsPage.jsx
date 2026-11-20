import React, { useState, useEffect } from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  PieChart, Pie, Cell, AreaChart, Area 
} from 'recharts';
import { BarChart3, TrendingUp, PieChart as PieIcon, Activity } from 'lucide-react';
import { useLanguage } from '../context/LanguageContext';
import api from '../services/api';

// Modern balanced tech palette: clean emerald, mint, amber, coral, cyan, violet
const PIE_COLORS = ['#10B981', '#34D399', '#F59E0B', '#F43F5E', '#06B6D4', '#8B5CF6'];

const SEVERITY_COLORS = {
  Healthy: '#10B981',
  Mild: '#34D399',
  Moderate: '#F59E0B',
  Severe: '#F43F5E',
};

export const AnalyticsPage = () => {
  const { t, translateDisease, translateSeverity } = useLanguage();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await api.get('/analytics/dashboard');
        setData(res.data);
      } catch (err) {
        console.error('Failed to load analytics:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, []);

  if (loading) {
    return (
      <div className="py-20 text-center text-xs text-agro-muted animate-pulse">
        {t('analytics.loading') || 'Loading Crop Analytics & Visualizations...'}
      </div>
    );
  }

  // Localize disease names in distribution
  const localizedDistribution = (data?.disease_distribution || []).map(item => ({
    ...item,
    displayName: translateDisease(item.name)
  }));

  // Localize severity distribution
  const localizedSeverity = (data?.severity_distribution || []).map(item => ({
    ...item,
    displayName: translateSeverity(item.name),
    color: SEVERITY_COLORS[item.name] || '#2FBF71'
  }));

  const customTooltipStyle = {
    backgroundColor: 'rgba(15, 23, 42, 0.95)',
    borderColor: 'rgba(255, 255, 255, 0.12)',
    borderRadius: '0.85rem',
    fontSize: '12px',
    color: '#F8FAFC',
    boxShadow: '0 10px 30px rgba(0, 0, 0, 0.35)',
    backdropFilter: 'blur(12px)'
  };

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-agro-cream tracking-tight">
          {t('analytics.title') || 'Crop Health & Disease Analytics'}
        </h1>
        <p className="text-xs sm:text-sm text-agro-muted mt-1">
          {t('analytics.subtitle') || 'Data science visualizations of disease prevalence, severity distributions, and monthly outbreak trends.'}
        </p>
      </div>

      {/* Grid: Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Monthly Disease Trends */}
        <div className="agro-panel p-6 rounded-2xl space-y-4">
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-agro-primary" />
            <h3 className="text-sm font-bold text-agro-cream">
              {t('analytics.monthly_trends') || 'Monthly Disease Outbreak Trends'}
            </h3>
          </div>
          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={data?.monthly_trends || []}>
                <defs>
                  <linearGradient id="diseasedGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#F43F5E" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#F43F5E" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="healthyGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <XAxis dataKey="month" stroke="#94A3B8" fontSize={11} tickLine={false} />
                <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} />
                <Tooltip contentStyle={customTooltipStyle} itemStyle={{ color: '#F8FAFC' }} />
                <Area 
                  type="monotone" 
                  dataKey="diseased" 
                  stroke="#F43F5E" 
                  strokeWidth={2}
                  fillOpacity={1} 
                  fill="url(#diseasedGrad)" 
                  name={t('analytics.diseased_scans') || 'Diseased Scans'} 
                />
                <Area 
                  type="monotone" 
                  dataKey="healthy" 
                  stroke="#10B981" 
                  strokeWidth={2}
                  fillOpacity={1} 
                  fill="url(#healthyGrad)" 
                  name={t('analytics.healthy_scans') || 'Healthy Scans'} 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Disease Prevalence Distribution */}
        <div className="agro-panel p-6 rounded-2xl space-y-4">
          <div className="flex items-center space-x-2">
            <PieIcon className="w-5 h-5 text-agro-primary" />
            <h3 className="text-sm font-bold text-agro-cream">
              {t('analytics.disease_share') || 'Disease Prevalence Share'}
            </h3>
          </div>
          <div className="h-64 w-full flex items-center justify-center">
            {localizedDistribution.length === 0 ? (
              <div className="text-xs text-agro-muted text-center py-10">
                {t('dashboard.no_scans') || 'No diagnostic records available yet.'}
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={localizedDistribution}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={90}
                    paddingAngle={4}
                    dataKey="count"
                    nameKey="displayName"
                    stroke="rgba(15, 23, 42, 0.4)"
                    strokeWidth={2}
                  >
                    {localizedDistribution.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={PIE_COLORS[index % PIE_COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={customTooltipStyle} itemStyle={{ color: '#F8FAFC' }} />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        {/* Severity Distribution */}
        <div className="agro-panel p-6 rounded-2xl space-y-4 lg:col-span-2">
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-5 h-5 text-agro-primary" />
            <h3 className="text-sm font-bold text-agro-cream">
              {t('analytics.severity_dist') || 'Leaf Lesion Severity Breakdown'}
            </h3>
          </div>
          <div className="h-64 w-full">
            {localizedSeverity.length === 0 ? (
              <div className="text-xs text-agro-muted text-center py-10">
                {t('dashboard.no_scans') || 'No diagnostic records available yet.'}
              </div>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={localizedSeverity}>
                  <XAxis dataKey="displayName" stroke="#7A786E" fontSize={11} tickLine={false} />
                  <YAxis stroke="#7A786E" fontSize={11} tickLine={false} />
                  <Tooltip contentStyle={customTooltipStyle} itemStyle={{ color: '#FAF7EF' }} />
                  <Bar dataKey="value" radius={[6, 6, 0, 0]} name="Occurrences">
                    {localizedSeverity.map((entry, index) => (
                      <Cell key={`bar-${index}`} fill={entry.color || '#2FBF71'} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

      </div>

    </div>
  );
};
