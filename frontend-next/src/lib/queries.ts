import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from './api';
import { PacientesParams } from '../types';

export function useKPIs(dataInicio?: string, dataFim?: string) {
  return useQuery({
    queryKey: ['kpis', dataInicio, dataFim],
    queryFn: () => api.get(`/api/censo/kpis`, { params: { data_inicio: dataInicio, data_fim: dataFim } }),
  });
}

export function usePacientes(params: PacientesParams) {
  return useQuery({
    queryKey: ['pacientes', params],
    queryFn: () => api.get('/api/censo/pacientes', { params }),
  });
}

export function usePaciente(prontuario: string) {
  return useQuery({
    queryKey: ['paciente', prontuario],
    queryFn: () => api.get(`/api/censo/paciente/${prontuario}`),
    enabled: !!prontuario,
  });
}

export function useIntervencoes(prontuario: string) {
  return useQuery({
    queryKey: ['intervencoes', prontuario],
    queryFn: () => api.get(`/api/egaa/intervencoes?prontuario=${prontuario}`),
    enabled: !!prontuario,
  });
}

export function useTiposIntervencao() {
  return useQuery({
    queryKey: ['tipos-intervencao'],
    queryFn: () => api.get('/api/egaa/tipos-intervencao'),
    staleTime: 5 * 60 * 1000,
  });
}

export function usePendenciaCodigos() {
  return useQuery({
    queryKey: ['pendencia-codigos'],
    queryFn: () => api.get('/api/egaa/pendencia/codigos'),
  });
}

export function usePendencias(prontuario: string) {
  return useQuery({
    queryKey: ['pendencias', prontuario],
    queryFn: () => api.get(`/api/egaa/pendencia/${prontuario}`),
    enabled: !!prontuario,
  });
}

export function useCriarIntervencao() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      prontuario: string;
      tipo_intervencao_id: number;
      titulo: string;
      descricao: string;
      status: string;
      usuario_responsavel: string;
      data_atuacao: string;
    }) => api.post('/api/egaa/intervencoes', data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['intervencoes', variables.prontuario] });
      queryClient.invalidateQueries({ queryKey: ['pacientes'] });
    },
  });
}

export function useAdicionarPendencia(prontuario: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { codigo: string }) => api.post(`/api/egaa/pendencia/${prontuario}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pendencias', prontuario] });
      queryClient.invalidateQueries({ queryKey: ['pacientes'] });
    },
  });
}

export function useAtualizarPendencia(prontuario: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, resolvida }: { id: number; resolvida: boolean }) =>
      api.put(`/api/egaa/pendencia/${prontuario}/${id}`, { resolvida }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['pendencias', prontuario] });
      queryClient.invalidateQueries({ queryKey: ['pacientes'] });
    },
  });
}

export function useAtualizarEvolucao(prontuario: string) {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: { evolucao: string }) => api.put(`/api/censo/paciente/${prontuario}/evolucao`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['paciente', prontuario] });
      queryClient.invalidateQueries({ queryKey: ['pacientes'] });
    },
  });
}

export function useIndicadores() {
  return useQuery({
    queryKey: ['indicadores'],
    queryFn: () => api.get('/api/egaa/indicadores'),
  });
}

// ─── Desfechos EGAA ──────────────────────────────────────────────

export function useDesfechos(filters?: { prontuario?: string; tipo?: string; data_inicio?: string; data_fim?: string }) {
  return useQuery({
    queryKey: ['desfechos', filters],
    queryFn: () => api.get('/api/egaa/desfechos', { params: filters }),
  });
}

export function useCriarDesfecho() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      prontuario: string;
      tipo: string;
      data_desfecho: string;
      descricao?: string;
      usuario_responsavel?: string;
      intervencao_id?: number;
    }) => api.post('/api/egaa/desfechos', data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['desfechos'] });
      queryClient.invalidateQueries({ queryKey: ['indicadores-desfecho'] });
      queryClient.invalidateQueries({ queryKey: ['pacientes'] });
    },
  });
}

export function useAtualizarDesfecho() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<{ prontuario: string; tipo: string; data_desfecho: string; descricao: string; usuario_responsavel: string; intervencao_id: number }> }) =>
      api.put(`/api/egaa/desfechos/${id}`, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['desfechos'] });
      queryClient.invalidateQueries({ queryKey: ['indicadores-desfecho'] });
    },
  });
}

export function useRemoverDesfecho() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) => api.delete(`/api/egaa/desfechos/${id}`),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['desfechos'] });
      queryClient.invalidateQueries({ queryKey: ['indicadores-desfecho'] });
    },
  });
}

export function useIndicadoresDesfecho() {
  return useQuery({
    queryKey: ['indicadores-desfecho'],
    queryFn: () => api.get('/api/egaa/indicadores/desfechos'),
  });
}
