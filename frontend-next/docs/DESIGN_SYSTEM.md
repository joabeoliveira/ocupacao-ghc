# Design System — Cores GHC

Paleta baseada no site oficial do Grupo Hospitalar Conceição ([ghc.com.br](https://www.ghc.com.br)).

## Cores Primárias

```ts
// tailwind.config.ts
colors: {
  ghc: {
    blue:        '#005C99',
    'blue-dark': '#004A7A',
    'blue-light':'#E8F0FE',
    teal:        '#00A79D',
    'teal-dark': '#008B82',
    'teal-light':'#E0F7F5',
  }
}
```

## Cores Semânticas

| Token | Cor | Uso |
|-------|-----|-----|
| `surface` | `#F7F9FB` | Fundo de página |
| `panel` | `#FFFFFF` | Cards e seções |
| `panel-border` | `#DCE3EA` | Bordas |
| `text` | `#1F2937` | Texto principal |
| `muted` | `#6B7280` | Texto secundário |

## Criticidade (Leitos)

| Classe | Cor | Faixa |
|--------|-----|-------|
| `priority-laranja` | `#F9A825` | 15-29 dias |
| `priority-vermelho` | `#C62828` | >= 30 dias |
| `priority-escuro` | `#7F1D1D` | >= 30 dias e >= 60 anos |
| `success` | `#2E7D32` | Concluído/resolvido |
| `info` | `#0288D1` | Informativo |

## Status de Intervenção

| Status | Cor |
|--------|-----|
| Aberta | `info` (`#0288D1`) |
| Em andamento | `warning` (`#F9A825`) |
| Concluída | `success` (`#2E7D32`) |
| Cancelada | `muted` (`#6B7280`) |

## Tipografia

- **Fonte:** Inter (Google Fonts)
- **Tamanhos:**
  - Título página: `text-2xl font-bold`
  - KPI value: `text-3xl font-extrabold`
  - Card título: `text-sm font-semibold uppercase muted`
  - Corpo: `text-sm`

## Componentes Base (Tailwind)

```tsx
// Card
<div className="bg-white rounded-xl border border-ghc-blue/10 shadow-sm p-4">

// Badge
<span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold">

// KPI Card
<div className="bg-white rounded-xl border border-ghc-blue/10 shadow-sm p-4">
  <span className="block text-xs font-bold uppercase text-ghc-blue/60 mb-1">
  <div className="text-3xl font-extrabold text-ghc-blue-dark">

// Botão primário
<button className="px-3 py-2.5 rounded-lg bg-ghc-blue text-white font-semibold hover:bg-ghc-blue-dark transition-colors">

// Botão secundário
<button className="px-3 py-2.5 rounded-lg bg-ghc-blue-light text-ghc-blue font-semibold border border-ghc-blue/20">

// Input
<input className="w-full px-3 py-2.5 rounded-lg border border-gray-300 bg-white text-sm">

// Select
<select className="w-full px-3 py-2.5 rounded-lg border border-gray-300 bg-white text-sm">
```

## Exemplo de Card de Leito

```tsx
<div className={cn(
  "relative bg-white rounded-xl border cursor-pointer p-4 shadow-sm hover:shadow-md transition-all",
  dias >= 30 && idade >= 60 ? "border-red-900" : dias >= 30 ? "border-red-600" : "border-orange-400"
)}>
  {/* Faixa superior */}
  <div className={cn(
    "absolute top-0 left-0 right-0 h-1 rounded-t-xl",
    dias >= 30 && idade >= 60 ? "bg-red-900" : dias >= 30 ? "bg-red-600" : "bg-orange-400"
  )} />
  
  <span className="text-xs font-bold uppercase text-gray-400">Leito {leito}</span>
  <div className="text-sm font-bold text-ghc-blue">#{prontuario}</div>
  <div className="font-bold text-gray-900 truncate">{nome}</div>
  <div className="text-sm text-gray-500">{dias} dias · {idade}a</div>
</div>
```
