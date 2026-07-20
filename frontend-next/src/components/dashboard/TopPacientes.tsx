'use client';

import React from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { Paciente } from '@/types';
import { ChevronRight, Calendar } from 'lucide-react';

interface TopPacientesProps {
  pacientes: Paciente[];
  isLoading: boolean;
  onSelectPaciente: (prontuario: string) => void;
}

export function TopPacientes({ pacientes, isLoading, onSelectPaciente }: TopPacientesProps) {
  const getPriorityVariant = (days: number) => {
    if (days >= 40) return 'error'; // Dark red priority
    if (days >= 30) return 'warning'; // Orange/red
    if (days >= 15) return 'default'; // Blue-ish general long permanency
    return 'neutral';
  };

  if (isLoading) {
    return (
      <Card>
        <CardHeader>
          <div className="h-5 bg-gray-200 rounded w-1/4 animate-pulse"></div>
        </CardHeader>
        <CardContent className="space-y-4">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="flex justify-between items-center py-2">
              <div className="h-4 bg-gray-200 rounded w-1/3 animate-pulse"></div>
              <div className="h-4 bg-gray-200 rounded w-1/12 animate-pulse"></div>
            </div>
          ))}
        </CardContent>
      </Card>
    );
  }

  // Take the first 10 patients
  const top10 = pacientes.slice(0, 10);

  return (
    <Card className="shadow-sm border border-panel-border">
      <CardHeader className="flex flex-row items-center justify-between">
        <div>
          <CardTitle>Top 10 Pacientes com Maior Tempo de Internação</CardTitle>
          <CardDescription>
            Casos críticos de longa permanência necessitando monitoramento ativo da regulação
          </CardDescription>
        </div>
        <Badge variant="error" className="h-fit">Alerta Crítico</Badge>
      </CardHeader>
      <CardContent className="p-0 overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-panel-border bg-gray-50/50 text-[10px] uppercase font-bold text-muted tracking-wider">
              <th className="px-6 py-3">Prontuário</th>
              <th className="px-6 py-3">Paciente</th>
              <th className="px-6 py-3">Idade</th>
              <th className="px-6 py-3">Tempo Internação</th>
              <th className="px-6 py-3">Especialidade</th>
              <th className="px-6 py-3">Unidade</th>
              <th className="px-6 py-3">Leito</th>
              <th className="px-6 py-3 text-right">Ação</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-panel-border">
            {top10.length === 0 ? (
              <tr>
                <td colSpan={8} className="px-6 py-10 text-center text-sm text-muted">
                  Nenhum paciente crítico de longa permanência encontrado.
                </td>
              </tr>
            ) : (
              top10.map((paciente) => (
                <tr
                  key={paciente.prontuario}
                  className="hover:bg-slate-50/50 transition-colors duration-150 text-xs"
                >
                  <td className="px-6 py-3.5 font-semibold text-text font-mono">
                    {paciente.prontuario}
                  </td>
                  <td className="px-6 py-3.5 font-bold text-ghc-blue uppercase">
                    {paciente.nome_paciente}
                  </td>
                  <td className="px-6 py-3.5 text-text">
                    {paciente.idade_anos} anos
                  </td>
                  <td className="px-6 py-3.5">
                    <div className="flex items-center space-x-2">
                      <Calendar className="w-3.5 h-3.5 text-muted" />
                      <span className="font-bold">{paciente.dias_internacao} dias</span>
                      <Badge variant={getPriorityVariant(paciente.dias_internacao || 0)}>
                        {paciente.dias_internacao && paciente.dias_internacao >= 40 ? 'Crítico 40d+' : paciente.dias_internacao && paciente.dias_internacao >= 30 ? 'Alerta 30d+' : 'Geral 15d+'}
                      </Badge>
                    </div>
                  </td>
                  <td className="px-6 py-3.5 text-muted font-medium uppercase text-[10px] tracking-wider">
                    {paciente.especialidade}
                  </td>
                  <td className="px-6 py-3.5 font-semibold text-text">
                    {paciente.unidade}
                  </td>
                  <td className="px-6 py-3.5 font-semibold text-ghc-teal">
                    {paciente.enfermaria} — {paciente.leito}
                  </td>
                  <td className="px-6 py-3.5 text-right">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => onSelectPaciente(paciente.prontuario)}
                      className="inline-flex items-center space-x-1"
                    >
                      <span>Acompanhar</span>
                      <ChevronRight className="w-3 h-3" />
                    </Button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </CardContent>
    </Card>
  );
}
