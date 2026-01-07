# Used to create an editable template from a StreamDeck "manifest.json" profile file

$script:RepoPath = $env:STREAMING_REPO_PATH

if (-not $script:RepoPath) {
  throw "STREAMING_REPO_PATH environment variable is not set. Please set it
    before running this script."
}

$script:RepoPath = if ($script:RepoPath) {
  ($script:RepoPath -replace '\\', '/').TrimEnd('/')
} else {
  $null
}

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
  $inputDirectory = Split-Path $InputFile -Parent
  $templateFileName = $inputFileName -replace "\.json$", ".vc-template.json"

  Write-Host "Creating StreamDeck template from real config..." -ForegroundColor Green
  Write-Host "Input:  $InputFile" -ForegroundColor Gray

  # Setup paths
  $vcFullPath = Join-Path ($script:RepoPath -replace '/', '\') $VcRelativePath
  $vcTemplatePath = Join-Path $vcFullPath $templateFileName

  Write-Host "Output: $vcTemplatePath" -ForegroundColor Gray

  $forwardSlashPath = $script:RepoPath
  $backslashPath = $script:RepoPath -replace '/', '\\'
  $escapedForward = [regex]::Escape($forwardSlashPath)
  $escapedBackslash = [regex]::Escape($backslashPath)

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

  # Remove existing template file or symlink in input directory
  $symlinkPath = Join-Path $inputDirectory $templateFileName
  if (Test-Path $symlinkPath) {
    Remove-Item $symlinkPath -Force
    Write-Host "Removed existing template/symlink" -ForegroundColor Gray
  }

  # Read and process content
  $content = Get-Content $InputFile -Raw

  # Replace both versions with the placeholder
  $content = $content -replace $escapedForward, "{{STREAMING_REPO_PATH}}"
  $content = $content -replace $escapedBackslash, "{{STREAMING_REPO_PATH}}"
  $content | Set-Content $vcTemplatePath -Encoding UTF8
  Write-Host "Template saved: $vcTemplatePath" -ForegroundColor Yellow

  # Create symlink in input directory pointing to VC directory
  New-Item -ItemType SymbolicLink -Path $symlinkPath -Target $vcTemplatePath | Out-Null
  Write-Host "Created symlink: $symlinkPath -> $vcTemplatePath" -ForegroundColor Green
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

  # Replace with backslash version for Windows paths
  $windowsPath = $script:RepoPath -replace '/', '\\'
  $content = $content -replace "{{STREAMING_REPO_PATH}}", $windowsPath

  $content | Set-Content $OutputFile -Encoding UTF8
  Write-Host "Real config saved: $OutputFile" -ForegroundColor Yellow
}

Write-Host "StreamDeck Templater functions loaded!" -ForegroundColor Green
Write-Host "Current paths:" -ForegroundColor Cyan
Write-Host "  Repo Path: $($script:RepoPath ?? 'Not set')" -ForegroundColor Gray
Write-Host "  The script should be used in a $env:APPDATA\Elgato\StreamDeck\ProfilesV2\#num\Profiles\#num folder" -ForegroundColor Gray
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  ConvertTo-StreamDeckTemplate 'manifest.json'                # Creates manifest.vc-template.json" -ForegroundColor Gray
Write-Host "  ConvertFrom-StreamDeckTemplate 'manifest.vc-template.json'  # Creates manifest.json" -ForegroundColor Gray
