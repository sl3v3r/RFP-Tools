import React, { useEffect, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import api from '../services/api';
import Card from '../components/Card';
import Badge from '../components/Badge';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

function Dashboard() {
  const [metrics, setMetrics] = useState(null);
  const [health, setHealth] = useState(null);
  const [status, setStatus] = useState(null);

  // Fetch metrics
  const metricsQuery = useQuery({
    queryKey: ['metrics'],
    queryFn: () => api.get('/metrics').then(r => r.data),
    refetchInterval: 5000,
  });

  // Fetch health
  const healthQuery = useQuery({
    queryKey: ['health'],
    queryFn: () => api.get('/health').then(r => r.data),
    refetchInterval: 10000,
  });

  // Fetch status
  const statusQuery = useQuery({
    queryKey: ['status'],
    queryFn: () => api.get('/status').then(r => r.data),
    refetchInterval: 10000,
  });

  useEffect(() => {
    if (metricsQuery.data) setMetrics(metricsQuery.data);
    if (healthQuery.data) setHealth(healthQuery.data);
    if (statusQuery.data) setStatus(statusQuery.data);
  }, [metricsQuery.data, healthQuery.data, statusQuery.data]);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">RFP Analysis System Overview</p>
      </div>

      {/* Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <div className="p-6">
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Status</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
              {status?.status || 'Loading...'}
            </p>
            <Badge variant={status?.status === 'operational' ? 'success' : 'warning'} className="mt-2">
              {status?.status === 'operational' ? '✓ Operational' : '⚠ Degraded'}
            </Badge>
          </div>
        </Card>

        <Card>
          <div className="p-6">
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Knowledge Base</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
              {status?.products || 0}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">Products Loaded</p>
          </div>
        </Card>

        <Card>
          <div className="p-6">
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Analyses</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
              {metrics?.total_analyses || 0}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">RFPs Analyzed</p>
          </div>
        </Card>

        <Card>
          <div className="p-6">
            <p className="text-sm font-medium text-gray-500 dark:text-gray-400">Total Evaluations</p>
            <p className="text-2xl font-bold text-gray-900 dark:text-white mt-2">
              {metrics?.total_evaluations || 0}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">Responses Evaluated</p>
          </div>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Activity Chart */}
        <Card>
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">API Activity</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={[
                { name: 'Analyses', value: metrics?.total_analyses || 0 },
                { name: 'Evaluations', value: metrics?.total_evaluations || 0 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        {/* System Health */}
        <Card>
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">System Health</h2>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">API Health</span>
                  <Badge variant={health?.status === 'healthy' ? 'success' : 'error'}>
                    {health?.status === 'healthy' ? '✓ Healthy' : '✗ Error'}
                  </Badge>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '95%' }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Knowledge Base</span>
                  <Badge variant="success">{health?.products_count || 0} Products</Badge>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <div className="bg-blue-500 h-2 rounded-full" style={{ width: '100%' }} />
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

export default Dashboard;
