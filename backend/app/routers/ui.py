from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse


router = APIRouter(tags=["UI"])


@router.get("/upload", response_class=HTMLResponse)
def upload_page() -> str:
    return """
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>EGAA - Upload de Arquivo</title>
  <style>
    :root {
      --bg: #F7F9FB;
      --panel: #FFFFFF;
      --panel-border: #DCE3EA;
      --text: #1F2937;
      --muted: #6B7280;
      --brand: #005C99;
      --brand-hover: #004A7A;
    }
    body { font-family: Inter, Arial, sans-serif; background: linear-gradient(180deg, #ffffff 0%, var(--bg) 100%); margin: 0; padding: 24px; color: var(--text); }
    .card { max-width: 720px; margin: 0 auto; background: var(--panel); border: 1px solid var(--panel-border); border-radius: 12px; padding: 20px; box-shadow: 0 8px 24px rgba(16,24,40,0.06); }
    h1 { margin: 0 0 8px; font-size: 22px; color: var(--brand); }
    p { color: var(--muted); margin-top: 0; }
    label { display: block; margin-top: 14px; margin-bottom: 6px; font-weight: 600; color: var(--text); }
    select, input[type=file], button { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid var(--panel-border); }
    button { margin-top: 16px; background: var(--brand); color: #fff; border: none; font-weight: 600; cursor: pointer; }
    button:hover { background: var(--brand-hover); }
    pre { background: #102A43; color: #DCE3EA; padding: 12px; border-radius: 8px; overflow: auto; min-height: 120px; }
    .hint { font-size: 13px; color: var(--muted); margin-top: 8px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Upload de Arquivo EGAA</h1>
    <p>Envie um arquivo de censo ou historico sem precisar usar curl.</p>

    <label for="tipo">Tipo de processamento</label>
    <select id="tipo">
      <option value="auto">Automatico (recomendado)</option>
      <option value="censo">Censo diario</option>
      <option value="historico">Carga historica</option>
    </select>

    <label for="arquivo">Arquivo (.xls, .xlsx, .csv)</label>
    <input id="arquivo" type="file" accept=".xls,.xlsx,.csv" />

    <button id="enviar">Enviar arquivo</button>
    <p class="hint">Endpoint usado: <span id="endpoint">/api/upload/arquivo</span></p>

    <label>Resposta</label>
    <pre id="saida">Aguardando envio...</pre>
  </div>

  <script>
    const tipo = document.getElementById('tipo');
    const arquivo = document.getElementById('arquivo');
    const enviar = document.getElementById('enviar');
    const saida = document.getElementById('saida');
    const endpointEl = document.getElementById('endpoint');

    function resolveEndpoint() {
      if (tipo.value === 'censo') return '/api/upload/censo';
      if (tipo.value === 'historico') return '/api/upload/historico';
      return '/api/upload/arquivo';
    }

    tipo.addEventListener('change', () => {
      endpointEl.textContent = resolveEndpoint();
    });

    enviar.addEventListener('click', async () => {
      if (!arquivo.files || !arquivo.files.length) {
        saida.textContent = 'Selecione um arquivo antes de enviar.';
        return;
      }

      const formData = new FormData();
      formData.append('file', arquivo.files[0]);

      const endpoint = resolveEndpoint();
      endpointEl.textContent = endpoint;
      saida.textContent = 'Enviando...';

      try {
        const response = await fetch(endpoint, { method: 'POST', body: formData });
        const text = await response.text();
        if (!response.ok) {
          saida.textContent = `Erro ${response.status}: ${text}`;
          return;
        }
        try {
          saida.textContent = JSON.stringify(JSON.parse(text), null, 2);
        } catch {
          saida.textContent = text;
        }
      } catch (error) {
        saida.textContent = 'Falha de rede: ' + error;
      }
    });
  </script>
</body>
</html>
"""


def dashboard_page() -> str:
    return """
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>EGAA - Dashboard</title>
  <style>
    :root {
      --bg: #F7F9FB;
      --panel: #FFFFFF;
      --panel-border: #DCE3EA;
      --text: #1F2937;
      --muted: #6B7280;
      --brand: #005C99;
      --brand-strong: #004A7A;
      --secondary: #00A79D;
      --success: #2E7D32;
      --warning: #F9A825;
      --error: #C62828;
      --info: #0288D1;
    }
    body {
      font-family: Inter, Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(0, 92, 153, 0.08), transparent 28%),
        linear-gradient(180deg, #ffffff 0%, var(--bg) 100%);
      margin: 0;
      min-height: 100vh;
      color: var(--text);
    }
    .layout { display:grid; grid-template-columns: 260px 1fr; min-height: 100vh; }
    .sidebar {
      background: rgba(255,255,255,0.84);
      backdrop-filter: blur(10px);
      border-right: 1px solid var(--panel-border);
      padding: 24px 18px;
      position: sticky;
      top: 0;
      height: 100vh;
      box-sizing: border-box;
    }
    .brand { font-size: 18px; font-weight: 700; color: var(--brand-strong); margin: 0; }
    .brand-subtitle { margin: 6px 0 18px; color: var(--muted); font-size: 13px; }
    .nav { display:flex; flex-direction:column; gap:8px; margin-top: 18px; }
    .nav a {
      color: var(--text);
      text-decoration: none;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid transparent;
      font-weight: 600;
    }
    .nav a:hover { background: rgba(0, 92, 153, 0.06); border-color: var(--panel-border); }
    .nav a.primary { background: var(--brand); color: #fff; }
    .nav a.primary:hover { background: var(--brand-strong); border-color: transparent; }
    .sidebar-note {
      margin-top: 18px;
      padding: 12px;
      border-radius: 12px;
      background: #F0F7FC;
      border: 1px solid #D7E7F3;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }
    .main { padding: 24px; }
    .shell { max-width: 1200px; margin: 0 auto; }
    .header { display:flex; align-items:center; justify-content:space-between; gap: 16px; margin-bottom: 16px; }
    h1 { color:var(--brand-strong); margin:0; letter-spacing:-0.02em; }
    .subtitle { margin: 8px 0 0; color: var(--muted); }
    .header-actions { display:flex; gap: 10px; align-items:center; }
    .pill-link {
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:10px 12px;
      border-radius: 999px;
      background: var(--panel);
      border: 1px solid var(--panel-border);
      color: var(--brand);
      text-decoration: none;
      font-weight: 600;
    }
    .badge {
      display:inline-flex;
      align-items:center;
      gap:6px;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .02em;
      margin-bottom: 10px;
    }
    .badge-info { background: rgba(2, 136, 209, 0.12); color: var(--info); }
    .badge-warning { background: rgba(249, 168, 37, 0.16); color: #8A6500; }
    .badge-error { background: rgba(198, 40, 40, 0.12); color: var(--error); }
    .badge-success { background: rgba(46, 125, 50, 0.12); color: var(--success); }
    .badge-secondary { background: rgba(0, 167, 157, 0.12); color: var(--secondary); }
    .section-title { margin: 20px 0 10px; display:flex; align-items:end; justify-content:space-between; gap:12px; }
    .section-title h2 { margin:0; font-size: 18px; color: var(--brand-strong); }
    .section-title p { margin: 0; color: var(--muted); font-size: 13px; }
    .filters {
      margin-top: 14px;
      padding: 16px;
      background: rgba(255,255,255,0.9);
      border: 1px solid var(--panel-border);
      border-radius: 16px;
      box-shadow: 0 8px 24px rgba(16,24,40,0.06);
    }
    .filters-grid {
      display:grid;
      grid-template-columns: repeat(7, minmax(0, 1fr));
      gap: 10px;
      align-items:end;
    }
    .field { display:flex; flex-direction:column; gap:6px; min-width: 0; }
    .field label { font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); font-weight: 700; }
    .field input, .field select {
      width: 100%;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid #cfd8e3;
      box-sizing: border-box;
      background: #fff;
    }
    .actions { display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end; }
    .secondary-btn {
      background:#EEF5FA;
      color:var(--brand);
      border:1px solid var(--panel-border);
      cursor:pointer;
    }
    .cards { display:grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap:12px; margin-top:16px; }
    .card {
      background:var(--panel);
      padding:14px 16px;
      border-radius:14px;
      box-shadow:0 8px 24px rgba(16,24,40,0.08);
      border:1px solid var(--panel-border);
      min-width:0;
    }
    .card strong { display:block; color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; margin-bottom:6px; }
    .kpi-value { font-size:28px; font-weight:700; color:var(--brand-strong); line-height:1.1; }
    .section {
      margin-top:16px;
      background:var(--panel);
      border:1px solid var(--panel-border);
      border-radius:14px;
      box-shadow:0 8px 24px rgba(16,24,40,0.08);
      overflow:hidden;
    }
    .section-header {
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      padding:14px 16px;
      border-bottom:1px solid #edf2f7;
    }
    .section-header h2 { margin:0; font-size:16px; color:var(--brand-strong); }
    .section-header p { margin:4px 0 0; color:var(--muted); font-size:13px; }
    .section-body { padding: 0 16px 14px; }
    table { width:100%; border-collapse:collapse; margin-top:4px; background:transparent; }
    th, td { padding:10px 8px; border-bottom:1px solid #edf2f7; text-align:left }
    th { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; }
    .controls { margin-top:12px; display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
    input, select, button { padding:8px 10px; border-radius:8px; border:1px solid #cfd8e3 }
    button { background:var(--brand); color:#fff; cursor:pointer; border:none }
    a { color:var(--brand); text-decoration:none; font-weight:600; }
    .muted { color:var(--muted); }
    .chart-list { display:flex; flex-direction:column; gap:10px; padding: 8px 0 2px; }
    .chart-row { display:grid; grid-template-columns: minmax(160px, 1.6fr) minmax(0, 3fr) 72px; gap: 12px; align-items:center; }
    .chart-name { font-size: 13px; color: var(--text); font-weight: 600; overflow:hidden; text-overflow: ellipsis; white-space: nowrap; }
    .chart-track { height: 14px; background: #edf2f7; border-radius: 999px; overflow:hidden; }
    .chart-fill { height: 100%; background: linear-gradient(90deg, var(--brand), var(--secondary)); border-radius: 999px; }
    .chart-value { text-align:right; color: var(--brand); font-weight: 700; font-size: 13px; }
    .patient-section { margin-top: 18px; }
    @media (max-width: 1100px) {
      .layout { grid-template-columns: 1fr; }
      .sidebar { position: static; height: auto; border-right: none; border-bottom: 1px solid var(--panel-border); }
      .filters-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .chart-row { grid-template-columns: 1fr; }
      .chart-value { text-align:left; }
    }
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <p class="brand">EGAA</p>
      <p class="brand-subtitle">Painel de regulação e censo</p>
      <nav class="nav">
        <a class="primary" href="/dashboard">Dashboard</a>
        <a href="/pacientes">Pacientes</a>
        <a href="/longa-permanencia">Longa Permanência</a>
        <a href="/configuracoes">Configurações</a>
        <a href="/upload">Importações</a>
        <a href="#resumo">Resumo</a>
      </nav>
      <div class="sidebar-note">
        A pergunta principal desta tela é simples: <strong>como está a ocupação hoje?</strong>
        Use os filtros acima para refinar a leitura.
      </div>
    </aside>
    <main class="main">
      <div class="shell">
        <div class="header">
          <div>
            <h1>Dashboard</h1>
            <p class="subtitle">Visão rápida dos internados, da concentração por unidade e da lista filtrável de pacientes.</p>
          </div>
          <div class="header-actions">
            <a class="pill-link" href="/upload">Ir para Upload</a>
            <a class="pill-link" href="/api/censo/export/xlsx">Exportar Pacientes</a>
            <a class="pill-link" href="/configuracoes">Configurações EGAA</a>
          </div>
        </div>

        <section id="resumo" class="filters">
          <div class="filters-grid">
            <div class="field">
              <label for="prontuario">Prontuário</label>
              <input id="prontuario" placeholder="ex: 123456" />
            </div>
            <div class="field">
              <label for="nome">Nome</label>
              <input id="nome" placeholder="ex: MARIA" />
            </div>
            <div class="field">
              <label for="especialidade">Especialidade</label>
              <input id="especialidade" placeholder="ex: DERMATO" />
            </div>
            <div class="field">
              <label for="unidade">Unidade</label>
              <input id="unidade" placeholder="ex: HFB" />
            </div>
            <div class="field">
              <label for="dataInicio">Data inicial</label>
              <input id="dataInicio" type="date" />
            </div>
            <div class="field">
              <label for="dataFim">Data final</label>
              <input id="dataFim" type="date" />
            </div>
            <div class="field">
              <label for="pageSizeSelect">Itens por página</label>
              <select id="pageSizeSelect">
                <option value="5">5</option>
                <option value="10" selected>10</option>
                <option value="20">20</option>
                <option value="50">50</option>
              </select>
            </div>
          </div>
          <div class="actions" style="margin-top: 12px;">
            <button id="filtrar">Aplicar filtros</button>
            <button id="refresh" class="secondary-btn">Recarregar</button>
          </div>
        </section>

        <div class="cards" id="kpis">
          <div class="card">Carregando...</div>
        </div>

        <section class="section" style="margin-top:16px;">
          <div class="section-header">
            <div>
              <h2>Longa permanência em foco</h2>
              <p id="longaResumo" class="muted">Aguardando dados...</p>
            </div>
            <a class="pill-link" href="/longa-permanencia">Abrir página dedicada</a>
          </div>
          <div class="section-body">
            <div class="chart-list" id="longaChart">
              <div class="muted">Aguardando dados...</div>
            </div>
          </div>
        </section>

        <section class="section">
          <div class="section-header">
            <div>
              <h2>Resultados do EGAA</h2>
              <p id="egaaResumo" class="muted">Aguardando indicadores de atuação.</p>
            </div>
          </div>
          <div class="section-body">
            <div class="cards" id="egaaKpis">
              <div class="card">Aguardando dados...</div>
            </div>
            <div class="grid" style="margin-top:16px;">
              <div class="card">
                <strong>Intervenções por status</strong>
                <div class="chart-list" id="egaaStatusChart">
                  <div class="muted">Aguardando dados...</div>
                </div>
              </div>
              <div class="card">
                <strong>Intervenções por tipo</strong>
                <div class="chart-list" id="egaaTipoChart">
                  <div class="muted">Aguardando dados...</div>
                </div>
              </div>
            </div>
            <div class="card" style="margin-top:16px;">
              <strong>Evolução mensal</strong>
              <div class="chart-list" id="egaaMesChart">
                <div class="muted">Aguardando dados...</div>
              </div>
            </div>
          </div>
        </section>

        <section class="section" id="unidadesSection">
          <div class="section-header">
            <div>
              <h2>Unidades com mais pacientes</h2>
              <p id="unidadesResumo" class="muted">Aguardando dados...</p>
            </div>
          </div>
          <div class="section-body">
            <div class="chart-list" id="unidadesChart">
              <div class="muted">Aguardando dados...</div>
            </div>
          </div>
        </section>

        <section class="patient-section" id="pacientes">
          <div class="section-title">
            <div>
              <h2>Pacientes internados</h2>
              <p>Lista filtrável ordenada por tempo de internação.</p>
            </div>
            <p class="muted" id="pageInfo">Página 1</p>
          </div>

          <div class="section">
            <div class="section-body">
              <table aria-live="polite">
                <thead>
                  <tr><th>Prontuario</th><th>Nome</th><th>Idade</th><th>Dias</th><th>Especialidade</th><th>Unidade</th></tr>
                </thead>
                <tbody id="rows">
                </tbody>
              </table>
              <div style="margin-top:12px; display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
                <button id="prev">Anterior</button>
                <button id="next">Próxima</button>
              </div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>

  <script>
    const API_PREFIX = '/api';
    const kpisEl = document.getElementById('kpis');
    const longaChartEl = document.getElementById('longaChart');
    const longaResumoEl = document.getElementById('longaResumo');
    const egaaResumoEl = document.getElementById('egaaResumo');
    const egaaKpisEl = document.getElementById('egaaKpis');
    const egaaStatusChartEl = document.getElementById('egaaStatusChart');
    const egaaTipoChartEl = document.getElementById('egaaTipoChart');
    const egaaMesChartEl = document.getElementById('egaaMesChart');
    const unidadesChartEl = document.getElementById('unidadesChart');
    const unidadesResumoEl = document.getElementById('unidadesResumo');
    const rowsEl = document.getElementById('rows');
    const prontuarioEl = document.getElementById('prontuario');
    const nomeEl = document.getElementById('nome');
    const especialidadeEl = document.getElementById('especialidade');
    const unidadeEl = document.getElementById('unidade');
    const dataInicioEl = document.getElementById('dataInicio');
    const dataFimEl = document.getElementById('dataFim');
    const filtrarBtn = document.getElementById('filtrar');
    const prevBtn = document.getElementById('prev');
    const nextBtn = document.getElementById('next');
    const pageInfo = document.getElementById('pageInfo');

    let page = 1; let pageSize = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10;

    async function loadKPIs() {
      const params = new URLSearchParams();
      if (dataInicioEl.value) params.set('data_inicio', dataInicioEl.value);
      if (dataFimEl.value) params.set('data_fim', dataFimEl.value);

      const query = params.toString();
      const res = await fetch(`${API_PREFIX}/censo/kpis${query ? `?${query}` : ''}`);
      if (!res.ok) return kpisEl.innerHTML = '<div class="card">Erro ao obter KPIs</div>';
      const data = await res.json();
      const unidades = Array.isArray(data.ocupacao_por_unidade) ? data.ocupacao_por_unidade : [];
      const topUnidades = unidades.slice(0, 5);
      const resto = Math.max(unidades.length - topUnidades.length, 0);
      kpisEl.innerHTML = `
        <div class="card"><span class="badge badge-info">Ao vivo</span><strong>Internados</strong><div class="kpi-value">${data.total_internados}</div></div>
        <div class="card"><span class="badge badge-warning">Atenção</span><strong>>=15 dias</strong><div class="kpi-value">${data.longa_permanencia_15}</div></div>
        <div class="card"><span class="badge badge-error">Crítico</span><strong>>=30 dias</strong><div class="kpi-value">${data.longa_permanencia_30}</div></div>
        <div class="card"><span class="badge badge-error">Crítico+</span><strong>>=40 dias</strong><div class="kpi-value">${data.longa_permanencia_40}</div></div>
        <div class="card"><span class="badge badge-secondary">60+ anos</span><strong>Pacientes</strong><div class="kpi-value">${data.longa_permanencia_60_anos}</div></div>
        <div class="card"><span class="badge badge-secondary">60+ e 15+</span><strong>Pacientes</strong><div class="kpi-value">${data.longa_permanencia_60_15}</div></div>
        <div class="card"><span class="badge badge-secondary">60+ e 30+</span><strong>Pacientes</strong><div class="kpi-value">${data.longa_permanencia_60_30}</div></div>
        <div class="card"><span class="badge badge-success">Ativo</span><strong>Unidades ativas</strong><div class="kpi-value">${unidades.length}</div><div class="muted" style="margin-top:6px">Top ${topUnidades.length}${resto ? ` + ${resto} outras` : ''}</div></div>`;
      unidadesResumoEl.textContent = unidades.length
        ? `Mostrando as ${topUnidades.length} unidades com mais pacientes de um total de ${unidades.length}.`
        : 'Nenhuma unidade retornada pela API.';
      const longaParams = new URLSearchParams();
      longaParams.set('min_dias', '15');
      longaParams.set('page_size', '5');
      if (dataInicioEl.value) longaParams.set('data_inicio', dataInicioEl.value);
      if (dataFimEl.value) longaParams.set('data_fim', dataFimEl.value);
      const longaRes = await fetch(`${API_PREFIX}/censo/pacientes?` + longaParams.toString());
      if (longaRes.ok) {
        const longaData = await longaRes.json();
        const longaItems = Array.isArray(longaData.items) ? longaData.items : [];
        longaResumoEl.textContent = longaItems.length
          ? `Top ${longaItems.length} pacientes com 15+ dias de internação.`
          : 'Nenhum paciente em longa permanência para exibir.';
        longaChartEl.innerHTML = longaItems.length
          ? longaItems.map(item => {
              const dias = Number(item.dias_internacao || 0);
              const width = Math.max(6, Math.min(100, dias * 3));
              return `
                <div class="chart-row">
                  <div class="chart-name" title="${item.nome_paciente || '--'}">${item.nome_paciente || '--'}</div>
                  <div class="chart-track" aria-hidden="true"><div class="chart-fill" style="width:${width}%"></div></div>
                  <div class="chart-value">${dias}d</div>
                </div>`;
            }).join('')
          : '<div class="muted">Nenhum paciente para exibir.</div>';
      } else {
        longaResumoEl.textContent = 'Falha ao carregar longa permanência.';
        longaChartEl.innerHTML = '<div class="muted">Não foi possível carregar a longa permanência.</div>';
      }
      const maxValue = topUnidades.reduce((acc, item) => Math.max(acc, item.total_pacientes || 0), 0) || 1;
      unidadesChartEl.innerHTML = topUnidades.length
        ? topUnidades.map(u => {
            const width = Math.max(6, Math.round(((u.total_pacientes || 0) / maxValue) * 100));
            return `
              <div class="chart-row">
                <div class="chart-name" title="${u.unidade || '--'}">${u.unidade || '--'}</div>
                <div class="chart-track" aria-hidden="true"><div class="chart-fill" style="width:${width}%"></div></div>
                <div class="chart-value">${u.total_pacientes}</div>
              </div>`;
          }).join('')
        : '<div class="muted">Nenhuma unidade para exibir.</div>';
    }

    async function loadEgaaIndicadores() {
      const res = await fetch(`${API_PREFIX}/egaa/indicadores`);
      if (!res.ok) {
        egaaResumoEl.textContent = 'Não foi possível carregar os indicadores do EGAA.';
        egaaKpisEl.innerHTML = '<div class="card">Erro ao obter indicadores</div>';
        egaaStatusChartEl.innerHTML = '<div class="muted">Sem dados.</div>';
        egaaTipoChartEl.innerHTML = '<div class="muted">Sem dados.</div>';
        egaaMesChartEl.innerHTML = '<div class="muted">Sem dados.</div>';
        return;
      }
      const data = await res.json();
      const porStatus = Array.isArray(data.por_status) ? data.por_status : [];
      const porTipo = Array.isArray(data.por_tipo) ? data.por_tipo : [];
      const porMes = Array.isArray(data.por_mes) ? data.por_mes : [];
      egaaResumoEl.textContent = data.total_intervencoes
        ? `${data.total_intervencoes} intervenções registradas em ${data.pacientes_com_intervencao} pacientes distintos.`
        : 'Ainda não há intervenções registradas.';
      egaaKpisEl.innerHTML = `
        <div class="card"><span class="badge badge-info">Total</span><strong>Intervenções</strong><div class="kpi-value">${data.total_intervencoes}</div></div>
        <div class="card"><span class="badge badge-warning">Abertas</span><strong>Pendentes</strong><div class="kpi-value">${data.abertas}</div></div>
        <div class="card"><span class="badge badge-secondary">Em andamento</span><strong>Ativas</strong><div class="kpi-value">${data.em_andamento}</div></div>
        <div class="card"><span class="badge badge-success">Concluídas</span><strong>Fechadas</strong><div class="kpi-value">${data.concluidas}</div></div>
      `;
      const statusMax = porStatus.reduce((acc, item) => Math.max(acc, item.total || 0), 0) || 1;
      egaaStatusChartEl.innerHTML = porStatus.length
        ? porStatus.map(item => {
            const width = Math.max(6, Math.round(((item.total || 0) / statusMax) * 100));
            return `
              <div class="chart-row">
                <div class="chart-name" title="${item.status || '--'}">${item.status || '--'}</div>
                <div class="chart-track" aria-hidden="true"><div class="chart-fill" style="width:${width}%"></div></div>
                <div class="chart-value">${item.total}</div>
              </div>`;
          }).join('')
        : '<div class="muted">Nenhum status para exibir.</div>';
      const tipoMax = porTipo.reduce((acc, item) => Math.max(acc, item.total || 0), 0) || 1;
      egaaTipoChartEl.innerHTML = porTipo.length
        ? porTipo.map(item => {
            const width = Math.max(6, Math.round(((item.total || 0) / tipoMax) * 100));
            return `
              <div class="chart-row">
                <div class="chart-name" title="${item.tipo_intervencao_nome || '--'}">${item.tipo_intervencao_nome || '--'}</div>
                <div class="chart-track" aria-hidden="true"><div class="chart-fill" style="width:${width}%"></div></div>
                <div class="chart-value">${item.total}</div>
              </div>`;
          }).join('')
        : '<div class="muted">Nenhum tipo para exibir.</div>';
      egaaMesChartEl.innerHTML = porMes.length
        ? porMes.map(item => `
            <div class="chart-row">
              <div class="chart-name" title="${item.mes || '--'}">${item.mes || '--'}</div>
              <div class="chart-track" aria-hidden="true"><div class="chart-fill" style="width:${Math.max(6, Math.round(((item.total || 0) / (porMes.reduce((acc, cur) => Math.max(acc, cur.total || 0), 0) || 1)) * 100))}%"></div></div>
              <div class="chart-value">${item.total}</div>
            </div>`).join('')
        : '<div class="muted">Nenhuma evolução mensal para exibir.</div>';
    }

    async function loadPacientes() {
      const params = new URLSearchParams();
      params.set('page', page);
      params.set('page_size', pageSize);
      if (prontuarioEl.value) params.set('prontuario', prontuarioEl.value);
      if (nomeEl.value) params.set('nome', nomeEl.value);
      if (especialidadeEl.value) params.set('especialidade', especialidadeEl.value);
      if (unidadeEl.value) params.set('unidade', unidadeEl.value);
      if (dataInicioEl.value) params.set('data_inicio', dataInicioEl.value);
      if (dataFimEl.value) params.set('data_fim', dataFimEl.value);

      const res = await fetch(`${API_PREFIX}/censo/pacientes?` + params.toString());
      if (!res.ok) return rowsEl.innerHTML = `<tr><td colspan="6">Erro ao obter pacientes (${res.status})</td></tr>`;
      const data = await res.json();
      rowsEl.innerHTML = data.items.map(it => `<tr><td>${it.prontuario}</td><td>${it.nome_paciente||''}</td><td>${it.idade_anos??''}</td><td>${it.dias_internacao??''}</td><td>${it.especialidade}</td><td>${it.unidade||''}</td></tr>`).join('');
      pageInfo.textContent = `Página ${data.page} de ${Math.ceil(data.total / data.page_size) || 1}`;
      prevBtn.disabled = data.page <= 1; nextBtn.disabled = data.page * data.page_size >= data.total;
    }

    filtrarBtn.addEventListener('click', () => { page = 1; pageSize = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10; loadPacientes(); loadKPIs(); });
    prevBtn.addEventListener('click', () => { if (page>1) page--; loadPacientes(); });
    nextBtn.addEventListener('click', () => { page++; loadPacientes(); });
    document.getElementById('pageSizeSelect').addEventListener('change', () => { page = 1; pageSize = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10; loadPacientes(); });
    dataInicioEl.addEventListener('change', () => { page = 1; loadPacientes(); loadKPIs(); });
    dataFimEl.addEventListener('change', () => { page = 1; loadPacientes(); loadKPIs(); });
    document.getElementById('refresh').addEventListener('click', () => { loadKPIs(); loadPacientes(); });

    loadKPIs(); loadPacientes(); loadEgaaIndicadores();
  </script>
</body>
</html>
"""

@router.get("/", include_in_schema=False)
def root_redirect() -> RedirectResponse:
    return RedirectResponse(url="/dashboard", status_code=307)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_route() -> str:
    return dashboard_page()


def _patients_page(title: str, subtitle: str, *, default_min_dias: int | None = None) -> str:
    default_min_dias_value = "" if default_min_dias is None else str(default_min_dias)
    egaa_column_header_html = "<th>EGAA</th>" if default_min_dias is not None else ""
    egaa_column_cell_html = """
              <td>
                <div class="badges">
                  <span class="badge badge-secondary">${{egaaBadgeLabel}}</span>
                </div>
                <div class="muted" style="margin-top:6px">${{egaaBadgeDetail}}</div>
              </td>""" if default_min_dias is not None else ""
    priority_field_html = """
            <div class="field">
              <label for="prioridade">Prioridade</label>
              <select id="prioridade">
                <option value="">Sem atalho</option>
                <option value="15">15+ dias</option>
                <option value="30">30+ dias</option>
                <option value="60">60+ anos</option>
                <option value="30-60">30+ dias e 60+ anos</option>
              </select>
            </div>
""" if default_min_dias is not None else ""
    badge_text = "Longa permanência" if default_min_dias is not None else "Lista geral"
    badge_class = "badge-warning" if default_min_dias is not None else "badge-info"
    nav_items = [
        ("Dashboard", "/dashboard", title == "Dashboard"),
        ("Pacientes", "/pacientes", title == "Pacientes"),
        ("Longa Permanência", "/longa-permanencia", title == "Longa Permanência"),
        ("Configurações", "/configuracoes", title == "Configurações"),
        ("Importações", "/upload", False),
    ]
    nav_html = "".join(
        '<a href="{0}"{1}>{2}</a>'.format(href, " class='primary'" if active else "", label)
        for label, href, active in nav_items
    )
    return f"""
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>EGAA - {title}</title>
  <style>
    :root {{
      --bg: #F7F9FB;
      --panel: #FFFFFF;
      --panel-border: #DCE3EA;
      --text: #1F2937;
      --muted: #6B7280;
      --brand: #005C99;
      --brand-strong: #004A7A;
      --secondary: #00A79D;
      --warning: #F9A825;
    }}
    body {{
      font-family: Inter, Arial, sans-serif;
      background: linear-gradient(180deg, #ffffff 0%, var(--bg) 100%);
      margin: 0;
      min-height: 100vh;
      color: var(--text);
    }}
    .layout {{ display:grid; grid-template-columns: 260px 1fr; min-height: 100vh; }}
    .sidebar {{
      background: rgba(255,255,255,0.84);
      backdrop-filter: blur(10px);
      border-right: 1px solid var(--panel-border);
      padding: 24px 18px;
      position: sticky;
      top: 0;
      height: 100vh;
      box-sizing: border-box;
    }}
    .brand {{ font-size: 18px; font-weight: 700; color: var(--brand-strong); margin: 0; }}
    .brand-subtitle {{ margin: 6px 0 18px; color: var(--muted); font-size: 13px; }}
    .nav {{ display:flex; flex-direction:column; gap:8px; margin-top: 18px; }}
    .nav a {{
      color: var(--text);
      text-decoration: none;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid transparent;
      font-weight: 600;
    }}
    .nav a:hover {{ background: rgba(0, 92, 153, 0.06); border-color: var(--panel-border); }}
    .nav a.primary {{ background: var(--brand); color: #fff; }}
    .nav a.primary:hover {{ background: var(--brand-strong); border-color: transparent; }}
    .sidebar-note {{
      margin-top: 18px;
      padding: 12px;
      border-radius: 12px;
      background: #F0F7FC;
      border: 1px solid #D7E7F3;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }}
    .main {{ padding: 24px; }}
    .shell {{ max-width: 1200px; margin: 0 auto; }}
    .header {{ display:flex; align-items:center; justify-content:space-between; gap: 16px; margin-bottom: 16px; }}
    h1 {{ color:var(--brand-strong); margin:0; letter-spacing:-0.02em; }}
    .subtitle {{ margin: 8px 0 0; color: var(--muted); }}
    .pill-link {{
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:10px 12px;
      border-radius: 999px;
      background: var(--panel);
      border: 1px solid var(--panel-border);
      color: var(--brand);
      text-decoration: none;
      font-weight: 600;
    }}
    .badge {{
      display:inline-flex;
      align-items:center;
      gap:6px;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .02em;
      margin-bottom: 10px;
    }}
    .badge-info {{ background: rgba(2, 136, 209, 0.12); color: #0288D1; }}
    .badge-warning {{ background: rgba(249, 168, 37, 0.16); color: #8A6500; }}
    .filters {{
      margin-top: 14px;
      padding: 16px;
      background: rgba(255,255,255,0.9);
      border: 1px solid var(--panel-border);
      border-radius: 16px;
      box-shadow: 0 8px 24px rgba(16,24,40,0.06);
    }}
    .filters-grid {{
      display:grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 10px;
      align-items:end;
    }}
    .field {{ display:flex; flex-direction:column; gap:6px; min-width: 0; }}
    .field label {{ font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); font-weight: 700; }}
    .field input, .field select {{
      width: 100%;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid #cfd8e3;
      box-sizing: border-box;
      background: #fff;
    }}
    .actions {{ display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end; margin-top: 12px; }}
    button {{
      padding: 10px 12px;
      border-radius: 8px;
      border: none;
      background: var(--brand);
      color: #fff;
      cursor: pointer;
      font-weight: 600;
    }}
    button.secondary {{
      background: #EEF5FA;
      color: var(--brand);
      border: 1px solid var(--panel-border);
    }}
    .cards {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap:12px; margin-top:16px; }}
    .card {{
      background:var(--panel);
      padding:14px 16px;
      border-radius:14px;
      box-shadow:0 8px 24px rgba(16,24,40,0.08);
      border:1px solid var(--panel-border);
      min-width:0;
    }}
    .card strong {{ display:block; color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; margin-bottom:6px; }}
    .kpi-value {{ font-size:28px; font-weight:700; color:var(--brand-strong); line-height:1.1; }}
    .section {{
      margin-top:16px;
      background:var(--panel);
      border:1px solid var(--panel-border);
      border-radius:14px;
      box-shadow:0 8px 24px rgba(16,24,40,0.08);
      overflow:hidden;
    }}
    .section-header {{
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      padding:14px 16px;
      border-bottom:1px solid #edf2f7;
    }}
    .section-header h2 {{ margin:0; font-size:16px; color:var(--brand-strong); }}
    .section-header p {{ margin:4px 0 0; color:var(--muted); font-size:13px; }}
    .section-body {{ padding: 0 16px 14px; }}
    table {{ width:100%; border-collapse:collapse; margin-top:4px; background:transparent; }}
    th, td {{ padding:10px 8px; border-bottom:1px solid #edf2f7; text-align:left }}
    th {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; }}
    .row-critical {{ background: rgba(198, 40, 40, 0.05); }}
    .row-warning {{ background: rgba(249, 168, 37, 0.08); }}
    .row-info {{ background: rgba(2, 136, 209, 0.05); }}
    .badges {{ display:flex; flex-wrap:wrap; gap:6px; }}
    .muted {{ color:var(--muted); }}
    .pagination {{ margin-top:12px; display:flex; gap:8px; align-items:center; flex-wrap:wrap; }}
    .empty {{ padding: 16px 0; color: var(--muted); }}
    @media (max-width: 1100px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{ position: static; height: auto; border-right: none; border-bottom: 1px solid var(--panel-border); }}
      .filters-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <p class="brand">EGAA</p>
      <p class="brand-subtitle">Painel de regulação e censo</p>
      <nav class="nav">
        {nav_html}
      </nav>
      <div class="sidebar-note">
        {subtitle}
      </div>
    </aside>
    <main class="main">
      <div class="shell">
        <div class="header">
          <div>
            <h1>{title}</h1>
            <p class="subtitle">{subtitle}</p>
          </div>
          <a class="pill-link" href="/dashboard">Voltar ao dashboard</a>
          <a class="pill-link" href="/api/censo/export/xlsx?min_dias=15">Exportar Longa Permanência</a>
        </div>

        <section class="filters">
          <div class="filters-grid">
            <div class="field">
              <label for="prontuario">Prontuário</label>
              <input id="prontuario" placeholder="ex: 123456" />
            </div>
            <div class="field">
              <label for="nome">Nome</label>
              <input id="nome" placeholder="ex: MARIA" />
            </div>
            <div class="field">
              <label for="especialidade">Especialidade</label>
              <input id="especialidade" placeholder="ex: DERMATO" />
            </div>
            <div class="field">
              <label for="unidade">Unidade</label>
              <input id="unidade" placeholder="ex: HFB" />
            </div>
            <div class="field">
              <label for="dataInicio">Data inicial</label>
              <input id="dataInicio" type="date" />
            </div>
            <div class="field">
              <label for="dataFim">Data final</label>
              <input id="dataFim" type="date" />
            </div>
            <div class="field">
              <label for="minDias">Dias mínimos</label>
              <input id="minDias" type="number" min="0" step="1" value="{default_min_dias_value}" placeholder="opcional" />
            </div>
            {priority_field_html}
            <div class="field">
              <label for="pageSizeSelect">Itens por página</label>
              <select id="pageSizeSelect">
                <option value="5">5</option>
                <option value="10" selected>10</option>
                <option value="20">20</option>
                <option value="50">50</option>
              </select>
            </div>
          </div>
          <div class="actions">
            <button id="filtrar">Aplicar filtros</button>
            <button id="refresh" class="secondary">Recarregar</button>
          </div>
        </section>

        <div class="cards" id="kpis">
          <div class="card"><span class="badge {badge_class}">{badge_text}</span><strong>Registros listados</strong><div class="kpi-value">Carregando...</div></div>
        </div>

        <section class="section">
          <div class="section-header">
            <div>
              <h2>Registros</h2>
              <p id="pageInfo" class="muted">Página 1</p>
            </div>
          </div>
          <div class="section-body">
            <table aria-live="polite">
              <thead>
                <tr><th>Prontuario</th><th>Nome</th><th>Idade</th><th>Dias</th><th>Especialidade</th><th>Unidade</th>{egaa_column_header_html}</tr>
              </thead>
              <tbody id="rows">
                <tr><td colspan="{7 if default_min_dias is not None else 6}" class="empty">Aguardando dados...</td></tr>
              </tbody>
            </table>
            <div class="pagination">
              <button id="prev">Anterior</button>
              <button id="next">Próxima</button>
            </div>
          </div>
        </section>

        <section class="section">
          <div class="section-header">
            <div>
              <h2>Histórico EGAA por prontuário</h2>
              <p>Consulta rápida para ver as atuações registradas no paciente.</p>
            </div>
          </div>
          <div class="section-body">
            <div class="filters-grid" style="grid-template-columns: 1.2fr 1fr auto;">
              <div class="field" style="margin-bottom:0;">
                <label for="histProntuario">Prontuário</label>
                <input id="histProntuario" placeholder="Digite um prontuário" />
              </div>
              <div class="field" style="margin-bottom:0;">
                <label for="histTipo">Tipo</label>
                <select id="histTipo">
                  <option value="">Todos</option>
                </select>
              </div>
              <div class="field" style="margin-bottom:0; align-self:end;">
                <button id="histBuscar" type="button">Buscar histórico</button>
              </div>
            </div>
            <p id="histResumo" class="muted" style="margin: 12px 0 0;">Informe um prontuário para consultar as atuações do EGAA.</p>
            <div class="chart-list" id="histRows" style="margin-top: 12px;">
              <div class="muted">Nenhuma consulta realizada.</div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>
  <script>
    const API_PREFIX = '/api';
    const isLongaPermanencia = {str(default_min_dias is not None).lower()};
    const diasMinimos = {('null' if default_min_dias is None else default_min_dias)};
    const kpisEl = document.getElementById('kpis');
    const rowsEl = document.getElementById('rows');
    const prontuarioEl = document.getElementById('prontuario');
    const nomeEl = document.getElementById('nome');
    const especialidadeEl = document.getElementById('especialidade');
    const unidadeEl = document.getElementById('unidade');
    const dataInicioEl = document.getElementById('dataInicio');
    const dataFimEl = document.getElementById('dataFim');
    const minDiasEl = document.getElementById('minDias');
    const prioridadeEl = document.getElementById('prioridade');
    const filtrarBtn = document.getElementById('filtrar');
    const prevBtn = document.getElementById('prev');
    const nextBtn = document.getElementById('next');
    const pageInfo = document.getElementById('pageInfo');
    const histProntuarioEl = document.getElementById('histProntuario');
    const histTipoEl = document.getElementById('histTipo');
    const histBuscarBtn = document.getElementById('histBuscar');
    const histRowsEl = document.getElementById('histRows');
    const histResumoEl = document.getElementById('histResumo');
    let page = 1;
    let pageSize = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10;
    let histTiposMap = {{}};

    function priorityMeta(item) {{
      const dias = Number(item.dias_internacao || 0);
      const idade = Number(item.idade_anos || 0);
      if (dias >= 30 && idade >= 60) return {{ label: 'Prioridade máxima', css: 'row-critical' }};
      if (dias >= 30) return {{ label: 'Longa permanência', css: 'row-warning' }};
      if (idade >= 60) return {{ label: '60+ anos', css: 'row-info' }};
      return {{ label: 'Acompanhamento', css: '' }};
    }}

    async function loadPacientes() {{
      const params = new URLSearchParams();
      params.set('page', page);
      params.set('page_size', pageSize);
      if (prontuarioEl.value) params.set('prontuario', prontuarioEl.value);
      if (nomeEl.value) params.set('nome', nomeEl.value);
      if (especialidadeEl.value) params.set('especialidade', especialidadeEl.value);
      if (unidadeEl.value) params.set('unidade', unidadeEl.value);
      if (dataInicioEl.value) params.set('data_inicio', dataInicioEl.value);
      if (dataFimEl.value) params.set('data_fim', dataFimEl.value);
      if (minDiasEl.value) params.set('min_dias', minDiasEl.value);
      if (prioridadeEl && prioridadeEl.value === '15') params.set('min_dias', '15');
      if (prioridadeEl && prioridadeEl.value === '30') params.set('min_dias', '30');
      if (prioridadeEl && prioridadeEl.value === '60') {{
        params.delete('min_dias');
        params.set('idade_minima', '60');
      }}
      if (prioridadeEl && prioridadeEl.value === '30-60') {{
        params.set('min_dias', '30');
        params.set('idade_minima', '60');
      }}

      const res = await fetch(`${{API_PREFIX}}/censo/pacientes?` + params.toString());
      if (!res.ok) {{
        rowsEl.innerHTML = `<tr><td colspan="6">Erro ao obter registros (${{res.status}})</td></tr>`;
        return;
      }}
      const data = await res.json();
      const items = Array.isArray(data.items) ? data.items : [];
      const diasMaximos = items.reduce((max, item) => Math.max(max, Number(item.dias_internacao || 0)), 0);
      const mediaDias = items.length
        ? Math.round(items.reduce((sum, item) => sum + Number(item.dias_internacao || 0), 0) / items.length)
        : 0;
      const unidadeLider = items.reduce((acc, item) => {{
        const unidade = item.unidade || '--';
        acc[unidade] = (acc[unidade] || 0) + 1;
        return acc;
      }}, {{}});
      const unidadeLiderNome = Object.entries(unidadeLider).sort((a, b) => b[1] - a[1])[0]?.[0] || '--';
      const unidadeLiderTotal = Object.entries(unidadeLider).sort((a, b) => b[1] - a[1])[0]?.[1] || 0;
      const egaaAtivos = items.filter(item => Number(item.egaa_total_atuacoes || 0) > 0).length;
      const egaaAtuacoesTotal = items.reduce((acc, item) => acc + Number(item.egaa_total_atuacoes || 0), 0);
      const egaaUltimaAtuacao = items.reduce((acc, item) => {{
        const atual = item.egaa_ultima_atuacao || '';
        return atual && (!acc || String(atual) > String(acc)) ? atual : acc;
      }}, '');
      kpisEl.innerHTML = `
        <div class="card"><span class="badge {badge_class}">{badge_text}</span><strong>Total encontrado</strong><div class="kpi-value">${{data.total}}</div></div>
        <div class="card"><span class="badge badge-info">Página atual</span><strong>Paginação</strong><div class="kpi-value">${{data.page}}</div></div>
        <div class="card"><span class="badge badge-secondary">Lote visual</span><strong>Itens por página</strong><div class="kpi-value">${{data.page_size}}</div></div>
        ${{isLongaPermanencia ? `<div class="card"><span class="badge badge-warning">Longa permanência</span><strong>Dias mínimos</strong><div class="kpi-value">${{diasMinimos}}</div></div>` : ''}}
        ${{isLongaPermanencia ? `<div class="card"><span class="badge badge-warning">Acompanhamento</span><strong>Média na página</strong><div class="kpi-value">${{mediaDias}}d</div></div>` : ''}}
        ${{isLongaPermanencia ? `<div class="card"><span class="badge badge-warning">Maior permanência</span><strong>Maior valor</strong><div class="kpi-value">${{diasMaximos}}d</div><div class="muted" style="margin-top:6px">${{unidadeLiderNome}} (${{unidadeLiderTotal}} registros)</div></div>` : ''}}
        ${{isLongaPermanencia ? `<div class="card"><span class="badge badge-secondary">EGAA</span><strong>Pacientes com atuações</strong><div class="kpi-value">${{egaaAtivos}}</div><div class="muted" style="margin-top:6px">${{egaaAtuacoesTotal}} atuações no recorte</div></div>` : ''}}
        ${{isLongaPermanencia ? `<div class="card"><span class="badge badge-secondary">EGAA</span><strong>Última atuação</strong><div class="kpi-value" style="font-size:18px; line-height:1.3">${{egaaUltimaAtuacao ? new Intl.DateTimeFormat('pt-BR').format(new Date(egaaUltimaAtuacao)) : '--'}}</div></div>` : ''}}
      `;
      rowsEl.innerHTML = items.length
        ? items.map(it => {{
            const meta = priorityMeta(it);
            const egaaTotal = Number(it.egaa_total_atuacoes || 0);
            const egaaBadgeLabel = egaaTotal > 0 ? `${{egaaTotal}} atuação(ões)` : 'Sem EGAA';
            const egaaBadgeDetail = egaaTotal > 0
              ? `Última: ${{it.egaa_ultima_atuacao ? new Intl.DateTimeFormat('pt-BR').format(new Date(it.egaa_ultima_atuacao)) : '--'}}`
              : 'Ainda sem registros do EGAA';
            return `<tr class="${{meta.css}}">
              <td><div class="badges"><span class="badge badge-info">${{meta.label}}</span></div><div style="margin-top:6px"><a href="/paciente/${{encodeURIComponent(it.prontuario)}}">${{it.prontuario}}</a></div></td>
              <td>${{it.nome_paciente||''}}</td>
              <td>${{it.idade_anos??''}}</td>
              <td>${{it.dias_internacao??''}}</td>
              <td>${{it.especialidade}}</td>
              <td>${{it.unidade||''}}</td>
              ${{isLongaPermanencia ? `
              <td>
                <div class="badges">
                  <span class="badge badge-secondary">${{egaaBadgeLabel}}</span>
                </div>
                <div class="muted" style="margin-top:6px">${{egaaBadgeDetail}}</div>
              </td>` : ''}}
            </tr>`;
          }}).join('')
        : '<tr><td colspan="' + (isLongaPermanencia ? '7' : '6') + '" class="empty">Nenhum registro encontrado com os filtros atuais.</td></tr>';
      pageInfo.textContent = `Página ${{data.page}} de ${{Math.ceil(data.total / data.page_size) || 1}}`;
      prevBtn.disabled = data.page <= 1;
      nextBtn.disabled = data.page * data.page_size >= data.total;
    }}

    async function loadHistoricoEGAA() {{
      const prontuario = histProntuarioEl.value.trim();
      if (!prontuario) {{
        histResumoEl.textContent = 'Informe um prontuário para consultar as atuações do EGAA.';
        histRowsEl.innerHTML = '<div class="muted">Nenhuma consulta realizada.</div>';
        return;
      }}
      const params = new URLSearchParams();
      params.set('prontuario', prontuario);
      if (histTipoEl.value) params.set('tipo_intervencao_id', histTipoEl.value);
      const res = await fetch(`${{API_PREFIX}}/egaa/intervencoes?` + params.toString());
      if (!res.ok) {{
        histResumoEl.textContent = 'Não foi possível carregar o histórico.';
        histRowsEl.innerHTML = '<div class="muted">Erro ao consultar intervenções.</div>';
        return;
      }}
      const data = await res.json();
      const items = Array.isArray(data) ? data : [];
      histResumoEl.textContent = items.length
        ? `Foram encontradas ${{items.length}} atuações para o prontuário ${{prontuario}}.`
        : `Nenhuma atuação do EGAA encontrada para o prontuário ${{prontuario}}.`;
      histRowsEl.innerHTML = items.length
        ? items.slice(0, 8).map(item => `
              <div class="card" style="padding:12px 14px;">
              <strong style="display:block; color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em;">${{item.status || 'sem status'}}</strong>
              <div style="font-weight:700; color:var(--brand-strong);">${{item.titulo || '--'}}</div>
              <div class="muted" style="margin-top:4px;">Tipo: ${{histTiposMap[item.tipo_intervencao_id] || item.tipo_intervencao_id || '--'}} · Responsável: ${{item.usuario_responsavel || '--'}}</div>
              <div class="muted" style="margin-top:4px;">Atuação em ${{fmtDate(item.data_atuacao)}} · Atualizado em ${{fmtDate(item.updated_at || item.created_at)}}</div>
            </div>`).join('')
        : '<div class="muted">Nenhuma intervenção registrada para este prontuário.</div>';
    }}

    filtrarBtn.addEventListener('click', () => {{ page = 1; pageSize = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10; loadPacientes(); }});
    prevBtn.addEventListener('click', () => {{ if (page > 1) page--; loadPacientes(); }});
    nextBtn.addEventListener('click', () => {{ page++; loadPacientes(); }});
    document.getElementById('pageSizeSelect').addEventListener('change', () => {{ page = 1; pageSize = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10; loadPacientes(); }});
    dataInicioEl.addEventListener('change', () => {{ page = 1; loadPacientes(); }});
    dataFimEl.addEventListener('change', () => {{ page = 1; loadPacientes(); }});
    minDiasEl.addEventListener('change', () => {{ page = 1; loadPacientes(); }});
    if (prioridadeEl) prioridadeEl.addEventListener('change', () => {{ page = 1; loadPacientes(); }});
    document.getElementById('refresh').addEventListener('click', () => {{ loadPacientes(); }});
    histBuscarBtn.addEventListener('click', () => loadHistoricoEGAA());
    histProntuarioEl.addEventListener('keydown', (event) => {{ if (event.key === 'Enter') loadHistoricoEGAA(); }});

    loadPacientes();
    if (histTipoEl) {{
      fetch(`${{API_PREFIX}}/egaa/tipos-intervencao`)
        .then(res => res.ok ? res.json() : [])
        .then(items => {{
          const list = Array.isArray(items) ? items : [];
          histTiposMap = list.reduce((acc, item) => {{
            acc[item.id] = item.nome || item.id;
            return acc;
          }}, {{}});
          histTipoEl.innerHTML = ['<option value="">Todos</option>'].concat(list.map(item => `<option value="${{item.id}}">${{item.nome || '--'}}</option>`)).join('');
        }})
        .catch(() => {{}});
    }}
  </script>
</body>
</html>
"""


@router.get("/pacientes", response_class=HTMLResponse)
def pacientes_route() -> str:
    return _patients_page(
        "Pacientes",
        "Visão filtrável de todos os pacientes internados em acompanhamento.",
    )


@router.get("/longa-permanencia", response_class=HTMLResponse)
def longa_permanencia_route() -> str:
    return _patients_page(
        "Longa Permanência",
        "Pacientes com 15+ dias de internação para acompanhamento prioritário.",
        default_min_dias=15,
    )


@router.get("/paciente/{prontuario}", response_class=HTMLResponse)
def paciente_detail_route(prontuario: str) -> str:
    return f"""
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>EGAA - Paciente {prontuario}</title>
  <style>
    :root {{
      --bg: #F7F9FB;
      --panel: #FFFFFF;
      --panel-border: #DCE3EA;
      --text: #1F2937;
      --muted: #6B7280;
      --brand: #005C99;
      --brand-strong: #004A7A;
      --secondary: #00A79D;
      --success: #2E7D32;
      --warning: #F9A825;
      --error: #C62828;
      --info: #0288D1;
    }}
    body {{
      font-family: Inter, Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(0, 92, 153, 0.08), transparent 28%),
        linear-gradient(180deg, #ffffff 0%, var(--bg) 100%);
      margin: 0;
      min-height: 100vh;
      color: var(--text);
    }}
    .layout {{ display:grid; grid-template-columns: 260px 1fr; min-height: 100vh; }}
    .sidebar {{
      background: rgba(255,255,255,0.84);
      backdrop-filter: blur(10px);
      border-right: 1px solid var(--panel-border);
      padding: 24px 18px;
      position: sticky;
      top: 0;
      height: 100vh;
      box-sizing: border-box;
    }}
    .brand {{ font-size: 18px; font-weight: 700; color: var(--brand-strong); margin: 0; }}
    .brand-subtitle {{ margin: 6px 0 18px; color: var(--muted); font-size: 13px; }}
    .nav {{ display:flex; flex-direction:column; gap:8px; margin-top: 18px; }}
    .nav a {{
      color: var(--text);
      text-decoration: none;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid transparent;
      font-weight: 600;
    }}
    .nav a.primary {{ background: var(--brand); color: #fff; }}
    .main {{ padding: 24px; }}
    .shell {{ max-width: 1240px; margin: 0 auto; }}
    .header {{ display:flex; align-items:center; justify-content:space-between; gap: 16px; margin-bottom: 16px; }}
    h1 {{ color:var(--brand-strong); margin:0; }}
    .subtitle {{ margin: 8px 0 0; color: var(--muted); }}
    .pill-link {{
      display:inline-flex; align-items:center; gap:8px; padding:10px 12px;
      border-radius: 999px; background: var(--panel); border: 1px solid var(--panel-border);
      color: var(--brand); text-decoration: none; font-weight: 600;
    }}
    .cards {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap:12px; margin-top:16px; }}
    .card {{
      background:var(--panel); padding:14px 16px; border-radius:14px; box-shadow:0 8px 24px rgba(16,24,40,0.08);
      border:1px solid var(--panel-border); min-width:0;
    }}
    .card strong {{ display:block; color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; margin-bottom:6px; }}
    .kpi-value {{ font-size:28px; font-weight:700; color:var(--brand-strong); line-height:1.1; }}
    .grid {{ display:grid; grid-template-columns: 1.15fr 1fr; gap: 16px; margin-top: 16px; }}
    .section {{
      background:var(--panel); border:1px solid var(--panel-border); border-radius:14px;
      box-shadow:0 8px 24px rgba(16,24,40,0.08); overflow:hidden;
    }}
    .section-header {{
      display:flex; align-items:center; justify-content:space-between; gap:12px;
      padding:14px 16px; border-bottom:1px solid #edf2f7;
    }}
    .section-header h2 {{ margin:0; font-size:16px; color:var(--brand-strong); }}
    .section-header p {{ margin:4px 0 0; color:var(--muted); font-size:13px; }}
    .section-body {{ padding: 16px; }}
    .muted {{ color: var(--muted); }}
    .field {{ display:flex; flex-direction:column; gap:6px; margin-bottom: 12px; }}
    .field label {{ font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); font-weight: 700; }}
    .field input, .field select, .field textarea {{
      width:100%; padding:10px 12px; border-radius:10px; border:1px solid #cfd8e3; box-sizing:border-box; background:#fff; font:inherit;
    }}
    .field textarea {{ min-height: 92px; resize: vertical; }}
    .row {{ display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }}
    .actions {{ display:flex; gap:8px; flex-wrap:wrap; margin-top: 12px; }}
    .drafts {{ display:flex; flex-direction:column; gap:12px; margin-bottom: 12px; }}
    .draft-card {{
      border: 1px solid var(--panel-border);
      border-radius: 14px;
      background: linear-gradient(180deg, #ffffff 0%, #fafdff 100%);
      padding: 14px;
      box-shadow: 0 4px 16px rgba(16,24,40,0.04);
    }}
    .draft-card-header {{ display:flex; align-items:center; justify-content:space-between; gap: 12px; margin-bottom: 12px; }}
    .draft-card-header strong {{ color: var(--brand-strong); }}
    .draft-card-header small {{ color: var(--muted); display:block; margin-top: 2px; }}
    .draft-grid {{ display:grid; grid-template-columns: 1.1fr 1.1fr; gap: 12px; }}
    .draft-actions {{ display:flex; gap:8px; flex-wrap:wrap; margin-top: 12px; }}
    .draft-remove {{ background: #FDECEC; color: var(--error); border: 1px solid rgba(198, 40, 40, 0.16); }}
    .draft-empty {{
      border: 1px dashed var(--panel-border);
      border-radius: 12px;
      padding: 16px;
      color: var(--muted);
      background: #FBFDFF;
    }}
    button {{
      padding:10px 12px; border-radius:8px; border:none; background:var(--brand); color:#fff; cursor:pointer; font-weight:600;
    }}
    button.secondary {{ background:#EEF5FA; color:var(--brand); border:1px solid var(--panel-border); }}
    .timeline {{ display:flex; flex-direction:column; gap:12px; }}
    .timeline-item {{
      padding:12px 14px; border:1px solid var(--panel-border); border-radius:12px; background:#fff;
    }}
    .badge {{
      display:inline-flex; align-items:center; gap:6px; padding: 5px 10px; border-radius: 999px;
      font-size: 12px; font-weight: 700; letter-spacing: .02em; margin-bottom: 10px;
    }}
    .badge-info {{ background: rgba(2, 136, 209, 0.12); color: var(--info); }}
    .badge-warning {{ background: rgba(249, 168, 37, 0.16); color: #8A6500; }}
    .badge-secondary {{ background: rgba(0, 167, 157, 0.12); color: var(--secondary); }}
    .badge-success {{ background: rgba(46, 125, 50, 0.12); color: var(--success); }}
    .badge-error {{ background: rgba(198, 40, 40, 0.12); color: var(--error); }}
    .timeline-title {{ font-weight: 700; color: var(--brand-strong); }}
    .timeline-meta {{ margin-top: 4px; color: var(--muted); font-size: 13px; }}
    @media (max-width: 1100px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{ position: static; height: auto; border-right: none; border-bottom: 1px solid var(--panel-border); }}
      .grid {{ grid-template-columns: 1fr; }}
      .row {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <p class="brand">EGAA</p>
      <p class="brand-subtitle">Detalhe do paciente</p>
      <nav class="nav">
        <a href="/dashboard">Dashboard</a>
        <a class="primary" href="/pacientes">Voltar para Pacientes</a>
        <a href="/longa-permanencia">Longa Permanência</a>
        <a href="/configuracoes">Configurações</a>
      </nav>
    </aside>
    <main class="main">
      <div class="shell">
        <div class="header">
          <div>
            <h1 id="titulo">Paciente {prontuario}</h1>
            <p class="subtitle" id="subtitulo">Carregando informações do paciente...</p>
          </div>
          <div class="actions">
            <a class="pill-link" href="/pacientes">Voltar</a>
            <a class="pill-link" id="linkLonga" href="/longa-permanencia">Longa permanência</a>
          </div>
        </div>

        <div class="cards" id="kpis">
          <div class="card"><strong>Prontuário</strong><div class="kpi-value">--</div></div>
          <div class="card"><strong>Dias</strong><div class="kpi-value">--</div></div>
          <div class="card"><strong>Idade</strong><div class="kpi-value">--</div></div>
          <div class="card"><strong>Unidade</strong><div class="kpi-value">--</div></div>
        </div>

        <div class="grid">
          <section class="section">
            <div class="section-header">
              <div>
                <h2>Resumo clínico</h2>
                <p>Dados ativos do paciente internado.</p>
              </div>
            </div>
            <div class="section-body">
              <div id="resumo" class="muted">Aguardando dados...</div>
            </div>
          </section>

          <section class="section">
            <div class="section-header">
              <div>
                <h2>Nova atuação EGAA</h2>
                <p>Adicione várias atuações para o mesmo paciente antes de salvar.</p>
              </div>
            </div>
            <div class="section-body">
              <form id="intervencaoForm">
                <div class="actions" style="margin-top:0">
                  <button type="button" class="secondary" id="adicionarAtuacao">Adicionar atuação</button>
                  <button type="button" class="secondary" id="limparAtuacoes">Limpar tudo</button>
                </div>
                <p class="muted" style="margin:10px 0 12px;">Cada cartão representa uma atuação do EGAA. Você pode registrar quantas forem necessárias para este prontuário.</p>
                <div class="drafts" id="drafts"></div>
                <div class="actions">
                  <button type="submit">Salvar todas as atuações</button>
                  <button type="button" class="secondary" id="recarregar">Recarregar</button>
                </div>
              </form>
            </div>
          </section>

          <section class="section" style="grid-column: 1 / -1;">
            <div class="section-header">
              <div>
                <h2>Linha do tempo EGAA</h2>
                <p>Intervenções registradas para este prontuário.</p>
              </div>
            </div>
            <div class="section-body">
              <div class="timeline" id="timeline">
                <div class="muted">Carregando histórico...</div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>

  <script>
    const API_PREFIX = '/api';
    const PRONTUARIO = {prontuario!r};
    const resumoEl = document.getElementById('resumo');
    const kpisEl = document.getElementById('kpis');
    const timelineEl = document.getElementById('timeline');
    const subtituloEl = document.getElementById('subtitulo');
    const draftsEl = document.getElementById('drafts');
    const form = document.getElementById('intervencaoForm');
    const adicionarAtuacaoBtn = document.getElementById('adicionarAtuacao');
    const limparAtuacoesBtn = document.getElementById('limparAtuacoes');
    let tiposOptions = [];
    let tiposById = {{}};
    let draftSeq = 0;
    let drafts = [];

    function escapeHtml(value) {{
      return String(value ?? '').replace(/[&<>"']/g, (character) => ({{
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
      }}[character] || character));
    }}

    function renderTipoOptions(selectedValue) {{
      const selected = selectedValue ? String(selectedValue) : '';
      const options = ['<option value="">Selecione...</option>'].concat(
        tiposOptions.map(item => `<option value="${{item.id}}" ${{String(item.id) === selected ? 'selected' : ''}}>${{escapeHtml(item.nome || '--')}}</option>`)
      );
      return options.join('');
    }}

    function createDraft() {{
      draftSeq += 1;
      return {{
        id: `${{Date.now()}}-${{draftSeq}}`,
        tipo_intervencao_id: '',
        titulo: '',
        descricao: '',
        status: 'aberta',
        usuario_responsavel: '',
        data_atuacao: todayValue(),
        data_prevista: '',
        data_conclusao: '',
        observacao: '',
      }};
    }}

    function todayValue() {{
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      return `${{year}}-${{month}}-${{day}}`;
    }}

    function renderDrafts() {{
      if (!drafts.length) {{
        draftsEl.innerHTML = '<div class="draft-empty">Nenhuma atuação adicionada ainda. Use "Adicionar atuação" para montar o lote.</div>';
        return;
      }}
      draftsEl.innerHTML = drafts.map((draft, index) => `
        <article class="draft-card" data-index="${{index}}">
          <div class="draft-card-header">
            <div>
              <strong>Atuação ${{index + 1}}</strong>
              <small>Preencha os campos e salve tudo de uma vez.</small>
            </div>
            <button type="button" class="draft-remove" data-action="remove-draft" data-index="${{index}}">Remover</button>
          </div>
          <div class="field">
            <label>Tipo de intervenção</label>
            <select data-field="tipo_intervencao_id" data-index="${{index}}" required>
              ${{renderTipoOptions(draft.tipo_intervencao_id)}}
            </select>
          </div>
          <div class="field">
            <label>Título</label>
            <input data-field="titulo" data-index="${{index}}" required placeholder="Ex: Pendência para alta" value="${{escapeHtml(draft.titulo || '')}}" />
          </div>
          <div class="field">
            <label>Descrição</label>
            <textarea data-field="descricao" data-index="${{index}}" placeholder="Detalhe a atuação do EGAA">${{escapeHtml(draft.descricao || '')}}</textarea>
          </div>
          <div class="draft-grid">
            <div class="field">
              <label>Status</label>
              <select data-field="status" data-index="${{index}}">
                <option value="aberta" ${{draft.status === 'aberta' ? 'selected' : ''}}>Aberta</option>
                <option value="em_andamento" ${{draft.status === 'em_andamento' ? 'selected' : ''}}>Em andamento</option>
                <option value="concluida" ${{draft.status === 'concluida' ? 'selected' : ''}}>Concluída</option>
                <option value="cancelada" ${{draft.status === 'cancelada' ? 'selected' : ''}}>Cancelada</option>
              </select>
            </div>
            <div class="field">
              <label>Responsável</label>
              <input data-field="usuario_responsavel" data-index="${{index}}" placeholder="Nome do profissional" value="${{escapeHtml(draft.usuario_responsavel || '')}}" />
            </div>
          </div>
          <div class="draft-grid">
            <div class="field">
              <label>Data da atuação</label>
              <input data-field="data_atuacao" data-index="${{index}}" type="date" value="${{draft.data_atuacao || ''}}" />
            </div>
            <div class="field">
              <label>Data prevista</label>
              <input data-field="data_prevista" data-index="${{index}}" type="date" value="${{draft.data_prevista || ''}}" />
            </div>
          </div>
          <div class="draft-grid">
            <div class="field">
              <label>Data de conclusão</label>
              <input data-field="data_conclusao" data-index="${{index}}" type="datetime-local" value="${{draft.data_conclusao || ''}}" />
            </div>
            <div class="field">
              <label>Observação</label>
              <input data-field="observacao" data-index="${{index}}" placeholder="Campo livre" value="${{escapeHtml(draft.observacao || '')}}" />
            </div>
          </div>
        </article>
      `).join('');
    }}

    function syncDraftField(index, field, value) {{
      const draft = drafts[index];
      if (!draft) return;
      draft[field] = value;
    }}

    function addDraft() {{
      drafts.push(createDraft());
      renderDrafts();
    }}

    function removeDraft(index) {{
      drafts.splice(index, 1);
      if (!drafts.length) {{
        drafts.push(createDraft());
      }}
      renderDrafts();
    }}

    function fmtDate(value) {{
      if (!value) return '--';
      try {{
        const normalized = typeof value === 'string' && /^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(value)
          ? `${{value}}T00:00:00`
          : value;
        return new Intl.DateTimeFormat('pt-BR', {{ dateStyle: 'short', timeStyle: 'short' }}).format(new Date(normalized));
      }} catch {{
        return String(value);
      }}
    }}

    async function loadPaciente() {{
      const res = await fetch(`${{API_PREFIX}}/censo/paciente/${{encodeURIComponent(PRONTUARIO)}}`);
      if (!res.ok) {{
        resumoEl.innerHTML = '<div class="muted">Paciente não encontrado ou indisponível.</div>';
        return null;
      }}
      const data = await res.json();
      kpisEl.innerHTML = `
        <div class="card"><strong>Prontuário</strong><div class="kpi-value">${{data.prontuario || '--'}}</div></div>
        <div class="card"><strong>Dias</strong><div class="kpi-value">${{data.dias_internacao ?? '--'}}</div></div>
        <div class="card"><strong>Idade</strong><div class="kpi-value">${{data.idade_anos ?? '--'}}</div></div>
        <div class="card"><strong>Unidade</strong><div class="kpi-value" style="font-size:18px; line-height:1.3">${{data.unidade || '--'}}</div></div>
      `;
      subtituloEl.textContent = `${{data.nome_paciente || 'Paciente'}} · ${{data.especialidade || '--'}}`;
      resumoEl.innerHTML = `
        <div><strong>Nome:</strong> ${{data.nome_paciente || '--'}}</div>
        <div><strong>Especialidade:</strong> ${{data.especialidade || '--'}}</div>
        <div><strong>Unidade:</strong> ${{data.unidade || '--'}}</div>
        <div><strong>Enfermaria:</strong> ${{data.enfermaria || '--'}}</div>
        <div><strong>Leito:</strong> ${{data.leito || '--'}}</div>
        <div><strong>CID:</strong> ${{data.cid_internacao_codigo || '--'}} ${{data.cid_internacao_descricao ? '- ' + data.cid_internacao_descricao : ''}}</div>
        <div><strong>Internação:</strong> ${{fmtDate(data.data_internacao)}}</div>
      `;
      return data;
    }}

    async function loadTipos() {{
      const res = await fetch(`${{API_PREFIX}}/egaa/tipos-intervencao`);
      if (!res.ok) {{
        tiposOptions = [];
        tiposById = {{}};
        return [];
      }}
      const items = await res.json();
      const list = Array.isArray(items) ? items : [];
      tiposById = list.reduce((acc, item) => {{
        acc[item.id] = item.nome || item.id;
        return acc;
      }}, {{}});
      tiposOptions = list;
      renderDrafts();
      return list;
    }}

    async function loadHistorico() {{
      const res = await fetch(`${{API_PREFIX}}/egaa/intervencoes?prontuario=${{encodeURIComponent(PRONTUARIO)}}`);
      if (!res.ok) {{
        timelineEl.innerHTML = '<div class="muted">Erro ao carregar histórico.</div>';
        return [];
      }}
      const items = await res.json();
      const list = Array.isArray(items) ? items : [];
      timelineEl.innerHTML = list.length ? list.map(item => {{
        const tipoNome = escapeHtml(tiposById[item.tipo_intervencao_id] || ('ID ' + (item.tipo_intervencao_id || '--')));
        const dataAtuacao = item.data_atuacao ? fmtDate(item.data_atuacao) : '--';
        return `
        <div class="timeline-item">
          <div class="badge badge-info">${{escapeHtml(item.status || 'sem status')}}</div>
          <div class="timeline-title">${{escapeHtml(item.titulo || '--')}}</div>
          <div class="timeline-meta">Tipo: ${{tipoNome}} · Atuação: ${{dataAtuacao}} · Responsável: ${{escapeHtml(item.usuario_responsavel || '--')}}</div>
          <div class="timeline-meta">${{escapeHtml(item.descricao || '')}}</div>
          <div class="timeline-meta">Atualizado em ${{fmtDate(item.updated_at || item.created_at)}}</div>
        </div>
      `;
      }}).join('') : '<div class="muted">Nenhuma intervenção registrada para este paciente.</div>';
      return list;
    }}

    draftsEl.addEventListener('input', (event) => {{
      const target = event.target;
      if (!(target instanceof HTMLElement)) return;
      const field = target.getAttribute('data-field');
      const index = Number(target.getAttribute('data-index'));
      if (!field || Number.isNaN(index)) return;
      syncDraftField(index, field, target.value);
    }});

    draftsEl.addEventListener('change', (event) => {{
      const target = event.target;
      if (!(target instanceof HTMLElement)) return;
      const field = target.getAttribute('data-field');
      const index = Number(target.getAttribute('data-index'));
      if (!field || Number.isNaN(index)) return;
      syncDraftField(index, field, target.value);
    }});

    draftsEl.addEventListener('click', (event) => {{
      const target = event.target;
      if (!(target instanceof HTMLElement)) return;
      const action = target.getAttribute('data-action');
      if (action === 'remove-draft') {{
        const index = Number(target.getAttribute('data-index'));
        if (!Number.isNaN(index)) removeDraft(index);
      }}
    }});

    adicionarAtuacaoBtn.addEventListener('click', () => {{
      addDraft();
    }});

    limparAtuacoesBtn.addEventListener('click', () => {{
      drafts = [createDraft()];
      renderDrafts();
    }});

    form.addEventListener('submit', async (event) => {{
      event.preventDefault();
      try {{
        const items = drafts
          .filter(item => Object.values(item).some(value => value !== '' && value !== null && value !== undefined))
          .map(item => {{
            if (!item.tipo_intervencao_id) {{
              throw new Error('Selecione o tipo de intervenção em todas as atuações preenchidas.');
            }}
            if (!item.titulo.trim()) {{
              throw new Error('Informe o título de todas as atuações preenchidas.');
            }}
            return {{
              ocupacao_leito_id: null,
              prontuario: PRONTUARIO,
              tipo_intervencao_id: Number(item.tipo_intervencao_id),
              titulo: item.titulo.trim(),
              descricao: item.descricao.trim() || null,
              status: item.status,
              usuario_responsavel: item.usuario_responsavel.trim() || null,
              data_atuacao: item.data_atuacao || null,
              data_prevista: item.data_prevista || null,
              data_conclusao: item.data_conclusao ? `${{item.data_conclusao}}:00` : null,
              observacao: item.observacao.trim() || null,
            }};
          }});

        if (!items.length) {{
          alert('Adicione pelo menos uma atuação antes de salvar.');
          return;
        }}

        const payload = {{ items }};
        const res = await fetch(`${{API_PREFIX}}/egaa/intervencoes/lote`, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(payload),
        }});
        if (!res.ok) {{
          const message = await res.text();
          alert(`Não foi possível salvar as atuações. ${{message}}`);
          return;
        }}
        drafts = [createDraft()];
        renderDrafts();
        await loadHistorico();
      }} catch (error) {{
        alert(error.message || 'Verifique os dados preenchidos.');
        return;
      }}
    }});

    document.getElementById('recarregar').addEventListener('click', async () => {{
      await loadPaciente();
      await loadTipos();
      await loadHistorico();
    }});

    drafts = [createDraft()];
    renderDrafts();
    (async () => {{
      await loadPaciente();
      await loadTipos();
      await loadHistorico();
    }})();
  </script>
</body>
</html>
"""


@router.get("/configuracoes", response_class=HTMLResponse)
def configuracoes_route() -> str:
    return """
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>EGAA - Configurações</title>
  <style>
    :root {
      --bg: #F7F9FB;
      --panel: #FFFFFF;
      --panel-border: #DCE3EA;
      --text: #1F2937;
      --muted: #6B7280;
      --brand: #005C99;
      --brand-strong: #004A7A;
      --secondary: #00A79D;
      --success: #2E7D32;
      --warning: #F9A825;
      --error: #C62828;
      --info: #0288D1;
    }
    body {
      font-family: Inter, Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(0, 92, 153, 0.08), transparent 28%),
        linear-gradient(180deg, #ffffff 0%, var(--bg) 100%);
      margin: 0;
      min-height: 100vh;
      color: var(--text);
    }
    .layout { display:grid; grid-template-columns: 260px 1fr; min-height: 100vh; }
    .sidebar {
      background: rgba(255,255,255,0.84);
      backdrop-filter: blur(10px);
      border-right: 1px solid var(--panel-border);
      padding: 24px 18px;
      position: sticky;
      top: 0;
      height: 100vh;
      box-sizing: border-box;
    }
    .brand { font-size: 18px; font-weight: 700; color: var(--brand-strong); margin: 0; }
    .brand-subtitle { margin: 6px 0 18px; color: var(--muted); font-size: 13px; }
    .nav { display:flex; flex-direction:column; gap:8px; margin-top: 18px; }
    .nav a {
      color: var(--text);
      text-decoration: none;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid transparent;
      font-weight: 600;
    }
    .nav a:hover { background: rgba(0, 92, 153, 0.06); border-color: var(--panel-border); }
    .nav a.primary { background: var(--brand); color: #fff; }
    .nav a.primary:hover { background: var(--brand-strong); border-color: transparent; }
    .sidebar-note {
      margin-top: 18px;
      padding: 12px;
      border-radius: 12px;
      background: #F0F7FC;
      border: 1px solid #D7E7F3;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.45;
    }
    .main { padding: 24px; }
    .shell { max-width: 1240px; margin: 0 auto; }
    .header { display:flex; align-items:center; justify-content:space-between; gap: 16px; margin-bottom: 16px; }
    h1 { color:var(--brand-strong); margin:0; letter-spacing:-0.02em; }
    .subtitle { margin: 8px 0 0; color: var(--muted); }
    .header-actions { display:flex; gap: 10px; flex-wrap:wrap; align-items:center; }
    .pill-link {
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:10px 12px;
      border-radius: 999px;
      background: var(--panel);
      border: 1px solid var(--panel-border);
      color: var(--brand);
      text-decoration: none;
      font-weight: 600;
    }
    .badge {
      display:inline-flex;
      align-items:center;
      gap:6px;
      padding: 6px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: .02em;
      margin-bottom: 10px;
    }
    .badge-info { background: rgba(2, 136, 209, 0.12); color: var(--info); }
    .badge-secondary { background: rgba(0, 167, 157, 0.12); color: var(--secondary); }
    .badge-warning { background: rgba(249, 168, 37, 0.16); color: #8A6500; }
    .badge-success { background: rgba(46, 125, 50, 0.12); color: var(--success); }
    .cards { display:grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap:12px; margin-top:16px; }
    .card {
      background:var(--panel);
      padding:14px 16px;
      border-radius:14px;
      box-shadow:0 8px 24px rgba(16,24,40,0.08);
      border:1px solid var(--panel-border);
      min-width:0;
    }
    .card strong { display:block; color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; margin-bottom:6px; }
    .kpi-value { font-size:28px; font-weight:700; color:var(--brand-strong); line-height:1.1; }
    .grid { display:grid; grid-template-columns: 1.1fr 1.1fr; gap: 16px; margin-top: 16px; }
    .section {
      background:var(--panel);
      border:1px solid var(--panel-border);
      border-radius:14px;
      box-shadow:0 8px 24px rgba(16,24,40,0.08);
      overflow:hidden;
    }
    .section-header {
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      padding:14px 16px;
      border-bottom:1px solid #edf2f7;
    }
    .section-header h2 { margin:0; font-size:16px; color:var(--brand-strong); }
    .section-header p { margin:4px 0 0; color:var(--muted); font-size:13px; }
    .section-body { padding: 16px; }
    .field { display:flex; flex-direction:column; gap:6px; margin-bottom: 12px; }
    .field label { font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: var(--muted); font-weight: 700; }
    .field input, .field textarea, .field select {
      width: 100%;
      padding: 10px 12px;
      border-radius: 10px;
      border: 1px solid #cfd8e3;
      box-sizing: border-box;
      background: #fff;
      font: inherit;
    }
    .field textarea { min-height: 96px; resize: vertical; }
    .row { display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; }
    .actions { display:flex; gap:8px; flex-wrap:wrap; margin-top: 12px; }
    button {
      padding: 10px 12px;
      border-radius: 8px;
      border: none;
      background: var(--brand);
      color: #fff;
      cursor: pointer;
      font-weight: 600;
    }
    button.secondary {
      background: #EEF5FA;
      color: var(--brand);
      border: 1px solid var(--panel-border);
    }
    button:disabled { opacity: .65; cursor: not-allowed; }
    table { width:100%; border-collapse:collapse; margin-top:4px; background:transparent; }
    th, td { padding:10px 8px; border-bottom:1px solid #edf2f7; text-align:left; vertical-align: top; }
    th { color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; }
    .muted { color:var(--muted); }
    .pill { display:inline-flex; align-items:center; padding:4px 8px; border-radius:999px; font-size:12px; font-weight:700; }
    .pill.active { background: rgba(46, 125, 50, 0.12); color: var(--success); }
    .pill.inactive { background: rgba(198, 40, 40, 0.12); color: var(--error); }
    .full { grid-column: 1 / -1; }
    @media (max-width: 1100px) {
      .layout { grid-template-columns: 1fr; }
      .sidebar { position: static; height: auto; border-right: none; border-bottom: 1px solid var(--panel-border); }
      .grid { grid-template-columns: 1fr; }
      .row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <p class="brand">EGAA</p>
      <p class="brand-subtitle">Painel de regulação e censo</p>
      <nav class="nav">
        <a href="/dashboard">Dashboard</a>
        <a href="/pacientes">Pacientes</a>
        <a href="/longa-permanencia">Longa Permanência</a>
        <a class="primary" href="/configuracoes">Configurações</a>
        <a href="/upload">Importações</a>
      </nav>
      <div class="sidebar-note">
        Parametrização do fluxo operacional, com tipos de intervenção e registro rápido para acompanhamento da equipe.
      </div>
    </aside>
    <main class="main">
      <div class="shell">
        <div class="header">
          <div>
            <h1>Configurações EGAA</h1>
            <p class="subtitle">Administre tipos de intervenção e registre ações operacionais diretamente pela interface.</p>
          </div>
          <div class="header-actions">
            <a class="pill-link" href="/dashboard">Voltar ao dashboard</a>
            <a class="pill-link" href="/longa-permanencia">Abrir longa permanência</a>
            <a class="pill-link" href="/api/egaa/export/xlsx">Exportar EGAA</a>
          </div>
        </div>

        <div class="cards" id="kpis">
          <div class="card"><span class="badge badge-info">Tipos</span><strong>Cadastrados</strong><div class="kpi-value">--</div></div>
          <div class="card"><span class="badge badge-secondary">Ativos</span><strong>Disponíveis</strong><div class="kpi-value">--</div></div>
          <div class="card"><span class="badge badge-warning">Intervenções</span><strong>Registradas</strong><div class="kpi-value">--</div></div>
        </div>

        <div class="grid">
          <section class="section">
            <div class="section-header">
              <div>
                <h2>Novo tipo de intervenção</h2>
                <p>Use esta área para manter o catálogo do EGAA organizado.</p>
              </div>
            </div>
            <div class="section-body">
              <form id="tipoForm">
                <div class="field">
                  <label for="tipoNome">Nome</label>
                  <input id="tipoNome" required placeholder="Ex: Evolução EGAA" />
                </div>
                <div class="field">
                  <label for="tipoDescricao">Descrição</label>
                  <textarea id="tipoDescricao" placeholder="Descreva o uso deste tipo de intervenção"></textarea>
                </div>
                <div class="row">
                  <div class="field">
                    <label for="tipoOrdem">Ordem</label>
                    <input id="tipoOrdem" type="number" min="0" step="1" value="0" />
                  </div>
                  <div class="field">
                    <label for="tipoAtivo">Status</label>
                    <select id="tipoAtivo">
                      <option value="true">Ativo</option>
                      <option value="false">Inativo</option>
                    </select>
                  </div>
                </div>
                <div class="actions">
                  <button type="submit">Salvar tipo</button>
                  <button type="button" class="secondary" id="reloadTipos">Recarregar</button>
                </div>
              </form>
            </div>
          </section>

          <section class="section">
            <div class="section-header">
              <div>
                <h2>Registro rápido de intervenção</h2>
                <p>Fluxo operacional mínimo para registrar uma ação no paciente.</p>
              </div>
            </div>
            <div class="section-body">
              <form id="intervencaoForm">
                <div class="row">
                  <div class="field">
                    <label for="ocupacaoLeitoId">Ocupação do leito</label>
                    <input id="ocupacaoLeitoId" type="number" min="1" step="1" placeholder="Opcional" />
                  </div>
                  <div class="field">
                    <label for="prontuario">Prontuário</label>
                    <input id="prontuario" required placeholder="Número do prontuário" />
                  </div>
                </div>
                <div class="row">
                  <div class="field">
                    <label for="tipoIntervencaoId">Tipo de intervenção</label>
                    <select id="tipoIntervencaoId" required>
                      <option value="">Carregando...</option>
                    </select>
                  </div>
                  <div class="field">
                    <label for="statusIntervencao">Status</label>
                    <select id="statusIntervencao">
                      <option value="aberta">Aberta</option>
                      <option value="em_andamento">Em andamento</option>
                      <option value="concluida">Concluída</option>
                      <option value="cancelada">Cancelada</option>
                    </select>
                  </div>
                </div>
                <div class="field">
                  <label for="tituloIntervencao">Título</label>
                  <input id="tituloIntervencao" required placeholder="Ex: Pendência para alta" />
                </div>
                <div class="field">
                  <label for="descricaoIntervencao">Descrição</label>
                  <textarea id="descricaoIntervencao" placeholder="Detalhe a intervenção ou a pendência"></textarea>
                </div>
                <div class="row">
                  <div class="field">
                    <label for="responsavelIntervencao">Responsável</label>
                    <input id="responsavelIntervencao" placeholder="Nome do profissional" />
                  </div>
                  <div class="field">
                    <label for="dataAtuacaoIntervencao">Data da atuação</label>
                    <input id="dataAtuacaoIntervencao" type="date" />
                  </div>
                </div>
                <div class="row">
                  <div class="field">
                    <label for="dataPrevistaIntervencao">Data prevista</label>
                    <input id="dataPrevistaIntervencao" type="date" />
                  </div>
                  <div class="field">
                    <label for="dataConclusaoIntervencao">Data de conclusão</label>
                    <input id="dataConclusaoIntervencao" type="datetime-local" />
                  </div>
                </div>
                <div class="row">
                  <div class="field">
                    <label for="observacaoIntervencao">Observação</label>
                    <input id="observacaoIntervencao" placeholder="Campo livre" />
                  </div>
                </div>
                <div class="actions">
                  <button type="submit">Salvar intervenção</button>
                  <button type="button" class="secondary" id="reloadIntervencoes">Recarregar</button>
                </div>
              </form>
            </div>
          </section>

          <section class="section full">
            <div class="section-header">
              <div>
                <h2>Tipos cadastrados</h2>
                <p>Catálogo disponível para uso no registro operacional.</p>
              </div>
            </div>
            <div class="section-body">
              <table>
                <thead>
                  <tr><th>Nome</th><th>Descrição</th><th>Ordem</th><th>Status</th></tr>
                </thead>
                <tbody id="tiposRows">
                  <tr><td colspan="4" class="muted">Aguardando dados...</td></tr>
                </tbody>
              </table>
            </div>
          </section>

          <section class="section full">
            <div class="section-header">
              <div>
                <h2>Intervenções recentes</h2>
                <p>Últimos registros realizados pelo EGAA.</p>
              </div>
            </div>
            <div class="section-body">
              <table>
                <thead>
                  <tr><th>Prontuário</th><th>Título</th><th>Tipo</th><th>Status</th><th>Responsável</th><th>Atuação</th><th>Atualizado</th></tr>
                </thead>
                <tbody id="intervencoesRows">
                  <tr><td colspan="7" class="muted">Aguardando dados...</td></tr>
                </tbody>
              </table>
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>

  <script>
    const API_PREFIX = '/api';
    const kpisEl = document.getElementById('kpis');
    const tiposRowsEl = document.getElementById('tiposRows');
    const intervencoesRowsEl = document.getElementById('intervencoesRows');
    const tipoForm = document.getElementById('tipoForm');
    const intervencaoForm = document.getElementById('intervencaoForm');
    const tipoIntervencaoId = document.getElementById('tipoIntervencaoId');

    function fmtDate(value) {
      if (!value) return '--';
      try {
        const normalized = typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value)
          ? `${value}T00:00:00`
          : value;
        return new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short' }).format(new Date(normalized));
      } catch {
        return String(value);
      }
    }

    function todayInputValue() {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    }

    async function loadTipos() {
      const res = await fetch(`${API_PREFIX}/egaa/tipos-intervencao`);
      if (!res.ok) {
        tiposRowsEl.innerHTML = '<tr><td colspan="4" class="muted">Erro ao carregar tipos.</td></tr>';
        return [];
      }
      const items = await res.json();
      const list = Array.isArray(items) ? items : [];
      tiposRowsEl.innerHTML = list.length
        ? list.map(item => `
            <tr>
              <td><strong>${item.nome || '--'}</strong></td>
              <td>${item.descricao || '<span class="muted">Sem descrição</span>'}</td>
              <td>${item.ordem_exibicao ?? 0}</td>
              <td><span class="pill ${item.ativo ? 'active' : 'inactive'}">${item.ativo ? 'Ativo' : 'Inativo'}</span></td>
            </tr>`).join('')
        : '<tr><td colspan="4" class="muted">Nenhum tipo cadastrado.</td></tr>';
      tipoIntervencaoId.innerHTML = list.length
        ? ['<option value="">Selecione...</option>'].concat(list.map(item => `<option value="${item.id}">${item.nome || '--'}</option>`)).join('')
        : '<option value="">Nenhum tipo disponível</option>';
      return list;
    }

    async function loadIntervencoes(tiposById = {}) {
      const res = await fetch(`${API_PREFIX}/egaa/intervencoes`);
      if (!res.ok) {
        intervencoesRowsEl.innerHTML = '<tr><td colspan="7" class="muted">Erro ao carregar intervenções.</td></tr>';
        return [];
      }
      const items = await res.json();
      const list = Array.isArray(items) ? items : [];
      intervencoesRowsEl.innerHTML = list.length
          ? list.slice(0, 10).map(item => `
            <tr>
              <td>${item.prontuario || '--'}</td>
              <td><strong>${item.titulo || '--'}</strong><div class="muted">${item.descricao || ''}</div></td>
              <td>${tiposById[item.tipo_intervencao_id] || item.tipo_intervencao_id || '--'}</td>
              <td>${item.status || '--'}</td>
              <td>${item.usuario_responsavel || '--'}</td>
              <td>${fmtDate(item.data_atuacao || item.created_at)}</td>
              <td>${fmtDate(item.updated_at || item.created_at)}</td>
            </tr>`).join('')
        : '<tr><td colspan="7" class="muted">Nenhuma intervenção registrada.</td></tr>';
      return list;
    }

    function refreshKPIs(tipos, intervencoes) {
      const ativos = tipos.filter(item => item.ativo).length;
      kpisEl.innerHTML = `
        <div class="card"><span class="badge badge-info">Tipos</span><strong>Cadastrados</strong><div class="kpi-value">${tipos.length}</div></div>
        <div class="card"><span class="badge badge-secondary">Ativos</span><strong>Disponíveis</strong><div class="kpi-value">${ativos}</div></div>
        <div class="card"><span class="badge badge-warning">Intervenções</span><strong>Registradas</strong><div class="kpi-value">${intervencoes.length}</div></div>
      `;
    }

    async function reloadAll() {
      const tipos = await loadTipos();
      const tiposById = tipos.reduce((acc, item) => {
        acc[item.id] = item.nome || item.id;
        return acc;
      }, {});
      const intervencoes = await loadIntervencoes(tiposById);
      refreshKPIs(tipos, intervencoes);
    }

    tipoForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const payload = {
        nome: document.getElementById('tipoNome').value.trim(),
        descricao: document.getElementById('tipoDescricao').value.trim() || null,
        ativo: document.getElementById('tipoAtivo').value === 'true',
        ordem_exibicao: Number(document.getElementById('tipoOrdem').value || 0),
      };
      const res = await fetch(`${API_PREFIX}/egaa/tipos-intervencao`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        alert('Não foi possível salvar o tipo de intervenção.');
        return;
      }
      tipoForm.reset();
      document.getElementById('tipoOrdem').value = 0;
      document.getElementById('tipoAtivo').value = 'true';
      await reloadAll();
    });

    intervencaoForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const payload = {
        ocupacao_leito_id: document.getElementById('ocupacaoLeitoId').value ? Number(document.getElementById('ocupacaoLeitoId').value) : null,
        prontuario: document.getElementById('prontuario').value.trim(),
        tipo_intervencao_id: Number(tipoIntervencaoId.value),
        titulo: document.getElementById('tituloIntervencao').value.trim(),
        descricao: document.getElementById('descricaoIntervencao').value.trim() || null,
        status: document.getElementById('statusIntervencao').value,
        usuario_responsavel: document.getElementById('responsavelIntervencao').value.trim() || null,
        data_atuacao: document.getElementById('dataAtuacaoIntervencao').value || null,
        data_prevista: document.getElementById('dataPrevistaIntervencao').value || null,
        data_conclusao: document.getElementById('dataConclusaoIntervencao').value ? `${document.getElementById('dataConclusaoIntervencao').value}:00` : null,
        observacao: document.getElementById('observacaoIntervencao').value.trim() || null,
      };
      const res = await fetch(`${API_PREFIX}/egaa/intervencoes`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        alert('Não foi possível salvar a intervenção.');
        return;
      }
      intervencaoForm.reset();
      document.getElementById('dataAtuacaoIntervencao').value = todayInputValue();
      await reloadAll();
    });

    document.getElementById('reloadTipos').addEventListener('click', reloadAll);
    document.getElementById('reloadIntervencoes').addEventListener('click', reloadAll);

    document.getElementById('dataAtuacaoIntervencao').value = todayInputValue();
    reloadAll();
  </script>
</body>
</html>
"""
