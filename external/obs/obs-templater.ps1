# Used to create an editable template from an OBS "scenes.json" file

$script:DataPath = $env:STREAMING_DATA_PATH
$script:RepoPath = $env:STREAMING_REPO_PATH

# Validate environment setup
if (-not $script:RepoPath) {
  throw "STREAMING_REPO_PATH environment variable is not set. Please set it
    before running this script."
}

if (-not $script:DataPath) {
  throw "Warning: STREAMING_DATA_PATH environment variable is not set. Please
    set it before running this script."
}

# Normalize paths to use forward slashes and trim trailing slashes
$script:DataPath = if ($script:DataPath) {
  ($script:DataPath -replace '\\', '/').TrimEnd('/')
} else {
  $null
}

$script:RepoPath = if ($script:RepoPath) {
  ($script:RepoPath -replace '\\', '/').TrimEnd('/')
} else {
  $null
}

$script:DefaultVcPath = "external/obs/version-control"

function ConvertTo-ObsTemplate {
  param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [Parameter(Mandatory=$false)]
    [string]$VcRelativePath = $script:DefaultVcPath
  )

  # Convert input to absolute path
  $InputFile = (Resolve-Path $InputFile).Path
  $inputFileName = Split-Path $InputFile -Leaf
  $inputDirectory = Split-Path $InputFile -Parent
  $templateFileName = $inputFileName -replace "\.json$", ".vc-template.json"

  Write-Host "Creating template from real config..." -ForegroundColor Green
  Write-Host "Input:  $InputFile" -ForegroundColor Gray

  # Setup paths
  $vcFullPath = Join-Path ($script:RepoPath -replace '/', '\') $VcRelativePath
  $vcTemplatePath = Join-Path $vcFullPath $templateFileName

  Write-Host "Output: $vcTemplatePath" -ForegroundColor Gray

  # Ensure the VC directory exists
  if (-not (Test-Path $vcFullPath)) {
    New-Item -ItemType Directory -Path $vcFullPath -Force | Out-Null
    Write-Host "Created VC directory: $vcFullPath" -ForegroundColor Cyan
  }

  # CREATE BACKUP FIRST
  $backupFileName = $inputFileName -replace "\.json$", ".backup.json"
  $backupPath = Join-Path $vcFullPath $backupFileName
  Copy-Item $InputFile $backupPath -Force
  Write-Host "Backup saved: $backupPath" -ForegroundColor Magenta

  # Remove existing symlink before reading/writing anything
  $symlinkPath = Join-Path $inputDirectory $templateFileName
  if (Test-Path $symlinkPath) {
    Remove-Item $symlinkPath -Force
    Write-Host "Removed existing template/symlink" -ForegroundColor Gray
  }

  # Read and process content
  $content = Get-Content $InputFile -Raw

  # Replace actual paths with placeholders
  $content = $content -replace [regex]::Escape($script:RepoPath), "{{STREAMING_REPO_PATH}}"
  $content = $content -replace [regex]::Escape($script:DataPath), "{{STREAMING_DATA_PATH}}"
  $content | Set-Content $vcTemplatePath -Encoding UTF8
  Write-Host "Template saved: $vcTemplatePath" -ForegroundColor Yellow

  # Create symlink in OBS scenes folder pointing to VC location
  New-Item -ItemType SymbolicLink -Path $symlinkPath -Target $vcTemplatePath | Out-Null
  Write-Host "Created symlink: $symlinkPath -> $vcTemplatePath" -ForegroundColor Green
}

function ConvertFrom-ObsTemplate {
  param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile
  )

  $OutputFile = $InputFile -replace "\.vc-template\.", "."

  Write-Host "Creating real config from template..." -ForegroundColor Green
  Write-Host "Input:  $InputFile" -ForegroundColor Gray
  Write-Host "Output: $OutputFile" -ForegroundColor Gray

  $content = Get-Content $InputFile -Raw

  # Replace placeholders
  $content = $content -replace "{{STREAMING_REPO_PATH}}", $script:RepoPath
  $content = $content -replace "{{STREAMING_DATA_PATH}}", $script:DataPath

  $content | Set-Content $OutputFile -Encoding UTF8
  Write-Host "Real config saved: $OutputFile" -ForegroundColor Yellow
}

Write-Host "OBS Templater functions loaded!" -ForegroundColor Green
Write-Host "Current paths:" -ForegroundColor Cyan
Write-Host "  Data Path: $($script:DataPath ?? 'Not set')" -ForegroundColor Gray
Write-Host "  Repo Path: $($script:RepoPath ?? 'Not set')" -ForegroundColor Gray
Write-Host "  The script should be used in $env:APPDATA\obs-studio\basic\scenes" -ForegroundColor Gray
Write-Host "  Default VC Path: $script:DefaultVcPath" -ForegroundColor Gray
Write-Host ""
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  ConvertTo-ObsTemplate 'Dota.json'                # Uses default VC path, creates symlink" -ForegroundColor Gray
Write-Host "  ConvertTo-ObsTemplate 'Dota.json' 'custom/path'  # Uses custom VC path" -ForegroundColor Gray
Write-Host "  ConvertFrom-ObsTemplate 'Dota.vc-template.json'" -ForegroundColor Gray

