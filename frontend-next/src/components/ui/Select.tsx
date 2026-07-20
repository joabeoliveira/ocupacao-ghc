import React from 'react';
import { cn } from '@/lib/utils';

interface SelectOption {
  value: string | number;
  label: string;
}

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  options: SelectOption[];
  error?: string;
}

export const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, label, options, error, ...props }, ref) => {
    return (
      <div className="w-full">
        {label && (
          <label className="block text-sm font-medium text-text mb-1.5">
            {label}
          </label>
        )}
        <select
          className={cn(
            'flex w-full rounded border border-panel-border bg-white px-3 py-2 text-sm text-text transition-colors duration-200 focus:border-ghc-blue focus:outline-none focus:ring-1 focus:ring-ghc-blue disabled:cursor-not-allowed disabled:bg-gray-100 disabled:opacity-50',
            error && 'border-priority-vermelho focus:border-priority-vermelho focus:ring-priority-vermelho',
            className
          )}
          ref={ref}
          {...props}
        >
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        {error && (
          <p className="mt-1 text-xs text-priority-vermelho font-medium">
            {error}
          </p>
        )}
      </div>
    );
  }
);

Select.displayName = 'Select';
