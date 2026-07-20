// src/types/index.ts
export interface Paciente {
  id: number;
  prontuario: string;
  nome_paciente: string | null;
  idade_anos: number | null;
  data_internacao: string | null;
  dias_internacao: number | null;
  especialidade: string;
  unidade: string | null;
  enfermaria: string | null;
  leito: string | null;
  status_leito: string | null;
  cid_internacao_codigo: string | null;
  cid_internacao_descricao: string | null;
  evolucao: string | null;
  egaa_total_atuacoes: number;
  egaa_ultima_atuacao: string | null;
}

export interface Intervencao {
  id: number;
  prontuario: string;
  tipo_intervencao_id: number;
  titulo: string;
  descricao: string | null;
  status: 'aberta' | 'em_andamento' | 'concluida' | 'cancelada';
  usuario_responsavel: string | null;
  data_atuacao: string | null;
  data_prevista: string | null;
  data_conclusao: string | null;
  observacao: string | null;
}

export interface Pendencia {
  id: number;
  prontuario: string;
  codigo: string;
  resolvida: boolean;
}

export interface TipoIntervencao {
  id: number;
  nome: string;
  descricao: string | null;
  ativo: boolean;
  ordem_exibicao: number;
}

export interface PacientesParams {
  page?: number;
  page_size?: number;
  prontuario?: string;
  nome?: string;
  especialidade?: string;
  unidade?: string;
  min_dias?: number;
  idade_minima?: number;
  data_inicio?: string;
  data_fim?: string;
}

export interface Desfecho {
  id: number;
  prontuario: string;
  tipo: 'alta' | 'obito';
  data_desfecho: string;
  descricao: string | null;
  usuario_responsavel: string | null;
  intervencao_id: number | null;
  created_at: string | null;
  updated_at: string | null;
}

export interface IndicadoresDesfecho {
  total_desfechos: number;
  total_altas: number;
  total_obitos: number;
  pacientes_com_desfecho: number;
  por_tipo: { tipo: string; total: number }[];
  por_mes: { mes: string; total: number }[];
}
