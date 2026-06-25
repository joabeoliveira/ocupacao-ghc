# Design System

## Objetivo

O MVP deve seguir a identidade visual institucional do Grupo Hospitalar Conceição (GHC), transmitindo confiança, clareza, acessibilidade e profissionalismo. A interface deve privilegiar a análise de dados e a tomada de decisão pelos gestores hospitalares.

---

# Inspiração

- Portal institucional do GHC
- Identidade Visual oficial do GHC
- Sistemas corporativos da área da saúde
- Design simples, limpo e funcional

---

# Princípios

- Simplicidade
- Consistência
- Legibilidade
- Acessibilidade (WCAG AA)
- Responsividade
- Componentização

---

# Cores

| Token | Cor |
|--------|------|
| Primary | #005C99 |
| Primary Hover | #004A7A |
| Secondary | #00A79D |
| Success | #2E7D32 |
| Warning | #F9A825 |
| Error | #C62828 |
| Info | #0288D1 |
| Background | #F7F9FB |
| Surface | #FFFFFF |
| Border | #DCE3EA |
| Text Primary | #1F2937 |
| Text Secondary | #6B7280 |


---

:root {
  --color-primary: #00767d;
  --color-accent: #00A2A2;
  --color-accent-hover: #10E7E7;
  --color-secondary: #84c9bd;
  --color-text-main: #404040;
  --color-text-dark: #000000;
  --color-surface: #ffffff;
  --color-border-light: #E6E6FA;
  --color-success: green;
}

# Tipografia

Fonte:

Inter

Pesos:

- 400
- 500
- 600
- 700

---

# Espaçamento

Escala baseada em 8px.

```
4
8
16
24
32
48
64
```

---

# Bordas

Radius padrão:

```
8px
```

Radius grande:

```
12px
```

---

# Componentes

Sugestão de componentes reutilizáveis:

- Button
- Card
- StatCard
- Badge
- Alert
- Modal
- Input
- Select
- DatePicker
- DataTable
- FilterBar
- Pagination
- Sidebar
- Header
- Breadcrumb
- EmptyState
- Loading

---

# Layout

Sidebar recolhível.

Header superior.

Conteúdo centralizado.

Cards para indicadores.

Tabelas para consultas com filtros.

Gráficos para evolução histórica.

Responsividade para desktop, tablet e mobile.

---

# Navegação

- Dashboard
- Leitos
- Pacientes
- Longa Permanência
- Relatórios
- Importações
- Configurações

---

# Status

Livre → Verde

Ocupado → Azul

Bloqueado → Vermelho

Impedido → Amarelo

Manutenção → Cinza

---

# Gráficos

Utilizar:

- Linha
- Barras
- Pizza
- Área
- Evolução histórica

---

# Ícones

Lucide React

---

# Tema

Modo claro inicialmente.

Arquitetura preparada para Dark Mode.

---

# UX

Cada tela deve responder a uma pergunta de negócio.

Dashboard:
"Como está a ocupação hoje?"

Leitos:
"Quais leitos estão disponíveis?"

Pacientes:
"Quem está internado?"

Longa Permanência:
"Quem precisa de atenção?"

Relatórios:
"O que aconteceu em determinado período?"

Importações:
"Os dados foram carregados corretamente?"