import React from 'react';
import { cn } from '@/lib/utils';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg';
}

export function Button({
  children,
  className,
  variant = 'primary',
  size = 'md',
  ...props
}: ButtonProps) {
  const baseStyle = 'inline-flex items-center justify-center font-medium transition-all duration-200 rounded focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-ghc-blue disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variants = {
    primary: 'bg-ghc-blue text-white hover:bg-ghc-blue-dark active:scale-[0.98]',
    secondary: 'bg-ghc-teal text-white hover:bg-ghc-teal-dark active:scale-[0.98]',
    outline: 'border border-panel-border text-text hover:bg-gray-50',
    ghost: 'text-text hover:bg-gray-100',
    danger: 'bg-priority-vermelho text-white hover:bg-red-800 active:scale-[0.98]',
    success: 'bg-success text-white hover:bg-emerald-800 active:scale-[0.98]',
  };

  const sizes = {
    sm: 'px-3 py-1.5 text-xs',
    md: 'px-4 py-2 text-sm',
    lg: 'px-5 py-2.5 text-base',
  };

  return (
    <button
      className={cn(baseStyle, variants[variant], sizes[size], className)}
      {...props}
    >
      {children}
    </button>
  );
}
