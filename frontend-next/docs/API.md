# Documentação da API REST (FastAPI)

Base URL: `{NEXT_PUBLIC_API_URL}` (ex: `https://app.exemplo.com/api`)

---

## Autenticação

### `POST /api/auth/login`

Autentica o usuário e retorna JWT.

**Request:**
```json
{
  "email": "user@ghc.com.br",
  "senha": "123456"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "usuario": {
    "nome": "João Silva",
    "email": "user@ghc.com.br"
  }
}
```

---

## Censo

### `GET /api/censo/kpis`

Retorna KPIs de ocupação.

**Query params:** `?data_inicio=2026-07-01&data_fim=2026-07-13`

**Response (200):**
```json
{
  "total_internados": 412,
  "longa_permanencia_15": 152,
  "longa_permanencia_30": 84,
  "longa_permanencia_40": 53,
  "longa_permanencia_60_anos": 98,
  "longa_permanencia_60_15": 45,
  "longa_permanencia_60_30": 28,
  "leitos_ocupados": 412,
  "leitos_livres": 165,
  "leitos_bloqueados": 65,
  "taxa_ocupacao_geral_percentual": 64.1,
  "taxa_ocupacao_operacional_percentual": 71.4,
  "taxa_ocupacao_ajustada_sem_emergencia_percentual": 68.2,
  "ocupacao_por_unidade": [
    { "unidade": "HFB", "total_pacientes": 280 }
  ]
}
```

### `GET /api/censo/pacientes`

Lista pacientes internados com paginação e filtros.

**Query params:**
| Parâmetro | Tipo | Descrição |
|-----------|------|-----------|
| `page` | int | Página atual (default: 1) |
| `page_size` | int | Itens por página (1-200, default: 10) |
| `prontuario` | string | Busca parcial por prontuário |
| `nome` | string | Busca parcial por nome |
| `especialidade` | string | Filtro por especialidade |
| `unidade` | string | Filtro por unidade |
| `min_dias` | int | Dias mínimos de internação |
| `idade_minima` | int | Idade mínima |
| `data_inicio` | date | Filtro por data (YYYY-MM-DD) |
| `data_fim` | date | Filtro por data (YYYY-MM-DD) |

**Response (200):**
```json
{
  "total": 412,
  "page": 1,
  "page_size": 10,
  "items": [
    {
      "id": 1,
      "prontuario": "8399062",
      "nome_paciente": "IRENE DOS SANTOS",
      "idade_anos": 83,
      "data_internacao": "2025-12-11T00:00:00",
      "dias_internacao": 210,
      "especialidade": "CLÍNICA MÉDICA",
      "unidade": "HFB",
      "enfermaria": "CM Mista",
      "leito": "220-13",
      "status_leito": "Ocupado",
      "cid_internacao_codigo": "I50",
      "cid_internacao_descricao": "Insuficiência cardíaca",
      "evolucao": "ENF: 21/01/2026 - ...",
      "egaa_total_atuacoes": 12,
      "egaa_ultima_atuacao": "2026-07-09"
    }
  ]
}
```

### `GET /api/censo/paciente/{prontuario}`

Detalhe completo de um paciente.

**Response (200):** Mesmo schema de `PacienteInternadoResponse` acima, incluindo `evolucao`.

### `PUT /api/censo/paciente/{prontuario}/evolucao`

Atualiza o campo de evolução do paciente.

**Request:**
```json
{
  "evolucao": "ENF: 13/07/2026 - Paciente estável..."
}
```

### `GET /api/censo/export/xlsx`

Exporta lista de pacientes em XLSX. Aceita mesmos filtros de `GET /pacientes`.

---

## EGAA — Intervenções

### `GET /api/egaa/tipos-intervencao`

Lista tipos de intervenção disponíveis.

**Response (200):**
```json
[
  {
    "id": 1,
    "nome": "Evolução EGAA",
    "descricao": "Registro de evolução clínica pelo EGAA",
    "ativo": true,
    "ordem_exibicao": 0
  }
]
```

### `GET /api/egaa/intervencoes?prontuario=X`

Lista intervenções de um paciente.

**Response (200):**
```json
[
  {
    "id": 1,
    "prontuario": "8399062",
    "tipo_intervencao_id": 1,
    "titulo": "Evolução EGAA",
    "descricao": "Descrição textual...",
    "status": "concluida",
    "usuario_responsavel": "ENF EDUARDO",
    "data_atuacao": "2026-02-25",
    "observacao": "Round realizado."
  }
]
```

### `POST /api/egaa/intervencoes`

Cria nova intervenção.

**Request:**
```json
{
  "prontuario": "8399062",
  "tipo_intervencao_id": 5,
  "titulo": "Acompanhamento clínico",
  "descricao": "Paciente estável...",
  "status": "aberta",
  "usuario_responsavel": "ENF EDUARDO",
  "data_atuacao": "2026-07-13"
}
```

### `POST /api/egaa/intervencoes/lote`

Cria múltiplas intervenções de uma vez.

### `PUT /api/egaa/intervencoes/{id}`

Atualiza uma intervenção.

### `DELETE /api/egaa/intervencoes/{id}`

Remove uma intervenção.

---

## EGAA — Pendências

### `GET /api/egaa/pendencia/codigos`

Lista códigos padronizados de pendências.

**Response (200):**
```json
[
  { "codigo": "regulacao", "rotulo": "Regulação" },
  { "codigo": "antibioticoterapia", "rotulo": "Antibioticoterapia" },
  { "codigo": "exame_pendente", "rotulo": "Exame pendente" }
]
```

### `GET /api/egaa/pendencia/{prontuario}`

Lista pendências de um paciente.

**Response (200):**
```json
[
  {
    "id": 1,
    "prontuario": "8399062",
    "codigo": "regulacao",
    "resolvida": false
  }
]
```

### `POST /api/egaa/pendencia/{prontuario}`

Adiciona pendência.

**Request:**
```json
{
  "codigo": "regulacao"
}
```

### `PUT /api/egaa/pendencia/{prontuario}/{id}`

Atualiza pendência (ex: marcar como resolvida).

**Request:**
```json
{
  "resolvida": true
}
```

### `DELETE /api/egaa/pendencia/{prontuario}/{id}`

Remove pendência.

---

## EGAA — Indicadores

### `GET /api/egaa/indicadores`

Indicadores gerais do EGAA.

---

## Upload

### `POST /api/upload/arquivo`

Upload de arquivo (processamento automático).

### `POST /api/upload/censo`

Upload de censo diário.

### `POST /api/upload/historico`

Upload de carga histórica.
