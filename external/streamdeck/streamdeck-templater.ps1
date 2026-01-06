# Used to create an editable template from a StreamDeck "manifest.json" profile file

$script:RepoPath = $env:STREAMING_REPO_PATH

$script:RepoPath = if ($script:RepoPath) {
  ($script:RepoPath -replace '\\', '/').TrimEnd('/')
} else {
  $null
}

$script:CurrentPath = Get-Location
$script:DefaultVcPath = "external/streamdeck/version-control"

function ConvertTo-StreamDeckTemplate {
  param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [Parameter(Mandatory=$false)]
    [string]$VcRelativePath = $script:DefaultVcPath
  )

  # Convert input to absolute path
  $InputFile = (Resolve-Path $InputFile).Path
  $inputFileName = Split-Path $InputFile -Leaf
  $OutputFile = $InputFile -replace "\.json$", ".vc-template.json"

  Write-Host "Creating StreamDeck template from real config..." -ForegroundColor Green
  Write-Host "Input:  $InputFile" -ForegroundColor Gray
  Write-Host "Output: $OutputFile" -ForegroundColor Gray


  if ($script:RepoPath) {
    $vcFullPath = Join-Path ($script:RepoPath -replace '/', '\') $VcRelativePath
    $vcTemplatePath = Join-Path $vcFullPath $templateFileName

    $forwardSlashPath = $script:RepoPath
    $backslashPath = $script:RepoPath -replace '/', '\\'

    $escapedForward = [regex]::Escape($forwardSlashPath)
    $escapedBackslash = [regex]::Escape($backslashPath)

    # Ensure the VC directory exists
    if (-not (Test-Path $vcFullPath)) {
      New-Item -ItemType Directory -Path $vcFullPath -Force | Out-Null
      Write-Host "Created VC directory: $vcFullPath" -ForegroundColor Cyan
    }
  } else {
    $vcTemplatePath = Join-Path $script:CurrentPath $templateFileName
    Write-Host "Warning: STREAMING_REPO_PATH not set, saving template locally" -ForegroundColor Yellow
  }


  # CREATE BACKUP FIRST
  if ($script:RepoPath) {
    $backupFileName = $inputFileName -replace "\.json$", ".backup.json"
    $backupPath = Join-Path (Split-Path $vcTemplatePath -Parent) $backupFileName
    Copy-Item $InputFile $backupPath -Force
    Write-Host "Backup saved: $backupPath" -ForegroundColor Magenta
  } else {
    $backupPath = Join-Path $script:CurrentPath ($inputFileName -replace "\.json$", ".backup.json")
    Copy-Item $InputFile $backupPath -Force
    Write-Host "Backup saved locally, due to STREAMING_REPO_PATH not set: $backupPath" -ForegroundColor Magenta
  }

  Copy-Item $InputFile $backupPath -Force
  Write-Host "Backup saved: $backupPath" -ForegroundColor Magenta

  # Remove existing symlink before reading/writing anything
  $symlinkPath = Join-Path $script:CurrentPath $templateFileName
  if (Test-Path $symlinkPath) {
    Remove-Item $symlinkPath -Force
    Write-Host "Removed existing symlink" -ForegroundColor Gray
  }

  $content = Get-Content $InputFile -Raw

  # Replace both versions with the placeholder
  $content = $content -replace $escapedForward, "{{STREAMING_REPO_PATH}}"
  $content = $content -replace $escapedBackslash, "{{STREAMING_REPO_PATH}}"

  $content | Set-Content $OutputFile -Encoding UTF8
  Write-Host "Template saved: $OutputFile" -ForegroundColor Yellow

  # Create symlink in OBS scenes folder pointing to VC location
  if ($script:RepoPath) {
    New-Item -ItemType SymbolicLink -Path $symlinkPath -Target $vcTemplatePath | Out-Null
    Write-Host "Created symlink: $symlinkPath -> $vcTemplatePath" -ForegroundColor Green
  } else {
    Write-Host "Warning: STREAMING_REPO_PATH not set, symlink not created" -ForegroundColor Yellow
  }
}

function ConvertFrom-StreamDeckTemplate {
  param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile
  )

  $OutputFile = $InputFile -replace "\.template\.", "."

  Write-Host "Creating real StreamDeck config from template..." -ForegroundColor Green
  Write-Host "Input:  $InputFile" -ForegroundColor Gray
  Write-Host "Output: $OutputFile" -ForegroundColor Gray

  $content = Get-Content $InputFile -Raw

  if ($content -match "{{STREAMING_REPO_PATH}}" -and -not $script:RepoPath) {
    throw "Template contains {{STREAMING_REPO_PATH}} but STREAMING_REPO_PATH environment variable is not set"
  }

  if ($script:RepoPath) {
    # Replace with backslash version for Windows paths
    $windowsPath = $script:RepoPath -replace '/', '\\'
    $content = $content -replace "{{STREAMING_REPO_PATH}}", $windowsPath
  }

  $content | Set-Content $OutputFile -Encoding UTF8
  Write-Host "Real config saved: $OutputFile" -ForegroundColor Yellow
}

Write-Host "StreamDeck Templater functions loaded!" -ForegroundColor Green
Write-Host "Current paths:" -ForegroundColor Cyan
Write-Host "  Repo Path: $($script:RepoPath ?? 'Not set')" -ForegroundColor Gray
Write-Host ""
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  ConvertTo-StreamDeckTemplate 'manifest.json'             # Creates manifest.vc-template.json" -ForegroundColor Gray
Write-Host "  ConvertFrom-StreamDeckTemplate 'manifest.vc-template.json'  # Creates manifest.json" -ForegroundColor Gray
