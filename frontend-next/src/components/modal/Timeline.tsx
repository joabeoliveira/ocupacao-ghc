'use client';

import React from 'react';
import { Intervencao } from '@/types';
import { Calendar, User, Clock, CheckCircle2, AlertCircle } from 'lucide-react';
import { Badge } from '../ui/Badge';
import { cn } from '@/lib/utils';

interface TimelineProps {
  intervencoes: Intervencao[];
  isLoading: boolean;
}

export function Timeline({ intervencoes, isLoading }: TimelineProps) {
  if (isLoading) {
    return (
      <div className="space-y-4 py-4">
        {Array.from({ length: 2 }).map((_, idx) => (
          <div key={idx} className="flex space-x-3 animate-pulse">
            <div className="w-8 h-8 rounded-full bg-gray-200"></div>
            <div className="flex-1 space-y-2 py-1">
              <div className="h-3 bg-gray-200 rounded w-1/4"></div>
              <div className="h-3 bg-gray-200 rounded w-3/4"></div>
            </div>
          </div>
        ))}
      </div>
    );
  }

  // Sort interventions newest first
  const sorted = [...intervencoes].sort(
    (a, b) => {
      const dateB = b.data_atuacao ? new Date(b.data_atuacao).getTime() : 0;
      const dateA = a.data_atuacao ? new Date(a.data_atuacao).getTime() : 0;
      return dateB - dateA;
    }
  );

  return (
    <div className="space-y-6 relative border-l-2 border-slate-100 pl-6 ml-3 py-2">
      {sorted.length === 0 ? (
        <div className="text-center py-6 text-muted text-xs">
          Nenhuma intervenção registrada pelo EGAA para este paciente ainda.
        </div>
      ) : (
        sorted.map((item) => {
          const isConcluded = item.status === 'concluida';
          return (
            <div key={item.id} className="relative group">
              {/* Timeline dot */}
              <div
                className={cn(
                  'absolute -left-[35px] top-1.5 w-4 h-4 rounded-full border-2 bg-white flex items-center justify-center transition-all duration-200 group-hover:scale-110',
                  isConcluded ? 'border-ghc-teal' : 'border-priority-laranja'
                )}
              >
                <div
                  className={cn(
                    'w-1.5 h-1.5 rounded-full',
                    isConcluded ? 'bg-ghc-teal' : 'bg-priority-laranja'
                  )}
                />
              </div>

              {/* Card wrapper */}
              <div className="bg-slate-50 border border-slate-200/60 rounded-lg p-4 space-y-2 hover:border-slate-300 transition-colors duration-200 shadow-sm">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-slate-800 uppercase">
                    {item.titulo}
                  </h4>
                  <div className="flex items-center space-x-2">
                    <Badge variant={isConcluded ? 'success' : 'warning'} className="text-[9px]">
                      {isConcluded ? 'Concluída' : 'Em Andamento'}
                    </Badge>
                  </div>
                </div>

                {item.descricao && (
                  <p className="text-xs text-text leading-relaxed">
                    {item.descricao}
                  </p>
                )}

                {item.observacao && (
                  <div className="bg-white px-2.5 py-1.5 rounded border border-slate-200/50 text-[11px] text-muted leading-snug">
                    <span className="font-bold text-slate-700">Obs:</span> {item.observacao}
                  </div>
                )}

                {/* Footer metadata */}
                <div className="flex items-center justify-between text-[10px] text-muted border-t border-slate-200/50 pt-2">
                  <div className="flex items-center space-x-1">
                    <User className="w-3.5 h-3.5" />
                    <span className="font-semibold uppercase tracking-wider text-slate-600">
                      {item.usuario_responsavel}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="flex items-center space-x-0.5">
                      <Calendar className="w-3.5 h-3.5" />
                      <span>Atuação: {item.data_atuacao}</span>
                    </div>
                    {item.data_conclusao && (
                      <div className="flex items-center space-x-0.5 text-ghc-teal font-medium">
                        <CheckCircle2 className="w-3.5 h-3.5" />
                        <span>Conclusão: {item.data_conclusao}</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
}
