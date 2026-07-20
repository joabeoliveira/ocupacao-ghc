'use client';

import React, { useState } from 'react';
import { useKPIs, usePacientes } from '@/lib/queries';
import { KpiRow } from '@/components/dashboard/KpiRow';
import { GraficoUnidade } from '@/components/dashboard/GraficoUnidade';
import { TopPacientes } from '@/components/dashboard/TopPacientes';
import { ModalPaciente } from '@/components/modal/ModalPaciente';
import { Badge } from '@/components/ui/Badge';
import { ShieldCheck, HeartPulse } from 'lucide-react';

export default function DashboardPage() {
  const [selectedProntuario, setSelectedProntuario] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Load metrics and patients list
  const { data: kpis, isLoading: loadingKpis } = useKPIs();
  const { data: pacientesRes, isLoading: loadingPacientes } = usePacientes({ page: 1, page_size: 50 });

  const handleSelectPaciente = (prontuario: string) => {
    setSelectedProntuario(prontuario);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedProntuario(null);
  };

  const pacList = pacientesRes?.items || [];

  return (
    <div className="space-y-6">
      {/* Title Header Section */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-panel-border pb-5 gap-3">
        <div className="space-y-1">
          <div className="flex items-center space-x-2">
            <HeartPulse className="w-5 h-5 text-ghc-blue animate-pulse" />
            <h1 className="text-xl font-extrabold text-text uppercase tracking-tight">
              Regulação &amp; Censo Hospitalar
            </h1>
          </div>
          <p className="text-xs text-muted font-medium">
            Painel Geral do Grupo Hospitalar Conceição para Gestão de Leitos e Desospitalização (EGAA)
          </p>
        </div>
        <div className="flex items-center space-x-2 bg-emerald-50 text-emerald-800 border border-emerald-100 px-3 py-1.5 rounded text-xs font-semibold">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>Monitoramento de Longa Permanência Ativo</span>
        </div>
      </div>

      {/* KPI row */}
      <KpiRow data={kpis} isLoading={loadingKpis} />

      {/* Main visualization grid */}
      <div className="grid grid-cols-1 gap-6">
        {/* Occupied units distribution chart */}
        <GraficoUnidade data={kpis?.ocupacao_por_unidade || []} isLoading={loadingKpis} />

        {/* Top patients table */}
        <TopPacientes
          pacientes={pacList}
          isLoading={loadingPacientes}
          onSelectPaciente={handleSelectPaciente}
        />
      </div>

      {/* Interactive patient details chart modal */}
      <ModalPaciente
        prontuario={selectedProntuario}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </div>
  );
}
