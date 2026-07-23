import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  loading?: boolean;
}

function Button({ children, variant = 'primary', loading = false, disabled, ...props }: ButtonProps) {
  const baseClass = 'px-4 py-2 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2';
  const variantClass = variant === 'primary'
    ? 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500'
    : 'bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500';

  return (
    <button
      className={`${baseClass} ${variantClass} ${disabled || loading ? 'opacity-50 cursor-not-allowed' : ''}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? '⟳ Loading...' : children}
    </button>
  );
}

export default Button;
