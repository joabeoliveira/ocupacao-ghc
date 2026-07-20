import React from 'react';
import { cn } from '@/lib/utils';

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info' | 'neutral';
}

export function Badge({ children, className, variant = 'default', ...props }: BadgeProps) {
  const styles = {
    default: 'bg-ghc-blue-light text-ghc-blue border border-ghc-blue/20',
    success: 'bg-success/10 text-success border border-success/20',
    warning: 'bg-priority-laranja/10 text-priority-laranja border border-priority-laranja/20',
    error: 'bg-priority-vermelho/10 text-priority-vermelho border border-priority-vermelho/20',
    info: 'bg-info/10 text-info border border-info/20',
    neutral: 'bg-gray-100 text-gray-700 border border-gray-200',
  };

  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold uppercase tracking-wider',
        styles[variant],
        className
      )}
      {...props}
    >
      {children}
    </span>
  );
}
