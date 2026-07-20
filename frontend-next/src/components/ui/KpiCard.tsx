import React from 'react';
import { Card, CardContent } from './Card';
import { cn } from '@/lib/utils';

interface KpiCardProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  subtitle?: string;
  trend?: {
    value: string;
    isPositive?: boolean;
  };
  className?: string;
}

export function KpiCard({ title, value, icon, subtitle, trend, className }: KpiCardProps) {
  return (
    <Card className={cn('hover:shadow-md transition-shadow duration-300', className)}>
      <CardContent className="p-5 flex items-start justify-between">
        <div className="space-y-1">
          <p className="text-xs font-semibold uppercase tracking-wider text-muted">
            {title}
          </p>
          <div className="flex items-baseline space-x-1.5">
            <h4 className="text-2xl font-bold text-text tracking-tight">
              {value}
            </h4>
            {trend && (
              <span
                className={cn(
                  'text-xs font-semibold px-1 rounded',
                  trend.isPositive ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
                )}
              >
                {trend.value}
              </span>
            )}
          </div>
          {subtitle && (
            <p className="text-[11px] text-muted">
              {subtitle}
            </p>
          )}
        </div>
        {icon && (
          <div className="p-2.5 bg-gray-50 text-ghc-blue rounded-lg border border-gray-100">
            {icon}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
