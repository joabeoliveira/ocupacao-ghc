import { Desfecho, IndicadoresDesfecho, Paciente, Intervencao, Pendencia, TipoIntervencao } from '@/types';

// Let's pre-populate mock data
let tiposIntervencao: TipoIntervencao[] = [
  { id: 1, nome: 'Evolução EGAA', descricao: 'Registro de evolução clínica pelo EGAA', ativo: true, ordem_exibicao: 1 },
  { id: 2, nome: 'Round Clínico', descricao: 'Discussão multiprofissional do plano de cuidado', ativo: true, ordem_exibicao: 2 },
  { id: 3, nome: 'Contato Familiar', descricao: 'Alinhamento de alta ou suporte familiar', ativo: true, ordem_exibicao: 3 },
  { id: 4, nome: 'Acionamento Assistência Social', descricao: 'Suporte pós-alta, órteses/próteses, transporte', ativo: true, ordem_exibicao: 4 },
  { id: 5, nome: 'Parecer Temático', descricao: 'Solicitação de avaliação por especialista', ativo: true, ordem_exibicao: 5 },
  { id: 6, nome: 'Acompanhamento de Exame', descricao: 'Agilização de exames de alta complexidade', ativo: true, ordem_exibicao: 6 },
];

let pendenciasMock: Pendencia[] = [
  { id: 1, prontuario: '8399062', codigo: 'regulacao', resolvida: false },
  { id: 2, prontuario: '8399062', codigo: 'antibioticoterapia', resolvida: true },
  { id: 3, prontuario: '5420199', codigo: 'exame_pendente', resolvida: false },
  { id: 4, prontuario: '1273948', codigo: 'assistencia_social', resolvida: false },
  { id: 5, prontuario: '9482711', codigo: 'fisioterapia', resolvida: false },
];

let desfechosMock: Desfecho[] = [
  {
    id: 1,
    prontuario: '8399062',
    tipo: 'alta',
    data_desfecho: '2026-07-13',
    descricao: 'Alta hospitalar com apoio do EGAA. Paciente recebeu alta com oxigenoterapia domiciliar após articulação com Assistência Social.',
    usuario_responsavel: 'ENF EDUARDO',
    intervencao_id: 1,
    created_at: '2026-07-13T10:30:00',
    updated_at: '2026-07-13T10:30:00'
  },
  {
    id: 2,
    prontuario: '5420199',
    tipo: 'alta',
    data_desfecho: '2026-07-10',
    descricao: 'Alta para cuidados paliativos domiciliares. Familiares orientados e suporte da atenção primária acionado.',
    usuario_responsavel: 'DRA CLAUDIA',
    intervencao_id: null,
    created_at: '2026-07-10T14:00:00',
    updated_at: '2026-07-10T14:00:00'
  },
  {
    id: 3,
    prontuario: '3849102',
    tipo: 'obito',
    data_desfecho: '2026-07-12',
    descricao: 'Óbito por progressão de neoplasia. Paciente em cuidados paliativos, equipe EGAA prestou suporte à família.',
    usuario_responsavel: 'ENF EDUARDO',
    intervencao_id: null,
    created_at: '2026-07-12T08:15:00',
    updated_at: '2026-07-12T08:15:00'
  },
  {
    id: 4,
    prontuario: '1273948',
    tipo: 'alta',
    data_desfecho: '2026-07-08',
    descricao: 'Alta para hospital dia com suporte multidisciplinar. Transferência articulada pelo EGAA.',
    usuario_responsavel: 'ASS SOC ANA',
    intervencao_id: null,
    created_at: '2026-07-08T16:45:00',
    updated_at: '2026-07-08T16:45:00'
  },
  {
    id: 5,
    prontuario: '9482711',
    tipo: 'alta',
    data_desfecho: '2026-07-05',
    descricao: 'Alta com acompanhamento ambulatorial. Encaminhamentos realizados e família orientada.',
    usuario_responsavel: 'DRA CLAUDIA',
    intervencao_id: null,
    created_at: '2026-07-05T11:20:00',
    updated_at: '2026-07-05T11:20:00'
  }
];

let intervencoesMock: Intervencao[] = [
  {
    id: 1,
    prontuario: '8399062',
    tipo_intervencao_id: 1,
    titulo: 'Evolução EGAA',
    descricao: 'Paciente estável clinicamente. Aguardando liberação de oxigênio domiciliar pela Assistência Social municipal. Planejada visita amanhã.',
    status: 'concluida',
    usuario_responsavel: 'ENF EDUARDO',
    data_atuacao: '2026-07-09',
    data_prevista: '2026-07-09',
    data_conclusao: '2026-07-09',
    observacao: 'Discutido com familiar.'
  },
  {
    id: 2,
    prontuario: '8399062',
    tipo_intervencao_id: 2,
    titulo: 'Round Clínico',
    descricao: 'Realizado round na enfermaria 220. Equipe médica concorda que paciente tem condições de alta sob oxigenoterapia se assistencial conseguir concentrador.',
    status: 'concluida',
    usuario_responsavel: 'DRA CLAUDIA',
    data_atuacao: '2026-07-11',
    data_prevista: '2026-07-11',
    data_conclusao: '2026-07-11',
    observacao: 'Foco na desospitalização.'
  },
  {
    id: 3,
    prontuario: '5420199',
    tipo_intervencao_id: 4,
    titulo: 'Acionamento Assistência Social',
    descricao: 'Solicitado parecer da assistente social referente ao transporte sanitário para retorno ao município de origem pós-alta.',
    status: 'em_andamento',
    usuario_responsavel: 'ENF EDUARDO',
    data_atuacao: '2026-07-12',
    data_prevista: '2026-07-14',
    data_conclusao: null,
    observacao: 'Aguardando parecer da assistente.'
  }
];

let pacientesMock: Paciente[] = [
  {
    id: 1,
    prontuario: '8399062',
    nome_paciente: 'IRENE DOS SANTOS',
    idade_anos: 83,
    data_internacao: '2025-12-11T00:00:00',
    dias_internacao: 210,
    especialidade: 'CLÍNICA MÉDICA',
    unidade: 'HFB',
    enfermaria: 'CM Mista',
    leito: '220-13',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'I50',
    cid_internacao_descricao: 'Insuficiência cardíaca',
    evolucao: 'ENF: 13/07/2026 - Paciente idosa, 83 anos, longa internação decorrente de descompensação cardíaca de repetição. Necessita concentrador de O2 domiciliar. Equipe de serviço social segue agilizando com a secretaria de saúde de Alvorada.',
    egaa_total_atuacoes: 12,
    egaa_ultima_atuacao: '2026-07-11'
  },
  {
    id: 2,
    prontuario: '5420199',
    nome_paciente: 'JOÃO BATISTA DA SILVA',
    idade_anos: 67,
    data_internacao: '2026-05-14T00:00:00',
    dias_internacao: 60,
    especialidade: 'NEUROLOGIA',
    unidade: 'HNSC',
    enfermaria: 'Neuro 3A',
    leito: '315-A',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'I64',
    cid_internacao_descricao: 'Acidente vascular cerebral',
    evolucao: 'MED: 12/07/2026 - Paciente com sequelas motoras e de deglutição pós-AVC isquêmico extenso. Em reabilitação fonoaudiológica e fisioterápica intensa. Aguarda avaliação para Home Care / PAD.',
    egaa_total_atuacoes: 4,
    egaa_ultima_atuacao: '2026-07-12'
  },
  {
    id: 3,
    prontuario: '1273948',
    nome_paciente: 'MARIA APARECIDA OLIVEIRA',
    idade_anos: 45,
    data_internacao: '2026-06-10T00:00:00',
    dias_internacao: 33,
    especialidade: 'CIRURGIA GERAL',
    unidade: 'HNSC',
    enfermaria: 'Cirurgia 2B',
    leito: '211-12',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'K80',
    cid_internacao_descricao: 'Colelitíase com colangite',
    evolucao: 'ENF: 10/07/2026 - Pós-operatório tardio complicado por infecção de sítio cirúrgico. Em antibioticoterapia de amplo espectro de longa duração. Programado round de infectologia.',
    egaa_total_atuacoes: 2,
    egaa_ultima_atuacao: '2026-07-10'
  },
  {
    id: 4,
    prontuario: '9482711',
    nome_paciente: 'CARLOS ALBERTO DE MELLO',
    idade_anos: 72,
    data_internacao: '2026-06-25T00:00:00',
    dias_internacao: 18,
    especialidade: 'CARDIOLOGIA',
    unidade: 'HCR',
    enfermaria: 'Cardio A',
    leito: '102-04',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'I21',
    cid_internacao_descricao: 'Infarto agudo do miocárdio',
    evolucao: 'MED: 11/07/2026 - Pós-angioplastia coronária. Aguardando ajuste de anticoagulação oral para alta segura. Apresenta boa evolução clínica, deambulando.',
    egaa_total_atuacoes: 1,
    egaa_ultima_atuacao: '2026-07-11'
  },
  {
    id: 5,
    prontuario: '3128954',
    nome_paciente: 'ANA FLAVIA SOUZA DE PAULA',
    idade_anos: 38,
    data_internacao: '2026-07-02T00:00:00',
    dias_internacao: 11,
    especialidade: 'CLÍNICA MÉDICA',
    unidade: 'HF',
    enfermaria: 'Ginecologia 1',
    leito: '110-B',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'N39',
    cid_internacao_descricao: 'Infecção do trato urinário',
    evolucao: null,
    egaa_total_atuacoes: 0,
    egaa_ultima_atuacao: null
  },
  {
    id: 6,
    prontuario: '7362940',
    nome_paciente: 'PEDRO ALMEIDA NUNES',
    idade_anos: 61,
    data_internacao: '2026-05-10T00:00:00',
    dias_internacao: 64,
    especialidade: 'CLÍNICA MÉDICA',
    unidade: 'HNSC',
    enfermaria: 'CM Masculina',
    leito: '304-01',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'J44',
    cid_internacao_descricao: 'Doença pulmonar obstrutiva crônica',
    evolucao: 'MED: 10/07/2026 - DPOC exacerbada crônica. Dificuldade de desmame de oxigenoterapia. Equipe multidisciplinar avaliando condições para oxigenoterapia domiciliar.',
    egaa_total_atuacoes: 5,
    egaa_ultima_atuacao: '2026-07-10'
  },
  {
    id: 7,
    prontuario: '4839201',
    nome_paciente: 'FRANCISCO DE ASSIS SANTANA',
    idade_anos: 59,
    data_internacao: '2026-06-20T00:00:00',
    dias_internacao: 23,
    especialidade: 'CIRURGIA VASCULAR',
    unidade: 'HCR',
    enfermaria: 'Vascular 1A',
    leito: '105-02',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'E11',
    cid_internacao_descricao: 'Pé diabético infectado',
    evolucao: 'MED: 09/07/2026 - Submetido a amputação parcial. Ferida operatória com bom aspecto, sob curativo diário pela enfermagem. Programando alta com encaminhamento para rede básica.',
    egaa_total_atuacoes: 2,
    egaa_ultima_atuacao: '2026-07-09'
  },
  {
    id: 8,
    prontuario: '2938475',
    nome_paciente: 'TEREZA CRISTINA FONSECA',
    idade_anos: 79,
    data_internacao: '2026-05-20T00:00:00',
    dias_internacao: 54,
    especialidade: 'CLÍNICA MÉDICA',
    unidade: 'HF',
    enfermaria: 'Fêmina CM',
    leito: '412-A',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'A41',
    cid_internacao_descricao: 'Sepse de foco pulmonar',
    evolucao: 'MED: 12/07/2026 - Paciente geriátrica em fase final de antibioticoterapia. Já sem suporte de O2. Aguarda consulta agendada de fisiatria para avaliar encaminhamento a hospital de retaguarda.',
    egaa_total_atuacoes: 3,
    egaa_ultima_atuacao: '2026-07-12'
  },
  {
    id: 9,
    prontuario: '1948273',
    nome_paciente: 'JOÃO ALBERTO REIS',
    idade_anos: 62,
    data_internacao: '2026-06-12T00:00:00',
    dias_internacao: 31,
    especialidade: 'NEUROLOGIA',
    unidade: 'HNSC',
    enfermaria: 'Neuro 3B',
    leito: '318-B',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'G30',
    cid_internacao_descricao: 'Doença de Alzheimer',
    evolucao: 'ENF: 08/07/2026 - Paciente com quadro demencial avançado. Longa permanência devido à dificuldade de estruturação familiar para cuidados domiciliares. Assistência social em tratativas intensas.',
    egaa_total_atuacoes: 6,
    egaa_ultima_atuacao: '2026-07-08'
  },
  {
    id: 10,
    prontuario: '9384729',
    nome_paciente: 'HELENA MARQUES PINTO',
    idade_anos: 85,
    data_internacao: '2026-05-12T00:00:00',
    dias_internacao: 62,
    especialidade: 'CLÍNICA MÉDICA',
    unidade: 'HNSC',
    enfermaria: 'CM Feminina',
    leito: '308-14',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'M19',
    cid_internacao_descricao: 'Artrose grave com complicação local',
    evolucao: 'MED: 13/07/2026 - Internação prolongada por infecção de pele secundária. Em reabilitação fisioterápica. Estável clinicamente.',
    egaa_total_atuacoes: 4,
    egaa_ultima_atuacao: '2026-07-13'
  },
  {
    id: 11,
    prontuario: '2837492',
    nome_paciente: 'ANTONIO CARDOSO VIEIRA',
    idade_anos: 48,
    data_internacao: '2026-07-08T00:00:00',
    dias_internacao: 5,
    especialidade: 'CIRURGIA GERAL',
    unidade: 'HCR',
    enfermaria: 'Cirurgia 1C',
    leito: '106-03',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'K35',
    cid_internacao_descricao: 'Apendicite aguda',
    evolucao: null,
    egaa_total_atuacoes: 0,
    egaa_ultima_atuacao: null
  },
  {
    id: 12,
    prontuario: '3849102',
    nome_paciente: 'SEBASTIÃO GOMES DE SOUZA',
    idade_anos: 74,
    data_internacao: '2026-05-28T00:00:00',
    dias_internacao: 46,
    especialidade: 'ONCOLOGIA',
    unidade: 'HNSC',
    enfermaria: 'Onco 4A',
    leito: '401-12',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'C34',
    cid_internacao_descricao: 'Neoplasia maligna de brônquios',
    evolucao: 'ENF: 11/07/2026 - Paciente oncológico em cuidados paliativos de controle de sintomas. Longa permanência para ajuste álgico complexo e organização de suporte de rede de atenção primária.',
    egaa_total_atuacoes: 3,
    egaa_ultima_atuacao: '2026-07-11'
  },
  {
    id: 13,
    prontuario: '9481029',
    nome_paciente: 'LUCIA DE SOUZA RAMOS',
    idade_anos: 29,
    data_internacao: '2026-07-10T00:00:00',
    dias_internacao: 3,
    especialidade: 'PEDIATRIA',
    unidade: 'HCS',
    enfermaria: 'Pediatria A',
    leito: '012-04',
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'J21',
    cid_internacao_descricao: 'Bronquiolite aguda',
    evolucao: null,
    egaa_total_atuacoes: 0,
    egaa_ultima_atuacao: null
  }
];

// Let's create more patients dynamically to populate a total of 45 patients
const sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Rodrigues', 'Ferreira', 'Alves', 'Pereira', 'Lima', 'Gomes', 'Costa', 'Ribeiro', 'Martins', 'Carvalho', 'Rocha', 'Melo', 'Barbosa', 'Cardoso', 'Teixeira', 'Moreira'];
const nomesM = ['José', 'Manuel', 'Antônio', 'Francisco', 'João', 'Luiz', 'Paulo', 'Carlos', 'Marcos', 'Roberto', 'Julio', 'Jorge', 'Fernando', 'Ricardo', 'Lucas', 'Gabriel', 'Daniel', 'Marcelo', 'Bruno', 'Thiago'];
const nomesF = ['Maria', 'Ana', 'Francisca', 'Antônia', 'Adriana', 'Juliana', 'Sandra', 'Márcia', 'Patricia', 'Camila', 'Beatriz', 'Letícia', 'Aline', 'Larissa', 'Mariana', 'Fernanda', 'Cláudia', 'Gabriela', 'Luana'];
const especialidades = ['CLÍNICA MÉDICA', 'NEUROLOGIA', 'CARDIOLOGIA', 'CIRURGIA GERAL', 'ONCOLOGIA', 'CIRURGIA VASCULAR', 'PEDIATRIA'];
const unidades = ['HNSC', 'HCR', 'HF', 'HCS', 'HFB'];

// Generate another 32 patients
for (let i = 14; i <= 45; i++) {
  const isM = Math.random() > 0.5;
  const nome = (isM ? nomesM[i % nomesM.length] : nomesF[i % nomesF.length]) + ' ' + sobrenomes[(i * 3) % sobrenomes.length] + ' ' + sobrenomes[(i * 7) % sobrenomes.length];
  const idade = Math.floor(Math.random() * 75) + 15; // 15 to 90
  const dias = Math.floor(Math.random() * 120) + 1; // 1 to 120 days
  const esp = especialidades[i % especialidades.length];
  const uni = unidades[i % unidades.length];
  const enf = esp === 'PEDIATRIA' ? 'Pediatria B' : 'Ala ' + (i % 4 + 1);
  const leitoNum = (100 + i) + '-' + (i % 4 + 1);
  const pront = String(Math.floor(Math.random() * 8000000) + 1000000);

  // Let's determine long permanency and some evolucao
  let evolucao = null;
  let egaa_total_atuacoes = 0;
  let egaa_ultima_atuacao = null;

  if (dias >= 15) {
    egaa_total_atuacoes = Math.floor(Math.random() * 6);
    if (egaa_total_atuacoes > 0) {
      egaa_ultima_atuacao = '2026-07-' + String(14 - Math.floor(Math.random() * 10)).padStart(2, '0');
      evolucao = `ENF: ${egaa_ultima_atuacao} - Paciente acompanhado no round. Pendências avaliadas de forma positiva. Planejamento de alta em andamento.`;
    }
  }

  pacientesMock.push({
    id: i,
    prontuario: pront,
    nome_paciente: nome,
    idade_anos: idade,
    data_internacao: new Date(Date.now() - dias * 24 * 60 * 60 * 1000).toISOString(),
    dias_internacao: dias,
    especialidade: esp,
    unidade: uni,
    enfermaria: enf,
    leito: leitoNum,
    status_leito: 'Ocupado',
    cid_internacao_codigo: 'J18',
    cid_internacao_descricao: 'Pneumonia não especificada',
    evolucao: evolucao,
    egaa_total_atuacoes,
    egaa_ultima_atuacao
  });
}

// Helpers
export const dbMock = {
  getKPIs(dataInicio?: string, dataFim?: string) {
    // Let's filter or calculate KPIs based on our mock database
    const total_internados = pacientesMock.length;
    
    // Filter long stay patients (dias >= 15)
    const lp_pacientes = pacientesMock.filter(p => (p.dias_internacao || 0) >= 15);
    const longa_permanencia_15 = lp_pacientes.length;
    const longa_permanencia_30 = lp_pacientes.filter(p => (p.dias_internacao || 0) >= 30).length;
    const longa_permanencia_40 = lp_pacientes.filter(p => (p.dias_internacao || 0) >= 40).length;
    const longa_permanencia_60_anos = pacientesMock.filter(p => (p.idade_anos || 0) >= 60).length;
    const longa_permanencia_60_15 = lp_pacientes.filter(p => (p.idade_anos || 0) >= 60).length;
    const longa_permanencia_60_30 = lp_pacientes.filter(p => (p.dias_internacao || 0) >= 30 && (p.idade_anos || 0) >= 60).length;

    const leitos_ocupados = total_internados;
    const leitos_livres = 68;
    const leitos_bloqueados = 12;
    const total_leitos = leitos_ocupados + leitos_livres + leitos_bloqueados;

    const taxa_ocupacao_geral_percentual = parseFloat(((leitos_ocupados / total_leitos) * 100).toFixed(1));
    const taxa_ocupacao_operacional_percentual = parseFloat(((leitos_ocupados / (leitos_ocupados + leitos_livres)) * 100).toFixed(1));
    const taxa_ocupacao_ajustada_sem_emergencia_percentual = parseFloat((taxa_ocupacao_operacional_percentual * 0.92).toFixed(1));

    // Grouping by unit
    const ocupacao_por_unidade_map: Record<string, number> = {};
    pacientesMock.forEach(p => {
      if (p.unidade) {
        ocupacao_por_unidade_map[p.unidade] = (ocupacao_por_unidade_map[p.unidade] || 0) + 1;
      }
    });

    const ocupacao_por_unidade = Object.entries(ocupacao_por_unidade_map).map(([unidade, total_pacientes]) => ({
      unidade,
      total_pacientes
    }));

    return {
      total_internados,
      longa_permanencia_15,
      longa_permanencia_30,
      longa_permanencia_40,
      longa_permanencia_60_anos,
      longa_permanencia_60_15,
      longa_permanencia_60_30,
      leitos_ocupados,
      leitos_livres,
      leitos_bloqueados,
      taxa_ocupacao_geral_percentual,
      taxa_ocupacao_operacional_percentual,
      taxa_ocupacao_ajustada_sem_emergencia_percentual,
      ocupacao_por_unidade
    };
  },

  getPacientes(params: {
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
  }) {
    const page = Number(params.page || 1);
    const page_size = Number(params.page_size || 10);
    
    let filtered = [...pacientesMock];

    if (params.prontuario) {
      filtered = filtered.filter(p => p.prontuario.includes(params.prontuario!));
    }
    if (params.nome) {
      filtered = filtered.filter(p => p.nome_paciente && p.nome_paciente.toLowerCase().includes(params.nome!.toLowerCase()));
    }
    if (params.especialidade) {
      filtered = filtered.filter(p => p.especialidade === params.especialidade);
    }
    if (params.unidade) {
      filtered = filtered.filter(p => p.unidade === params.unidade);
    }
    if (params.min_dias !== undefined) {
      filtered = filtered.filter(p => (p.dias_internacao || 0) >= params.min_dias!);
    }
    if (params.idade_minima !== undefined) {
      filtered = filtered.filter(p => (p.idade_anos || 0) >= params.idade_minima!);
    }

    // Sort by longest stay first
    filtered.sort((a, b) => (b.dias_internacao || 0) - (a.dias_internacao || 0));

    const total = filtered.length;
    const start = (page - 1) * page_size;
    const items = filtered.slice(start, start + page_size);

    return {
      total,
      page,
      page_size,
      items
    };
  },

  getPaciente(prontuario: string) {
    const patient = pacientesMock.find(p => p.prontuario === prontuario);
    return patient || null;
  },

  updateEvolucao(prontuario: string, evolucao: string) {
    const patientIndex = pacientesMock.findIndex(p => p.prontuario === prontuario);
    if (patientIndex !== -1) {
      pacientesMock[patientIndex].evolucao = evolucao;
      pacientesMock[patientIndex].egaa_total_atuacoes += 1;
      pacientesMock[patientIndex].egaa_ultima_atuacao = new Date().toISOString().split('T')[0];
      return pacientesMock[patientIndex];
    }
    return null;
  },

  getTiposIntervencao() {
    return tiposIntervencao;
  },

  saveTipoIntervencao(data: Omit<TipoIntervencao, 'id'>) {
    const newId = tiposIntervencao.length > 0 ? Math.max(...tiposIntervencao.map(t => t.id)) + 1 : 1;
    const record = { id: newId, ...data };
    tiposIntervencao.push(record);
    return record;
  },

  updateTipoIntervencao(id: number, data: Partial<TipoIntervencao>) {
    const idx = tiposIntervencao.findIndex(t => t.id === id);
    if (idx !== -1) {
      tiposIntervencao[idx] = { ...tiposIntervencao[idx], ...data };
      return tiposIntervencao[idx];
    }
    return null;
  },

  getIntervencoes(prontuario: string) {
    return intervencoesMock.filter(i => i.prontuario === prontuario);
  },

  addIntervencao(data: Omit<Intervencao, 'id'>) {
    const newId = intervencoesMock.length > 0 ? Math.max(...intervencoesMock.map(i => i.id)) + 1 : 1;
    const newIntervencao: Intervencao = {
      id: newId,
      prontuario: data.prontuario,
      tipo_intervencao_id: Number(data.tipo_intervencao_id),
      titulo: data.titulo || 'Atuação EGAA',
      descricao: data.descricao || null,
      status: data.status || 'aberta',
      usuario_responsavel: data.usuario_responsavel || 'SISTEMA',
      data_atuacao: data.data_atuacao || new Date().toISOString().split('T')[0],
      data_prevista: data.data_prevista || null,
      data_conclusao: data.status === 'concluida' ? new Date().toISOString().split('T')[0] : null,
      observacao: data.observacao || null
    };
    intervencoesMock.push(newIntervencao);

    // Also increment paciente actuaciones
    const patientIndex = pacientesMock.findIndex(p => p.prontuario === data.prontuario);
    if (patientIndex !== -1) {
      pacientesMock[patientIndex].egaa_total_atuacoes += 1;
      pacientesMock[patientIndex].egaa_ultima_atuacao = newIntervencao.data_atuacao;
    }

    return newIntervencao;
  },

  getPendenciaCodigos() {
    return [
      { codigo: 'regulacao', rotulo: 'Regulação' },
      { codigo: 'antibioticoterapia', rotulo: 'Antibioticoterapia' },
      { codigo: 'exame_pendente', rotulo: 'Exame pendente' },
      { codigo: 'assistencia_social', rotulo: 'Assistência Social' },
      { codigo: 'fisioterapia', rotulo: 'Fisioterapia' }
    ];
  },

  getPendencias(prontuario: string) {
    return pendenciasMock.filter(p => p.prontuario === prontuario);
  },

  addPendencia(prontuario: string, codigo: string) {
    const newId = pendenciasMock.length > 0 ? Math.max(...pendenciasMock.map(p => p.id)) + 1 : 1;
    const newPendencia: Pendencia = {
      id: newId,
      prontuario,
      codigo,
      resolvida: false
    };
    pendenciasMock.push(newPendencia);
    return newPendencia;
  },

  updatePendencia(prontuario: string, id: number, resolvida: boolean) {
    const idx = pendenciasMock.findIndex(p => p.prontuario === prontuario && p.id === id);
    if (idx !== -1) {
      pendenciasMock[idx].resolvida = resolvida;
      return pendenciasMock[idx];
    }
    return null;
  },

  deletePendencia(prontuario: string, id: number) {
    const idx = pendenciasMock.findIndex(p => p.prontuario === prontuario && p.id === id);
    if (idx !== -1) {
      const removed = pendenciasMock[idx];
      pendenciasMock.splice(idx, 1);
      return removed;
    }
    return null;
  },

  getIndicadores() {
    // Total LP, and resolved pendencies
    const lp = pacientesMock.filter(p => (p.dias_internacao || 0) >= 15);
    const lpTotal = lp.length;
    const lpHighest = lp.reduce((max, p) => (p.dias_internacao || 0) > max ? p.dias_internacao || 0 : max, 0);

    const pendenciasResolvidas = pendenciasMock.filter(p => p.resolvida).length;
    const pendenciasAbertas = pendenciasMock.filter(p => !p.resolvida).length;
    const taxPendenciasResolvidas = pendenciasMock.length > 0 ? parseFloat(((pendenciasResolvidas / pendenciasMock.length) * 100).toFixed(1)) : 100;

    return {
      lp_total: lpTotal,
      lp_maior_tempo_dias: lpHighest,
      pendencias_totais: pendenciasMock.length,
      pendencias_abertas: pendenciasAbertas,
      pendencias_resolvidas: pendenciasResolvidas,
      taxa_resolucao_pendencias: taxPendenciasResolvidas
    };
  },

  uploadArquivo(tipo: string, content: string) {
    const count = Math.floor(Math.random() * 5) + 3;
    return {
      sucesso: true,
      mensagem: `${count} registros processados e atualizados com sucesso via carga de ${tipo}.`
    };
  },

  // ─── Desfechos EGAA ──────────────────────────────────────

  getDesfechos(filters?: { prontuario?: string; tipo?: string; data_inicio?: string; data_fim?: string }) {
    let filtered = [...desfechosMock];

    if (filters?.prontuario) {
      filtered = filtered.filter(d => d.prontuario.includes(filters.prontuario!));
    }
    if (filters?.tipo) {
      filtered = filtered.filter(d => d.tipo === filters.tipo);
    }
    if (filters?.data_inicio) {
      filtered = filtered.filter(d => d.data_desfecho >= filters.data_inicio!);
    }
    if (filters?.data_fim) {
      filtered = filtered.filter(d => d.data_desfecho <= filters.data_fim!);
    }

    // Sort by most recent first
    filtered.sort((a, b) => b.data_desfecho.localeCompare(a.data_desfecho));

    return filtered;
  },

  addDesfecho(data: { prontuario: string; tipo: string; data_desfecho: string; descricao?: string; usuario_responsavel?: string; intervencao_id?: number }) {
    const newId = desfechosMock.length > 0 ? Math.max(...desfechosMock.map(d => d.id)) + 1 : 1;
    const now = new Date().toISOString();
    const newDesfecho: Desfecho = {
      id: newId,
      prontuario: data.prontuario,
      tipo: data.tipo as 'alta' | 'obito',
      data_desfecho: data.data_desfecho,
      descricao: data.descricao || null,
      usuario_responsavel: data.usuario_responsavel || 'SISTEMA',
      intervencao_id: data.intervencao_id || null,
      created_at: now,
      updated_at: now
    };
    desfechosMock.push(newDesfecho);
    return newDesfecho;
  },

  updateDesfecho(id: number, data: { prontuario?: string; tipo?: string; data_desfecho?: string; descricao?: string; usuario_responsavel?: string; intervencao_id?: number }) {
    const idx = desfechosMock.findIndex(d => d.id === id);
    if (idx !== -1) {
      desfechosMock[idx] = {
        ...desfechosMock[idx],
        ...data,
        updated_at: new Date().toISOString()
      } as Desfecho;
      return desfechosMock[idx];
    }
    return null;
  },

  deleteDesfecho(id: number) {
    const idx = desfechosMock.findIndex(d => d.id === id);
    if (idx !== -1) {
      const removed = desfechosMock[idx];
      desfechosMock.splice(idx, 1);
      return removed;
    }
    return null;
  },

  getIndicadoresDesfecho(): IndicadoresDesfecho {
    const total_desfechos = desfechosMock.length;
    const total_altas = desfechosMock.filter(d => d.tipo === 'alta').length;
    const total_obitos = desfechosMock.filter(d => d.tipo === 'obito').length;
    const pacientes_com_desfecho = new Set(desfechosMock.map(d => d.prontuario)).size;

    // Group by tipo
    const tipoMap: Record<string, number> = {};
    desfechosMock.forEach(d => {
      tipoMap[d.tipo] = (tipoMap[d.tipo] || 0) + 1;
    });
    const por_tipo = Object.entries(tipoMap).map(([tipo, total]) => ({ tipo, total }));

    // Group by month
    const mesMap: Record<string, number> = {};
    desfechosMock.forEach(d => {
      const mes = d.data_desfecho.substring(0, 7);
      mesMap[mes] = (mesMap[mes] || 0) + 1;
    });
    const por_mes = Object.entries(mesMap)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([mes, total]) => ({ mes, total }));

    return {
      total_desfechos,
      total_altas,
      total_obitos,
      pacientes_com_desfecho,
      por_tipo,
      por_mes
    };
  }
};
