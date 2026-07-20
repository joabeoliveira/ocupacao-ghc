'use client';

import React, { useState } from 'react';
import {
  usePendencias,
  usePendenciaCodigos,
  useAdicionarPendencia,
  useAtualizarPendencia
} from '@/lib/queries';
import { Button } from '../ui/Button';
import { Select } from '../ui/Select';
import { Badge } from '../ui/Badge';
import { Pendencia } from '@/types';
import { AlertCircle, CheckCircle2, Plus, Ban } from 'lucide-react';
import { cn } from '@/lib/utils';

interface PendenciasProps {
  prontuario: string;
}

export function Pendencias({ prontuario }: PendenciasProps) {
  const { data: pendencias, isLoading: loadingPendencias } = usePendencias(prontuario);
  const { data: codigos } = usePendenciaCodigos();
  const addMutation = useAdicionarPendencia(prontuario);
  const updateMutation = useAtualizarPendencia(prontuario);

  const [selectedCodigo, setSelectedCodigo] = useState('');

  const activeCodes = codigos || [
    { codigo: 'regulacao', rotulo: 'Regulação' },
    { codigo: 'antibioticoterapia', rotulo: 'Antibioticoterapia' },
    { codigo: 'exame_pendente', rotulo: 'Exame pendente' },
    { codigo: 'assistencia_social', rotulo: 'Assistência Social' },
    { codigo: 'fisioterapia', rotulo: 'Fisioterapia' }
  ];

  const handleAddPendencia = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCodigo) return;

    try {
      await addMutation.mutateAsync({ codigo: selectedCodigo });
      setSelectedCodigo('');
    } catch (err) {
      console.error(err);
    }
  };

  const handleTogglePendencia = async (id: number, resolvida: boolean) => {
    try {
      await updateMutation.mutateAsync({ id, resolvida });
    } catch (err) {
      console.error(err);
    }
  };

  const getRotulo = (code: string) => {
    const item = activeCodes.find((c: any) => c.codigo === code);
    return item ? item.rotulo : code.toUpperCase();
  };

  return (
    <div className="space-y-4 border border-slate-100 bg-slate-50/50 p-4 rounded-lg">
      <div className="flex items-center justify-between border-b border-slate-100 pb-2 mb-2">
        <div className="flex items-center space-x-2">
          <AlertCircle className="w-5 h-5 text-priority-vermelho" />
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-800">
            Pendências de Alta / Gargalos
          </h4>
        </div>
        <Badge variant="error" className="text-[9px]">Gargalos Ativos</Badge>
      </div>

      {/* Adding Form */}
      <form onSubmit={handleAddPendencia} className="flex items-end space-x-2">
        <div className="flex-1">
          <Select
            label="Novo Impeditivo"
            options={[
              { value: '', label: 'Selecione uma pendência...' },
              ...activeCodes.map((c: any) => ({ value: c.codigo, label: c.rotulo }))
            ]}
            value={selectedCodigo}
            onChange={(e) => setSelectedCodigo(e.target.value)}
          />
        </div>
        <Button
          type="submit"
          size="sm"
          disabled={addMutation.isPending || !selectedCodigo}
          className="h-9 inline-flex items-center space-x-1"
        >
          <Plus className="w-4 h-4" />
          <span>Sinalizar</span>
        </Button>
      </form>

      {/* List */}
      {loadingPendencias ? (
        <div className="py-6 text-center text-xs text-muted animate-pulse">
          Carregando barreiras de alta...
        </div>
      ) : (pendencias || []).length === 0 ? (
        <div className="text-center py-6 text-xs text-muted bg-emerald-50 text-emerald-800 border border-emerald-100 rounded p-4 flex items-center justify-center space-x-2 font-semibold">
          <CheckCircle2 className="w-4 h-4" />
          <span>Nenhum gargalo ou pendência ativa de alta para este paciente!</span>
        </div>
      ) : (
        <div className="space-y-2">
          {(pendencias || []).map((p: Pendencia) => (
            <div
              key={p.id}
              className={cn(
                'flex items-center justify-between p-3 rounded border text-xs font-medium transition-all duration-200',
                p.resolvida
                  ? 'bg-emerald-50/50 text-emerald-800 border-emerald-200/50 line-through'
                  : 'bg-white text-slate-800 border-slate-200 shadow-sm'
              )}
            >
              <div className="flex items-center space-x-3">
                <input
                  type="checkbox"
                  checked={p.resolvida}
                  onChange={(e) => handleTogglePendencia(p.id, e.target.checked)}
                  disabled={updateMutation.isPending}
                  className="w-4.5 h-4.5 text-ghc-blue border-slate-300 rounded focus:ring-ghc-blue cursor-pointer"
                />
                <span className="font-bold">{getRotulo(p.codigo)}</span>
              </div>
              <div>
                <Badge variant={p.resolvida ? 'success' : 'error'} className="text-[9px]">
                  {p.resolvida ? 'Resolvida' : 'Impedimento'}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
