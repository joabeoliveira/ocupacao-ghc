import React from 'react';
import { KpiCard } from '../ui/KpiCard';
import { Users, AlertTriangle, Activity, ShieldAlert } from 'lucide-react';

interface KpisData {
  total_internados: number;
  longa_permanencia_15: number;
  longa_permanencia_30: number;
  longa_permanencia_40: number;
  longa_permanencia_60_anos: number;
  longa_permanencia_60_15: number;
  longa_permanencia_60_30: number;
  leitos_ocupados: number;
  leitos_livres: number;
  leitos_bloqueados: number;
  taxa_ocupacao_geral_percentual: number;
  taxa_ocupacao_operacional_percentual: number;
  taxa_ocupacao_ajustada_sem_emergencia_percentual: number;
}

interface KpiRowProps {
  data: KpisData;
  isLoading: boolean;
}

export function KpiRow({ data, isLoading }: KpiRowProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
        {Array.from({ length: 4 }).map((_, index) => (
          <div key={index} className="bg-panel border border-panel-border rounded-lg p-5 h-24 animate-pulse">
            <div className="h-3 bg-gray-200 rounded w-1/2 mb-4"></div>
            <div className="h-6 bg-gray-200 rounded w-1/3"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
      <KpiCard
        title="Total Internados"
        value={data.total_internados}
        icon={<Users className="w-5 h-5 text-ghc-blue" />}
        subtitle={`Leitos Ocupados: ${data.leitos_ocupados}`}
      />
      <KpiCard
        title="Longa Permanência (15d+)"
        value={data.longa_permanencia_15}
        icon={<ShieldAlert className="w-5 h-5 text-priority-vermelho" />}
        subtitle={`30 dias+: ${data.longa_permanencia_30} | 40 dias+: ${data.longa_permanencia_40}`}
        className="border-l-4 border-l-priority-vermelho"
      />
      <KpiCard
        title="Ocupação Operacional"
        value={`${data.taxa_ocupacao_operacional_percentual}%`}
        icon={<Activity className="w-5 h-5 text-ghc-teal" />}
        subtitle={`Leitos Livres: ${data.leitos_livres} | Bloqueados: ${data.leitos_bloqueados}`}
      />
      <KpiCard
        title="Idosos Internados (60+)"
        value={data.longa_permanencia_60_anos}
        icon={<AlertTriangle className="w-5 h-5 text-priority-laranja" />}
        subtitle={`LP (15d+): ${data.longa_permanencia_60_15} | LP (30d+): ${data.longa_permanencia_60_30}`}
      />
    </div>
  );
}
