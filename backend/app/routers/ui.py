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
    body { font-family: Arial, sans-serif; background: #f5f7fa; margin: 0; padding: 24px; }
    .card { max-width: 720px; margin: 0 auto; background: #fff; border: 1px solid #dfe6ee; border-radius: 12px; padding: 20px; }
    h1 { margin: 0 0 8px; font-size: 22px; color: #003d66; }
    p { color: #4b5563; margin-top: 0; }
    label { display: block; margin-top: 14px; margin-bottom: 6px; font-weight: 600; color: #1f2937; }
    select, input[type=file], button { width: 100%; padding: 10px; border-radius: 8px; border: 1px solid #cfd8e3; }
    button { margin-top: 16px; background: #005c99; color: #fff; border: none; font-weight: 600; cursor: pointer; }
    button:hover { background: #004a7a; }
    pre { background: #0b1220; color: #d1e7ff; padding: 12px; border-radius: 8px; overflow: auto; min-height: 120px; }
    .hint { font-size: 13px; color: #6b7280; margin-top: 8px; }
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
      --bg: #eef3f8;
      --panel: #ffffff;
      --panel-border: #d9e2ec;
      --text: #102a43;
      --muted: #627d98;
      --brand: #005c99;
      --brand-strong: #003d66;
      --accent: #00994d;
    }
    body {
      font-family: Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(0, 92, 153, 0.08), transparent 28%),
        linear-gradient(180deg, #f7fbff 0%, var(--bg) 100%);
      margin: 0;
      padding: 24px;
      color: var(--text);
    }
    .wrap { max-width: 1120px; margin: 0 auto; }
    .header { display:flex; align-items:center; justify-content:space-between; gap: 16px; }
    h1 { color:var(--brand-strong); margin:0; letter-spacing:-0.02em; }
    .subtitle { margin: 8px 0 0; color: var(--muted); }
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
  </style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <div>
        <h1>EGAA - Dashboard</h1>
        <p class="subtitle">Visao rapida dos internados e das unidades com maior volume.</p>
      </div>
      <a href="/upload">Ir para Upload</a>
    </div>

    <div class="cards" id="kpis">
      <div class="card">Carregando...</div>
    </div>

    <div class="section" id="unidadesSection">
      <div class="section-header">
        <div>
          <h2>Unidades com mais pacientes</h2>
          <p id="unidadesResumo" class="muted">Aguardando dados...</p>
        </div>
      </div>
      <div class="section-body">
        <table>
          <thead>
            <tr><th>Unidade</th><th>Pacientes</th></tr>
          </thead>
          <tbody id="unidadesRows">
            <tr><td colspan="2">Aguardando dados...</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="controls">
      <label>Especialidade: <input id="especialidade" placeholder="ex: DERMATO" /></label>
      <label>Unidade: <input id="unidade" placeholder="ex: HFB" /></label>
      <label>Data inicial: <input id="dataInicio" type="date" /></label>
      <label>Data final: <input id="dataFim" type="date" /></label>
      <label>Itens por página: 
        <select id="pageSizeSelect">
          <option value="5">5</option>
          <option value="10" selected>10</option>
          <option value="20">20</option>
          <option value="50">50</option>
        </select>
      </label>
      <button id="filtrar">Filtrar</button>
      <button id="refresh" style="background:#00994d;margin-left:8px">Recarregar</button>
    </div>

    <table aria-live="polite">
      <thead>
        <tr><th>Prontuario</th><th>Nome</th><th>Idade</th><th>Dias</th><th>Especialidade</th><th>Unidade</th></tr>
      </thead>
      <tbody id="rows">
      </tbody>
    </table>

    <div style="margin-top:12px; display:flex; gap:8px; align-items:center">
      <button id="prev">Anterior</button>
      <span id="pageInfo">Página 1</span>
      <button id="next">Próxima</button>
    </div>
  </div>

  <script>
    const API_PREFIX = '/api';
    const kpisEl = document.getElementById('kpis');
    const unidadesRowsEl = document.getElementById('unidadesRows');
    const unidadesResumoEl = document.getElementById('unidadesResumo');
    const rowsEl = document.getElementById('rows');
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
        <div class="card"><strong>Internados</strong><div class="kpi-value">${data.total_internados}</div></div>
        <div class="card"><strong>>=15 dias</strong><div class="kpi-value">${data.longa_permanencia_15}</div></div>
        <div class="card"><strong>>=30 dias</strong><div class="kpi-value">${data.longa_permanencia_30}</div></div>
        <div class="card"><strong>Unidades ativas</strong><div class="kpi-value">${unidades.length}</div><div class="muted" style="margin-top:6px">Top ${topUnidades.length}${resto ? ` + ${resto} outras` : ''}</div></div>`;
      unidadesResumoEl.textContent = unidades.length
        ? `Mostrando as ${topUnidades.length} unidades com mais pacientes de um total de ${unidades.length}.`
        : 'Nenhuma unidade retornada pela API.';
      unidadesRowsEl.innerHTML = topUnidades.length
        ? topUnidades.map(u => `<tr><td>${u.unidade || '--'}</td><td>${u.total_pacientes}</td></tr>`).join('')
        : '<tr><td colspan="2">Nenhuma unidade para exibir.</td></tr>';
    }

    async function loadPacientes() {
      const params = new URLSearchParams();
      params.set('page', page);
      params.set('page_size', pageSize);
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

    loadKPIs(); loadPacientes();
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
