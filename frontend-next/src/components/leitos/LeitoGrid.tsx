'use client';

import React, { useState } from 'react';
import { LeitoCard } from './LeitoCard';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';
import { Toggle } from '../ui/Toggle';
import { Pagination } from '../ui/Pagination';
import { Badge } from '../ui/Badge';
import { Paciente } from '@/types';
import {
  Grid,
  List,
  Search,
  Filter,
  FilterX,
  PlusCircle,
  Calendar,
  AlertTriangle
} from 'lucide-react';

interface LeitoGridProps {
  pacientes: Paciente[];
  totalItems: number;
  currentPage: number;
  onPageChange: (page: number) => void;
  filters: {
    nome: string;
    prontuario: string;
    unidade: string;
    especialidade: string;
    min_dias: string;
    idade_minima: string;
  };
  setFilters: React.Dispatch<React.SetStateAction<{
    nome: string;
    prontuario: string;
    unidade: string;
    especialidade: string;
    min_dias: string;
    idade_minima: string;
  }>>;
  onSelectPaciente: (prontuario: string) => void;
  isLoading: boolean;
}

export function LeitoGrid({
  pacientes,
  totalItems,
  currentPage,
  onPageChange,
  filters,
  setFilters,
  onSelectPaciente,
  isLoading
}: LeitoGridProps) {
  const [viewMode, setViewMode] = useState<string>('grid');

  const unidades = [
    { value: '', label: 'Todas as Unidades' },
    { value: 'HNSC', label: 'HNSC' },
    { value: 'HCR', label: 'HCR' },
    { value: 'HF', label: 'HF' },
    { value: 'HCS', label: 'HCS' },
    { value: 'HFB', label: 'HFB' }
  ];

  const especialidades = [
    { value: '', label: 'Todas as Especialidades' },
    { value: 'CLÍNICA MÉDICA', label: 'CLÍNICA MÉDICA' },
    { value: 'NEUROLOGIA', label: 'NEUROLOGIA' },
    { value: 'CARDIOLOGIA', label: 'CARDIOLOGIA' },
    { value: 'CIRURGIA GERAL', label: 'CIRURGIA GERAL' },
    { value: 'ONCOLOGIA', label: 'ONCOLOGIA' },
    { value: 'CIRURGIA VASCULAR', label: 'CIRURGIA VASCULAR' },
    { value: 'PEDIATRIA', label: 'PEDIATRIA' }
  ];

  const minDiasOptions = [
    { value: '', label: 'Qualquer Permanência' },
    { value: '15', label: '15 dias ou mais (Longa)' },
    { value: '30', label: '30 dias ou mais (Crítico)' },
    { value: '40', label: '40 dias ou mais (Extrema)' }
  ];

  const idadeMinimaOptions = [
    { value: '', label: 'Qualquer Idade' },
    { value: '60', label: '60+ anos (Geriátricos)' },
    { value: '75', label: '75+ anos (Geriátricos Extremos)' }
  ];

  const handleClearFilters = () => {
    setFilters({
      nome: '',
      prontuario: '',
      unidade: '',
      especialidade: '',
      min_dias: '',
      idade_minima: ''
    });
    onPageChange(1);
  };

  const getPriorityVariant = (days: number) => {
    if (days >= 40) return 'error';
    if (days >= 30) return 'warning';
    if (days >= 15) return 'default';
    return 'neutral';
  };

  return (
    <div className="space-y-6">
      {/* Filters Card */}
      <div className="bg-white p-5 rounded-lg border border-panel-border shadow-sm space-y-4">
        <div className="flex items-center justify-between border-b border-panel-border pb-3">
          <div className="flex items-center space-x-2">
            <Filter className="w-5 h-5 text-ghc-blue" />
            <h3 className="text-sm font-bold uppercase tracking-wider text-text">
              Filtros de Pesquisa & Busca Ativa
            </h3>
          </div>
          <div className="flex items-center space-x-3">
            <Toggle
              value={viewMode}
              onChange={setViewMode}
              options={[
                { value: 'grid', label: 'Leitos Grid', icon: <Grid className="w-4 h-4" /> },
                { value: 'table', label: 'Tabela Censo', icon: <List className="w-4 h-4" /> }
              ]}
            />
            <Button
              variant="outline"
              size="sm"
              onClick={handleClearFilters}
              className="inline-flex items-center space-x-1.5 text-xs text-muted font-bold"
            >
              <FilterX className="w-4 h-4" />
              <span>Limpar Filtros</span>
            </Button>
          </div>
        </div>

        {/* Filters Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
          <Input
            placeholder="Nome do Paciente..."
            value={filters.nome}
            onChange={(e) => {
              setFilters((prev) => ({ ...prev, nome: e.target.value }));
              onPageChange(1);
            }}
            className="h-9"
          />
          <Input
            placeholder="Nº Prontuário..."
            value={filters.prontuario}
            onChange={(e) => {
              setFilters((prev) => ({ ...prev, prontuario: e.target.value }));
              onPageChange(1);
            }}
            className="h-9 font-mono"
          />
          <Select
            options={unidades}
            value={filters.unidade}
            onChange={(e) => {
              setFilters((prev) => ({ ...prev, unidade: e.target.value }));
              onPageChange(1);
            }}
            className="h-9"
          />
          <Select
            options={especialidades}
            value={filters.especialidade}
            onChange={(e) => {
              setFilters((prev) => ({ ...prev, especialidade: e.target.value }));
              onPageChange(1);
            }}
            className="h-9"
          />
          <Select
            options={minDiasOptions}
            value={filters.min_dias}
            onChange={(e) => {
              setFilters((prev) => ({ ...prev, min_dias: e.target.value }));
              onPageChange(1);
            }}
            className="h-9"
          />
          <Select
            options={idadeMinimaOptions}
            value={filters.idade_minima}
            onChange={(e) => {
              setFilters((prev) => ({ ...prev, idade_minima: e.target.value }));
              onPageChange(1);
            }}
            className="h-9"
          />
        </div>
      </div>

      {/* Grid or Table listing based on toggled mode */}
      {isLoading ? (
        <div className="py-20 flex flex-col items-center justify-center space-y-3">
          <div className="w-12 h-12 border-4 border-ghc-blue/30 border-t-ghc-blue rounded-full animate-spin"></div>
          <p className="text-sm text-muted font-medium">Buscando censo do EGAA...</p>
        </div>
      ) : pacientes.length === 0 ? (
        <div className="bg-white rounded-lg border border-panel-border p-16 text-center space-y-4 shadow-sm">
          <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mx-auto text-muted">
            <FilterX className="w-6 h-6" />
          </div>
          <h4 className="text-base font-bold text-text uppercase">Nenhum paciente encontrado</h4>
          <p className="text-sm text-muted max-w-md mx-auto">
            Não existem pacientes com os filtros selecionados. Tente ajustar os campos de busca ativa ou limpar os filtros.
          </p>
          <Button variant="outline" size="sm" onClick={handleClearFilters}>
            Resetar Busca Ativa
          </Button>
        </div>
      ) : viewMode === 'grid' ? (
        /* Dense Beds Grid View */
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
          {pacientes.map((paciente) => (
            <LeitoCard
              key={paciente.prontuario}
              paciente={paciente}
              onClick={() => onSelectPaciente(paciente.prontuario)}
            />
          ))}
        </div>
      ) : (
        /* Detailed Table View */
        <div className="bg-white rounded-lg border border-panel-border shadow-sm overflow-hidden overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-panel-border bg-gray-50/50 text-[10px] uppercase font-bold text-muted tracking-wider">
                <th className="px-6 py-3">Prontuário</th>
                <th className="px-6 py-3">Paciente</th>
                <th className="px-6 py-3">Idade</th>
                <th className="px-6 py-3">Permanência</th>
                <th className="px-6 py-3">Especialidade</th>
                <th className="px-6 py-3">Unidade</th>
                <th className="px-6 py-3">Ala / Enfermaria</th>
                <th className="px-6 py-3 text-right">Ação</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-panel-border">
              {pacientes.map((paciente) => (
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
                    >
                      Acompanhar
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Pagination component */}
      {!isLoading && pacientes.length > 0 && (
        <Pagination
          currentPage={currentPage}
          totalItems={totalItems}
          pageSize={10}
          onPageChange={onPageChange}
        />
      )}
    </div>
  );
}
