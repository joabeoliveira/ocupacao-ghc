import React from 'react';
import { cn } from '@/lib/utils';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = 'text', label, error, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-text mb-1.5">
            {label}
          </label>
        )}
        <input
          type={type}
          className={cn(
            'flex w-full rounded border border-panel-border bg-white px-3 py-2 text-sm text-text transition-colors duration-200 placeholder:text-muted focus:border-ghc-blue focus:outline-none focus:ring-1 focus:ring-ghc-blue disabled:cursor-not-allowed disabled:bg-gray-100 disabled:opacity-50',
            error && 'border-priority-vermelho focus:border-priority-vermelho focus:ring-priority-vermelho',
            className
          )}
          ref={ref}
          {...props}
        />
        {error && (
          <p className="mt-1 text-xs text-priority-vermelho font-medium">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
