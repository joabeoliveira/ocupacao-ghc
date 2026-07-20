# Especificação Técnica do MVP

## 1. Objetivo

Substituir o frontend atual (HTML inline servido pelo FastAPI) por uma aplicação Next.js moderna, consumindo a mesma API REST FastAPI já em produção. A reescrita é **exclusivamente de frontend** — o backend permanece inalterado.

## 2. Público-alvo

Equipe de enfermagem, médicos e assistentes sociais do Grupo Hospitalar Conceição (GHC) que atuam no EGAA (Escritório de Gestão de Altas e Acompanhamento).

## 3. Funcionalidades por Página

### 3.1 Login (`/login`)

- Formulário de email + senha
- Validação com Zod
- Autenticação via `POST /api/auth/login` (a ser criada no backend)
- Redireciona para `/dashboard` após sucesso
- Proteger rotas com Next.js Middleware
- Sessão via cookie httpOnly com JWT

### 3.2 Dashboard (`/dashboard`)

**Objetivo:** Visão rápida e objetiva — apenas o essencial.

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  4 cards de KPI (ocupados, livres, bloqueados, %)  │
├─────────────────────────────────────────────────────┤
│  Gráfico de ocupação por unidade (barras)          │
├─────────────────────────────────────────────────────┤
│  Lista compacta: Top 10 pacientes + dias           │
│  + atalhos: [Longa Permanência] [Upload]           │
└─────────────────────────────────────────────────────┘
```

**Dados:**
- `GET /api/censo/kpis` — KPIs gerais
- `GET /api/censo/pacientes?page=1&page_size=10` — Top pacientes
- `GET /api/egaa/indicadores` — Indicadores EGAA

### 3.3 Longa Permanência — Centro de Controle (`/longa-permanencia`)

**Objetivo:** Foco principal no **grid de leitos**. Tabela é secundária.

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  KPIs compactos (total LP, 15+, 30+, 60+)          │
├─────────────────────────────────────────────────────┤
│  Filtros: prontuário, nome, especialidade, unidade │
├─────────────────────────────────────────────────────┤
│  [🛏️ Leitos] [📋 Tabela] ← toggle                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐    │
│  │Leito │ │Leito │ │Leito │ │Leito │ │Leito │    │
│  │13     │ │15    │ │22    │ │27    │ │31    │    │
│  │João..│ │Maria │ │Carl..│ │Ana.. │ │Pedro │    │
│  │32d   │ │19d   │ │45d   │ │28d   │ │60d   │    │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘    │
│                                                     │
│  < Página 1 de 12 >                                │
└─────────────────────────────────────────────────────┘
```

**Card do leito:**
- Faixa colorida no topo: laranja (15-29d) / vermelho (30+) / escuro (30+ e 60+)
- Nome do paciente (truncado)
- Prontuário e dias
- Badge EGAA (se tem atuações)
- **Hover:** tooltip com dados completos
- **Click:** abre modal de gestão EGAA

**Modal EGAA (ao clicar no leito):**
```
┌─ Nome · #prontuario ─────────────────────────[×]─┐
│                                                    │
│ ┌─📝 Nova atuação──────────┐ ┌─📋 Intervenções──┐│
│ │ Tipo        [dropdown]  │ │ 📌 Round         ││
│ │ Responsável [text]      │ │ 🔄 Acompanhamento ││
│ │ Data        [date]      │ └──────────────────┘│
│ │ Status      [dropdown]  │ ┌─🚧 Pendências───┐│
│ │ Descrição   [textarea]  │ │ ⬜ Regul   [✓]  ││
│ │ [Adicionar]             │ │ ☑ ATB           ││
│ └──────────────────────────┘ │ [+] Pendência   ││
│ ┌─📄 Evolução─────────────┐ └──────────────────┘│
│ │ [textarea] [Salvar]     │                      │
│ └──────────────────────────┘                      │
│              [Abrir página completa →]            │
└────────────────────────────────────────────────────┘
```

**Endpoints:**
- `GET /api/censo/pacientes?min_dias=15&page=1&page_size=50`
- `GET /api/censo/kpis` (com filtro de data)
- `GET /api/egaa/intervencoes?prontuario=X`
- `POST /api/egaa/intervencoes`
- `GET /api/egaa/pendencia/{prontuario}`
- `POST /api/egaa/pendencia/{prontuario}`
- `PUT /api/egaa/pendencia/{prontuario}/{id}`
- `GET /api/egaa/tipos-intervencao`
- `GET /api/egaa/pendencia/codigos`
- `PUT /api/censo/paciente/{prontuario}/evolucao`

### 3.4 Configurações (`/configuracoes`)

- Lista de tipos de intervenção (com toggle ativo/inativo)
- Ordem de exibição editável
- Formulário de registro rápido de intervenção avulsa

### 3.5 Upload (`/upload`)

- Drag & drop de arquivo CSV/XLSX
- Select de tipo: Automático / Censo diário / Carga histórica
- Feedback visual de progresso
- `POST /api/upload/arquivo`

## 4. Componentes Planejados

```
src/components/
├── ui/                    # Átomos
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Select.tsx
│   ├── Badge.tsx
│   ├── Card.tsx
│   ├── Modal.tsx
│   └── KpiCard.tsx
├── leitos/                # Gerência de leitos
│   ├── LeitoGrid.tsx      # Grid de cards
│   ├── LeitoCard.tsx      # Card individual + tooltip
│   └── LeitoTooltip.tsx   # Tooltip no hover
├── modal/                 # Modal EGAA
│   ├── ModalPaciente.tsx  # Container do modal
│   ├── NovaAtuacao.tsx    # Formulário de atuação
│   ├── Timeline.tsx       # Lista de intervenções
│   ├── Pendencias.tsx     # Lista de pendências
│   └── Evolucao.tsx       # Campo de evolução
├── dashboard/
│   ├── KpiRow.tsx         # Linha de KPIs
│   ├── GraficoUnidade.tsx # Gráfico de ocupação
│   └── TopPacientes.tsx   # Top 10 pacientes
└── layout/
    ├── Sidebar.tsx        # Navegação lateral
    └── Header.tsx         # Topo com versão
```

## 5. Regras de Negócio

1. **Longa permanência:** pacientes com `dias_internacao >= 15`
2. **Criticidade:**
   - Laranja: 15-29 dias
   - Vermelho: >= 30 dias
   - Vermelho escuro: >= 30 dias E >= 60 anos
3. **Censo diário:** usar sempre `fonte_dado = 'censo_diario'`
4. **Snapshot:** quando sem filtro de data, usar `MAX(data_snapshot)`
