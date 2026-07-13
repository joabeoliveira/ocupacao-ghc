"""Fix: Adiciona CSS .sidebar-version na página de configurações."""
from pathlib import Path

path = Path("backend/app/routers/ui.py")
content = path.read_text(encoding="utf-8")

old = '</style>\n</head>\n<body>\n  <div class="layout">\n    <aside class="sidebar">\n      <p class="brand">EGAA</p>\n      <p class="brand-subtitle">Painel de regulação e censo</p>'

new_css = '''    .sidebar-version {
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
      <p class="brand-subtitle">Administração</p>'''

if old in content:
    content = content.replace(old, new_css)
    path.write_text(content, encoding="utf-8")
    print("OK - CSS adicionado na página de configurações")
else:
    print("ERRO: texto não encontrado")
    idx = content.find("Administração</p>")
    print(content[idx-80:idx+50])
