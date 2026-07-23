import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import api from '../services/api';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import toast from 'react-hot-toast';

function Evaluator() {
  const [rfpText, setRfpText] = useState('');
  const [responseText, setResponseText] = useState('');
  const [evalResult, setEvalResult] = useState(null);

  const evaluateMutation = useMutation({
    mutationFn: (data) => api.post('/evaluate', data),
    onSuccess: (response) => {
      setEvalResult(response.data);
      toast.success('Response evaluated successfully!');
    },
    onError: (error) => {
      toast.error('Error evaluating response: ' + error.message);
    },
  });

  const handleEvaluate = () => {
    if (!rfpText.trim() || !responseText.trim()) {
      toast.error('Please enter both RFP and response text');
      return;
    }
    evaluateMutation.mutate({
      rfp_text: rfpText,
      response_text: responseText,
    });
  };

  const getRecommendationColor = (rec) => {
    switch (rec) {
      case 'Excellent': return 'success';
      case 'Good': return 'info';
      case 'Acceptable': return 'warning';
      default: return 'error';
    }
  };

  const chartData = evalResult ? [
    { name: 'Completeness', value: evalResult.sections.completeness.score },
    { name: 'Relevance', value: evalResult.sections.relevance.score },
    { name: 'Compliance', value: evalResult.sections.compliance.score },
    { name: 'Clarity', value: evalResult.sections.clarity.score },
    { name: 'Pricing', value: evalResult.sections.pricing.score },
  ] : [];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Response Evaluator</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">Evaluate RFP response quality with detailed metrics</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Inputs */}
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <div className="p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">RFP Text</h2>
              <textarea
                value={rfpText}
                onChange={(e) => setRfpText(e.target.value)}
                placeholder="Paste RFP text here..."
                className="w-full h-32 p-4 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </Card>

          <Card>
            <div className="p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Response Text</h2>
              <textarea
                value={responseText}
                onChange={(e) => setResponseText(e.target.value)}
                placeholder="Paste response text here..."
                className="w-full h-32 p-4 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500"
              />
              <Button onClick={handleEvaluate} loading={evaluateMutation.isPending} className="w-full mt-4">
                Evaluate Response
              </Button>
            </div>
          </Card>
        </div>

        {/* Results */}
        {evalResult && (
          <Card>
            <div className="p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Evaluation Results</h2>
              
              <div className="text-center mb-6">
                <p className="text-4xl font-bold text-blue-600">{evalResult.overall_score.toFixed(1)}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Overall Score</p>
                <Badge variant={getRecommendationColor(evalResult.recommendation)} className="mt-2 justify-center">
                  {evalResult.recommendation}
                </Badge>
              </div>

              <div className="space-y-2">
                {evalResult.analysis.strengths && evalResult.analysis.strengths.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold text-green-600 dark:text-green-400 uppercase">Strengths</p>
                    {evalResult.analysis.strengths.map((s, i) => (
                      <p key={i} className="text-xs text-gray-600 dark:text-gray-400 mb-1">✓ {s}</p>
                    ))}
                  </div>
                )}
                {evalResult.analysis.weaknesses && evalResult.analysis.weaknesses.length > 0 && (
                  <div>
                    <p className="text-xs font-semibold text-red-600 dark:text-red-400 uppercase">Weaknesses</p>
                    {evalResult.analysis.weaknesses.map((w, i) => (
                      <p key={i} className="text-xs text-gray-600 dark:text-gray-400 mb-1">✗ {w}</p>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </Card>
        )}
      </div>

      {/* Chart */}
      {evalResult && (
        <Card>
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Score Breakdown</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0, 100]} />
                <Tooltip />
                <Bar dataKey="value" fill="#3b82f6">
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.value >= 80 ? '#10b981' : entry.value >= 60 ? '#f59e0b' : '#ef4444'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>
      )}
    </div>
  );
}

export default Evaluator;
