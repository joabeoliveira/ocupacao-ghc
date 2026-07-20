'use client';

import React, { useState, useEffect } from 'react';
import { useAtualizarEvolucao } from '@/lib/queries';
import { Button } from '../ui/Button';
import { FileText, Save } from 'lucide-react';

interface EvolucaoProps {
  prontuario: string;
  initialEvolucao: string | null;
  onSuccess: () => void;
}

export function Evolucao({ prontuario, initialEvolucao, onSuccess }: EvolucaoProps) {
  const updateMutation = useAtualizarEvolucao(prontuario);
  const [evolucao, setEvolucao] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    setEvolucao(initialEvolucao || '');
  }, [initialEvolucao]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await updateMutation.mutateAsync({ evolucao });
      onSuccess();
    } catch (err) {
      setError('Erro ao salvar evolução clínica.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 border border-slate-100 bg-slate-50/50 p-4 rounded-lg">
      <div className="flex items-center space-x-2 border-b border-slate-100 pb-2 mb-2">
        <FileText className="w-5 h-5 text-ghc-blue" />
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-800">
          Evolução Clínica Geral (Censo)
        </h4>
      </div>

      {error && (
        <div className="bg-red-50 text-priority-vermelho px-3 py-2 rounded text-xs font-semibold border border-red-200">
          {error}
        </div>
      )}

      <div>
        <textarea
          rows={5}
          className="flex w-full rounded border border-panel-border bg-white px-3 py-2 text-sm text-text transition-colors duration-200 placeholder:text-muted focus:border-ghc-blue focus:outline-none focus:ring-1 focus:ring-ghc-blue"
          placeholder="Insira notas do censo diário hospitalar, histórico de intercorrências ou plano terapêutico integrado..."
          value={evolucao}
          onChange={(e) => setEvolucao(e.target.value)}
        />
      </div>

      <div className="flex justify-end">
        <Button
          type="submit"
          disabled={updateMutation.isPending}
          className="inline-flex items-center space-x-1.5"
          size="sm"
        >
          {updateMutation.isPending ? (
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <Save className="w-4 h-4" />
          )}
          <span>Salvar Notas de Evolução</span>
        </Button>
      </div>
    </form>
  );
}
