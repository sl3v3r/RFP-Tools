import React from 'react';
import { Link } from 'react-router-dom';
import { Moon, Sun } from 'react-feather';

interface NavigationProps {
  darkMode: boolean;
  onToggleDark: () => void;
}

function Navigation({ darkMode, onToggleDark }: NavigationProps) {
  return (
    <nav className="bg-white dark:bg-gray-800 shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <span className="text-xl font-bold text-blue-600 dark:text-blue-400">🎯 RFP Tools</span>
            </Link>
            <div className="hidden md:flex ml-10 space-x-4">
              <NavLink to="/">Dashboard</NavLink>
              <NavLink to="/analyze">Analyze</NavLink>
              <NavLink to="/evaluate">Evaluate</NavLink>
              <NavLink to="/products">Products</NavLink>
              <NavLink to="/batch">Batch</NavLink>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <button
              onClick={onToggleDark}
              className="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              {darkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

function NavLink({ to, children }: { to: string; children: React.ReactNode }) {
  return (
    <Link
      to={to}
      className="px-3 py-2 rounded-md text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700"
    >
      {children}
    </Link>
  );
}

export default Navigation;
