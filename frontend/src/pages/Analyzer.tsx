import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import api from '../services/api';
import Card from '../components/Card';
import Button from '../components/Button';
import toast from 'react-hot-toast';

function Analyzer() {
  const [rfpText, setRfpText] = useState('');
  const [useMultiAgent, setUseMultiAgent] = useState(true);
  const [result, setResult] = useState(null);

  const analyzeMutation = useMutation({
    mutationFn: (data) => api.post('/analyze', data),
    onSuccess: (response) => {
      setResult(response.data);
      toast.success('RFP analyzed successfully!');
    },
    onError: (error) => {
      toast.error('Error analyzing RFP: ' + error.message);
    },
  });

  const handleAnalyze = () => {
    if (!rfpText.trim()) {
      toast.error('Please enter RFP text');
      return;
    }
    analyzeMutation.mutate({
      rfp_text: rfpText,
      use_multi_agent: useMultiAgent,
    });
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">RFP Analyzer</h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">Analyze RFP documents and generate responses</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input */}
        <Card>
          <div className="p-6">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Input RFP</h2>
            
            <textarea
              value={rfpText}
              onChange={(e) => setRfpText(e.target.value)}
              placeholder="Paste your RFP document here..."
              className="w-full h-64 p-4 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <div className="mt-4 space-y-3">
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={useMultiAgent}
                  onChange={(e) => setUseMultiAgent(e.target.checked)}
                  className="w-4 h-4 text-blue-600 rounded"
                />
                <span className="ml-2 text-sm text-gray-700 dark:text-gray-300">
                  Use multi-agent orchestration
                </span>
              </label>
            </div>

            <Button
              onClick={handleAnalyze}
              loading={analyzeMutation.isPending}
              className="w-full mt-4"
            >
              Analyze RFP
            </Button>
          </div>
        </Card>

        {/* Output */}
        {result && (
          <Card>
            <div className="p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Analysis Result</h2>
              
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {result.analysis && (
                  <div>
                    <h3 className="font-medium text-gray-900 dark:text-white mb-2">Requirements</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">
                      {typeof result.analysis === 'string' ? result.analysis : JSON.stringify(result.analysis).substring(0, 200)}
                    </p>
                  </div>
                )}

                {result.sections && (
                  <div>
                    <h3 className="font-medium text-gray-900 dark:text-white mb-2">Response Sections</h3>
                    {Object.entries(result.sections).map(([key, value]) => (
                      <div key={key} className="mb-2">
                        <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase">{key}</p>
                        <p className="text-sm text-gray-600 dark:text-gray-300">
                          {typeof value === 'string' ? value.substring(0, 100) : JSON.stringify(value).substring(0, 100)}
                        </p>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <Button variant="secondary" className="w-full mt-4">
                Download Report
              </Button>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

export default Analyzer;
