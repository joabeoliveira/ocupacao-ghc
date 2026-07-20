import React from 'react';
import { cn } from '@/lib/utils';

interface ToggleProps {
  value: string;
  onChange: (value: string) => void;
  options: {
    value: string;
    label: string;
    icon?: React.ReactNode;
  }[];
  className?: string;
}

export function Toggle({ value, onChange, options, className }: ToggleProps) {
  return (
    <div className={cn('inline-flex bg-gray-100 p-1 rounded-lg border border-gray-200 shadow-inner', className)}>
      {options.map((option) => {
        const isActive = value === option.value;
        return (
          <button
            key={option.value}
            type="button"
            onClick={() => onChange(option.value)}
            className={cn(
              'inline-flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold rounded-md transition-all duration-200 focus:outline-none',
              isActive
                ? 'bg-white text-ghc-blue shadow-sm ring-1 ring-black/5'
                : 'text-muted hover:text-text'
            )}
          >
            {option.icon && <span className="w-4 h-4">{option.icon}</span>}
            <span>{option.label}</span>
          </button>
        );
      })}
    </div>
  );
}
