STATUS DO PROJETO - Ocupação NIR
Data: 2026-06-26

Resumo do que foi feito
- ETL: parsing robusto de CSV/XLS/XLSX, normalização e hashing por `hash_registro` para idempotência.
- Sanitização: `_sanitize_record_for_sql` evita `NaT/NaN` sendo enviados ao MySQL.
- Correção: `_recalculate_dias` implementada e integrada em `normalize_historico` e `normalize_censo` (commit enviado) para evitar valores absurdos em `dias_internacao`.
- Persistência: inserção por batches + upsert (`ON DUPLICATE KEY UPDATE`) via SQLAlchemy/MySQL.
- Backend: FastAPI com endpoints `/api/censo/kpis` e `/api/censo/pacientes` funcionando.
- UI: páginas de `upload` e `dashboard` implementadas; backend retorna dados (possível problema cliente se dashboard mostrar vazio).
- Scripts: `scripts/prod_smoke.sh` e `scripts/prod_smoke.ps1` adicionados para checagens de produção.

Próximos passos (prioridade alta → baixa)
1) Redeploy em produção
   - Objetivo: colocar a correção do ETL em produção.
   - Comandos (exemplo):
     ```powershell
     docker build -t ghcr.io/<user>/ocupacao-ghc:latest .
     docker push ghcr.io/<user>/ocupacao-ghc:latest
     ```
   - Alternativa: usar painel Easypanel para atualizar a imagem a partir do repositório.

2) Reprocessar/validar com arquivo de teste
   - Rodar localmente o ETL com `--persist` em um arquivo de amostra ou no ambiente de staging.
     ```powershell
     python src/etl/etl_process.py --historico data/samples/relatorio-internacao.xls --persist --lote-id test-20260626
     ```

3) Corrigir dados existentes no banco (opcional/urgente)
   - Executar SQL que recalcula `dias_internacao` no banco (fazer backup antes):
     ```sql
     UPDATE ocupacao_leitos_ghc
     SET dias_internacao = GREATEST(
       CASE
         WHEN data_internacao IS NULL THEN NULL
         WHEN data_alta IS NULL THEN DATEDIFF(CURDATE(), DATE(data_internacao))
         ELSE DATEDIFF(DATE(data_alta), DATE(data_internacao))
       END, 0
     );
     ```
   - Preferível aplicar via migration para rastreabilidade.

4) Diagnóstico do dashboard (se continuar vazio)
   - Verificar DevTools → Console/Network para erros JS e requests falhando a `/api/censo/*`.
   - Rodar `./scripts/prod_smoke.sh` (ou `.
ecipes	ools
un_smoke.ps1`) para reproduzir.
   - Se quiser, eu faço a investigação remota/loca agora (cole logs do console ou permita que eu execute checagens).

5) Prevenção e qualidade
   - Adicionar testes unitários para `dias_internacao` e para sanitização `NaT/NaN`.
   - Criar CI que rode testes e lint antes do deploy.

6) Migração (opcional)
   - Criar migration que execute o SQL de correção e registre a operação (reversível se necessário).

Como validar as correções
- Endpoints:
  - `/api/censo/kpis` — deve retornar `total_internados` > 0 e distribuições por unidade.
  - `/api/censo/pacientes` — deve retornar lista de pacientes com `dias_internacao` plausíveis.
- UI:
  - Abrir `/dashboard`, forçar reload (Ctrl+F5) e usar o botão Recarregar na página.
- Banco:
  - Verificar valores máximos de `dias_internacao` via SQL: `SELECT MAX(dias_internacao) FROM ocupacao_leitos_ghc;` (valores > 1000 indicam problema histórico).

Próximo passo imediato sugerido
- Deseja que eu: (A) gere a migration SQL para correção no banco, (B) rode um reprocessamento de teste localmente agora, (C) abra diagnóstico do dashboard (peça-me os logs do console), ou (D) apenas documente isso e aguarde seu redeploy? 

Arquivo criado: `STATUS_PROJETO.md`
