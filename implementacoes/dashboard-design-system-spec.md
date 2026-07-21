# Especificação: Design System do Dashboard e componente "Evolução Mensal"
Data: 2026-07-21

Resumo
--
Documento técnico para padronizar o Dashboard do MVP, usando a paleta GHC já existente, e especificar a troca do gráfico "EVOLUÇÃO MENSAL" para um gráfico de colunas verticais implementado em SVG. Inclui API contract, tokens de design, componente JS/SVG de exemplo e instruções de integração mínima (sem aplicar alterações no código do servidor).

Objetivo e Escopo
--
- Objetivo: transformar o Dashboard em um conjunto de componentes reutilizáveis (design-system) e substituir o gráfico "EVOLUÇÃO MENSAL" por um gráfico de colunas verticais acessível e responsivo.
- Escopo inicial: componente de Card, KPI, Legend, Loader, Empty State, e `ChartColumnSVG` (SVG custom). Não toca em frontend-next; alterações previstas em [backend/app/routers/ui.py](backend/app/routers/ui.py).

Tokens de Design (usar variáveis GHC existentes)
--
- Cores (exemplos — alinhar com variáveis já definidas no projeto):
  - `--ghc-primary` (brand)
  - `--ghc-accent` (accent)
  - `--ghc-success` (success)
  - `--ghc-warning` (warning)
  - `--ghc-danger` (danger)
  - `--ghc-muted` (borders/labels)
- Tipografia:
  - base: 14px; escala: 14 / 16 / 20 / 28 (body / label / title / kpi)
- Espaçamento:
  - spacing unit: 8px; use multiples (8,16,24)
- Grid:
  - container gap: 16px; responsive columns: 1 / 2 / 3

Componentes (APIs esperadas)
--
- Card: `Card({title, actions, children})` — header, body, footer.
- KPI: `KPI({value, label, delta, deltaSign})` — delta com cor (success/warning/danger).
- Legend: `Legend({items})` — cada item: {key, label, color, visible}.
- Chart wrapper: `renderColumnChart(container, config)` — ver abaixo.

Mapeamento de Dados / Endpoints
--
- KPIs gerais: `GET /api/censo/kpis` → JSON com valores para KPIs.
- Evolução mensal (séries): idealmente `GET /api/egaa/indicadores` ou um novo endpoint `GET /api/egaa/evolucao-mensal` que retorne:

```json
{
  "labels": ["Jan","Fev",...],
  "series": [
    {"key":"intervencoes","label":"Intervenções","values":[10,12,8,...]},
    {"key":"altas","label":"Altas","values":[5,6,7,...]}
  ]
}
```

Especificação do gráfico "EVOLUÇÃO MENSAL"
--
- Tipo: colunas verticais (SVG), suportando séries agrupadas ou empilhadas.
- Eixos:
  - X: labels (meses), abreviados.
  - Y: escala automática com linhas de grid leves.
- Interatividade: tooltip ao hover/focus; legenda togglable para ativar/desativar séries.
- Acessibilidade: cada barra com `role="img"` ou `role="button"` e `aria-label` descrevendo mês e valor; keyboard focus navegável.
- Responsividade: em telas <480px mudar para empilhado ou mostrar resumo com botão "Ver detalhes".

Decisão de Implementação
--
- Recomendado: SVG custom (controle total, leve). Se futuramente precisarmos de animações avançadas ou zoom, considerar Chart.js/ApexCharts.

Exemplo de componente JS/SVG (implementação mínima)
--
Copiar/colar diretamente no arquivo de scripts do dashboard. A função é auto-contida, não requer libs externas.

```javascript
function renderColumnChart(container, {labels, series, colors, options={}}) {
  // limpa container
  container.innerHTML = '';
  const width = container.clientWidth || 600;
  const height = options.height || 220;
  const padding = {top: 20, right: 12, bottom: 40, left: 40};
  const innerW = width - padding.left - padding.right;
  const innerH = height - padding.top - padding.bottom;

  // montar dados agregados para escala Y
  const maxVal = Math.max(...series.flatMap(s => s.values));
  const svgNS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(svgNS, 'svg');
  svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
  svg.setAttribute('width', '100%');
  svg.setAttribute('height', height);

  // grid linhas Y
  const gridGroup = document.createElementNS(svgNS, 'g');
  gridGroup.setAttribute('aria-hidden', 'true');
  const gridLines = 4;
  for (let i=0;i<=gridLines;i++){
    const y = padding.top + (innerH * i / gridLines);
    const line = document.createElementNS(svgNS, 'line');
    line.setAttribute('x1', padding.left);
    line.setAttribute('x2', padding.left + innerW);
    line.setAttribute('y1', y);
    line.setAttribute('y2', y);
    line.setAttribute('stroke', 'var(--ghc-muted, #e6e6e6)');
    line.setAttribute('stroke-width', '1');
    gridGroup.appendChild(line);
  }
  svg.appendChild(gridGroup);

  // barras
  const cols = labels.length;
  const seriesCount = series.length;
  const bandWidth = innerW / cols;
  const barGap = Math.max(4, Math.floor(bandWidth * 0.08));
  const barWidth = Math.max(6, Math.floor((bandWidth - barGap*2) / seriesCount));

  const barsGroup = document.createElementNS(svgNS, 'g');
  for (let i=0;i<cols;i++){
    const xBase = padding.left + i * bandWidth;
    for (let s=0;s<seriesCount;s++){
      const val = series[s].values[i] || 0;
      const h = maxVal === 0 ? 0 : (val / maxVal) * innerH;
      const x = xBase + barGap + s * barWidth;
      const y = padding.top + (innerH - h);
      const rect = document.createElementNS(svgNS, 'rect');
      rect.setAttribute('x', x);
      rect.setAttribute('y', y);
      rect.setAttribute('width', barWidth - 1);
      rect.setAttribute('height', Math.max(0, h));
      const color = (colors && colors[s]) || `var(--ghc-accent)`;
      rect.setAttribute('fill', color);
      rect.setAttribute('role', 'img');
      rect.setAttribute('tabindex', '0');
      rect.setAttribute('aria-label', `${labels[i]}: ${series[s].label}: ${val}`);
      rect.addEventListener('mouseenter', e => showTooltip(e, `${series[s].label}: ${val}`));
      rect.addEventListener('focus', e => showTooltip(e, `${series[s].label}: ${val}`));
      rect.addEventListener('mouseleave', hideTooltip);
      rect.addEventListener('blur', hideTooltip);
      barsGroup.appendChild(rect);
    }
    // label X
    const tx = document.createElementNS(svgNS, 'text');
    tx.setAttribute('x', xBase + bandWidth/2);
    tx.setAttribute('y', padding.top + innerH + 16);
    tx.setAttribute('text-anchor', 'middle');
    tx.setAttribute('fill', 'var(--ghc-muted)');
    tx.setAttribute('font-size', '12');
    tx.textContent = labels[i];
    svg.appendChild(tx);
  }
  svg.appendChild(barsGroup);

  // tooltip (simple)
  const tooltip = document.createElement('div');
  tooltip.className = 'chart-tooltip';
  tooltip.style.position = 'absolute';
  tooltip.style.pointerEvents = 'none';
  tooltip.style.display = 'none';
  container.style.position = 'relative';
  container.appendChild(svg);
  container.appendChild(tooltip);

  function showTooltip(e, text){
    tooltip.textContent = text;
    tooltip.style.display = 'block';
    const rect = container.getBoundingClientRect();
    tooltip.style.left = (e.clientX - rect.left + 8) + 'px';
    tooltip.style.top = (e.clientY - rect.top - 28) + 'px';
  }
  function hideTooltip(){ tooltip.style.display = 'none'; }
}

// Uso esperado:
// renderColumnChart(document.getElementById('evolucao'), {labels, series, colors:['var(--ghc-primary)','var(--ghc-warning)']});
```

CSS sugerido (exemplo curto)
--
```css
.card { background: white; border-radius: 8px; padding: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.04);} 
.kpi { font-size: 28px; color: var(--ghc-primary);} 
.chart-tooltip { background: rgba(0,0,0,0.8); color: #fff; padding:6px 8px; border-radius:4px; font-size:12px;}
```

Integração mínima sugerida (não aplicar automaticamente)
--
No fluxo JS atual do [backend/app/routers/ui.py](backend/app/routers/ui.py) substituir a renderização textual/list-style do bloco "EVOLUÇÃO MENSAL" por um container com id `evolucao` e chamar `renderColumnChart` após buscar os indicadores:

```js
// após fetch('/api/egaa/indicadores')
const data = await resp.json();
const container = document.getElementById('evolucao');
renderColumnChart(container, {labels: data.labels, series: data.series, colors: ['var(--ghc-primary)','var(--ghc-success)']});
```

Planos de migração e testes
--
1. Criar componente local e incluir em um card de preview (feature branch).
2. Validar contrato da API (adicionar endpoint ou adaptar `indicadores`).
3. Testes manuais: sem dados, dados zero, múltiplas séries, mobile.
4. A11y check com `axe` e testes de teclado.
5. Aprovação visual e merge.

Checklist pré-implantação
--
- Tokens de cor e tipografia definidos e usados.
- Componente `renderColumnChart` testado com dados reais.
- Fallback visual para telas pequenas.
- Documentação de uso adicionada a [implementacoes/21-07-2026.md](implementacoes/21-07-2026.md) (log de implementação).

Próximo passo
--
Se aprovar, posso gerar o patch mínimo com a implementação do `renderColumnChart` dentro de [backend/app/routers/ui.py](backend/app/routers/ui.py) e os ajustes HTML necessários. Deseja que eu gere o patch agora?
