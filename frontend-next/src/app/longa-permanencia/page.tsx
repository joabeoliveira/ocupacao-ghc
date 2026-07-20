'use client';

import React, { useState } from 'react';
import { usePacientes } from '@/lib/queries';
import { LeitoGrid } from '@/components/leitos/LeitoGrid';
import { ModalPaciente } from '@/components/modal/ModalPaciente';
import { HeartPulse } from 'lucide-react';

export default function LongaPermanenciaPage() {
  const [currentPage, setCurrentPage] = useState(1);
  const [selectedProntuario, setSelectedProntuario] = useState<string | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Filter state
  const [filters, setFilters] = useState({
    nome: '',
    prontuario: '',
    unidade: '',
    especialidade: '',
    min_dias: '',
    idade_minima: ''
  });

  // Load patient list with active filters and current page
  const { data, isLoading } = usePacientes({
    page: currentPage,
    page_size: 12, // smaller page size is better for grid view
    nome: filters.nome || undefined,
    prontuario: filters.prontuario || undefined,
    unidade: filters.unidade || undefined,
    especialidade: filters.especialidade || undefined,
    min_dias: filters.min_dias ? Number(filters.min_dias) : undefined,
    idade_minima: filters.idade_minima ? Number(filters.idade_minima) : undefined
  });

  const handleSelectPaciente = (prontuario: string) => {
    setSelectedProntuario(prontuario);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setSelectedProntuario(null);
  };

  return (
    <div className="space-y-6">
      {/* Title Header Section */}
      <div className="border-b border-panel-border pb-5">
        <div className="flex items-center space-x-2">
          <HeartPulse className="w-5 h-5 text-ghc-blue" />
          <h1 className="text-xl font-extrabold text-text uppercase tracking-tight">
            Gestão de Longa Permanência &amp; Leitos
          </h1>
        </div>
        <p className="text-xs text-muted font-medium mt-1">
          Busca ativa de pacientes internados por leito, especialidade médica, dias de permanência e idades clínicas.
        </p>
      </div>

      {/* Grid and Table Leito Search Component */}
      <LeitoGrid
        pacientes={data?.items || []}
        totalItems={data?.total || 0}
        currentPage={currentPage}
        onPageChange={setCurrentPage}
        filters={filters}
        setFilters={setFilters}
        onSelectPaciente={handleSelectPaciente}
        isLoading={isLoading}
      />

      {/* Interactive clinical details card modal */}
      <ModalPaciente
        prontuario={selectedProntuario}
        isOpen={isModalOpen}
        onClose={handleCloseModal}
      />
    </div>
  );
}
