$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$source = Join-Path $root 'src'
$output = Join-Path $root 'pdf'
$reports = @(
  'EE5430_Assignment_1_Report_Nguyen_Thai_Thanh_Binh_2570175',
  'EE5430_Assignment_1_Report_Vu_Tien_Giang_2570188',
  'EE5430_Assignment_1_Report_Pham_Huy_Thanh_2570317'
)
if (-not (Get-Command xelatex -ErrorAction SilentlyContinue)) {
  throw 'xelatex was not found. Install MiKTeX or TeX Live.'
}
New-Item -ItemType Directory -Force $output | Out-Null
Push-Location $source
try {
  foreach ($report in $reports) {
    Write-Host "Building $report.tex"
    & xelatex -interaction=nonstopmode -halt-on-error "$report.tex"
    if ($LASTEXITCODE -ne 0) { throw "XeLaTeX pass 1 failed: $report" }
    & xelatex -interaction=nonstopmode -halt-on-error "$report.tex"
    if ($LASTEXITCODE -ne 0) { throw "XeLaTeX pass 2 failed: $report" }
    Copy-Item -LiteralPath "$report.pdf" -Destination $output -Force
    [System.IO.File]::Delete((Join-Path $source "$report.pdf"))
  }
} finally {
  Pop-Location
}
Get-ChildItem -LiteralPath $source -File | Where-Object {
  $_.Name -match '\.(aux|fdb_latexmk|fls|log|out|toc|xdv)$|\.synctex\.gz$'
} | ForEach-Object { [System.IO.File]::Delete($_.FullName) }
Write-Host "Build complete: $output"
