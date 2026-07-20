'use client';

import React, { useState } from 'react';
import { usePaciente, useIntervencoes } from '@/lib/queries';
import { Modal } from '../ui/Modal';
import { Badge } from '../ui/Badge';
import { Timeline } from './Timeline';
import { NovaAtuacao } from './NovaAtuacao';
import { Pendencias } from './Pendencias';
import { Evolucao } from './Evolucao';
import {
  Calendar,
  Clock,
  User,
  Heart,
  Activity,
  CheckCircle,
  FileText,
  AlertOctagon
} from 'lucide-react';
import { cn } from '@/lib/utils';

interface ModalPacienteProps {
  prontuario: string | null;
  isOpen: boolean;
  onClose: () => void;
}

export function ModalPaciente({ prontuario, isOpen, onClose }: ModalPacienteProps) {
  const { data: paciente, isLoading: loadingPaciente, refetch: refetchPaciente } = usePaciente(prontuario || '');
  const { data: intervencoes, isLoading: loadingIntervencoes, refetch: refetchIntervencoes } = useIntervencoes(prontuario || '');

  const [activeTab, setActiveTab] = useState<'timeline' | 'evolucao' | 'pendencias'>('timeline');

  if (!isOpen || !prontuario) return null;

  const handleAtuacoesSuccess = () => {
    refetchIntervencoes();
    refetchPaciente();
  };

  const handleEvolucaoSuccess = () => {
    refetchPaciente();
  };

  const getPriorityVariant = (days: number) => {
    if (days >= 40) return 'error';
    if (days >= 30) return 'warning';
    if (days >= 15) return 'default';
    return 'neutral';
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={loadingPaciente ? 'Carregando Ficha...' : `Prontuário: ${paciente?.prontuario || prontuario}`}
      size="4xl"
    >
      {loadingPaciente ? (
        <div className="py-20 flex flex-col items-center justify-center space-y-4">
          <div className="w-12 h-12 border-4 border-ghc-blue/30 border-t-ghc-blue rounded-full animate-spin"></div>
          <p className="text-sm text-muted font-semibold uppercase tracking-wider">Acessando prontuário GHC...</p>
        </div>
      ) : !paciente ? (
        <div className="py-12 text-center text-sm text-muted font-bold">
          Falha ao carregar prontuário ou paciente não localizado no censo.
        </div>
      ) : (
        <div className="space-y-6">
          {/* Patient Card Header Banner */}
          <div className="bg-slate-50 border border-slate-200/60 p-5 rounded-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div className="space-y-2">
              <div className="flex items-center space-x-2.5">
                <span className="text-sm font-extrabold text-slate-800 tracking-wider uppercase bg-slate-100 px-2.5 py-1 rounded border border-slate-200">
                  {paciente.leito || 'S/L'}
                </span>
                <h3 className="text-lg font-black text-ghc-blue uppercase tracking-tight">
                  {paciente.nome_paciente}
                </h3>
              </div>
              <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs text-muted">
                <span className="flex items-center space-x-1">
                  <User className="w-4 h-4 text-muted" />
                  <span>{paciente.idade_anos} anos</span>
                </span>
                <span>•</span>
                <span>Unidade: <strong className="text-text font-bold">{paciente.unidade}</strong></span>
                <span>•</span>
                <span>Especialidade: <strong className="text-text font-bold">{paciente.especialidade}</strong></span>
                <span>•</span>
                <span>Leito: <strong className="text-text font-bold">{paciente.enfermaria}</strong></span>
              </div>
            </div>

            {/* Stay time Badge */}
            <div className="flex flex-col items-end gap-1.5 self-start md:self-auto">
              <div className="flex items-center space-x-2">
                <Calendar className="w-4 h-4 text-muted" />
                <span className="text-sm font-black text-slate-800">{paciente.dias_internacao} dias internado</span>
                <Badge variant={getPriorityVariant(paciente.dias_internacao || 0)}>
                  {paciente.dias_internacao && paciente.dias_internacao >= 40 ? 'Crítico 40d+' : paciente.dias_internacao && paciente.dias_internacao >= 30 ? 'Alerta 30d+' : 'Geral 15d+'}
                </Badge>
              </div>
              <p className="text-[10px] text-muted font-medium uppercase tracking-tight">
                CID: <span className="font-bold text-slate-700">{paciente.cid_internacao_codigo}</span> - {paciente.cid_internacao_descricao}
              </p>
            </div>
          </div>

          {/* Quick clinical stats summary banner */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-semibold">
            <div className="bg-emerald-50/50 text-emerald-800 border border-emerald-100 p-3 rounded-lg flex items-center space-x-2">
              <CheckCircle className="w-5 h-5 flex-shrink-0 text-emerald-600" />
              <span>{paciente.egaa_total_atuacoes || 0} Atuações EGAA registradas | Última: {paciente.egaa_ultima_atuacao || 'Sem registro'}</span>
            </div>
            {paciente.evolucao ? (
              <div className="bg-sky-50 text-sky-800 border border-sky-100 p-3 rounded-lg flex items-center space-x-2">
                <FileText className="w-5 h-5 flex-shrink-0 text-sky-600" />
                <span className="truncate">Notas ativas do Censo: &ldquo;{paciente.evolucao}&rdquo;</span>
              </div>
            ) : (
              <div className="bg-amber-50 text-amber-800 border border-amber-100 p-3 rounded-lg flex items-center space-x-2">
                <AlertOctagon className="w-5 h-5 flex-shrink-0 text-amber-600" />
                <span>Nenhuma nota de evolução clínica registrada neste prontuário ainda.</span>
              </div>
            )}
          </div>

          {/* Tabs header */}
          <div className="flex border-b border-panel-border space-x-6">
            <button
              onClick={() => setActiveTab('timeline')}
              className={cn(
                'pb-3 text-xs font-bold uppercase tracking-wider transition-all duration-200 border-b-2 focus:outline-none',
                activeTab === 'timeline'
                  ? 'border-ghc-blue text-ghc-blue font-black'
                  : 'border-transparent text-muted hover:text-text'
              )}
            >
              Histórico &amp; Atuações
            </button>
            <button
              onClick={() => setActiveTab('evolucao')}
              className={cn(
                'pb-3 text-xs font-bold uppercase tracking-wider transition-all duration-200 border-b-2 focus:outline-none',
                activeTab === 'evolucao'
                  ? 'border-ghc-blue text-ghc-blue font-black'
                  : 'border-transparent text-muted hover:text-text'
              )}
            >
              Evolução Clínica Geral
            </button>
            <button
              onClick={() => setActiveTab('pendencias')}
              className={cn(
                'pb-3 text-xs font-bold uppercase tracking-wider transition-all duration-200 border-b-2 focus:outline-none',
                activeTab === 'pendencias'
                  ? 'border-ghc-blue text-ghc-blue font-black'
                  : 'border-transparent text-muted hover:text-text'
              )}
            >
              Gargalos de Alta
            </button>
          </div>

          {/* Tab content wrappers */}
          <div className="min-h-[280px]">
            {activeTab === 'timeline' && (
              <div className="space-y-6">
                <NovaAtuacao prontuario={paciente.prontuario} onSuccess={handleAtuacoesSuccess} />
                <div className="border-t border-slate-100 pt-4">
                  <h4 className="text-xs font-extrabold uppercase tracking-widest text-slate-500 mb-4">
                    Histórico de Acompanhamento EGAA
                  </h4>
                  <Timeline
                    intervencoes={intervencoes || []}
                    isLoading={loadingIntervencoes}
                  />
                </div>
              </div>
            )}

            {activeTab === 'evolucao' && (
              <Evolucao
                prontuario={paciente.prontuario}
                initialEvolucao={paciente.evolucao}
                onSuccess={handleEvolucaoSuccess}
              />
            )}

            {activeTab === 'pendencias' && (
              <Pendencias prontuario={paciente.prontuario} />
            )}
          </div>
        </div>
      )}
    </Modal>
  );
}
