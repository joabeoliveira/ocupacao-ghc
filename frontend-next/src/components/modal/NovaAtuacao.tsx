'use client';

import React, { useState } from 'react';
import { useCriarIntervencao, useTiposIntervencao } from '@/lib/queries';
import { Button } from '../ui/Button';
import { Input } from '../ui/Input';
import { Select } from '../ui/Select';
import { useAuth } from '@/lib/auth';
import { TipoIntervencao } from '@/types';
import { Sparkles, ClipboardList } from 'lucide-react';

interface NovaAtuacaoProps {
  prontuario: string;
  onSuccess: () => void;
}

export function NovaAtuacao({ prontuario, onSuccess }: NovaAtuacaoProps) {
  const { usuario } = useAuth();
  const { data: tipos, isLoading: loadingTipos } = useTiposIntervencao();
  const createIntervencao = useCriarIntervencao();

  const [formData, setFormData] = useState({
    tipo_intervencao_id: '',
    titulo: '',
    descricao: '',
    status: 'concluida', // Default to completed action
    observacao: ''
  });

  const [formError, setFormError] = useState('');

  const activeTipos = (tipos || []).filter((t: TipoIntervencao) => t.ativo);

  const selectOptions = [
    { value: '', label: 'Selecione um Tipo...' },
    ...activeTipos.map((t: TipoIntervencao) => ({
      value: String(t.id),
      label: t.nome
    }))
  ];

  const handleTipoChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    const selectedTipo = activeTipos.find((t: TipoIntervencao) => String(t.id) === val);
    
    setFormData(prev => ({
      ...prev,
      tipo_intervencao_id: val,
      titulo: selectedTipo ? selectedTipo.nome : ''
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError('');

    if (!formData.tipo_intervencao_id) {
      setFormError('Selecione o tipo de intervenção.');
      return;
    }
    if (!formData.descricao.trim()) {
      setFormError('Insira uma descrição textual da atuação.');
      return;
    }

    try {
      await createIntervencao.mutateAsync({
        prontuario,
        tipo_intervencao_id: Number(formData.tipo_intervencao_id),
        titulo: formData.titulo,
        descricao: formData.descricao,
        status: formData.status,
        usuario_responsavel: usuario?.nome || 'CLÍNICO EGAA',
        data_atuacao: new Date().toISOString().split('T')[0]
      });

      // Reset form
      setFormData({
        tipo_intervencao_id: '',
        titulo: '',
        descricao: '',
        status: 'concluida',
        observacao: ''
      });
      onSuccess();
    } catch (err) {
      setFormError('Erro ao registrar atuação clínica. Tente novamente.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 border border-slate-100 bg-slate-50/50 p-4 rounded-lg">
      <div className="flex items-center space-x-2 border-b border-slate-100 pb-2 mb-2">
        <ClipboardList className="w-5 h-5 text-ghc-blue" />
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-800">
          Registrar Nova Atuação EGAA
        </h4>
      </div>

      {formError && (
        <div className="bg-red-50 text-priority-vermelho px-3 py-2 rounded text-xs font-semibold border border-red-200">
          {formError}
        </div>
      )}

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Select
          label="Tipo de Atuação"
          options={selectOptions}
          value={formData.tipo_intervencao_id}
          onChange={handleTipoChange}
          disabled={loadingTipos}
        />
        <Select
          label="Status da Atuação"
          options={[
            { value: 'concluida', label: 'Concluída / Executada' },
            { value: 'em_andamento', label: 'Em Andamento / Agendada' }
          ]}
          value={formData.status}
          onChange={(e) => setFormData(prev => ({ ...prev, status: e.target.value }))}
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-text mb-1.5">
          Descrição Técnica / Relato Clínico
        </label>
        <textarea
          rows={3}
          className="flex w-full rounded border border-panel-border bg-white px-3 py-2 text-sm text-text transition-colors duration-200 placeholder:text-muted focus:border-ghc-blue focus:outline-none focus:ring-1 focus:ring-ghc-blue"
          placeholder="Descreva as ações de desospitalização executadas, contato familiar ou andamento do plano de alta..."
          value={formData.descricao}
          onChange={(e) => setFormData(prev => ({ ...prev, descricao: e.target.value }))}
        />
      </div>

      <div className="flex justify-end pt-2">
        <Button
          type="submit"
          disabled={createIntervencao.isPending}
          className="inline-flex items-center space-x-1.5"
          size="sm"
        >
          {createIntervencao.isPending ? (
            <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <Sparkles className="w-4 h-4" />
          )}
          <span>Salvar Atuação</span>
        </Button>
      </div>
    </form>
  );
}
