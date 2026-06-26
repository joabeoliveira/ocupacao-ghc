<#
Script de verificação rápida (smoke checks) para execução segura em produção.

Uso:
  ./prod_smoke.ps1 -Host my.server.com -Port 8000

O script realiza apenas requisições GET nos endpoints principais e opcionalmente faz um upload de teste
se você fornecer o parâmetro -TestUploadPath (arquivo pequeno). Por padrão, NÃO altera dados.
#>

param(
    [string]$Host = 'localhost',
    [int]$Port = 8000,
    [string]$TestUploadPath = ''
)

function Test-Get {
    param($Path)
    $url = "http://$Host`:$Port$Path"
    Write-Host "GET $url"
    try {
        $resp = Invoke-RestMethod -Uri $url -Method Get -TimeoutSec 20
        Write-Host "  OK"
        return @{ ok = $true; body = $resp }
    } catch {
        Write-Host "  ERRO: $($_.Exception.Message)" -ForegroundColor Red
        return @{ ok = $false; error = $_ }
    }
}

function Test-Upload {
    param($Path, $Endpoint)
    if (-not (Test-Path $Path)) { Write-Host "Arquivo de teste nao encontrado: $Path" -ForegroundColor Yellow; return @{ ok=$false; msg='file-not-found' } }
    $url = "http://$Host`:$Port$Endpoint"
    Write-Host "POST $url (arquivo: $Path)"
    try {
        $form = @{ file = Get-Item $Path }
        $resp = Invoke-RestMethod -Uri $url -Method Post -Form $form -TimeoutSec 120
        Write-Host "  OK"
        return @{ ok = $true; body = $resp }
    } catch {
        Write-Host "  ERRO: $($_.Exception.Message)" -ForegroundColor Red
        return @{ ok = $false; error = $_ }
    }
}

$allOk = $true

Write-Host "Smoke checks para http://$Host`:$Port" -ForegroundColor Cyan

$h = Test-Get -Path '/health'
if (-not $h.ok) { $allOk = $false }

$k = Test-Get -Path '/api/censo/kpis'
if (-not $k.ok) { $allOk = $false }

$p = Test-Get -Path '/api/censo/pacientes?page=1&page_size=1'
if (-not $p.ok) { $allOk = $false }

$u = Test-Get -Path '/upload'
if (-not $u.ok) { $allOk = $false }

$d = Test-Get -Path '/dashboard'
if (-not $d.ok) { $allOk = $false }

if ($TestUploadPath) {
    Write-Host "Executando upload de teste (opcional) - endpoint /api/upload/arquivo"
    $up = Test-Upload -Path $TestUploadPath -Endpoint '/api/upload/arquivo'
    if (-not $up.ok) { $allOk = $false }
}

if ($allOk) {
    Write-Host "Todos os checks OK" -ForegroundColor Green
    exit 0
} else {
    Write-Host "Alguns checks falharam" -ForegroundColor Red
    exit 2
}
