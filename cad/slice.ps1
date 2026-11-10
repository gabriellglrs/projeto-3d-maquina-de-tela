# Fatiar STL no OrcaSlicer via CLI
param(
    [Parameter(Mandatory = $true)][string]$Stl,
    [ValidateSet("base", "part", "solid")][string]$Profile = "part",
    [string]$Out = "C:\DEV\3dprint\export"
)

$ErrorActionPreference = "Continue"
$exe = "C:\Program Files\OrcaSlicer\orca-slicer.exe"
$dir = "C:\DEV\3dprint\orca_profiles"

New-Item -ItemType Directory -Force -Path $Out | Out-Null

$machine = Join-Path $dir "machine.json"
$process = Join-Path $dir "process_$Profile.json"
$filament = Join-Path $dir "filament_pla.json"

foreach ($f in @($exe, $machine, $process, $filament, $Stl)) {
    if (-not (Test-Path -LiteralPath $f)) {
        Write-Host "FALTANDO: $f"
        exit 1
    }
}

$base = [System.IO.Path]::GetFileNameWithoutExtension($Stl)
$logOut = Join-Path $Out "orca_stdout.txt"
$logErr = Join-Path $Out "orca_stderr.txt"

$argList = @(
    "--slice", "0",
    "--outputdir", $Out,
    "--load-settings", "$machine;$process",
    "--load-filaments", $filament,
    $Stl
)

Write-Host "== fatiando: $base  (perfil: $Profile)"
$proc = Start-Process -FilePath $exe -ArgumentList $argList -Wait -PassThru `
    -RedirectStandardOutput $logOut -RedirectStandardError $logErr

Write-Host "== exit code: $($proc.ExitCode)"
$so = Get-Content -LiteralPath $logOut -ErrorAction SilentlyContinue
$se = Get-Content -LiteralPath $logErr -ErrorAction SilentlyContinue
if ($so) { Write-Host "== stdout:"; $so | Select-Object -Last 30 }
if ($se) { Write-Host "== stderr:"; $se | Select-Object -Last 15 }

$g = Join-Path $Out "plate_1.gcode"
if ($proc.ExitCode -eq 0 -and (Test-Path -LiteralPath $g)) {
    $final = Join-Path $Out "$base.gcode"
    Move-Item -LiteralPath $g -Destination $final -Force
    $kb = [math]::Round((Get-Item -LiteralPath $final).Length / 1KB)
    Write-Host "== OK -> $final ($kb KB)"
}
else {
    Write-Host "== FALHOU"
    exit 2
}
