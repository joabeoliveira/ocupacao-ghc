'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';

interface UnitData {
  unidade: string;
  total_pacientes: number;
}

interface GraficoUnidadeProps {
  data: UnitData[];
  isLoading: boolean;
}

export function GraficoUnidade({ data, isLoading }: GraficoUnidadeProps) {
  if (isLoading) {
    return (
      <Card className="h-[380px]">
        <CardHeader>
          <div className="h-5 bg-gray-200 rounded w-1/3 animate-pulse"></div>
          <div className="h-3 bg-gray-200 rounded w-1/2 animate-pulse mt-2"></div>
        </CardHeader>
        <CardContent className="h-[280px] flex items-center justify-center">
          <div className="w-10 h-10 border-4 border-ghc-blue/30 border-t-ghc-blue rounded-full animate-spin"></div>
        </CardContent>
      </Card>
    );
  }

  // Soft palette of GHC colors to rotate through the bars
  const colors = ['#005C99', '#00A79D', '#0288D1', '#2E7D32', '#004A7A'];

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white border border-panel-border px-3 py-2 rounded shadow-md">
          <p className="text-xs font-bold text-text uppercase tracking-wider mb-0.5">
            {payload[0].payload.unidade}
          </p>
          <p className="text-xs text-ghc-blue font-semibold">
            {payload[0].value} pacientes internados
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card className="h-[380px] flex flex-col justify-between">
      <CardHeader className="flex-shrink-0">
        <CardTitle>Ocupação por Unidade Hospitalar</CardTitle>
        <CardDescription>
          Distribuição em tempo real do censo de pacientes ativos por hospital do grupo
        </CardDescription>
      </CardHeader>
      <CardContent className="flex-1 min-h-0 pb-6 pr-6">
        <div className="w-full h-full min-h-[220px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data}
              margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
            >
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E2E8F0" />
              <XAxis
                dataKey="unidade"
                tick={{ fill: '#64748B', fontSize: 11, fontWeight: 600 }}
                axisLine={{ stroke: '#CBD5E1' }}
                tickLine={false}
              />
              <YAxis
                tick={{ fill: '#64748B', fontSize: 11 }}
                axisLine={false}
                tickLine={false}
              />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: '#f8fafc' }} />
              <Bar dataKey="total_pacientes" radius={[4, 4, 0, 0]} maxBarSize={48}>
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
