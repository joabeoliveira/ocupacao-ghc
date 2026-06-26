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
      grid-template-columns: repeat(5, minmax(0, 1fr));
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
          </div>
        </div>

        <section id="resumo" class="filters">
          <div class="filters-grid">
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
    const unidadesChartEl = document.getElementById('unidadesChart');
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
        <div class="card"><span class="badge badge-info">Ao vivo</span><strong>Internados</strong><div class="kpi-value">${data.total_internados}</div></div>
        <div class="card"><span class="badge badge-warning">Atenção</span><strong>>=15 dias</strong><div class="kpi-value">${data.longa_permanencia_15}</div></div>
        <div class="card"><span class="badge badge-error">Crítico</span><strong>>=30 dias</strong><div class="kpi-value">${data.longa_permanencia_30}</div></div>
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


def _patients_page(title: str, subtitle: str, *, default_min_dias: int | None = None) -> str:
    default_min_dias_value = "" if default_min_dias is None else str(default_min_dias)
    badge_text = "Longa permanência" if default_min_dias is not None else "Lista geral"
    badge_class = "badge-warning" if default_min_dias is not None else "badge-info"
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
        <a href="/dashboard">Dashboard</a>
        <a class="primary" href="{('/longa-permanencia' if default_min_dias is not None else '/pacientes')}">{title}</a>
        <a href="/upload">Importações</a>
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
        </div>

        <section class="filters">
          <div class="filters-grid">
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
                <tr><th>Prontuario</th><th>Nome</th><th>Idade</th><th>Dias</th><th>Especialidade</th><th>Unidade</th></tr>
              </thead>
              <tbody id="rows">
                <tr><td colspan="6" class="empty">Aguardando dados...</td></tr>
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
  </div>
  <script>
    const API_PREFIX = '/api';
    const kpisEl = document.getElementById('kpis');
    const rowsEl = document.getElementById('rows');
    const especialidadeEl = document.getElementById('especialidade');
    const unidadeEl = document.getElementById('unidade');
    const dataInicioEl = document.getElementById('dataInicio');
    const dataFimEl = document.getElementById('dataFim');
    const minDiasEl = document.getElementById('minDias');
    const filtrarBtn = document.getElementById('filtrar');
    const prevBtn = document.getElementById('prev');
    const nextBtn = document.getElementById('next');
    const pageInfo = document.getElementById('pageInfo');
    let page = 1;
    let pageSize = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10;

    async function loadPacientes() {{
      const params = new URLSearchParams();
      params.set('page', page);
      params.set('page_size', pageSize);
      if (especialidadeEl.value) params.set('especialidade', especialidadeEl.value);
      if (unidadeEl.value) params.set('unidade', unidadeEl.value);
      if (dataInicioEl.value) params.set('data_inicio', dataInicioEl.value);
      if (dataFimEl.value) params.set('data_fim', dataFimEl.value);
      if (minDiasEl.value) params.set('min_dias', minDiasEl.value);

      const res = await fetch(`${{API_PREFIX}}/censo/pacientes?` + params.toString());
      if (!res.ok) {{
        rowsEl.innerHTML = `<tr><td colspan="6">Erro ao obter registros (${{res.status}})</td></tr>`;
        return;
      }}
      const data = await res.json();
      const items = Array.isArray(data.items) ? data.items : [];
      kpisEl.innerHTML = `
        <div class="card"><span class="badge {badge_class}">{badge_text}</span><strong>Total encontrado</strong><div class="kpi-value">${{data.total}}</div></div>
        <div class="card"><span class="badge badge-info">Página atual</span><strong>Paginação</strong><div class="kpi-value">${{data.page}}</div></div>
        <div class="card"><span class="badge badge-secondary">Lote visual</span><strong>Itens por página</strong><div class="kpi-value">${{data.page_size}}</div></div>
      `;
      rowsEl.innerHTML = items.length
        ? items.map(it => `<tr><td>${{it.prontuario}}</td><td>${{it.nome_paciente||''}}</td><td>${{it.idade_anos??''}}</td><td>${{it.dias_internacao??''}}</td><td>${{it.especialidade}}</td><td>${{it.unidade||''}}</td></tr>`).join('')
        : '<tr><td colspan="6" class="empty">Nenhum registro encontrado com os filtros atuais.</td></tr>';
      pageInfo.textContent = `Página ${{data.page}} de ${{Math.ceil(data.total / data.page_size) || 1}}`;
      prevBtn.disabled = data.page <= 1;
      nextBtn.disabled = data.page * data.page_size >= data.total;
    }}

    filtrarBtn.addEventListener('click', () => {{ page = 1; pageSize = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10; loadPacientes(); }});
    prevBtn.addEventListener('click', () => {{ if (page > 1) page--; loadPacientes(); }});
    nextBtn.addEventListener('click', () => {{ page++; loadPacientes(); }});
    document.getElementById('pageSizeSelect').addEventListener('change', () => {{ page = 1; pageSize = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10; loadPacientes(); }});
    dataInicioEl.addEventListener('change', () => {{ page = 1; loadPacientes(); }});
    dataFimEl.addEventListener('change', () => {{ page = 1; loadPacientes(); }});
    minDiasEl.addEventListener('change', () => {{ page = 1; loadPacientes(); }});
    document.getElementById('refresh').addEventListener('click', () => {{ loadPacientes(); }});

    loadPacientes();
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
