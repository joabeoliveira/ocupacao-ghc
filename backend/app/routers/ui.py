from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from app.config import settings


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
  <div class="top-nav" style="max-width:720px;margin:0 auto 12px;display:flex;gap:8px;">
    <a href="/dashboard" style="text-decoration:none;padding:8px 12px;border-radius:8px;background:#fff;border:1px solid #DCE3EA;color:var(--brand);font-weight:600;">Dashboard</a>
    <a href="/longa-permanencia" style="text-decoration:none;padding:8px 12px;border-radius:8px;background:#fff;border:1px solid #DCE3EA;color:var(--brand);font-weight:600;">Longa Permanência</a>
    <a href="/desfechos" style="text-decoration:none;padding:8px 12px;border-radius:8px;background:#fff;border:1px solid #DCE3EA;color:var(--brand);font-weight:600;">Desfechos EGAA</a>
    <a href="/configuracoes" style="text-decoration:none;padding:8px 12px;border-radius:8px;background:#fff;border:1px solid #DCE3EA;color:var(--brand);font-weight:600;">Configurações</a>
  </div>

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
      display: flex;
      flex-direction: column;
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
    .pie-wrapper { display:flex; gap:16px; align-items:center; flex-wrap:wrap; padding-top: 8px; }
    .pie-chart {
      width: 168px;
      height: 168px;
      border-radius: 50%;
      border: 1px solid #e5ecf3;
      background: #f4f7fb;
      flex: 0 0 auto;
    }
    .pie-legend { display:flex; flex-direction:column; gap:8px; min-width: 220px; flex: 1; }
    .pie-legend-item { display:flex; align-items:center; justify-content:space-between; gap:10px; font-size:13px; }
    .pie-legend-label { display:flex; align-items:center; gap:8px; min-width: 0; }
    .pie-dot { width:10px; height:10px; border-radius:50%; flex: 0 0 10px; }
    .pie-text { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:var(--text); font-weight:600; }
    .pie-value { color:var(--brand); font-weight:700; white-space:nowrap; }
    .chart-tooltip { position: absolute; background: rgba(0,0,0,0.8); color: #fff; padding:6px 8px; border-radius:4px; font-size:12px; pointer-events:none; display:none; z-index:50; }
    @media (max-width: 1100px) {
      .layout { grid-template-columns: 1fr; }
      .sidebar { position: static; height: auto; border-right: none; border-bottom: 1px solid var(--panel-border); }
      .filters-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .chart-row { grid-template-columns: 1fr; }
      .chart-value { text-align:left; }
    }
    .sidebar-version {
      margin-top: auto; padding: 10px 12px; border-radius: 10px;
      background: rgba(0,0,0,0.04); color: var(--muted); font-size: 11px;
      text-align: center; letter-spacing: .02em;
    }
      .sidebar-version {
      margin-top: auto; padding: 10px 12px; border-radius: 10px;
      background: rgba(0,0,0,0.04); color: var(--muted); font-size: 11px;
      text-align: center; letter-spacing: .02em;
    }
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <p class="brand">EGAA</p>
      <p class="brand-subtitle">Administração</p>
      <nav class="nav">
        <a class="primary" href="/dashboard">Dashboard</a>
        <a href="/longa-permanencia">Longa Permanência</a>
        <a href="/desfechos">Desfechos EGAA</a>
        <a href="/configuracoes">Configurações</a>
        <a href="/upload">Importações</a>
        <a href="#resumo">Resumo</a>
      </nav>
      <div class="sidebar-note">
        A pergunta principal desta tela é simples: <strong>como está a ocupação hoje?</strong>
        Use os filtros acima para refinar a leitura.
      </div>
      <div class="sidebar-version">v__APP_VERSION__ · __APP_ENV__</div>
    </aside>
    <main class="main">
      <div class="shell">
        <div class="header">
          <div>
            <h1>Dashboard</h1>
            <p class="subtitle">Visão rápida da ocupação, concentração por unidade e resultados do EGAA.</p>
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
          </div>
          <div class="actions" style="margin-top: 12px;">
            <button id="filtrar">Aplicar filtros</button>
            <button id="refresh" class="secondary-btn">Recarregar</button>
          </div>
        </section>

        <div class="cards" id="kpis">
          <div class="card">Carregando...</div>
        </div>

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
                <div class="pie-wrapper" id="egaaStatusChart">
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
            <div class="pie-wrapper" id="unidadesChart">
              <div class="muted">Aguardando dados...</div>
            </div>
          </div>
        </section>
      </div>
    </main>
  </div>

  <script>
    const API_PREFIX = '/api';
    const kpisEl = document.getElementById('kpis');
    const egaaResumoEl = document.getElementById('egaaResumo');
    const egaaKpisEl = document.getElementById('egaaKpis');
    const egaaStatusChartEl = document.getElementById('egaaStatusChart');
    const egaaMesChartEl = document.getElementById('egaaMesChart');
    const unidadesChartEl = document.getElementById('unidadesChart');
    const unidadesResumoEl = document.getElementById('unidadesResumo');
    const prontuarioEl = document.getElementById('prontuario');
    const nomeEl = document.getElementById('nome');
    const especialidadeEl = document.getElementById('especialidade');
    const unidadeEl = document.getElementById('unidade');
    const dataInicioEl = document.getElementById('dataInicio');
    const dataFimEl = document.getElementById('dataFim');
    const filtrarBtn = document.getElementById('filtrar');

    function escapeHtml(value) {
      return String(value ?? '').replace(/[&<>"']/g, (character) => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
      }[character] || character));
    }

    function normalizePieLabel(item) {
      if (item && typeof item.status === 'string' && item.status) return item.status;
      if (item && typeof item.unidade === 'string' && item.unidade) return item.unidade;
      if (item && typeof item.label === 'string' && item.label) return item.label;
      return '--';
    }

    function normalizePieValue(item) {
      if (!item || typeof item !== 'object') return 0;
      return Number(item.total ?? item.total_pacientes ?? item.value ?? 0) || 0;
    }

    function renderPieChart(container, items, emptyMessage) {
      if (!Array.isArray(items) || !items.length) {
        container.innerHTML = `<div class="muted">${emptyMessage}</div>`;
        return;
      }
      const total = items.reduce((acc, item) => acc + normalizePieValue(item), 0);
      if (!total) {
        container.innerHTML = `<div class="muted">${emptyMessage}</div>`;
        return;
      }
      const palette = ['#005C99', '#00A79D', '#F9A825', '#C62828', '#0288D1', '#2E7D32', '#6B7280'];
      let cursor = 0;
      const segments = items.map((item, index) => {
        const value = normalizePieValue(item);
        const percent = (value / total) * 100;
        const start = cursor;
        cursor += percent;
        return { label: normalizePieLabel(item), value, start, end: cursor, color: palette[index % palette.length] };
      });
      const gradient = segments
        .map((segment) => `${segment.color} ${segment.start.toFixed(2)}% ${segment.end.toFixed(2)}%`)
        .join(', ');
      const legend = segments
        .map((segment) => {
          const pct = ((segment.value / total) * 100).toFixed(1);
          return `<div class="pie-legend-item"><div class="pie-legend-label"><span class="pie-dot" style="background:${segment.color}"></span><span class="pie-text" title="${escapeHtml(segment.label)}">${escapeHtml(segment.label)}</span></div><span class="pie-value">${segment.value} (${pct}%)</span></div>`;
        })
        .join('');
      container.innerHTML = `<div class="pie-chart" aria-hidden="true" style="background:conic-gradient(${gradient});"></div><div class="pie-legend">${legend}</div>`;
    }

    function renderColumnChart(container, {labels, series, colors, options={}}) {
      container.innerHTML = '';
      try {
        const svgNS = 'http://www.w3.org/2000/svg';
        function getSeriesColor(key, idx, fallback) {
          const map = {
            intervencoes: 'var(--brand)',
            altas: 'var(--success)',
            abertas: 'var(--warning)',
            pendentes: 'var(--warning)',
            em_andamento: 'var(--secondary)',
            concluidas: 'var(--success)'
          };
        
          return (colors && colors[idx]) || fallback || map[key] || 'var(--brand)';
        }

        const localSeries = (series || []).map((s, i) => ({ ...s, visible: typeof s.visible === 'boolean' ? s.visible : true, color: getSeriesColor((s.key || s.label || '').toString().toLowerCase(), i, s.color) }));

        const render = () => {
          const existingWrap = container.querySelector('.chart-legend-wrap');
          container.innerHTML = '';
          if (existingWrap) container.appendChild(existingWrap);
          const width = container.clientWidth || 600;
          const height = options.height || 240;
          const padding = {top:24, right:12, bottom:48, left:44};
          const innerW = width - padding.left - padding.right;
          const innerH = height - padding.top - padding.bottom;

          const cols = labels.length;
          const isStacked = (options.stacked === true) || (width < 420 && series.length > 1);

          // calcular máximo
          let maxVal = 0;
          if (isStacked) {
            for (let i=0;i<cols;i++) {
              const sum = series.reduce((acc, s) => acc + ((s.values[i] || 0) * (s.visible ? 1 : 0)), 0);
              if (sum > maxVal) maxVal = sum;
            }
          } else {
            for (const s of series) {
              for (const v of s.values) if ((s.visible ?? true) && v > maxVal) maxVal = v;
            }
          }

          const svg = document.createElementNS(svgNS, 'svg');
          svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
          svg.setAttribute('width', '100%');
          svg.setAttribute('height', height);

          // grid
          const grid = document.createElementNS(svgNS, 'g');
          const lines = 4;
          for (let i=0;i<=lines;i++){
            const y = padding.top + (innerH * i / lines);
            const line = document.createElementNS(svgNS,'line');
            line.setAttribute('x1', padding.left);
            line.setAttribute('x2', padding.left + innerW);
            line.setAttribute('y1', y);
            line.setAttribute('y2', y);
            line.setAttribute('stroke', 'var(--muted)');
            line.setAttribute('stroke-width', '1');
            grid.appendChild(line);
          }
          svg.appendChild(grid);

          const bandWidth = innerW / Math.max(1, cols);
          const barGap = Math.max(6, Math.floor(bandWidth * 0.08));
          const barWidth = Math.max(8, Math.floor((bandWidth - barGap*2) / Math.max(1, series.length)));

          const barsGroup = document.createElementNS(svgNS,'g');

          for (let i=0;i<cols;i++){
            const xBase = padding.left + i * bandWidth;
            if (isStacked) {
              let cum = 0;
              for (let sIndex = 0; sIndex < localSeries.length; sIndex++){
                const s = localSeries[sIndex];
                if (!s.visible) continue;
                const val = s.values[i] || 0;
                const h = maxVal === 0 ? 0 : (val / maxVal) * innerH;
                const y = padding.top + (innerH - (cum + h));
                const rect = document.createElementNS(svgNS,'rect');
                rect.setAttribute('x', xBase + barGap);
                rect.setAttribute('y', y);
                rect.setAttribute('width', Math.max(0, bandWidth - barGap*2));
                rect.setAttribute('height', Math.max(0, h));
                rect.setAttribute('fill', s.color);
                rect.setAttribute('role','img');
                rect.setAttribute('tabindex','0');
                rect.setAttribute('aria-label', `${labels[i]}: ${s.label}: ${val}`);
                // animation: fade/translate
                rect.style.opacity = '0';
                rect.style.transform = 'translateY(8px)';
                rect.style.transition = 'transform 560ms cubic-bezier(.2,.9,.2,1), opacity 420ms ease';
                const fmt = (v) => new Intl.NumberFormat('pt-BR').format(Number(v || 0));
                rect.addEventListener('mouseenter', e => showTooltip(e, `${s.label}: ${fmt(val)}`));
                rect.addEventListener('focus', e => showTooltip(e, `${s.label}: ${fmt(val)}`));
                rect.addEventListener('mouseleave', hideTooltip);
                rect.addEventListener('blur', hideTooltip);
                barsGroup.appendChild(rect);
                // trigger animation
                requestAnimationFrame(() => { rect.style.opacity = '1'; rect.style.transform = 'translateY(0)'; });
                cum += h;
                // mostrar valor na própria barra (ajusta cor se barra for pequena)
                try {
                  const txt = document.createElementNS(svgNS,'text');
                  const w = Math.max(0, bandWidth - barGap*2);
                  const cx = xBase + barGap + w/2;
                  const yInside = y + Math.min(14, Math.max(8, h - 4));
                  const small = h < 18;
                  const yText = small ? (y - 4) : yInside;
                  txt.setAttribute('x', cx);
                  txt.setAttribute('y', yText);
                  txt.setAttribute('text-anchor','middle');
                  txt.setAttribute('fill', small ? 'var(--text)' : '#ffffff');
                  txt.setAttribute('font-size','12');
                  txt.setAttribute('font-weight','700');
                  txt.style.pointerEvents = 'none';
                  txt.textContent = new Intl.NumberFormat('pt-BR').format(Number(val || 0));
                  barsGroup.appendChild(txt);
                } catch(e) {/* ignore */}
              }
            } else {
              let visibleIdx = 0;
              for (let sIndex = 0; sIndex < localSeries.length; sIndex++){
                const s = localSeries[sIndex];
                if (!s.visible) continue;
                const val = s.values[i] || 0;
                const h = maxVal === 0 ? 0 : (val / maxVal) * innerH;
                const x = xBase + barGap + visibleIdx * barWidth;
                const y = padding.top + (innerH - h);
                const rect = document.createElementNS(svgNS,'rect');
                rect.setAttribute('x', x);
                rect.setAttribute('y', y);
                rect.setAttribute('width', Math.max(0, barWidth - 1));
                rect.setAttribute('height', Math.max(0, h));
                rect.setAttribute('fill', s.color);
                rect.setAttribute('role','img');
                rect.setAttribute('tabindex','0');
                rect.setAttribute('aria-label', `${labels[i]}: ${s.label}: ${val}`);
                rect.style.opacity = '0';
                rect.style.transform = 'translateY(8px)';
                rect.style.transition = 'transform 560ms cubic-bezier(.2,.9,.2,1), opacity 420ms ease';
                const fmt2 = (v) => new Intl.NumberFormat('pt-BR').format(Number(v || 0));
                rect.addEventListener('mouseenter', e => showTooltip(e, `${s.label}: ${fmt2(val)}`));
                rect.addEventListener('focus', e => showTooltip(e, `${s.label}: ${fmt2(val)}`));
                rect.addEventListener('mouseleave', hideTooltip);
                rect.addEventListener('blur', hideTooltip);
                barsGroup.appendChild(rect);
                requestAnimationFrame(() => { rect.style.opacity = '1'; rect.style.transform = 'translateY(0)'; });
                visibleIdx++;
                // mostrar valor na própria barra (ajusta cor se barra for pequena)
                try {
                  const txt = document.createElementNS(svgNS,'text');
                  const w = Math.max(0, barWidth - 1);
                  const cx = x + w/2;
                  const yInside = y + Math.min(14, Math.max(8, h - 4));
                  const small = h < 18;
                  const yText = small ? (y - 4) : yInside;
                  txt.setAttribute('x', cx);
                  txt.setAttribute('y', yText);
                  txt.setAttribute('text-anchor','middle');
                  txt.setAttribute('fill', small ? 'var(--text)' : '#ffffff');
                  txt.setAttribute('font-size','12');
                  txt.setAttribute('font-weight','700');
                  txt.style.pointerEvents = 'none';
                  txt.textContent = new Intl.NumberFormat('pt-BR').format(Number(val || 0));
                  barsGroup.appendChild(txt);
                } catch(e) {/* ignore */}
              }
            }
            const tx = document.createElementNS(svgNS,'text');
            tx.setAttribute('x', xBase + bandWidth/2);
            tx.setAttribute('y', padding.top + innerH + 18);
            tx.setAttribute('text-anchor','middle');
            tx.setAttribute('fill','var(--muted)');
            tx.setAttribute('font-size','12');
            tx.textContent = labels[i];
            svg.appendChild(tx);
          }
          svg.appendChild(barsGroup);

          container.appendChild(svg);
        };

        // legend + download
        const legendWrap = document.createElement('div');
        legendWrap.className = 'chart-legend-wrap';
        legendWrap.style.display = 'flex';
        legendWrap.style.alignItems = 'center';
        legendWrap.style.justifyContent = 'space-between';
        legendWrap.style.marginBottom = '8px';

        const legend = document.createElement('div');
        legend.className = 'chart-legend';
        legend.style.display = 'flex';
        legend.style.gap = '12px';
        legend.style.alignItems = 'center';
        series.forEach((s, idx) => {
          const item = document.createElement('button');
          item.type = 'button';
          item.className = 'legend-item';
          item.style.display = 'inline-flex';
          item.style.alignItems = 'center';
          item.style.gap = '8px';
          item.style.border = '1px solid transparent';
          item.style.background = 'transparent';
          item.style.cursor = 'pointer';
          item.style.padding = '6px 8px';
          item.style.borderRadius = '8px';
          item.setAttribute('aria-pressed', (s.visible ?? true) ? 'true' : 'false');
          const dot = document.createElement('span');
          dot.style.width = '12px';
          dot.style.height = '12px';
          dot.style.borderRadius = '50%';
          dot.style.background = (s.color || ((colors && colors[idx]) || 'var(--brand)'));
          const label = document.createElement('span');
          label.textContent = s.label || s.key || `Série ${idx+1}`;
          label.style.fontWeight = '600';
          label.style.color = 'var(--text)';
          item.appendChild(dot);
          item.appendChild(label);
          item.addEventListener('click', () => {
            s.visible = !s.visible;
            item.setAttribute('aria-pressed', s.visible ? 'true' : 'false');
            render();
          });
          legend.appendChild(item);
        });

        const controls = document.createElement('div');
        controls.style.display = 'flex';
        controls.style.gap = '8px';

        const downloadBtn = document.createElement('button');
        downloadBtn.type = 'button';
        downloadBtn.textContent = 'Download PNG';
        downloadBtn.title = 'Baixar gráfico como PNG';
        downloadBtn.style.padding = '6px 10px';
        downloadBtn.style.borderRadius = '8px';
        downloadBtn.style.border = '1px solid var(--panel-border)';
        downloadBtn.style.background = 'var(--panel)';
        downloadBtn.style.cursor = 'pointer';
        downloadBtn.style.color = 'var(--brand)';
        downloadBtn.addEventListener('click', () => {
          const svgEl = container.querySelector('svg');
          if (!svgEl) return;
          // serializar SVG e substituir variáveis CSS por valores computados
          const serializer = new XMLSerializer();
          let svgStr = serializer.serializeToString(svgEl);
          const styles = getComputedStyle(document.documentElement);
          svgStr = svgStr.replace(/var\\((--[a-zA-Z0-9\\-]+)\\)/g, (m, varName) => {
            const val = styles.getPropertyValue(varName).trim();
            return val || m;
          });
          const blob = new Blob([svgStr], {type: 'image/svg+xml;charset=utf-8'});
          const url = URL.createObjectURL(blob);
          const img = new Image();
          img.onload = () => {
            const canvas = document.createElement('canvas');
            // tentar usar viewBox se disponível
            const vb = svgEl.viewBox && svgEl.viewBox.baseVal ? svgEl.viewBox.baseVal : null;
            canvas.width = vb ? vb.width : (img.width || 800);
            canvas.height = vb ? vb.height : (img.height || 400);
            const ctx = canvas.getContext('2d');
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0,0,canvas.width,canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            URL.revokeObjectURL(url);
            canvas.toBlob((blobPng) => {
              const link = document.createElement('a');
              link.href = URL.createObjectURL(blobPng);
              link.download = 'evolucao-mensal.png';
              document.body.appendChild(link);
              link.click();
              link.remove();
            }, 'image/png');
          };
          img.onerror = () => { URL.revokeObjectURL(url); alert('Falha ao gerar imagem.'); };
          img.src = url;
        });

        controls.appendChild(downloadBtn);
        legendWrap.appendChild(legend);
        legendWrap.appendChild(controls);
        container.appendChild(legendWrap);

        // tooltip element shared
        const tooltip = document.createElement('div');
        tooltip.className = 'chart-tooltip';
        container.style.position = 'relative';
        container.appendChild(tooltip);

        function showTooltip(e, text){
          tooltip.textContent = text;
          tooltip.style.display = 'block';
          const containerRect = container.getBoundingClientRect();
          // suportar mouse events e focus events
          if (typeof e.clientX === 'number') {
            tooltip.style.left = (e.clientX - containerRect.left + 8) + 'px';
            tooltip.style.top = (e.clientY - containerRect.top - 28) + 'px';
          } else {
            const target = e.target || e.srcElement;
            if (target && target.getBoundingClientRect) {
              const r = target.getBoundingClientRect();
              const left = r.left + r.width / 2 - containerRect.left;
              const top = r.top - containerRect.top - 28;
              tooltip.style.left = left + 'px';
              tooltip.style.top = top + 'px';
            }
          }
        }
        function hideTooltip(){ tooltip.style.display = 'none'; }

        render();
        let resizeTimer;
        window.addEventListener('resize', () => {
          clearTimeout(resizeTimer);
          resizeTimer = setTimeout(render, 150);
        });
      } catch(err) {
        container.innerHTML = `<div class="muted">Erro ao renderizar gráfico.</div>`;
        console.error(err);
      }
    }

    async function loadKPIs() {
      const params = new URLSearchParams();
      if (dataInicioEl.value) params.set('data_inicio', dataInicioEl.value);
      if (dataFimEl.value) params.set('data_fim', dataFimEl.value);

      const query = params.toString();
      const res = await fetch(`${API_PREFIX}/censo/kpis${query ? `?${query}` : ''}`);
      if (!res.ok) return kpisEl.innerHTML = '<div class="card">Erro ao obter KPIs</div>';
      const data = await res.json();
      const fmtPct = (value) => `${Number(value || 0).toFixed(2)}%`;
      const unidades = Array.isArray(data.ocupacao_por_unidade) ? data.ocupacao_por_unidade : [];
      const topUnidades = unidades.slice(0, 5);
      kpisEl.innerHTML = `
        <div class="card"><span class="badge badge-info">Leitos</span><strong>Leitos ocupados</strong><div class="kpi-value">${data.leitos_ocupados}</div></div>
        <div class="card"><span class="badge badge-secondary">Leitos</span><strong>Leitos livres</strong><div class="kpi-value">${data.leitos_livres}</div></div>
        <div class="card"><span class="badge badge-warning">Leitos</span><strong>Leitos bloqueados</strong><div class="kpi-value">${data.leitos_bloqueados}</div></div>
        <div class="card"><span class="badge badge-success">Taxa</span><strong>Ocupação geral</strong><div class="kpi-value">${fmtPct(data.taxa_ocupacao_geral_percentual)}</div></div>
        <div class="card"><span class="badge badge-success">Taxa</span><strong>Ocupação operacional</strong><div class="kpi-value">${fmtPct(data.taxa_ocupacao_operacional_percentual)}</div></div>
        <div class="card"><span class="badge badge-warning">Atenção</span><strong>>=15 dias</strong><div class="kpi-value">${data.longa_permanencia_15}</div></div>
        <div class="card"><span class="badge badge-error">Crítico</span><strong>>=30 dias</strong><div class="kpi-value">${data.longa_permanencia_30}</div></div>
        <div class="card"><span class="badge badge-secondary">60+ anos</span><strong>Pacientes</strong><div class="kpi-value">${data.longa_permanencia_60_anos}</div></div>
        <div class="card"><span class="badge badge-secondary">60+ e 15+</span><strong>Pacientes</strong><div class="kpi-value">${data.longa_permanencia_60_15}</div></div>
        <div class="card"><span class="badge badge-secondary">60+ e 30+</span><strong>Pacientes</strong><div class="kpi-value">${data.longa_permanencia_60_30}</div></div>`;
      unidadesResumoEl.textContent = unidades.length
        ? `Mostrando as ${topUnidades.length} unidades com mais pacientes de um total de ${unidades.length}.`
        : 'Nenhuma unidade retornada pela API.';
      renderPieChart(unidadesChartEl, topUnidades, 'Nenhuma unidade para exibir.');
    }

    async function loadEgaaIndicadores() {
      const res = await fetch(`${API_PREFIX}/egaa/indicadores`);
      if (!res.ok) {
        egaaResumoEl.textContent = 'Não foi possível carregar os indicadores do EGAA.';
        egaaKpisEl.innerHTML = '<div class="card">Erro ao obter indicadores</div>';
        egaaStatusChartEl.innerHTML = '<div class="muted">Sem dados.</div>';
        egaaMesChartEl.innerHTML = '<div class="muted">Sem dados.</div>';
        return;
      }
      const data = await res.json();
      const porStatus = Array.isArray(data.por_status) ? data.por_status : [];
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
      renderPieChart(egaaStatusChartEl, porStatus, 'Nenhum status para exibir.');
      if (Array.isArray(porMes) && porMes.length) {
        const labels = porMes.map(item => item.mes || '--');
        const values = porMes.map(item => Number(item.total || 0));
        // series supports multiple series; here we use a single series named 'Intervenções'
        renderColumnChart(egaaMesChartEl, {
          labels,
          series: [{ key: 'intervencoes', label: 'Intervenções', values }],
          colors: ['var(--brand)'],
          options: { height: 220 }
        });
      } else {
        egaaMesChartEl.innerHTML = '<div class="muted">Nenhuma evolução mensal para exibir.</div>';
      }
    }

    filtrarBtn.addEventListener('click', () => { loadKPIs(); loadEgaaIndicadores(); });
    dataInicioEl.addEventListener('change', () => { loadKPIs(); });
    dataFimEl.addEventListener('change', () => { loadKPIs(); });
    document.getElementById('refresh').addEventListener('click', () => { loadKPIs(); loadEgaaIndicadores(); });

    loadKPIs(); loadEgaaIndicadores();
  </script>
</body>
</html>
"""

@router.get("/", include_in_schema=False)
def root_redirect() -> RedirectResponse:
    return RedirectResponse(url="/dashboard", status_code=307)


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_route() -> str:
    return dashboard_page().replace("__APP_VERSION__", settings.app_version).replace("__APP_ENV__", settings.app_env)


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
        ("Longa Permanência", "/longa-permanencia", title == "Longa Permanência"),
        ("Desfechos EGAA", "/desfechos", title == "Desfechos EGAA"),
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
    .sidebar {{
      display: flex;
      flex-direction: column;
    }}
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
    /* ── Alternador de visualização ── */
    .view-toggle {{
      display:inline-flex; gap:4px; padding:4px; background:#edf2f7;
      border-radius:10px; border:1px solid var(--panel-border);
    }}
    .view-toggle button {{
      padding:6px 14px; border-radius:8px; border:none; cursor:pointer;
      font-weight:600; font-size:13px; background:transparent; color:var(--muted);
      transition: all .15s;
    }}
    .view-toggle button.active {{ background:#fff; color:var(--brand); box-shadow:0 2px 8px rgba(16,24,40,0.10); }}

    /* ── Grid de leitos ── */
    .leitos-grid {{
      display:grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap:12px; margin-top: 4px;
    }}
    .leito-card {{
      position:relative; background:var(--panel); border-radius:12px;
      border:1px solid var(--panel-border); cursor:pointer;
      padding:14px; transition: all .15s;
      box-shadow:0 4px 12px rgba(16,24,40,0.04);
      overflow:hidden;
    }}
    .leito-card:hover {{
      box-shadow:0 8px 24px rgba(16,24,40,0.12); transform:translateY(-2px);
      border-color:var(--brand);
    }}
    .leito-card .leito-label {{
      font-size:11px; text-transform:uppercase; letter-spacing:.04em;
      color:var(--muted); font-weight:700; margin-bottom:4px;
    }}
    .leito-card .leito-pront {{
      font-size:12px; color:var(--brand); font-weight:700;
    }}
    .leito-card .leito-nome {{
      font-size:14px; font-weight:700; color:var(--text);
      margin:2px 0 6px; overflow:hidden; text-overflow:ellipsis;
      white-space:nowrap;
    }}
    .leito-card .leito-meta {{
      font-size:12px; color:var(--muted); line-height:1.4;
    }}
    .leito-card .leito-dias {{
      font-size:20px; font-weight:800; line-height:1;
    }}
    .leito-card .priority-line {{
      position:absolute; top:0; left:0; right:0; height:4px;
    }}
    .priority-laranja {{ --bar-bg: #F9A825; }}
    .priority-vermelho {{ --bar-bg: #C62828; }}
    .priority-escuro {{ --bar-bg: #7F1D1D; }}
    .priority-laranja .priority-line {{ background: var(--bar-bg); }}
    .priority-vermelho .priority-line {{ background: var(--bar-bg); }}
    .priority-escuro .priority-line {{ background: var(--bar-bg); }}
    .leito-card .leito-badge {{
      display:inline-block; padding:2px 8px; border-radius:999px;
      font-size:10px; font-weight:700; letter-spacing:.02em;
      margin-top:4px;
    }}
    .leito-card .leito-badge.egaa-ativo {{
      background: rgba(0, 167, 157, 0.12); color: var(--secondary);
    }}
    .leito-card .leito-badge.egaa-inativo {{
      background: rgba(107, 114, 128, 0.10); color: var(--muted);
    }}

    /* ── Tooltip ── */
    .leito-card .leito-tooltip {{
      visibility:hidden; opacity:0; transition: opacity .2s;
      position:absolute; bottom:calc(100% + 8px); left:50%; transform:translateX(-50%);
      background:#1F2937; color:#fff; padding:12px 14px; border-radius:10px;
      width:260px; font-size:13px; line-height:1.5; z-index:100;
      box-shadow:0 8px 24px rgba(0,0,0,0.25); pointer-events:none;
      text-align:left;
    }}
    .leito-card:hover .leito-tooltip {{
      visibility:visible; opacity:1;
    }}
    .leito-tooltip::after {{
      content:''; position:absolute; top:100%; left:50%; transform:translateX(-50%);
      border:6px solid transparent; border-top-color:#1F2937;
    }}
    .leito-tooltip strong {{ color:#fff; }}
    .leito-tooltip .tt-muted {{ color:#B0BEC5; font-size:12px; }}

    /* ── Modal ── */
    .modal-backdrop {{
      position:fixed; inset:0; background:rgba(0,0,0,0.45);
      backdrop-filter:blur(4px); z-index:1000; display:none;
      align-items:center; justify-content:center;
    }}
    .modal-backdrop.open {{ display:flex; }}
    .modal-dialog {{
      background:var(--panel); border-radius:16px; width:min(90vw, 860px);
      max-height:90vh; overflow-y:auto; box-shadow:0 24px 64px rgba(16,24,40,0.2);
      animation:modalIn .2s ease-out;
    }}
    @keyframes modalIn {{ from {{ opacity:0; transform:scale(.95) translateY(10px); }} to {{ opacity:1; transform:scale(1) translateY(0); }} }}
    .modal-header {{
      display:flex; align-items:center; justify-content:space-between; gap:12px;
      padding:18px 20px; border-bottom:1px solid #edf2f7; position:sticky; top:0;
      background:var(--panel); border-radius:16px 16px 0 0; z-index:1;
    }}
    .modal-header h2 {{ margin:0; font-size:18px; color:var(--brand-strong); }}
    .modal-close {{
      background:none; border:none; font-size:22px; cursor:pointer; color:var(--muted);
      padding:4px 8px; border-radius:8px;
    }}
    .modal-close:hover {{ background:#edf2f7; color:var(--text); }}
    .modal-body {{ padding:20px; }}
    .modal-loading {{ text-align:center; padding:40px; color:var(--muted); }}
    .sidebar-version {{
      margin-top: auto; padding: 10px 12px; border-radius: 10px;
      background: rgba(0,0,0,0.04); color: var(--muted); font-size: 11px;
      text-align: center; letter-spacing: .02em;
    }}

    @media (max-width: 1100px) {{
      .layout {{ grid-template-columns: 1fr; }}
      .sidebar {{ position: static; height: auto; border-right: none; border-bottom: 1px solid var(--panel-border); }}
      .filters-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .leitos-grid {{ grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); }}
    }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <p class="brand">EGAA</p>
      <p class="brand-subtitle">Administração</p>
      <nav class="nav">
        {nav_html}
      </nav>
      <div class="sidebar-note">
        {subtitle}
      </div>
      <div class="sidebar-version">v{settings.app_version} · {settings.app_env}</div>
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
            <div class="view-toggle" id="viewToggle" style="display:{'flex' if default_min_dias is not None else 'none'}">
              <button type="button" id="viewTableBtn" class="active">📋 Tabela</button>
              <button type="button" id="viewGridBtn">🛏️ Leitos</button>
            </div>
          </div>
          <div class="section-body">
            <div class="leitos-grid" id="leitosGrid" style="display:none;"></div>
            <table aria-live="polite" id="pacientesTable">
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

      </div>
    </main>
  <!-- ── Modal de detalhe do paciente ── -->
  <div class="modal-backdrop" id="modalBackdrop">
    <div class="modal-dialog" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
      <div class="modal-header">
        <h2 id="modalTitle">Carregando paciente...</h2>
        <button type="button" class="modal-close" id="modalClose" aria-label="Fechar">&times;</button>
      </div>
      <div class="modal-body" id="modalBody">
        <div class="modal-loading">Carregando dados do paciente...</div>
      </div>
    </div>
  </div>

  <script>
    // ── Variáveis globais ──
    const API_PREFIX = '/api';
    const IS_LONGA = {str(default_min_dias is not None).lower()};
    let pagina = 1;
    let tamanhoPagina = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10;
    let viewAtual = 'tabela'; // 'tabela' | 'leitos'
    let ultimosItems = [];

    // ── Alternância de visualização ──
    const viewToggle = document.getElementById('viewToggle');
    const viewTableBtn = document.getElementById('viewTableBtn');
    const viewGridBtn = document.getElementById('viewGridBtn');
    const pacientesTable = document.getElementById('pacientesTable');
    const leitosGrid = document.getElementById('leitosGrid');

    if (viewTableBtn && viewGridBtn) {{
      viewTableBtn.addEventListener('click', () => {{
        viewAtual = 'tabela';
        viewTableBtn.classList.add('active');
        viewGridBtn.classList.remove('active');
        pacientesTable.style.display = '';
        leitosGrid.style.display = 'none';
      }});
      viewGridBtn.addEventListener('click', () => {{
        viewAtual = 'leitos';
        viewGridBtn.classList.add('active');
        viewTableBtn.classList.remove('active');
        pacientesTable.style.display = 'none';
        leitosGrid.style.display = '';
        renderLeitosGrid(ultimosItems);
      }});
    }}

    // ── Renderizar grid de leitos ──
    function renderLeitosGrid(items) {{
      if (!items.length) {{
        leitosGrid.innerHTML = '<div class="muted" style="grid-column:1/-1;text-align:center;padding:32px;">Nenhum paciente encontrado com os filtros atuais.</div>';
        return;
      }}
      leitosGrid.innerHTML = items.map(item => {{
        const dias = Number(item.dias_internacao || 0);
        const idade = Number(item.idade_anos || 0);
        const egaaTotal = Number(item.egaa_total_atuacoes || 0);
        let prioridadeClass = 'priority-laranja';
        let badgeLabel = '15-29 dias';
        if (dias >= 30 && idade >= 60) {{ prioridadeClass = 'priority-escuro'; badgeLabel = '30+ dias · 60+ anos'; }}
        else if (dias >= 30) {{ prioridadeClass = 'priority-vermelho'; badgeLabel = '30+ dias'; }}
        const egaaBadge = egaaTotal > 0
          ? `<span class="leito-badge egaa-ativo">${{egaaTotal}} atuações</span>`
          : `<span class="leito-badge egaa-inativo">Sem EGAA</span>`;
        const pront = escapeHtml(item.prontuario || '');
        const nome = escapeHtml(item.nome_paciente || '');
        const unidade = escapeHtml(item.unidade || '--');
        const leito = escapeHtml(item.leito || '--');
        const especialidade = escapeHtml(item.especialidade || '--');
        const cid = escapeHtml(item.cid_internacao_descricao || '');
        const ultAtuacao = item.egaa_ultima_atuacao
          ? new Intl.DateTimeFormat('pt-BR').format(new Date(item.egaa_ultima_atuacao)) : '--';
        return `
          <div class="leito-card ${{prioridadeClass}}" data-prontuario="${{pront}}"
               onclick="abrirModal('${{pront}}')">
            <div class="priority-line"></div>
            <div class="leito-label">Leito ${{leito}}</div>
            <div class="leito-pront">#${{pront}}</div>
            <div class="leito-nome" title="${{nome}}">${{nome}}</div>
            <div class="leito-meta"><span class="leito-dias">${{dias}}</span> dias · ${{idade}}a</div>
            <div class="leito-meta">${{unidade}} · ${{especialidade}}</div>
            ${{egaaBadge}}

            <!-- Tooltip -->
            <div class="leito-tooltip">
              <strong>${{nome}}</strong><br>
              <span class="tt-muted">#${{pront}} · ${{idade}} anos · ${{dias}} dias internado</span><br>
              <span class="tt-muted">${{unidade}} · Leito ${{leito}} · ${{especialidade}}</span>
              <hr style="border:none;border-top:1px solid rgba(255,255,255,0.15);margin:8px 0;">
              <span class="tt-muted">CID: ${{cid || '--'}}</span><br>
              <span class="tt-muted">EGAA: ${{egaaTotal}} atuação(ões) · Última: ${{ultAtuacao}}</span>
              <span class="tt-muted" style="display:block;margin-top:6px;font-style:italic;">Clique para detalhes completos</span>
            </div>
          </div>`;
      }}).join('');
    }}

    // ── Modal ──
    const modalBackdrop = document.getElementById('modalBackdrop');
    const modalBody = document.getElementById('modalBody');
    const modalTitle = document.getElementById('modalTitle');
    const modalClose = document.getElementById('modalClose');

    // Cache de dados do modal para re-render
    let modalProntuario = '';
    let modalPacienteNome = '';
    let modalTipos = [];
    let modalCodigosPendencia = [];

    async function abrirModal(prontuario) {{
      modalProntuario = prontuario;
      modalBackdrop.classList.add('open');
      modalTitle.textContent = 'Carregando paciente...';
      modalBody.innerHTML = '<div class="modal-loading">Carregando dados do paciente...</div>';

      try {{
        // Carrega dados do paciente, tipos e códigos em paralelo
        const [pacRes, tiposRes, codigosRes] = await Promise.all([
          fetch(`${{API_PREFIX}}/censo/paciente/${{encodeURIComponent(prontuario)}}`),
          fetch(`${{API_PREFIX}}/egaa/tipos-intervencao`),
          fetch(`${{API_PREFIX}}/egaa/pendencia/codigos`)
        ]);

        const paciente = pacRes.ok ? await pacRes.json() : {{ nome_paciente: '--', prontuario: prontuario }};
        modalPacienteNome = paciente.nome_paciente || '--';
        modalTipos = tiposRes.ok ? (await tiposRes.json()) || [] : [];
        modalCodigosPendencia = codigosRes.ok ? (await codigosRes.json()) || [] : [];

        modalTitle.textContent = (paciente.nome_paciente || 'Paciente') + ' #' + (paciente.prontuario || '');

        // Renderiza layout do modal
        modalBody.innerHTML = `
          <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;">
            <!-- Coluna 1: Ações EGAA -->
            <div>
              <div class="section" style="margin-top:0;">
                <div class="section-header"><h2 style="font-size:14px;">📝 Nova atuação</h2></div>
                <div class="section-body" style="padding:12px 14px;">
                  <div class="field" style="margin-bottom:10px;">
                    <label>Tipo de intervenção</label>
                    <select id="modalTipoIntervencao" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;">
                      <option value="">Selecione...</option>
                      ${{modalTipos.filter(t=>t.ativo).map(t => `<option value="${{t.id}}">${{escapeHtml(t.nome)}}</option>`).join('')}}
                    </select>
                  </div>
                  <div class="field" style="margin-bottom:10px;">
                    <label>Descrição</label>
                    <textarea id="modalDescricao" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;min-height:80px;font:inherit;resize:vertical;"></textarea>
                  </div>
                  <div class="row" style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:10px;">
                    <div class="field" style="margin-bottom:0;">
                      <label>Responsável</label>
                      <input id="modalResponsavel" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;box-sizing:border-box;" placeholder="ex: ENF EDUARDO" />
                    </div>
                    <div class="field" style="margin-bottom:0;">
                      <label>Data da atuação</label>
                      <input id="modalDataAtuacao" type="date" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;box-sizing:border-box;" />
                    </div>
                  </div>
                  <div class="field" style="margin-bottom:10px;">
                    <label>Status</label>
                    <select id="modalStatusIntervencao" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;">
                      <option value="aberta">Aberta</option>
                      <option value="em_andamento">Em andamento</option>
                      <option value="concluida">Concluída</option>
                      <option value="cancelada">Cancelada</option>
                    </select>
                  </div>
                  <button type="button" id="modalSalvarAtuacao" style="width:100%;">Adicionar atuação</button>
                  <span id="modalAtuacaoStatus" class="muted" style="font-size:13px;display:block;margin-top:6px;"></span>
                </div>
              </div>
              <div class="section" style="margin-top:10px;">
                <div class="section-header"><h2 style="font-size:14px;">📄 Evolução do paciente</h2></div>
                <div class="section-body" style="padding:12px 14px;">
                  <textarea id="modalEvolucao" style="width:100%;min-height:80px;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;font:inherit;resize:vertical;">${{escapeHtml(paciente.evolucao || '')}}</textarea>
                  <div style="display:flex;gap:8px;margin-top:8px;">
                    <button type="button" id="modalSalvarEvolucao" style="flex:1;">Salvar evolução</button>
                    <span id="modalEvolucaoStatus" class="muted" style="font-size:13px;align-self:center;"></span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Coluna 2: Timeline + Pendências -->
            <div>
              <div class="section" style="margin-top:0;">
                <div class="section-header">
                  <h2 style="font-size:14px;">📋 Intervenções</h2>
                  <span id="modalIntervCount" class="muted" style="font-size:12px;"></span>
                </div>
                <div class="section-body" style="padding:8px 14px 12px;max-height:320px;overflow-y:auto;" id="modalTimeline">
                  <div class="muted">Carregando intervenções...</div>
                </div>
              </div>
              <div class="section" style="margin-top:10px;">
                <div class="section-header">
                  <h2 style="font-size:14px;">🚧 Pendências para alta</h2>
                  <span id="modalPendCount" class="muted" style="font-size:12px;"></span>
                </div>
                <div class="section-body" style="padding:8px 14px 12px;" id="modalPendencias">
                  <div class="muted">Carregando pendências...</div>
                  <div style="display:flex;gap:6px;margin-top:10px;">
                    <select id="modalNovaPendencia" style="flex:1;padding:8px 10px;border-radius:8px;border:1px solid #cfd8e3;">
                      <option value="">Adicionar pendência...</option>
                      ${{modalCodigosPendencia.map(c => `<option value="${{c.codigo}}">${{escapeHtml(c.rotulo || c.codigo)}}</option>`).join('')}}
                    </select>
                    <button type="button" id="modalAddPendencia" style="padding:8px 12px;">+</button>
                  </div>
                  <span id="modalPendenciaStatus" class="muted" style="font-size:13px;display:block;margin-top:4px;"></span>
                </div>
              </div>
            </div>
          </div>
          <div style="margin-top:14px;text-align:center;">
            <a href="/paciente/${{encodeURIComponent(paciente.prontuario)}}" class="pill-link" style="display:inline-flex;">Abrir página completa do paciente →</a>
          </div>`;

        // Carrega timeline e pendências
        carregarTimeline(prontuario);
        carregarPendencias(prontuario);

        // Eventos do modal
        document.getElementById('modalSalvarAtuacao').addEventListener('click', () => salvarAtuacao(prontuario));
        document.getElementById('modalSalvarEvolucao').addEventListener('click', () => salvarEvolucaoModal(prontuario));
        document.getElementById('modalAddPendencia').addEventListener('click', () => adicionarPendencia(prontuario));

      }} catch (err) {{
        modalTitle.textContent = 'Erro ao carregar';
        modalBody.innerHTML = '<div class="modal-loading" style="color:var(--error);">Não foi possível carregar os dados do paciente.</div>';
      }}
    }}

    async function carregarTimeline(prontuario) {{
      const el = document.getElementById('modalTimeline');
      const countEl = document.getElementById('modalIntervCount');
      try {{
        const res = await fetch(`${{API_PREFIX}}/egaa/intervencoes?prontuario=${{encodeURIComponent(prontuario)}}`);
        const items = res.ok ? (await res.json()) || [] : [];
        countEl.textContent = items.length + ' registro(s)';
        el.innerHTML = items.length
          ? items.map(item => {{
              const tipoNome = escapeHtml(modalTipos.find(t=>t.id===item.tipo_intervencao_id)?.nome || '--');
              const dataAtu = item.data_atuacao ? fmtDate(item.data_atuacao) : '--';
              const statusClass = item.status === 'concluida' ? 'badge-success' : item.status === 'em_andamento' ? 'badge-warning' : 'badge-info';
              const statusLabel = item.status === 'concluida' ? 'Concluída' : item.status === 'em_andamento' ? 'Em andamento' : 'Aberta';
              return `
                <div style="padding:10px 12px;border:1px solid var(--panel-border);border-radius:10px;margin-bottom:8px;background:#fff;">
                  <div style="display:flex;align-items:start;justify-content:space-between;gap:8px;">
                    <div>
                      <span class="badge ${{statusClass}}" style="margin-bottom:4px;">${{statusLabel}}</span>
                      <div style="font-weight:700;color:var(--brand-strong);font-size:14px;">${{tipoNome}}</div>
                      <div class="muted" style="font-size:12px;margin-top:2px;">${{escapeHtml(item.descricao || '')}}</div>
                      <div class="muted" style="font-size:12px;margin-top:4px;">${{dataAtu}} · ${{escapeHtml(item.usuario_responsavel || '--')}}</div>
                    </div>
                  </div>
                </div>`;
            }}).join('')
          : '<div class="muted" style="text-align:center;padding:16px;">Nenhuma intervenção registrada.</div>';
      }} catch {{
        el.innerHTML = '<div class="muted" style="text-align:center;padding:16px;">Erro ao carregar intervenções.</div>';
      }}
    }}

    async function carregarPendencias(prontuario) {{
      const el = document.getElementById('modalPendencias');
      const countEl = document.getElementById('modalPendCount');
      try {{
        const res = await fetch(`${{API_PREFIX}}/egaa/pendencia/${{encodeURIComponent(prontuario)}}`);
        const items = res.ok ? (await res.json()) || [] : [];
        const pendentes = items.filter(i => !i.resolvida);
        const resolvidas = items.filter(i => i.resolvida);
        countEl.textContent = pendentes.length + ' pendente(s)';

        let html = '';
        if (items.length) {{
          html += pendentes.map(function(p) {{
            return '<div style="display:flex;align-items:center;justify-content:space-between;padding:6px 0;border-bottom:1px solid #edf2f7;">' +
              '<span style="font-size:13px;">⬜ ' + escapeHtml(p.codigo || '--') + '</span>' +
              '<button class="resolver-pendencia" data-id="' + p.id + '" data-pront="' + prontuario + '" style="padding:3px 8px;font-size:11px;background:#EEF5FA;color:var(--brand);border:1px solid var(--panel-border);border-radius:6px;cursor:pointer;">Resolvido</button>' +
              '</div>';
          }}).join('');

          if (resolvidas.length) {{
            html += '<div style="margin-top:6px;font-size:12px;color:var(--muted);">✅ ' + resolvidas.length + ' resolvida(s)</div>';
            html += resolvidas.map(function(p) {{
              return '<div style="display:flex;align-items:center;padding:4px 0;font-size:12px;color:var(--muted);">' +
                '<span style="text-decoration:line-through;">☑ ' + escapeHtml(p.codigo || '--') + '</span></div>';
            }}).join('');
          }}
        }} else {{
          html += '<div class="muted" style="text-align:center;padding:16px;">Nenhuma pendência registrada.</div>';
        }}

        html += '<div style="display:flex;gap:6px;margin-top:10px;">' +
          '<select id="modalNovaPendencia" style="flex:1;padding:8px 10px;border-radius:8px;border:1px solid #cfd8e3;">' +
          '<option value="">Adicionar pendência...</option>';
        for (var ci = 0; ci < modalCodigosPendencia.length; ci++) {{
          var c = modalCodigosPendencia[ci];
          html += '<option value="' + c.codigo + '">' + escapeHtml(c.rotulo || c.codigo) + '</option>';
        }}
        html += '</select>' +
          '<button type="button" id="modalAddPendencia" style="padding:8px 12px;">+</button>' +
          '</div>' +
          '<span id="modalPendenciaStatus" class="muted" style="font-size:13px;display:block;margin-top:4px;"></span>';

        el.innerHTML = html;

        document.getElementById('modalAddPendencia')?.addEventListener('click', function() {{ adicionarPendencia(prontuario); }});
        el.querySelectorAll('.resolver-pendencia').forEach(function(btn) {{
          btn.addEventListener('click', function() {{ resolverPendencia(btn.getAttribute('data-id'), btn.getAttribute('data-pront')); }});
        }});
      }} catch {{
        countEl.textContent = '--';
        // Keep existing elements
      }}
    }}

    async function salvarAtuacao(prontuario) {{
      const tipoId = document.getElementById('modalTipoIntervencao').value;
      const descricao = document.getElementById('modalDescricao').value.trim();
      const responsavel = document.getElementById('modalResponsavel').value.trim();
      const dataAtuacao = document.getElementById('modalDataAtuacao').value || new Date().toISOString().split('T')[0];
      const status = document.getElementById('modalStatusIntervencao').value;
      const statusEl = document.getElementById('modalAtuacaoStatus');
      if (!tipoId) {{ statusEl.textContent = 'Selecione um tipo de intervenção.'; return; }}
      if (!descricao) {{ statusEl.textContent = 'Descreva a intervenção.'; return; }}
      statusEl.textContent = 'Salvando...';
      try {{
        const res = await fetch(`${{API_PREFIX}}/egaa/intervencoes`, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ prontuario, tipo_intervencao_id: parseInt(tipoId), titulo: modalTipos.find(t=>t.id==tipoId)?.nome || '', descricao, status, usuario_responsavel: responsavel || null, data_atuacao: dataAtuacao }})
        }});
        if (!res.ok) throw new Error('Erro ' + res.status);
        statusEl.textContent = '✅ Atuação salva!';
        document.getElementById('modalDescricao').value = '';
        document.getElementById('modalTipoIntervencao').value = '';
        document.getElementById('modalResponsavel').value = '';
        document.getElementById('modalDataAtuacao').value = '';
        document.getElementById('modalStatusIntervencao').value = 'aberta';
        carregarTimeline(prontuario);
      }} catch {{ statusEl.textContent = '❌ Erro ao salvar atuação.'; }}
    }}

    async function salvarEvolucaoModal(prontuario) {{
      const text = document.getElementById('modalEvolucao').value;
      const statusEl = document.getElementById('modalEvolucaoStatus');
      statusEl.textContent = 'Salvando...';
      try {{
        const res = await fetch(`${{API_PREFIX}}/censo/paciente/${{encodeURIComponent(prontuario)}}/evolucao`, {{
          method: 'PUT',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ evolucao: text }})
        }});
        if (!res.ok) throw new Error('Erro ' + res.status);
        statusEl.textContent = '✅ Evolução salva!';
        setTimeout(() => {{ statusEl.textContent = ''; }}, 3000);
      }} catch {{ statusEl.textContent = '❌ Erro ao salvar evolução.'; }}
    }}

    async function adicionarPendencia(prontuario) {{
      const select = document.getElementById('modalNovaPendencia');
      const codigo = select?.value;
      const statusEl = document.getElementById('modalPendenciaStatus');
      if (!codigo) {{ statusEl.textContent = 'Selecione uma pendência.'; return; }}
      statusEl.textContent = 'Adicionando...';
      try {{
        const res = await fetch(`${{API_PREFIX}}/egaa/pendencia/${{encodeURIComponent(prontuario)}}`, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ codigo }})
        }});
        if (!res.ok) throw new Error('Erro ' + res.status);
        statusEl.textContent = '✅ Pendência adicionada!';
        select.value = '';
        carregarPendencias(prontuario);
      }} catch {{ statusEl.textContent = '❌ Erro ao adicionar pendência.'; }}
    }}

    async function resolverPendencia(pendenciaId, prontuario) {{
      try {{
        const res = await fetch(`${{API_PREFIX}}/egaa/pendencia/${{encodeURIComponent(prontuario)}}/${{pendenciaId}}`, {{
          method: 'PUT',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ resolvida: true }})
        }});
        if (!res.ok) throw new Error('Erro ' + res.status);
        carregarPendencias(prontuario);
      }} catch {{ }}
    }}

    function fecharModal() {{
      modalBackdrop.classList.remove('open');
    }}

    if (modalClose) modalClose.addEventListener('click', fecharModal);
    if (modalBackdrop) modalBackdrop.addEventListener('click', (e) => {{
      if (e.target === modalBackdrop) fecharModal();
    }});
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') fecharModal();
    }});

    // ── Utilitários ──
    function escapeHtml(text) {{
      if (!text) return '';
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }}

    function fmtDate(value) {{
      if (!value) return '--';
      try {{
        return new Intl.DateTimeFormat('pt-BR').format(new Date(value));
      }} catch {{
        return String(value);
      }}
    }}

    // ── Função priorityMeta (já existia, mantida) ──
    function priorityMeta(item) {{
      const dias = Number(item.dias_internacao || 0);
      const idade = Number(item.idade_anos || 0);
      if (dias >= 30 && idade >= 60) return {{ label: 'Prioridade máxima', css: 'row-critical' }};
      if (dias >= 30) return {{ label: 'Longa permanência', css: 'row-warning' }};
      if (idade >= 60) return {{ label: '60+ anos', css: 'row-info' }};
      return {{ label: 'Acompanhamento', css: '' }};
    }}

    // ── Load pacientes (adaptado) ──
    async function loadPacientes() {{
      const params = new URLSearchParams();
      params.set('page', pagina);
      params.set('page_size', tamanhoPagina);
      const prontuarioEl = document.getElementById('prontuario');
      const nomeEl = document.getElementById('nome');
      const especialidadeEl = document.getElementById('especialidade');
      const unidadeEl = document.getElementById('unidade');
      const dataInicioEl = document.getElementById('dataInicio');
      const dataFimEl = document.getElementById('dataFim');
      const minDiasEl = document.getElementById('minDias');
      const prioridadeEl = document.getElementById('prioridade');
      if (prontuarioEl && prontuarioEl.value) params.set('prontuario', prontuarioEl.value);
      if (nomeEl && nomeEl.value) params.set('nome', nomeEl.value);
      if (especialidadeEl && especialidadeEl.value) params.set('especialidade', especialidadeEl.value);
      if (unidadeEl && unidadeEl.value) params.set('unidade', unidadeEl.value);
      if (dataInicioEl && dataInicioEl.value) params.set('data_inicio', dataInicioEl.value);
      if (dataFimEl && dataFimEl.value) params.set('data_fim', dataFimEl.value);
      if (minDiasEl && minDiasEl.value) params.set('min_dias', minDiasEl.value);
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
        document.getElementById('rows').innerHTML = '<tr><td colspan="' + (IS_LONGA ? '7' : '6') + '">Erro ao obter registros (' + res.status + ')</td></tr>';
        return;
      }}
      const data = await res.json();
      const items = Array.isArray(data.items) ? data.items : [];
      ultimosItems = items;

      // Atualiza KPIs
      document.getElementById('kpis').innerHTML = IS_LONGA
        ? renderLongaKPIs(data)
        : renderGeralKPIs(data);

      // Renderiza tabela
      renderTabela(items, data);

      // Se estiver na visualização de leitos, renderiza grid
      if (viewAtual === 'leitos') renderLeitosGrid(items);

      // Paginação
      document.getElementById('pageInfo').textContent = 'Página ' + data.page + ' de ' + (Math.ceil(data.total / data.page_size) || 1);
      document.getElementById('prev').disabled = data.page <= 1;
      document.getElementById('next').disabled = data.page * data.page_size >= data.total;
    }}

    function renderLongaKPIs(data) {{
      const items = data.items || [];
      const diasMaximos = items.reduce((max, item) => Math.max(max, Number(item.dias_internacao || 0)), 0);
      const mediaDias = items.length ? Math.round(items.reduce((sum, item) => sum + Number(item.dias_internacao || 0), 0) / items.length) : 0;
      const unidadeLider = items.reduce((acc, item) => {{ acc[item.unidade || '--'] = (acc[item.unidade || '--'] || 0) + 1; return acc; }}, {{}});
      const unidadeLiderNome = Object.entries(unidadeLider).sort((a, b) => b[1] - a[1])[0]?.[0] || '--';
      const unidadeLiderTotal = Object.entries(unidadeLider).sort((a, b) => b[1] - a[1])[0]?.[1] || 0;
      return `
        <div class="card"><span class="badge badge-info">Lista atual</span><strong>Total encontrado</strong><div class="kpi-value">${{data.total}}</div></div>
        <div class="card"><span class="badge badge-warning">Máximo</span><strong>Maior permanência</strong><div class="kpi-value">${{diasMaximos}} dias</div></div>
        <div class="card"><span class="badge badge-secondary">Média</span><strong>Média de dias</strong><div class="kpi-value">${{mediaDias}} dias</div></div>
        <div class="card"><span class="badge badge-info">Concentração</span><strong>${{unidadeLiderNome}}</strong><div class="kpi-value">${{unidadeLiderTotal}} pacientes</div></div>
      `;
    }}

    function renderGeralKPIs(data) {{
      return `
        <div class="card"><span class="badge {badge_class}">{badge_text}</span><strong>Total encontrado</strong><div class="kpi-value">${{data.total}}</div></div>
        <div class="card"><span class="badge badge-info">Página atual</span><strong>Paginação</strong><div class="kpi-value">${{data.page}}</div></div>
        <div class="card"><span class="badge badge-secondary">Lote visual</span><strong>Itens por página</strong><div class="kpi-value">${{data.page_size}}</div></div>
      `;
    }}

    function renderTabela(items, data) {{
      const rowsEl = document.getElementById('rows');
      const isLonga = IS_LONGA;
      rowsEl.innerHTML = items.length
        ? items.map(it => {{
            const meta = priorityMeta(it);
            const egaaTotal = Number(it.egaa_total_atuacoes || 0);
            const egaaBadgeLabel = egaaTotal > 0 ? `${{egaaTotal}} atuação(ões)` : 'Sem EGAA';
            const egaaBadgeDetail = egaaTotal > 0
              ? 'Última: ' + fmtDate(it.egaa_ultima_atuacao)
              : 'Ainda sem registros do EGAA';
            return '<tr class="' + meta.css + '">' +
              '<td><div class="badges"><span class="badge badge-info">' + meta.label + '</span></div><div style="margin-top:6px"><a href="/paciente/' + encodeURIComponent(it.prontuario) + '">' + escapeHtml(it.prontuario) + '</a></div></td>' +
              '<td>' + escapeHtml(it.nome_paciente||'') + '</td>' +
              '<td>' + (it.idade_anos??'') + '</td>' +
              '<td>' + (it.dias_internacao??'') + '</td>' +
              '<td>' + escapeHtml(it.especialidade) + '</td>' +
              '<td>' + escapeHtml(it.unidade||'') + '</td>' +
              (isLonga ? '<td><div class="badges"><span class="badge badge-secondary">' + egaaBadgeLabel + '</span></div><div class="muted" style="margin-top:6px">' + egaaBadgeDetail + '</div></td>' : '') +
              '</tr>';
          }}).join('')
        : '<tr><td colspan="' + (isLonga ? '7' : '6') + '" class="empty">Nenhum registro encontrado com os filtros atuais.</td></tr>';
    }}

    // ── Event listeners ──
    document.getElementById('filtrar').addEventListener('click', () => {{ pagina = 1; tamanhoPagina = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10; loadPacientes(); }});
    document.getElementById('prev').addEventListener('click', () => {{ if (pagina > 1) pagina--; loadPacientes(); }});
    document.getElementById('next').addEventListener('click', () => {{ pagina++; loadPacientes(); }});
    document.getElementById('pageSizeSelect').addEventListener('change', () => {{ pagina = 1; tamanhoPagina = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10; loadPacientes(); }});
    document.getElementById('dataInicio').addEventListener('change', () => {{ pagina = 1; loadPacientes(); }});
    document.getElementById('dataFim').addEventListener('change', () => {{ pagina = 1; loadPacientes(); }});
    document.getElementById('minDias').addEventListener('change', () => {{ pagina = 1; loadPacientes(); }});
    const prioridadeEl = document.getElementById('prioridade');
    if (prioridadeEl) prioridadeEl.addEventListener('change', () => {{ pagina = 1; loadPacientes(); }});
    document.getElementById('refresh').addEventListener('click', () => {{ loadPacientes(); }});

    // ── Inicializa ──
    loadPacientes();
  </script>
</body>
</html>
"""


@router.get("/pacientes", response_class=HTMLResponse)
def pacientes_route() -> RedirectResponse:
  return RedirectResponse(url="/dashboard", status_code=307)


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
    .sidebar-version {{
      margin-top: auto; padding: 10px 12px; border-radius: 10px;
      background: rgba(0,0,0,0.04); color: var(--muted); font-size: 11px;
      text-align: center; letter-spacing: .02em;
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
        <a class="primary" href="/longa-permanencia">Longa Permanência</a>
        <a href="/desfechos">Desfechos EGAA</a>
        <a href="/configuracoes">Configurações</a>
      </nav>
      <div class="sidebar-version">v{settings.app_version} · {settings.app_env}</div>
    </aside>
    <main class="main">
      <div class="shell">
        <div class="header">
          <div>
            <h1 id="titulo">Paciente {prontuario}</h1>
            <p class="subtitle" id="subtitulo">Carregando informações do paciente...</p>
          </div>
          <div class="actions">
            <div style="display:flex;gap:8px;align-items:center;margin-right:8px;">
              <input type="text" id="quickSearchPaciente" placeholder="Outro prontuário..."
                style="padding:8px 12px;border:1px solid var(--panel-border);border-radius:999px;font-size:13px;width:160px;"
                onkeydown="if(event.key==='Enter'){{const v=this.value.trim();if(v)window.location.href='/paciente/'+encodeURIComponent(v)}}" />
              <a class="pill-link" href="/desfechos" style="padding:8px 14px;">Desfechos</a>
            </div>
            <a class="pill-link" href="/dashboard">Voltar</a>
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
                <h2>Desfecho</h2>
                <p>Registro de alta ou óbito do paciente.</p>
              </div>
            </div>
            <div class="section-body">
              <div id="desfechoInfo" class="muted">Carregando...</div>
              <div id="desfechoActions" class="actions" style="display:none;">
                <button type="button" id="registrarDesfecho" class="secondary">Registrar desfecho</button>
              </div>
            </div>
          </section>

          <section class="section">
            <div class="section-header">
              <div>
                <h2>Evolução do paciente</h2>
                <p>Diário do EGAA — descreva a evolução clínica e social.</p>
              </div>
            </div>
            <div class="section-body">
              <textarea id="evolucao" style="width:100%;min-height:140px;padding:12px;border-radius:10px;border:1px solid #cfd8e3;box-sizing:border-box;background:#fff;font:inherit;resize:vertical;" placeholder='Descreva a evolução do paciente, incluindo data e profissional.&#10;&#10;Ex:&#10;ENF: 21/01/2026 - Enf Eduardo: Paciente...&#10;SESO: 25/02/2026: Abordagem social...'></textarea>
              <div class="actions">
                <button type="button" id="salvarEvolucao">Salvar evolução</button>
                <span id="evolucaoStatus" class="muted" style="font-size:13px;"></span>
              </div>
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
                <h2>Pendências para alta</h2>
                <p>Adicione ou remova pendências — itens resolvidos permanecem marcados no histórico.</p>
              </div>
            </div>
            <div class="section-body">
              <div class="field" style="margin-bottom:12px;">
                <label for="pendenciaSelect">Adicionar pendência</label>
                <div style="display:flex;gap:8px;">
                  <select id="pendenciaSelect" style="flex:1;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;">
                    <option value="">Selecione...</option>
                  </select>
                  <button type="button" id="addPendencia" class="secondary" style="white-space:nowrap;">Adicionar</button>
                </div>
              </div>
              <div id="pendenciaList" style="display:flex;flex-wrap:wrap;gap:8px;min-height:40px;">
                <span class="muted">Carregando pendências...</span>
              </div>
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
    let pacienteData = null;
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

      // Detectar se paciente ja teve alta/obito
      const temAlta = data.desfecho_tipo || data.data_alta || data.data_obito;
      const labelDesfecho = data.desfecho_tipo === 'obito' ? 'Obito' : (data.desfecho_tipo === 'alta' ? 'Alta' : null);
      const dataDesfecho = data.data_obito || data.data_alta;

      // Subtitle
      let subtitulo = data.nome_paciente || 'Paciente';
      if (temAlta) {{
        subtitulo += ' - ' + (labelDesfecho || 'Alta') + ' em ' + fmtDate(dataDesfecho);
      }} else {{
        subtitulo += ' - ' + (data.especialidade || '--');
      }}
      subtituloEl.textContent = subtitulo;

      // KPIs
      let labelKpi = temAlta ? 'Desfecho' : 'Dias';
      let valorKpi = temAlta ? fmtDate(dataDesfecho) : (data.dias_internacao ?? '--');
      kpisEl.innerHTML = `
        <div class="card"><strong>Prontuario</strong><div class="kpi-value">${{data.prontuario || '--'}}</div></div>
        <div class="card"><strong>${{labelKpi}}</strong><div class="kpi-value">${{valorKpi}}</div></div>
        <div class="card"><strong>Idade</strong><div class="kpi-value">${{data.idade_anos ?? '--'}}</div></div>
        <div class="card"><strong>Unidade</strong><div class="kpi-value" style="font-size:18px; line-height:1.3">${{data.unidade || '--'}}</div></div>
      `;

      // Resumo
      let resumoHtml = `
        <div><strong>Nome:</strong> ${{data.nome_paciente || '--'}}</div>
        <div><strong>Especialidade:</strong> ${{data.especialidade || '--'}}</div>
        <div><strong>Unidade:</strong> ${{data.unidade || '--'}}</div>
        <div><strong>Enfermaria:</strong> ${{data.enfermaria || '--'}}</div>
        <div><strong>Leito:</strong> ${{data.leito || '--'}}</div>
        <div><strong>CID:</strong> ${{data.cid_internacao_codigo || '--'}} ${{data.cid_internacao_descricao ? '- ' + data.cid_internacao_descricao : ''}}</div>
        <div><strong>Internacao:</strong> ${{fmtDate(data.data_internacao)}}</div>
      `;
      if (data.data_alta) resumoHtml += '<div><strong>Data da Alta:</strong> ' + fmtDate(data.data_alta) + '</div>';
      if (data.data_obito) resumoHtml += '<div><strong>Data do Obito:</strong> ' + fmtDate(data.data_obito) + '</div>';
      if (data.tipo_alta) resumoHtml += '<div><strong>Tipo de Alta:</strong> ' + data.tipo_alta + '</div>';
      resumoEl.innerHTML = resumoHtml;
      pacienteData = data;
      const evolucaoEl = document.getElementById('evolucao');
      if (evolucaoEl) evolucaoEl.value = data.evolucao || '';
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
        const updatedText = item.updated_at ? fmtDate(item.updated_at) : (item.created_at ? fmtDate(item.created_at) : '--');
        return `
        <div class="timeline-item" data-id="${{item.id}}">
          <div style="display:flex;align-items:start;justify-content:space-between;gap:8px;">
            <div style="flex:1;">
              <div class="badge badge-info">${{escapeHtml(item.status || 'sem status')}}</div>
              <div class="timeline-title">${{escapeHtml(item.titulo || '--')}}</div>
              <div class="timeline-meta">Tipo: ${{tipoNome}} · Atuação: ${{dataAtuacao}} · Responsável: ${{escapeHtml(item.usuario_responsavel || '--')}}</div>
              <div class="timeline-meta">${{escapeHtml(item.descricao || '')}}</div>
              <div class="timeline-meta">Atualizado em ${{updatedText}}</div>
            </div>
            <div style="display:flex;flex-direction:column;gap:4px;flex-shrink:0;">
              <button type="button" class="edit-intervencao" data-id="${{item.id}}" style="padding:4px 8px;font-size:12px;background:#EEF5FA;color:var(--brand);border:1px solid var(--panel-border);border-radius:6px;cursor:pointer;">✏️ Editar</button>
              <button type="button" class="delete-intervencao" data-id="${{item.id}}" style="padding:4px 8px;font-size:12px;background:#FDECEC;color:var(--error);border:1px solid rgba(198,40,40,0.16);border-radius:6px;cursor:pointer;">🗑️ Excluir</button>
            </div>
          </div>
          <div class="edit-form" id="edit-form-${{item.id}}" style="display:none;margin-top:12px;padding-top:12px;border-top:1px solid #edf2f7;">
            <div class="field">
              <label>Tipo de intervenção</label>
              <select class="edit-tipo" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;">
                <option value="">Selecione...</option>
                ${{tiposOptions.map(t => `<option value="${{t.id}}" ${{t.id === item.tipo_intervencao_id ? 'selected' : ''}}>${{escapeHtml(t.nome)}}</option>`).join('')}}
              </select>
            </div>
            <div class="field">
              <label>Descrição</label>
              <textarea class="edit-descricao" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;min-height:60px;font:inherit;resize:vertical;">${{escapeHtml(item.descricao || '')}}</textarea>
            </div>
            <div class="row" style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
              <div class="field">
                <label>Status</label>
                <select class="edit-status" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;">
                  <option value="aberta" ${{item.status === 'aberta' ? 'selected' : ''}}>Aberta</option>
                  <option value="em_andamento" ${{item.status === 'em_andamento' ? 'selected' : ''}}>Em andamento</option>
                  <option value="concluida" ${{item.status === 'concluida' ? 'selected' : ''}}>Concluída</option>
                  <option value="cancelada" ${{item.status === 'cancelada' ? 'selected' : ''}}>Cancelada</option>
                </select>
              </div>
              <div class="field">
                <label>Responsável</label>
                <input class="edit-responsavel" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;" value="${{escapeHtml(item.usuario_responsavel || '')}}" />
              </div>
            </div>
            <div class="row" style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
              <div class="field">
                <label>Data da atuação</label>
                <input class="edit-data-atuacao" type="date" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;" value="${{item.data_atuacao || ''}}" />
              </div>
              <div class="field">
                <label>Observação</label>
                <input class="edit-observacao" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;" value="${{escapeHtml(item.observacao || '')}}" />
              </div>
            </div>
            <div class="actions" style="margin-top:8px;">
              <button type="button" class="save-edit" data-id="${{item.id}}" style="padding:8px 12px;border-radius:8px;border:none;background:var(--brand);color:#fff;cursor:pointer;font-weight:600;">Salvar</button>
              <button type="button" class="cancel-edit" data-id="${{item.id}}" style="padding:8px 12px;border-radius:8px;border:1px solid var(--panel-border);background:#EEF5FA;color:var(--brand);cursor:pointer;font-weight:600;">Cancelar</button>
              <span class="edit-status-msg" style="font-size:13px;color:var(--muted);"></span>
            </div>
          </div>
        </div>
      `;
      }}).join('') : '<div class="muted">Nenhuma intervenção registrada para este paciente.</div>';

      // --- Eventos de editar/excluir ---
      timelineEl.querySelectorAll('.edit-intervencao').forEach(btn => {{
        btn.addEventListener('click', () => {{
          const id = btn.getAttribute('data-id');
          const form = document.getElementById('edit-form-' + id);
          if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none';
        }});
      }});

      timelineEl.querySelectorAll('.cancel-edit').forEach(btn => {{
        btn.addEventListener('click', () => {{
          const id = btn.getAttribute('data-id');
          const form = document.getElementById('edit-form-' + id);
          if (form) form.style.display = 'none';
        }});
      }});

      timelineEl.querySelectorAll('.save-edit').forEach(btn => {{
        btn.addEventListener('click', async () => {{
          const id = btn.getAttribute('data-id');
          const form = document.getElementById('edit-form-' + id);
          if (!form) return;
          const msgEl = form.querySelector('.edit-status-msg');
          msgEl.textContent = 'Salvando...';
          try {{
            const tipoEl = form.querySelector('.edit-tipo');
            const descEl = form.querySelector('.edit-descricao');
            const statusEl = form.querySelector('.edit-status');
            const respEl = form.querySelector('.edit-responsavel');
            const dataEl = form.querySelector('.edit-data-atuacao');
            const obsEl = form.querySelector('.edit-observacao');
            const tipoNome = tiposById[Number(tipoEl.value)] || 'Atuação EGAA';
            const payload = {{
              ocupacao_leito_id: null,
              prontuario: PRONTUARIO,
              tipo_intervencao_id: Number(tipoEl.value),
              titulo: tipoNome,
              descricao: descEl.value.trim() || null,
              status: statusEl.value,
              usuario_responsavel: respEl.value.trim() || null,
              data_atuacao: dataEl.value || null,
              data_prevista: null,
              data_conclusao: null,
              observacao: obsEl.value.trim() || null,
            }};
            const res = await fetch(`${{API_PREFIX}}/egaa/intervencoes/${{id}}`, {{
              method: 'PUT',
              headers: {{ 'Content-Type': 'application/json' }},
              body: JSON.stringify(payload),
            }});
            if (!res.ok) {{
              msgEl.textContent = 'Erro ao salvar.';
              return;
            }}
            msgEl.textContent = 'Salvo!';
            form.style.display = 'none';
            await loadHistorico();
          }} catch {{
            msgEl.textContent = 'Falha de rede.';
          }}
        }});
      }});

      timelineEl.querySelectorAll('.delete-intervencao').forEach(btn => {{
        btn.addEventListener('click', async () => {{
          const id = btn.getAttribute('data-id');
          if (!confirm('Excluir esta atuação permanentemente?')) return;
          const res = await fetch(`${{API_PREFIX}}/egaa/intervencoes/${{id}}`, {{ method: 'DELETE' }});
          if (!res.ok) {{ alert('Erro ao excluir.'); return; }}
          await loadHistorico();
        }});
      }});
      return list;
    }}

    // --- Pendencias para alta ---
    const pendenciaSelectEl = document.getElementById('pendenciaSelect');
    const pendenciaListEl = document.getElementById('pendenciaList');
    const addPendenciaBtn = document.getElementById('addPendencia');

    async function loadCodigosPendencia() {{
      const res = await fetch(`${{API_PREFIX}}/egaa/pendencia/codigos`);
      if (!res.ok) return;
      const items = await res.json();
      if (!Array.isArray(items)) return;
      if (pendenciaSelectEl) {{
        pendenciaSelectEl.innerHTML = '<option value="">Selecione...</option>' +
          items.map(item => `<option value="${{item.codigo}}">${{item.rotulo}}</option>`).join('');
      }}
    }}

    async function loadPendencias() {{
      const res = await fetch(`${{API_PREFIX}}/egaa/pendencia/${{encodeURIComponent(PRONTUARIO)}}`);
      if (!res.ok) {{
        if (pendenciaListEl) pendenciaListEl.innerHTML = '<span class="muted">Erro ao carregar pendências.</span>';
        return;
      }}
      const items = await res.json();
      const list = Array.isArray(items) ? items : [];
      if (!pendenciaListEl) return;
      if (!list.length) {{
        pendenciaListEl.innerHTML = '<span class="muted">Nenhuma pendência cadastrada.</span>';
        return;
      }}
      pendenciaListEl.innerHTML = list.map(item => {{
        const resolvida = item.resolvida;
        const label = pendenciaSelectEl
          ? (pendenciaSelectEl.querySelector(`option[value="${{item.codigo}}"]`)?.textContent || item.codigo)
          : item.codigo;
        const bg = resolvida ? '#E8F5E9' : '#FFF3E0';
        const border = resolvida ? '#A5D6A7' : '#FFE0B2';
        const color = resolvida ? '#2E7D32' : '#E65100';
        return `<span style="display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:999px;background:${{bg}};border:1px solid ${{border}};font-size:13px;font-weight:600;">
          <span style="color:${{color}};">${{label}}</span>
          <button type="button" data-pendencia-id="${{item.id}}" data-action="toggle-pendencia" style="background:none;border:none;cursor:pointer;padding:0;font-size:14px;line-height:1;color:${{resolvida ? '#2E7D32' : '#E65100'}}" title="${{resolvida ? 'Reabrir' : 'Resolver'}}">
            ${{resolvida ? '&#10003;' : '&#9711;'}}
          </button>
          <button type="button" data-pendencia-id="${{item.id}}" data-action="remove-pendencia" style="background:none;border:none;cursor:pointer;padding:0;font-size:14px;line-height:1;color:#C62828;" title="Remover">&times;</button>
        </span>`;
      }}).join('');
    }}

    if (addPendenciaBtn) {{
      addPendenciaBtn.addEventListener('click', async () => {{
        const codigo = pendenciaSelectEl ? pendenciaSelectEl.value : '';
        if (!codigo) return;
        const res = await fetch(`${{API_PREFIX}}/egaa/pendencia/${{encodeURIComponent(PRONTUARIO)}}`, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{ codigo }}),
        }});
        if (!res.ok) {{
          if (res.status === 409) alert('Pendência já cadastrada.');
          else alert('Erro ao adicionar pendência.');
          return;
        }}
        if (pendenciaSelectEl) pendenciaSelectEl.value = '';
        await loadPendencias();
      }});
    }}

    if (pendenciaListEl) {{
      pendenciaListEl.addEventListener('click', async (event) => {{
        const target = event.target;
        if (!(target instanceof HTMLElement)) return;
        const action = target.getAttribute('data-action');
        const id = target.getAttribute('data-pendencia-id');
        if (!action || !id) return;

        if (action === 'toggle-pendencia') {{
          const pendencia = await (await fetch(`${{API_PREFIX}}/egaa/pendencia/${{encodeURIComponent(PRONTUARIO)}}/${{id}}`)).json();
          const novaResolvida = !pendencia.resolvida;
          await fetch(`${{API_PREFIX}}/egaa/pendencia/${{encodeURIComponent(PRONTUARIO)}}/${{id}}`, {{
            method: 'PUT',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ resolvida: novaResolvida }}),
          }});
          await loadPendencias();
        }}

        if (action === 'remove-pendencia') {{
          if (!confirm('Remover esta pendência?')) return;
          await fetch(`${{API_PREFIX}}/egaa/pendencia/${{encodeURIComponent(PRONTUARIO)}}/${{id}}`, {{
            method: 'DELETE',
          }});
          await loadPendencias();
        }}
      }});
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
            const tipoNome = tiposById[item.tipo_intervencao_id] || item.titulo.trim() || 'Atuação EGAA';
            return {{
              ocupacao_leito_id: null,
              prontuario: PRONTUARIO,
              tipo_intervencao_id: Number(item.tipo_intervencao_id),
              titulo: tipoNome,
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

    const salvarEvolucaoBtn = document.getElementById('salvarEvolucao');
    const evolucaoStatusEl = document.getElementById('evolucaoStatus');
    if (salvarEvolucaoBtn) {{
      salvarEvolucaoBtn.addEventListener('click', async () => {{
        const evolucaoEl = document.getElementById('evolucao');
        if (!evolucaoEl) return;
        const texto = evolucaoEl.value;
        evolucaoStatusEl.textContent = 'Salvando...';
        try {{
          const res = await fetch(`${{API_PREFIX}}/censo/paciente/${{encodeURIComponent(PRONTUARIO)}}/evolucao`, {{
            method: 'PUT',
            headers: {{ 'Content-Type': 'application/json' }},
            body: JSON.stringify({{ evolucao: texto }}),
          }});
          if (!res.ok) {{
            evolucaoStatusEl.textContent = 'Erro ao salvar evolução.';
            return;
          }}
          evolucaoStatusEl.textContent = 'Evolução salva em ' + new Date().toLocaleTimeString('pt-BR');
        }} catch {{
          evolucaoStatusEl.textContent = 'Falha de rede ao salvar.';
        }}
      }});
    }}

    // ─── Desfecho ──────────────────────────────────────────────
    const desfechoInfoEl = document.getElementById('desfechoInfo');
    const desfechoActionsEl = document.getElementById('desfechoActions');
    const registrarDesfechoBtn = document.getElementById('registrarDesfecho');

    function fmtDateBR(value) {{
      if (!value) return '--';
      try {{
        const d = new Date(value + (typeof value === 'string' && /^\\d{{4}}-\\d{{2}}-\\d{{2}}$/.test(value) ? 'T00:00:00' : ''));
        return d.toLocaleDateString('pt-BR');
      }} catch {{
        return String(value);
      }}
    }}

    async function loadPacienteDesfecho() {{
      if (!desfechoInfoEl) return;
      try {{
        const res = await fetch(`${{API_PREFIX}}/egaa/desfechos?prontuario=${{encodeURIComponent(PRONTUARIO)}}`);
        if (!res.ok) throw new Error('Erro ao carregar desfecho');
        const items = await res.json();
        const list = Array.isArray(items) ? items : [];
        if (list.length > 0) {{
          const d = list[0];
          const badgeClass = d.tipo === 'obito' ? 'badge-error' : 'badge-success';
          const badgeLabel = d.tipo === 'obito' ? 'Obito' : 'Alta';
          let desfCardHtml = `
            <div><span class="badge ${{badgeClass}}" style="font-size:14px;padding:8px 14px;">${{badgeLabel}}</span></div>
            <div style="margin-top:10px;"><strong>Data do desfecho:</strong> ${{fmtDateBR(d.data_desfecho)}}</div>
            <div><strong>Descricao:</strong> ${{escapeHtml(d.descricao || '--')}}</div>
            <div><strong>Responsavel:</strong> ${{escapeHtml(d.usuario_responsavel || '--')}}</div>
          `;
          if (pacienteData && pacienteData.data_alta) desfCardHtml += '<div style="margin-top:8px;padding-top:8px;border-top:1px solid #edf2f7;"><strong>Data de Alta (Sist.):</strong> ' + fmtDateBR(pacienteData.data_alta) + '</div>';
          if (pacienteData && pacienteData.tipo_alta) desfCardHtml += '<div><strong>Tipo de Alta (Sist.):</strong> ' + escapeHtml(pacienteData.tipo_alta) + '</div>';
          desfechoInfoEl.innerHTML = desfCardHtml;
          if (desfechoActionsEl) desfechoActionsEl.style.display = 'none';
        }} else {{
          desfechoInfoEl.innerHTML = '<span class="badge badge-warning" style="font-size:14px;padding:8px 14px;">Pendente</span><p style="margin-top:10px;">Nenhum desfecho registrado para este paciente.</p>';
          if (desfechoActionsEl) desfechoActionsEl.style.display = 'flex';
        }}
      }} catch {{
        desfechoInfoEl.innerHTML = '<span class="muted">Erro ao carregar desfecho.</span>';
      }}
    }}

    // Modal de desfecho
    const desfechoModal = document.createElement('div');
    desfechoModal.innerHTML = `
      <div id="desfechoModalOverlay" style="display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.4);z-index:1000;align-items:center;justify-content:center;">
        <div style="background:#fff;border-radius:16px;padding:24px;max-width:460px;width:90%;box-shadow:0 16px 48px rgba(0,0,0,0.2);">
          <h3 style="margin:0 0 16px;color:var(--brand-strong);">Registrar Desfecho</h3>
          <form id="desfechoForm">
            <div class="field">
              <label>Prontuário</label>
              <input id="desfechoProntuario" value="${{PRONTUARIO}}" readonly style="background:#f5f7fa;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;width:100%;box-sizing:border-box;" />
            </div>
            <div class="field">
              <label>Tipo</label>
              <select id="desfechoTipo" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;">
                <option value="alta">Alta</option>
                <option value="obito">Óbito</option>
              </select>
            </div>
            <div class="field">
              <label>Data do desfecho</label>
              <input id="desfechoData" type="date" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;box-sizing:border-box;" />
            </div>
            <div class="field">
              <label>Descrição</label>
              <textarea id="desfechoDescricao" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;min-height:80px;font:inherit;resize:vertical;box-sizing:border-box;" placeholder="Motivo do desfecho (opcional)"></textarea>
            </div>
            <div class="field">
              <label>Responsável EGAA</label>
              <input id="desfechoResponsavel" style="width:100%;padding:10px 12px;border-radius:10px;border:1px solid #cfd8e3;background:#fff;box-sizing:border-box;" placeholder="Nome do profissional (opcional)" />
            </div>
            <div class="actions" style="margin-top:16px;">
              <button type="submit" style="padding:10px 12px;border-radius:8px;border:none;background:var(--brand);color:#fff;cursor:pointer;font-weight:600;">Salvar desfecho</button>
              <button type="button" id="cancelarDesfecho" style="padding:10px 12px;border-radius:8px;border:1px solid var(--panel-border);background:#EEF5FA;color:var(--brand);cursor:pointer;font-weight:600;">Cancelar</button>
              <span id="desfechoStatus" style="font-size:13px;color:var(--muted);"></span>
            </div>
          </form>
        </div>
      </div>
    `;
    document.body.appendChild(desfechoModal);

    const desfechoOverlay = document.getElementById('desfechoModalOverlay');
    const desfechoForm = document.getElementById('desfechoForm');
    const desfechoDataInput = document.getElementById('desfechoData');

    // Preencher data atual
    desfechoDataInput.value = new Date().toISOString().split('T')[0];

    if (registrarDesfechoBtn) {{
      registrarDesfechoBtn.addEventListener('click', () => {{
        desfechoOverlay.style.display = 'flex';
      }});
    }}

    document.getElementById('cancelarDesfecho').addEventListener('click', () => {{
      desfechoOverlay.style.display = 'none';
    }});

    desfechoOverlay.addEventListener('click', (e) => {{
      if (e.target === desfechoOverlay) desfechoOverlay.style.display = 'none';
    }});

    desfechoForm.addEventListener('submit', async (e) => {{
      e.preventDefault();
      const statusEl = document.getElementById('desfechoStatus');
      statusEl.textContent = 'Salvando...';
      try {{
        const payload = {{
          prontuario: PRONTUARIO,
          tipo: document.getElementById('desfechoTipo').value,
          data_desfecho: document.getElementById('desfechoData').value,
          descricao: document.getElementById('desfechoDescricao').value.trim() || null,
          usuario_responsavel: document.getElementById('desfechoResponsavel').value.trim() || null,
        }};
        const res = await fetch(`${{API_PREFIX}}/egaa/desfechos`, {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify(payload),
        }});
        if (!res.ok) throw new Error(await res.text());
        statusEl.textContent = 'Desfecho registrado com sucesso!';
        desfechoOverlay.style.display = 'none';
        await loadPacienteDesfecho();
      }} catch (err) {{
        statusEl.textContent = 'Erro: ' + (err.message || 'Falha ao salvar');
      }}
    }});

    drafts = [createDraft()];
    renderDrafts();
    (async () => {{
      await loadPaciente();
      await loadTipos();
      await loadHistorico();
      await loadCodigosPendencia();
      await loadPendencias();
      await loadPacienteDesfecho();
    }})();
  </script>
</body>
</html>
"""


@router.get("/configuracoes", response_class=HTMLResponse)
def configuracoes_route() -> str:
    html = """
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
      .sidebar-version {
      margin-top: auto; padding: 10px 12px; border-radius: 10px;
      background: rgba(0,0,0,0.04); color: var(--muted); font-size: 11px;
      text-align: center; letter-spacing: .02em;
    }
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <p class="brand">EGAA</p>
      <p class="brand-subtitle">Administração</p>
      <nav class="nav">
        <a href="/dashboard">Dashboard</a>
        <a href="/longa-permanencia">Longa Permanência</a>
        <a href="/desfechos">Desfechos EGAA</a>
        <a class="primary" href="/configuracoes">Configurações</a>
        <a href="/upload">Importações</a>
      </nav>
      <div class="sidebar-note">
        Parametrização do fluxo operacional, com tipos de intervenção e registro rápido para acompanhamento da equipe.
      </div>
      <div class="sidebar-version">v{settings.app_version} · {settings.app_env}</div>
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
        const normalized = typeof value === 'string' && /^\\d{4}-\\d{2}-\\d{2}$/.test(value)
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
    return html.replace("{settings.app_version}", settings.app_version).replace("{settings.app_env}", settings.app_env)


@router.get("/desfechos", response_class=HTMLResponse)
def desfechos_route() -> str:
    html = """
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>EGAA - Desfechos EGAA</title>
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
    .header-actions { display:flex; gap: 10px; align-items:center; }
    .pill-link {
      display:inline-flex;
      align-items:center;
      gap:6px;
      text-decoration:none;
      padding:8px 16px;
      border-radius:30px;
      background:#fff;
      border:1px solid var(--panel-border);
      color:var(--text);
      font-weight:600;
      font-size:14px;
    }
    .pill-link:hover { border-color: var(--brand); color: var(--brand); }
    .btn-primary {
      display:inline-flex;
      align-items:center;
      gap:6px;
      padding:9px 18px;
      border-radius:8px;
      background:var(--brand);
      color:#fff;
      border:none;
      font-weight:600;
      font-size:14px;
      cursor:pointer;
    }
    .btn-primary:hover { background:var(--brand-strong); }
    .btn-secondary {
      display:inline-flex;
      align-items:center;
      gap:6px;
      padding:9px 18px;
      border-radius:8px;
      background:#fff;
      color:var(--text);
      border:1px solid var(--panel-border);
      font-weight:600;
      font-size:14px;
      cursor:pointer;
    }
    .btn-secondary:hover { border-color:var(--brand); color:var(--brand); }
    .btn-danger {
      display:inline-flex;
      align-items:center;
      gap:4px;
      padding:5px 10px;
      border-radius:6px;
      background:transparent;
      color:var(--error);
      border:1px solid transparent;
      font-weight:600;
      font-size:12px;
      cursor:pointer;
    }
    .btn-danger:hover { background:#FFF0F0; border-color:#FFCDD2; }
    .kpis {
      display:grid;
      grid-template-columns: repeat(4, 1fr);
      gap:16px;
      margin-bottom:20px;
    }
    .kpi-card {
      background:var(--panel);
      border:1px solid var(--panel-border);
      border-radius:10px;
      padding:16px;
    }
    .kpi-card .label { font-size:11px; font-weight:700; color:var(--muted); text-transform:uppercase; letter-spacing:0.5px; }
    .kpi-card .value { font-size:26px; font-weight:800; color:var(--text); margin:4px 0; }
    .kpi-card .sub { font-size:11px; color:var(--muted); }
    .card {
      background:var(--panel);
      border:1px solid var(--panel-border);
      border-radius:12px;
      margin-bottom:20px;
      overflow:hidden;
    }
    .card-header {
      padding:16px 20px;
      border-bottom:1px solid var(--panel-border);
      background:#F8FAFC;
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap:12px;
      flex-wrap:wrap;
    }
    .card-header h3 { margin:0; font-size:16px; }
    .card-header p { margin:4px 0 0; font-size:13px; color:var(--muted); }
    .card-body { padding:0; overflow-x:auto; }
    table { width:100%; border-collapse:collapse; }
    th {
      text-align:left;
      padding:10px 16px;
      font-size:11px;
      font-weight:700;
      color:var(--muted);
      text-transform:uppercase;
      letter-spacing:0.5px;
      border-bottom:1px solid var(--panel-border);
      background:#F8FAFC;
    }
    td { padding:12px 16px; font-size:13px; border-bottom:1px solid var(--panel-border); }
    tr:hover { background:#FAFBFD; }
    .badge {
      display:inline-block;
      padding:2px 10px;
      border-radius:20px;
      font-size:11px;
      font-weight:700;
      text-transform:uppercase;
      letter-spacing:0.3px;
    }
    .badge-success { background:#E8F5E9; color:var(--success); }
    .badge-danger { background:#FFF0F0; color:var(--error); }
    .filter-bar {
      display:flex;
      gap:8px;
      align-items:center;
    }
    .filter-bar input, .filter-bar select {
      padding:7px 10px;
      border:1px solid var(--panel-border);
      border-radius:6px;
      font-size:13px;
    }
    .filter-bar input:focus, .filter-bar select:focus {
      outline:none;
      border-color:var(--brand);
    }
    .mono { font-family: 'Courier New', monospace; font-size:13px; font-weight:700; }
    .muted { color:var(--muted); }
    .modal-overlay {
      display:none;
      position:fixed;
      inset:0;
      background:rgba(15,23,42,0.6);
      backdrop-filter:blur(2px);
      z-index:100;
      align-items:center;
      justify-content:center;
    }
    .modal-overlay.open { display:flex; }
    .modal {
      background:var(--panel);
      border-radius:12px;
      width:100%;
      max-width:560px;
      max-height:90vh;
      overflow-y:auto;
      box-shadow:0 20px 60px rgba(0,0,0,0.15);
    }
    .modal-header {
      padding:16px 20px;
      border-bottom:1px solid var(--panel-border);
      display:flex;
      align-items:center;
      justify-content:space-between;
    }
    .modal-header h3 { margin:0; font-size:16px; }
    .modal-close {
      background:none;
      border:none;
      font-size:20px;
      cursor:pointer;
      padding:4px 8px;
      border-radius:6px;
      color:var(--muted);
    }
    .modal-close:hover { background:#F1F5F9; color:var(--text); }
    .modal-body { padding:20px; }
    .field { margin-bottom:16px; }
    .field label { display:block; font-size:13px; font-weight:600; margin-bottom:6px; color:var(--text); }
    .field input, .field select, .field textarea {
      width:100%;
      padding:9px 12px;
      border:1px solid var(--panel-border);
      border-radius:8px;
      font-size:14px;
      box-sizing:border-box;
    }
    .field textarea { min-height:80px; resize:vertical; }
    .field input:focus, .field select:focus, .field textarea:focus { outline:none; border-color:var(--brand); }
    .modal-actions {
      display:flex;
      justify-content:flex-end;
      gap:10px;
      padding-top:16px;
      border-top:1px solid var(--panel-border);
      margin-top:8px;
    }
    .toast {
      position:fixed;
      bottom:24px;
      right:24px;
      background:#1F2937;
      color:#fff;
      padding:12px 20px;
      border-radius:8px;
      font-size:14px;
      box-shadow:0 4px 12px rgba(0,0,0,0.15);
      z-index:200;
      opacity:0;
      transition: opacity 0.3s;
    }
    .toast.show { opacity:1; }
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <div>
        <h2 class="brand">Painel EGAA</h2>
        <p class="brand-subtitle">Censo Hospitalar GHC</p>
      </div>
      <nav class="nav">
        <a href="/dashboard">Dashboard</a>
        <a href="/longa-permanencia">Longa Permanência</a>
        <a class="primary" href="/desfechos">Desfechos EGAA</a>
        <a href="/configuracoes">Configurações</a>
        <a href="/upload">Importações</a>
      </nav>
      <div class="sidebar-note">
        <strong>Desfechos EGAA</strong><br/>
        Registre altas e óbitos com atuação do EGAA para demonstrar resultados da desospitalização.
      </div>
    </aside>

    <main class="main">
      <div class="shell">
        <div class="header">
          <div>
            <h1>Desfechos EGAA</h1>
            <p class="subtitle">Altas e óbitos com atuação do EGAA — demonstrando resultados da desospitalização</p>
          </div>
          <div class="header-actions">
            <div style="display:flex;gap:8px;align-items:center;">
              <input type="text" id="quickSearch" placeholder="Buscar prontuário..."
                style="padding:8px 14px;border:1px solid var(--panel-border);border-radius:8px;font-size:14px;width:180px;"
                onkeydown="if(event.key==='Enter'){navegarPaciente()}" />
              <button class="btn-secondary" onclick="navegarPaciente()" title="Ir para paciente" style="padding:8px 12px;">🔍</button>
            </div>
            <button class="btn-primary" onclick="openModal()">+ Novo Desfecho</button>
          </div>
        </div>

        <!-- KPIs -->
        <div class="kpis">
          <div class="kpi-card">
            <div class="label">Total de Desfechos</div>
            <div class="value" id="totalDesfechos">--</div>
          </div>
          <div class="kpi-card">
            <div class="label">Altas</div>
            <div class="value" id="totalAltas">--</div>
            <div class="sub">Com apoio do EGAA</div>
          </div>
          <div class="kpi-card">
            <div class="label">Óbitos</div>
            <div class="value" id="totalObitos">--</div>
            <div class="sub">Com suporte EGAA à família</div>
          </div>
          <div class="kpi-card">
            <div class="label">Pacientes Atendidos</div>
            <div class="value" id="totalPacientes">--</div>
            <div class="sub">Com desfecho registrado</div>
          </div>
        </div>

        <!-- Lista -->
        <div class="card">
          <div class="card-header">
            <div>
              <h3>Registros de Desfechos</h3>
              <p id="registroCount">Carregando...</p>
            </div>
            <div class="filter-bar">
              <input type="text" id="searchInput" placeholder="Buscar prontuário..." oninput="applyFilters()" />
              <select id="tipoFilter" onchange="applyFilters()">
                <option value="">Todos os tipos</option>
                <option value="alta">Altas</option>
                <option value="obito">Óbitos</option>
              </select>
              <label style="display:flex;align-items:center;gap:6px;font-size:13px;color:var(--muted);cursor:pointer;white-space:nowrap;">
                <input type="checkbox" id="mostrarTodos" onchange="loadDesfechos()" />
                Mostrar todos (importados)
              </label>
            </div>
          </div>
          <div class="card-body">
            <table>
              <thead>
                <tr>
                  <th>Prontuário</th>
                  <th>Tipo</th>
                  <th>Data</th>
                  <th>Responsável</th>
                  <th>Descrição</th>
                  <th style="text-align:right;">Ações</th>
                </tr>
              </thead>
              <tbody id="desfechosBody">
                <tr><td colspan="6" class="muted" style="text-align:center;padding:32px;">Carregando...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  </div>

  <!-- Modal -->
  <div class="modal-overlay" id="modalOverlay">
    <div class="modal">
      <div class="modal-header">
        <h3>Novo Desfecho EGAA</h3>
        <button class="modal-close" onclick="closeModal()">&times;</button>
      </div>
      <div class="modal-body">
        <form id="desfechoForm" onsubmit="submitDesfecho(event)">
          <div class="field">
            <label for="prontuario">Prontuário do Paciente</label>
            <input id="prontuario" required placeholder="Ex: 8399062" />
          </div>
          <div class="field">
            <label for="tipo">Tipo de Desfecho</label>
            <select id="tipo" required>
              <option value="alta">Alta Hospitalar</option>
              <option value="obito">Óbito</option>
            </select>
          </div>
          <div class="field">
            <label for="dataDesfecho">Data do Desfecho</label>
            <input id="dataDesfecho" type="date" required />
          </div>
          <div class="field">
            <label for="descricao">Descrição / Observação</label>
            <textarea id="descricao" placeholder="Descreva como o EGAA atuou neste desfecho..."></textarea>
          </div>
          <div class="field">
            <label for="responsavel">Responsável EGAA</label>
            <input id="responsavel" placeholder="Seu nome" />
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" onclick="closeModal()">Cancelar</button>
            <button type="submit" class="btn-primary" id="submitBtn">Registrar Desfecho</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <div class="toast" id="toast"></div>

  <script>
    const API = '/api';

    function showToast(msg) {
      const el = document.getElementById('toast');
      el.textContent = msg;
      el.classList.add('show');
      setTimeout(() => el.classList.remove('show'), 3000);
    }

    function openModal() {
      document.getElementById('modalOverlay').classList.add('open');
      document.getElementById('dataDesfecho').value = todayValue();
    }

    function closeModal() {
      document.getElementById('modalOverlay').classList.remove('open');
      document.getElementById('desfechoForm').reset();
    }

    function todayValue() {
      const d = new Date();
      return d.getFullYear() + '-' + String(d.getMonth()+1).padStart(2,'0') + '-' + String(d.getDate()).padStart(2,'0');
    }

    function fmtDate(value) {
      if (!value) return '--';
      try {
        const d = new Date(value + 'T00:00:00');
        return d.toLocaleDateString('pt-BR');
      } catch { return value; }
    }

    function escapeHtml(str) {
      if (!str) return '';
      return String(str).replace(/[&<>'"]/g, function(c) {
        return {'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c] || c;
      });
    }

    function navegarPaciente() {
      const pront = document.getElementById('quickSearch').value.trim();
      if (pront) {
        window.location.href = '/paciente/' + encodeURIComponent(pront);
      }
    }

    let allDesfechos = [];

    async function loadDesfechos() {
      try {
        const mostrarTodos = document.getElementById('mostrarTodos')?.checked || false;
        const url = mostrarTodos ? (API + '/egaa/desfechos?apenas_egaa=false') : (API + '/egaa/desfechos');
        const res = await fetch(url);
        if (!res.ok) throw new Error(await res.text());
        allDesfechos = await res.json();
        applyFilters();
      } catch (e) {
        document.getElementById('desfechosBody').innerHTML =
          '<tr><td colspan="6" class="muted" style="text-align:center;padding:32px;">Erro ao carregar: ' + e.message + '</td></tr>';
      }
    }

    async function loadIndicadores() {
      try {
        const mostrarTodos = document.getElementById('mostrarTodos')?.checked || false;
        const url = mostrarTodos ? (API + '/egaa/indicadores/desfechos') : (API + '/egaa/indicadores/desfechos?apenas_egaa=true');
        const res = await fetch(url);
        if (!res.ok) return;
        const data = await res.json();
        document.getElementById('totalDesfechos').textContent = data.total_desfechos ?? 0;
        document.getElementById('totalAltas').textContent = data.total_altas ?? 0;
        document.getElementById('totalObitos').textContent = data.total_obitos ?? 0;
        document.getElementById('totalPacientes').textContent = data.pacientes_com_desfecho ?? 0;
      } catch (e) {
        console.error('Erro ao carregar indicadores:', e);
      }
    }

    function applyFilters() {
      const search = document.getElementById('searchInput').value;
      const tipo = document.getElementById('tipoFilter').value;

      let filtered = allDesfechos;
      if (search) {
        filtered = filtered.filter(d => d.prontuario.includes(search) || (d.descricao && d.descricao.toLowerCase().includes(search.toLowerCase())));
      }
      if (tipo) {
        filtered = filtered.filter(d => d.tipo === tipo);
      }

      document.getElementById('registroCount').textContent = filtered.length + ' registro(s) encontrado(s)';

      if (!filtered.length) {
        document.getElementById('desfechosBody').innerHTML =
          '<tr><td colspan="6" class="muted" style="text-align:center;padding:32px;">Nenhum desfecho encontrado.</td></tr>';
        return;
      }

      document.getElementById('desfechosBody').innerHTML = filtered.map(d => {
        const badgeClass = d.tipo === 'alta' ? 'badge-success' : 'badge-danger';
        const label = d.tipo === 'alta' ? 'Alta' : 'Óbito';
        const prontUrl = '/paciente/' + encodeURIComponent(d.prontuario);
        return '<tr>' +
          '<td class="mono"><a href="' + prontUrl + '" style="color:var(--brand);text-decoration:none;font-weight:700;">' + escapeHtml(d.prontuario) + '</a></td>' +
          '<td><span class="badge ' + badgeClass + '">' + label + '</span></td>' +
          '<td class="muted">' + fmtDate(d.data_desfecho) + '</td>' +
          '<td>' + (d.usuario_responsavel || '-') + '</td>' +
          '<td class="muted" style="max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">' + (d.descricao || '-') + '</td>' +
          '<td style="text-align:right;white-space:nowrap;">' +
            '<a href="' + prontUrl + '" class="btn-secondary" style="padding:4px 10px;font-size:12px;text-decoration:none;margin-right:4px;">Abrir</a>' +
            '<button class="btn-danger" onclick="deleteDesfecho(' + d.id + ')">Remover</button></td>' +
          '</tr>';
      }).join('');
    }

    async function deleteDesfecho(id) {
      if (!confirm('Tem certeza que deseja remover este desfecho?')) return;
      try {
        const res = await fetch(API + '/egaa/desfechos/' + id, { method: 'DELETE' });
        if (!res.ok) throw new Error(await res.text());
        showToast('Desfecho removido com sucesso!');
        await loadDesfechos();
        await loadIndicadores();
      } catch (e) {
        showToast('Erro ao remover: ' + e.message);
      }
    }

    async function submitDesfecho(event) {
      event.preventDefault();
      const btn = document.getElementById('submitBtn');
      btn.disabled = true;
      btn.textContent = 'Salvando...';

      const payload = {
        prontuario: document.getElementById('prontuario').value.trim(),
        tipo: document.getElementById('tipo').value,
        data_desfecho: document.getElementById('dataDesfecho').value,
        descricao: document.getElementById('descricao').value.trim() || null,
        usuario_responsavel: document.getElementById('responsavel').value.trim() || null,
      };

      try {
        const res = await fetch(API + '/egaa/desfechos', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        if (!res.ok) throw new Error(await res.text());
        showToast('Desfecho registrado com sucesso!');
        closeModal();
        await loadDesfechos();
        await loadIndicadores();
      } catch (e) {
        showToast('Erro: ' + e.message);
      } finally {
        btn.disabled = false;
        btn.textContent = 'Registrar Desfecho';
      }
    }

    loadDesfechos();
    loadIndicadores();
  </script>
</body>
</html>
"""
    return html
