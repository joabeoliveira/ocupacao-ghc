# Estrutura do Projeto Next.js

```
egaa-frontend/
├── .env.local                    # Variáveis de ambiente
├── next.config.js                # Config Next.js
├── tailwind.config.ts            # Paleta GHC + plugins
├── tsconfig.json                 # TypeScript strict
├── package.json
├── Dockerfile                    # Deploy Easypanel
│
├── src/
│   ├── middleware.ts             # Proteção de rotas (JWT)
│   │
│   ├── app/                      # App Router
│   │   ├── layout.tsx            # Layout raiz (sidebar global)
│   │   ├── page.tsx              # Redirect → /dashboard
│   │   │
│   │   ├── login/
│   │   │   └── page.tsx          # Formulário de login
│   │   │
│   │   ├── dashboard/
│   │   │   └── page.tsx          # KPIs + gráfico + top pacientes
│   │   │
│   │   ├── longa-permanencia/
│   │   │   └── page.tsx          # Centro de controle (grid leitos)
│   │   │
│   │   ├── configuracoes/
│   │   │   └── page.tsx          # Admin tipos de intervenção
│   │   │
│   │   └── upload/
│   │       └── page.tsx          # Upload drag & drop
│   │
│   ├── components/
│   │   ├── ui/                   # Átomos
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Select.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── KpiCard.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Toggle.tsx        # Alternador Tabela/Leitos
│   │   │   └── Pagination.tsx
│   │   │
│   │   ├── leitos/               # Gerência de leitos
│   │   │   ├── LeitoGrid.tsx     # Grid responsivo
│   │   │   ├── LeitoCard.tsx     # Card individual
│   │   │   └── LeitoTooltip.tsx  # Tooltip hover
│   │   │
│   │   ├── modal/                # Modal EGAA (paciente)
│   │   │   ├── ModalPaciente.tsx # Container + abrir/fechar
│   │   │   ├── NovaAtuacao.tsx   # Formulário de atuação
│   │   │   ├── Timeline.tsx      # Lista de intervenções
│   │   │   ├── Pendencias.tsx    # Lista de pendências
│   │   │   └── Evolucao.tsx      # Campo de evolução
│   │   │
│   │   ├── dashboard/
│   │   │   ├── KpiRow.tsx        # Linha de cards KPI
│   │   │   ├── GraficoUnidade.tsx # Gráfico ocupação
│   │   │   └── TopPacientes.tsx  # Top 10 tabela
│   │   │
│   │   └── layout/
│   │       ├── Sidebar.tsx       # Navegação lateral
│   │       └── VersionBadge.tsx  # Badge de versão
│   │
│   ├── lib/
│   │   ├── api.ts                # Cliente HTTP (fetch wrapper)
│   │   ├── auth.ts               # Context de autenticação
│   │   ├── utils.ts              # Helpers (fmtDate, cn, etc.)
│   │   └── queries.ts            # TanStack Query hooks
│   │
│   └── types/
│       └── index.ts              # Interfaces TypeScript
│
└── public/
    └── logo-ghc.svg              # Logo GHC
```

## Dependências (package.json)

```json
{
  "dependencies": {
    "next": "^14.2",
    "react": "^18.3",
    "react-dom": "^18.3",
    "@tanstack/react-query": "^5.0",
    "react-hook-form": "^7.0",
    "@hookform/resolvers": "^3.0",
    "zod": "^3.0",
    "recharts": "^2.0",
    "clsx": "^2.0",
    "lucide-react": "^0.0"
  },
  "devDependencies": {
    "typescript": "^5.0",
    "tailwindcss": "^3.4",
    "postcss": "^8.0",
    "autoprefixer": "^10.0",
    "@types/node": "^20.0",
    "@types/react": "^18.0"
  }
}
```

## Principais Hooks TanStack Query

```ts
// src/lib/queries.ts
import { useQuery, useMutation } from '@tanstack/react-query';
import { api } from './api';

export function useKPIs(dataInicio?: string, dataFim?: string) {
  return useQuery({
    queryKey: ['kpis', dataInicio, dataFim],
    queryFn: () => api.get(`/censo/kpis`, { params: { data_inicio: dataInicio, data_fim: dataFim } }),
  });
}

export function usePacientes(params: PacientesParams) {
  return useQuery({
    queryKey: ['pacientes', params],
    queryFn: () => api.get('/censo/pacientes', { params }),
  });
}

export function useIntervencoes(prontuario: string) {
  return useQuery({
    queryKey: ['intervencoes', prontuario],
    queryFn: () => api.get(`/egaa/intervencoes?prontuario=${prontuario}`),
    enabled: !!prontuario,
  });
}

export function useTiposIntervencao() {
  return useQuery({
    queryKey: ['tipos-intervencao'],
    queryFn: () => api.get('/egaa/tipos-intervencao'),
    staleTime: 5 * 60 * 1000, // 5 min cache
  });
}

export function useCriarIntervencao() {
  return useMutation({
    mutationFn: (data: any) => api.post('/egaa/intervencoes', data),
  });
}
```

## Types

```ts
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
```
