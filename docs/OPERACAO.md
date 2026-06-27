# Operação e fechamento do MVP EGAA

Este guia consolida os passos finais para homologar o MVP depois que o banco `ocupacao_leitos_ghc` já estiver populado.

## 1. Pré-requisitos

- API configurada com `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT` e `MYSQL_DATABASE`.
- Migration `migrations/001_create_ocupacao_leitos_esusreport.sql` aplicada no banco.
- Dados históricos e/ou censo diário já carregados pelo ETL.

## 1.1 Aplicação de migrations

Para aplicar as tabelas novas do EGAA, use o runner local:

```bash
python scripts/apply_migrations.py
```

O script cria a tabela `schema_migrations`, aplica os arquivos `.sql` em ordem e registra o que já foi executado.

## 2. Auditoria do banco populado

Execute `scripts/auditoria_ocupacao_leitos.sql` no MySQL de produção ou homologação. A revisão deve confirmar:

1. Totais por `fonte_dado`, lote e arquivo.
2. Ausência de campos obrigatórios vazios: `prontuario`, `especialidade`, `hash_registro`, `lote_importacao_id` e `data_internacao`.
3. Ausência de altas anteriores à internação.
4. `censo_diario` sempre com `data_snapshot` preenchida.
5. Nenhuma duplicidade lógica por `(fonte_dado, hash_registro)`.
6. KPIs SQL compatíveis com `GET /api/censo/kpis`.

Diferenças entre linhas processadas no upload e `COUNT(*)` no banco podem ser esperadas quando houver upsert pela chave única `(fonte_dado, hash_registro)`.

## 3. Validação da API

Com a aplicação em execução, valide os endpoints abaixo:

```bash
curl -f http://localhost:8000/health
curl -f http://localhost:8000/api/censo/kpis
curl -f 'http://localhost:8000/api/censo/pacientes?page=1&page_size=10'
```

Critérios mínimos de aceite:

- `/health` retorna HTTP 200.
- `/api/censo/kpis` retorna totais coerentes com a auditoria SQL.
- `/api/censo/pacientes` pagina resultados e permite filtros por `especialidade`, `unidade`, `data_inicio`, `data_fim` e `min_dias`.
- A tela `/upload` continua disponível para novas cargas operacionais.

## 4. Fluxo da interface

As rotas principais da interface web são:

- `/dashboard` ou `/` redirecionado para `dashboard`
- `/pacientes` para a lista filtrável de internações
- `/longa-permanencia` para foco em pacientes com `15+` dias
- `/configuracoes` para parametrizar tipos de intervenção e registrar ações do EGAA
- `/upload` para envio manual de arquivos

Uso recomendado:

1. Abrir `/dashboard` para a leitura executiva inicial.
2. Usar os filtros do topo para recorte por especialidade, unidade e período.
3. Abrir `/longa-permanencia` quando a prioridade for atuação sobre internações prolongadas.
4. Abrir `/pacientes` quando a prioridade for investigação de casos individuais.

## 5. Validação automatizada local

Antes de publicar alterações, rode:

```bash
python -m py_compile src/etl/etl_process.py
pytest -q
```

Esses checks protegem principalmente parsing, normalização, geração de hash e sanitização de valores pandas nulos antes do upsert no MySQL.

## 6. Checklist pós-deploy no Easypanel

1. Confirmar variáveis de ambiente do MySQL no painel.
2. Verificar logs do contêiner após o build.
3. Acessar `GET /health`.
4. Comparar `GET /api/censo/kpis` com a seção de KPIs do script de auditoria.
5. Abrir `/dashboard`, `/pacientes`, `/longa-permanencia` e `/configuracoes` para confirmar navegação e filtros.
6. Abrir `/upload` e testar um upload pequeno de censo, se aplicável.
7. Revisar se novos uploads não criam duplicidades inesperadas.

## 7. Critério de conclusão

Considere o MVP concluído quando:

- Testes automatizados passam.
- Auditoria SQL não aponta inconsistências críticas.
- API responde com dados coerentes do banco populado.
- Deploy está documentado e reproduzível.
- O fluxo de upload diário está validado para uso operacional.
- As rotas `/dashboard`, `/pacientes`, `/longa-permanencia`, `/configuracoes` e `/upload` estão funcionais e alinhadas ao design-system.
