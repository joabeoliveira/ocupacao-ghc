from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import HTMLResponse


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
    body { font-family: Arial, sans-serif; background: #f5f7fa; margin: 0; padding: 24px; }
    .wrap { max-width: 1100px; margin: 0 auto; }
    .header { display:flex; align-items:center; justify-content:space-between; }
    h1 { color:#003d66; margin:0; }
    .cards { display:flex; gap:12px; margin-top:16px; }
    .card { background:#fff; padding:12px 16px; border-radius:10px; box-shadow:0 1px 2px rgba(16,24,40,0.05); min-width:160px }
    table { width:100%; border-collapse:collapse; margin-top:12px; background:#fff; }
    th, td { padding:8px 10px; border-bottom:1px solid #eee; text-align:left }
    .controls { margin-top:12px; display:flex; gap:8px; align-items:center }
    input, select, button { padding:8px 10px; border-radius:8px; border:1px solid #cfd8e3 }
    button { background:#005c99; color:#fff; cursor:pointer; border:none }
  </style>
</head>
<body>
  <div class="wrap">
    <div class="header">
      <h1>EGAA - Dashboard</h1>
      <a href="/upload">Ir para Upload</a>
    </div>

    <div class="cards" id="kpis">
      <div class="card">Carregando...</div>
    </div>

    <div class="controls">
      <label>Especialidade: <input id="especialidade" placeholder="ex: DERMATO" /></label>
      <label>Unidade: <input id="unidade" placeholder="ex: HFB" /></label>
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
    const rowsEl = document.getElementById('rows');
    const especialidadeEl = document.getElementById('especialidade');
    const unidadeEl = document.getElementById('unidade');
    const filtrarBtn = document.getElementById('filtrar');
    const prevBtn = document.getElementById('prev');
    const nextBtn = document.getElementById('next');
    const pageInfo = document.getElementById('pageInfo');

    let page = 1; let pageSize = parseInt(document.getElementById('pageSizeSelect').value, 10) || 10;

    async function loadKPIs() {
      const res = await fetch(`${API_PREFIX}/censo/kpis`);
      if (!res.ok) return kpisEl.innerHTML = '<div class="card">Erro ao obter KPIs</div>';
      const data = await res.json();
      kpisEl.innerHTML = `
        <div class="card"><strong>Internados</strong><div style="font-size:22px">${data.total_internados}</div></div>
        <div class="card"><strong>>=15 dias</strong><div style="font-size:22px">${data.longa_permanencia_15}</div></div>
        <div class="card"><strong>>=30 dias</strong><div style="font-size:22px">${data.longa_permanencia_30}</div></div>
        <div class="card"><strong>Por unidade</strong><div>${data.ocupacao_por_unidade.map(u => `<div>${u.unidade||'--'}: ${u.total_pacientes}</div>`).join('')}</div></div>`;
    }

    async function loadPacientes() {
      const params = new URLSearchParams();
      params.set('page', page);
      params.set('page_size', pageSize);
      if (especialidadeEl.value) params.set('especialidade', especialidadeEl.value);
      if (unidadeEl.value) params.set('unidade', unidadeEl.value);

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
    document.getElementById('refresh').addEventListener('click', () => { loadKPIs(); loadPacientes(); });

    loadKPIs(); loadPacientes();
  </script>
</body>
</html>
"""

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard_route() -> str:
    return dashboard_page()
