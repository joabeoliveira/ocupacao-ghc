'use client';

import React from 'react';
import { Paciente } from '@/types';
import { Card, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Calendar, User, Clock, AlertCircle } from 'lucide-react';
import { cn } from '@/lib/utils';

interface LeitoCardProps {
  paciente: Paciente;
  onClick: () => void;
}

export function LeitoCard({ paciente, onClick }: LeitoCardProps) {
  const days = paciente.dias_internacao || 0;

  // Visual highlights for beds based on length of stay
  const getBorderColor = () => {
    if (days >= 40) return 'border-l-4 border-l-priority-escuro hover:ring-priority-escuro';
    if (days >= 30) return 'border-l-4 border-l-priority-vermelho hover:ring-priority-vermelho';
    if (days >= 15) return 'border-l-4 border-l-priority-laranja hover:ring-priority-laranja';
    return 'border-l-4 border-l-ghc-blue hover:ring-ghc-blue';
  };

  const getPriorityBg = () => {
    if (days >= 40) return 'bg-red-50';
    if (days >= 30) return 'bg-rose-50/50';
    if (days >= 15) return 'bg-amber-50/50';
    return 'bg-white';
  };

  return (
    <Card
      className={cn(
        'cursor-pointer transition-all duration-300 hover:shadow-md hover:ring-1 hover:-translate-y-0.5 select-none',
        getBorderColor(),
        getPriorityBg()
      )}
      onClick={onClick}
    >
      <CardContent className="p-4 flex flex-col justify-between h-full space-y-3">
        {/* Top bar: bed name & unit badge */}
        <div className="flex items-center justify-between">
          <span className="text-xs font-extrabold text-slate-800 tracking-wider uppercase bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
            {paciente.leito || 'N/A'}
          </span>
          <Badge variant="default" className="text-[9px]">
            {paciente.unidade}
          </Badge>
        </div>

        {/* Patient Name */}
        <div className="space-y-1">
          <p className="text-xs font-bold text-ghc-blue uppercase line-clamp-1">
            {paciente.nome_paciente || 'PACIENTE INDENTIFICADO'}
          </p>
          <div className="flex items-center text-[11px] text-muted space-x-1">
            <User className="w-3.5 h-3.5" />
            <span>Prontuário: {paciente.prontuario} | {paciente.idade_anos} anos</span>
          </div>
        </div>

        {/* Mid section: diagnosis / cid */}
        <div className="text-[10px] text-muted uppercase tracking-tight line-clamp-1 border-t border-slate-100 pt-2 font-medium">
          CID: <span className="font-bold text-slate-700">{paciente.cid_internacao_codigo}</span> — {paciente.cid_internacao_descricao}
        </div>

        {/* Footer info: days & action flags */}
        <div className="flex items-center justify-between pt-1 text-[11px]">
          <div className="flex items-center space-x-1 text-slate-800 font-bold">
            <Calendar className="w-3.5 h-3.5 text-muted" />
            <span>{days} dias</span>
          </div>

          <div className="flex items-center space-x-1.5">
            {paciente.egaa_total_atuacoes > 0 ? (
              <div
                className="flex items-center space-x-0.5 text-ghc-teal font-bold"
                title={`${paciente.egaa_total_atuacoes} atuações do EGAA`}
              >
                <Clock className="w-3.5 h-3.5" />
                <span>{paciente.egaa_total_atuacoes}</span>
              </div>
            ) : (
              <div
                className="flex items-center space-x-0.5 text-priority-laranja font-bold"
                title="Sem atuação recente"
              >
                <AlertCircle className="w-3.5 h-3.5" />
                <span>0</span>
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
