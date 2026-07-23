import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import Analyzer from './pages/Analyzer';
import Evaluator from './pages/Evaluator';
import Products from './pages/Products';
import BatchProcessor from './pages/BatchProcessor';
import './App.css';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <Router>
      <div className={darkMode ? 'dark' : ''}>
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
          <Navigation darkMode={darkMode} onToggleDark={() => setDarkMode(!darkMode)} />
          
          <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analyze" element={<Analyzer />} />
              <Route path="/evaluate" element={<Evaluator />} />
              <Route path="/products" element={<Products />} />
              <Route path="/batch" element={<BatchProcessor />} />
            </Routes>
          </main>
        </div>
        <Toaster />
      </div>
    </Router>
  );
}

export default App;
