import React, { useState } from 'react';
import Card from '../components/Card';
import Button from '../components/Button';
import Badge from '../components/Badge';
import toast from 'react-hot-toast';

function BatchProcessor() {
  const [jobs, setJobs] = useState([]);
  const [jobId, setJobId] = useState('');
  const [showMonitor, setShowMonitor] = useState(false);

  const handleStartBatch = () => {
    const newJob = {
      id: `batch_${Date.now()}`,
      status: 'processing',
      progress: 0,
      startTime: new Date(),
      items: Math.floor(Math.random() * 10) + 1,
    };
    setJobs([...jobs, newJob]);
    toast.success(`Batch job ${newJob.id} started`);

    // Simulate progress
    const interval = setInterval(() => {
      setJobs(prevJobs =>
        prevJobs.map(job =>
          job.id === newJob.id
            ? { ...job, progress: Math.min(job.progress + Math.random() * 30, 100), status: job.progress >= 100 ? 'completed' : 'processing' }
            : job
        )
      );
    }, 2000);

    setTimeout(() => clearInterval(interval), 30000);
  };

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Batch Processor</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">Process multiple RFPs at once</p>
        </div>
        <Button onClick={handleStartBatch}>Start Batch Job</Button>
      </div>

      {/* Active Jobs */}
      <div className="space-y-4">
        {jobs.map(job => (
          <Card key={job.id}>
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">{job.id}</h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {job.items} RFPs • Started {job.startTime.toLocaleTimeString()}
                  </p>
                </div>
                <Badge variant={job.status === 'completed' ? 'success' : 'info'}>
                  {job.status === 'completed' ? '✓ Completed' : '⟳ Processing'}
                </Badge>
              </div>
              
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <div
                  className="bg-blue-500 h-2 rounded-full transition-all"
                  style={{ width: `${job.progress}%` }}
                />
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">{Math.round(job.progress)}% Complete</p>
            </div>
          </Card>
        ))}
        
        {jobs.length === 0 && (
          <Card>
            <div className="p-12 text-center">
              <p className="text-gray-500 dark:text-gray-400">No batch jobs yet. Start one to begin processing.</p>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}

export default BatchProcessor;
