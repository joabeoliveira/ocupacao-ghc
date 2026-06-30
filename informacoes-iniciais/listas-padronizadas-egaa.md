# Listas Padronizadas EGAA

Fonte base: `lista-suspensa-planilha.md`

## Objetivo

Padronizar os campos de seleção do MVP do EGAA para que o formulário, os filtros e os relatórios usem os mesmos códigos e rótulos.

Regra principal do modelo operacional:

- `1 paciente -> N atuações EGAA`
- cada atuação pertence a um prontuário e pode registrar uma intervenção isolada ou uma combinação de ações

## Regras de modelagem

- usar código estável para integração com banco e API;
- usar rótulo legível na interface;
- permitir multisseleção apenas onde a operação exigir;
- manter histórico legado mapeável para os novos códigos;
- sempre que houver sinônimos, escolher um nome canônico e guardar os demais como observação/alias.

## Lista 1. Tipo de atuação EGAA

Lista principal sugerida para o formulário do paciente.

### Assistencial e clínico

- `evolucao_egaa` - Evolução EGAA
- `entrevista_clinica` - Entrevista clínica
- `entrevista_enfermagem` - Entrevista de enfermagem
- `acompanhamento_quadro_clinico` - Acompanhamento do quadro clínico
- `manejo_clinico` - Manejo clínico
- `manejo_sintomatico` - Manejo sintomático
- `reavaliacao_medica` - Reavaliação médica
- `procedimento` - Procedimento
- `tratamento_terapeutico` - Realizando tratamento terapêutico
- `tratamento_oncologico` - Tratamento oncológico / regulação

### Exames e diagnósticos

- `laudo` - Laudos
- `encaixe_exame` - Encaixe de exame
- `exame_pendente` - Exame pendente
- `resultado_exame_pendente` - Resultado de exame pendente
- `cpre` - CPRE
- `ecott` - ECOTT
- `ecote` - ECOTE
- `tomografia` - Tomografia
- `ressonancia_magnetica` - Ressonância magnética
- `holter` - Holter
- `doppler` - Doppler
- `biopsia` - Biópsia

### Regulação, leito e transferência

- `movimentacao_leito` - Solicitação de movimentação de leito
- `regulacao` - Regulação
- `regulacao_clinica_hd` - Regulação clínica satélite de HD
- `acompanhamento_regulacao` - Acompanhar exames/consultas/procedimentos regulados via NIR
- `transferencia_hospitalar` - Aguarda regulação para transferência hospitalar
- `transferencia_oncologica` - Acompanhar solicitação de transferência para hospital oncológico
- `transferencia_transplante` - Transferência para transplante
- `abrigo` - Regulado para abrigo
- `leito_cuidados_prolongados` - Aguarda vaga de leito de cuidados prolongados
- `home_care` - Aguarda home care
- `padi_pmec` - Aguarda PADI / PMEC
- `melhor_em_casa` - Melhor em Casa

### Social, família e rede

- `articulacao_equipe_especialistas` - Articulação com equipe de especialistas
- `articulacao_rede` - Articulação com a rede
- `reuniao_equipe_assistencial` - Reunião com equipe assistencial
- `conferencia_familiar` - Conferência familiar
- `contato_cuidador_familiar` - Contato com cuidador/familiar
- `entrevista_social` - Entrevista social
- `servico_social` - Serviço social
- `orientacao_educativa` - Orientação educativa
- `orientacao_recursos_terapeuticos` - Orientação quanto aos recursos terapêuticos disponíveis
- `orientacao_recursos_sociais` - Orientação quanto aos recursos sociais
- `assistencia_social` - Longa permanência / ação social
- `vulnerabilidade_social` - Vulnerabilidade social
- `vulnerabilidade_socioeconomica` - Vulnerabilidade socioeconômica
- `vulnerabilidade_emocional` - Vulnerabilidade emocional
- `familia_nao_cooperativa` - Família não cooperativa
- `familia_acompanhante_alta` - Familiar acompanhante para alta
- `documentacao_pendente` - Aguardando documentação via cartório
- `documento_identidade` - Documento de identidade

### Alta e desospitalização

- `planejamento_alta` - Planejamento da alta hospitalar
- `pendencia_alta` - Pendência para alta
- `programacao_internacao` - Organização de programação para internação e regulação de leito
- `alta_hospitalar` - Alta hospitalar
- `alta_assistida` - Alta assistida
- `cuidados_paliativos` - Cuidados paliativos
- `cuidados_pos_operatorios` - Cuidados pós-operatórios
- `cuidados_fim_vida` - Cuidados de fim de vida
- `oxigenoterapia_domiciliar` - Oxigenoterapia domiciliar
- `transporte_sanitario` - Transporte sanitário eletivo

## Lista 2. Pendências para alta

Lista recomendada para o campo `motivo_pendencia` ou equivalente.

- `regulacao`
- `ajuste_inr`
- `ajuste_medicamento`
- `tratamento_lesoes`
- `antibioticoterapia`
- `definicao_diagnostica`
- `ajuste_laboratorial`
- `exame_pendente`
- `aguarda_parecer_especialista`
- `definicao_terapeutica`
- `reavaliacao_medica`
- `descompensacao_clinica`
- `procedimento_cirurgico`
- `aguarda_gtt_por_eda`
- `aguarda_cirurgia_cardiaca`
- `manejo_clinico`
- `manejo_sintomatico`
- `cuidados_paliativos`
- `cuidados_pos_operatorios`
- `cuidados_fim_vida`
- `fragilidade_familiar`
- `vulnerabilidade_social`
- `vulnerabilidade_socioeconomica`
- `vulnerabilidade_emocional`
- `documento_identidade`
- `familia_nao_cooperativa`
- `aguarda_padi_pmec`
- `aguarda_home_care`
- `aguarda_vaga_abrigo`
- `aguardando_documentacao`
- `transporte_sanitario_eletivo`
- `familiar_acompanhante_alta`
- `aguarda_leito_cuidados_prolongados`
- `aguarda_regulacao_transferencia`
- `aguarda_regulacao_marcapasso`

## Lista 3. Status da atuação

- `aberta`
- `em_andamento`
- `concluida`
- `cancelada`

## Lista 4. Prioridade operacional

- `baixa`
- `media`
- `alta`
- `critica`

## Lista 5. Regras de multisseleção

O formulário do paciente deve permitir:

- adicionar várias atuações no mesmo prontuário;
- salvar todas em lote;
- manter cada atuação como registro independente no banco;
- exibir o histórico em ordem temporal;
- reutilizar o mesmo prontuário sem recriar o paciente.

## Sugestão de uso no projeto

- formulário do paciente: usar `tipo de atuação`, `título`, `status`, `responsável`, `data prevista`, `data de conclusão`, `observação`;
- linha do tempo: mostrar o rótulo do tipo, o status e a data da última atualização;
- relatórios: usar os códigos canônicos para agrupar indicadores;
- planilha/seed: manter esta lista como base de referência para novas migrações.


## Lista de intervenções EGAA constante na planilha

- LAUDOS
- ENCAIXE DE EXAME
- ARTICULAÇÃO COM EQUIPE DE ESPECIALISTAS
- ENTREVISTA CLÍNICA
- ORIENTAÇÃO QUANTO AOS RECURSOS TERAPÊUTICOS DISPONÍVEIS
- PROCEDIMENTOS
- SOLICITADO ACOMPANHAMENTO DA T.O.
- SOLICITADO MOVIMENTAÇÃO DE LEITO - NIR
- ORIENTAÇÃO QUANTO A REGULAÇÃO
- SOLICITADO AGILIDADE NA RESPOSTA DO PARECER
- SOLICITADO ACOMPANHAMENTO DA ODONTOLOGIA
- DISCUTIDO PENDENCIAS E CONDUTAS EM ROUND
- REUNIÃO COM EQUIPE ASSISTENCIAL
- SOLICITADO ACOMPANHAMENTO DA FISIOTERAPIA
- ORIENTAÇÃO EDUCATIVA
- SOLICITADO ACOMPANHAMENTO DO SERVIÇO SOCIAL
- MELHOR EM CASA
- CONFERENCIA FAMILIAR
- SOLICITAÇÃO DE TRANSPORTE
- ENTREVISTA SOCIAL
- SOLICITADO ACOMPANHAMENTO DA PSICOLOGIA
- ORIENTAÇÃO QUANTO AOS RECURSOS SOCIAIS
- CONTATO COM CUIDADOR/FAMILIAR
- SERVIÇO SOCIAL
- REGULADO PARA ABRIGO
- ORGANIZAÇÃO DE PROGRAMAÇÃO PARA INTERNAÇÃO E REGULAÇÃO DE LEITO
- ARTICULAÇÃO COM A REDE
- ENTREVISTA DE ENFERMAGEM
- ACOMPANHAMENTO DO QUADRO CLÍNICO DE PACIENTE
- SOLICITADO BREVIDADE EM EXAMES LABORATORIAIS
- ACOMPANHAR EXAMES/CONSULTAS/PROCEDIMENTOS REGULADOS VIA NIR
- ACOMPANHAMENTO DE REGULAÇÃO DE HD
- ACOMPANHAR SOLICITAÇÃO DE TRANSFERÊNCIA PARA HOSPITAL ONCOLÓGICO
- PLANEJAMENTO DA ALTA HOSPITALAR

## Lista otimizada para o formulário do paciente

- Acompanhado pela Fisioterapia
- Acompanhado pela Odontologia
- Acompanhado pela Psicologia
- Acompanhado pela Terapia Ocupacional
- Acompanhado pelo Serviço Social
- Articulado com a rede
- Avaliado quadro clínico
- Organizada vaga (NIR)
- Planejada alta hospitalar
- Realizada conferência familiar
- Realizada entrevista clínica
- Realizada entrevista social
- Realizada reunião com equipe
- Registradas orientações
- Registrado laudo técnico
- Solicitados exames/consultas
- Solicitado transporte

