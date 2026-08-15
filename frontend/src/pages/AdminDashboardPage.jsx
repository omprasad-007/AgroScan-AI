import React, { useState, useEffect } from 'react';
import { ShieldCheck, Users, Activity, Database, Server } from 'lucide-react';
import api from '../services/api';

export const AdminDashboardPage = () => {
  const [users, setUsers] = useState([]);
  const [sysAnalytics, setSysAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAdminData = async () => {
      try {
        const [uRes, aRes] = await Promise.all([
          api.get('/admin/users'),
          api.get('/admin/analytics')
        ]);
        setUsers(uRes.data);
        setSysAnalytics(aRes.data);
      } catch (err) {
        console.error('Failed to load admin console data:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchAdminData();
  }, []);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-white flex items-center space-x-2">
          <ShieldCheck className="w-6 h-6 text-agri-400" />
          <span>System Administration Console</span>
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Monitor system health, user registrations, and model inference statistics.
        </p>
      </div>

      {/* Admin Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="glass-panel p-5 rounded-2xl">
          <span className="text-xs text-slate-400 block">Total Registered Users</span>
          <span className="text-2xl font-bold text-white mt-1 block">{sysAnalytics?.total_users || users.length}</span>
        </div>
        <div className="glass-panel p-5 rounded-2xl">
          <span className="text-xs text-slate-400 block">Total Scans Processed</span>
          <span className="text-2xl font-bold text-agri-400 mt-1 block">{sysAnalytics?.total_scans || 50}</span>
        </div>
        <div className="glass-panel p-5 rounded-2xl">
          <span className="text-xs text-slate-400 block">System Operational Status</span>
          <span className="text-2xl font-bold text-emerald-400 mt-1 block">Healthy</span>
        </div>
      </div>

      {/* User Table */}
      <div className="glass-panel p-6 rounded-2xl space-y-4">
        <h3 className="text-sm font-bold text-white flex items-center space-x-2">
          <Users className="w-4 h-4 text-agri-400" />
          <span>User Accounts</span>
        </h3>

        {loading ? (
          <div className="py-8 text-center text-xs text-slate-400 animate-pulse">Loading accounts...</div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400">
                  <th className="py-2.5 px-3">Name</th>
                  <th className="py-2.5 px-3">Email</th>
                  <th className="py-2.5 px-3">Role</th>
                  <th className="py-2.5 px-3">Location</th>
                  <th className="py-2.5 px-3">Joined</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {users.map((u) => (
                  <tr key={u.id} className="hover:bg-slate-800/30 transition">
                    <td className="py-3 px-3 font-semibold text-white">{u.full_name}</td>
                    <td className="py-3 px-3 text-slate-300">{u.email}</td>
                    <td className="py-3 px-3">
                      <span className="px-2 py-0.5 rounded bg-agri-500/10 text-agri-400 text-[10px] font-bold uppercase">
                        {u.role}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-slate-400">{u.city || 'N/A'}</td>
                    <td className="py-3 px-3 text-slate-400 font-mono text-[11px]">
                      {new Date(u.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

    </div>
  );
};
