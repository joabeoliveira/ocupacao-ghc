# EGAA — Frontend Next.js

Painel de Regulação e Censo Hospitalar (EGAA) — Grupo Hospitalar Conceição (GHC).

> **Status:** MVP em reescrita do frontend legado (FastAPI + HTML inline) para Next.js 14 + Tailwind CSS + TypeScript.
> **Backend:** FastAPI atual permanece como REST API.

## Stack

| Tecnologia | Versão | Finalidade |
|-----------|--------|-----------|
| Next.js | 14 (App Router) | Framework React full-stack |
| TypeScript | strict | Tipagem segura |
| Tailwind CSS | 3.x | Estilização utilitária |
| TanStack Query | 5.x | Cache e estado servidor |
| React Hook Form | 7.x | Formulários performáticos |
| Zod | 3.x | Validação de schemas |
| JWT | — | Autenticação stateless |

## Páginas

| Rota | Descrição |
|------|-----------|
| `/login` | Autenticação email + senha |
| `/dashboard` | KPIs e visão geral otimizada |
| `/longa-permanencia` | **Centro de controle** — grid de leitos como foco principal |
| `/configuracoes` | Admin de tipos de intervenção |
| `/upload` | Upload de arquivos CSV/XLSX |

## Repositórios

- **Frontend:** `github.com/joabeoliveira/egaa-frontend`
- **Backend:** `github.com/joabeoliveira/ocupacao-ghc` (API FastAPI existente)

## Como Rodar

```bash
# Desenvolvimento
npm install
npm run dev

# Build produção
npm run build
npm start
```

## Variáveis de Ambiente

```env
NEXT_PUBLIC_API_URL=https://api.exemplo.com/api
JWT_SECRET=seu-segredo-aqui
```
