import React from 'react';
import classNames from 'classnames';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'success' | 'warning' | 'error' | 'info' | 'secondary';
  className?: string;
}

function Badge({ children, variant = 'secondary', className = '' }: BadgeProps) {
  const variantClass = {
    success: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    warning: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    error: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    info: 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
    secondary: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200',
  };

  return (
    <span className={classNames('inline-flex items-center px-3 py-1 rounded-full text-sm font-medium', variantClass[variant], className)}>
      {children}
    </span>
  );
}

export default Badge;
