# Used to create an editable template from a OBS scenes file

$script:DataPath = $env:STREAMING_DATA_PATH
$script:RepoPath = $env:STREAMING_REPO_PATH

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

$script:ObsScenesPath = "$env:APPDATA\obs-studio\basic\scenes"
$script:DefaultVcPath = "external/obs/version-control"  # Default VC path in repo

function ConvertTo-ObsTemplate {
  param(
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [Parameter(Mandatory=$false)]
    [string]$VcRelativePath = $script:DefaultVcPath  # Use default if not specified
  )

  # Convert input to absolute path
  $InputFile = (Resolve-Path $InputFile).Path
  $inputFileName = Split-Path $InputFile -Leaf
  $templateFileName = $inputFileName -replace "\.json$", ".vc-template.json"

  Write-Host "Creating template from real config..." -ForegroundColor Green
  Write-Host "Input:  $InputFile" -ForegroundColor Gray

  # Determine final VC location
  if ($script:RepoPath) {
    $vcFullPath = Join-Path ($script:RepoPath -replace '/', '\') $VcRelativePath
    $vcTemplatePath = Join-Path $vcFullPath $templateFileName

    # Ensure the VC directory exists
    if (-not (Test-Path $vcFullPath)) {
      New-Item -ItemType Directory -Path $vcFullPath -Force | Out-Null
      Write-Host "Created VC directory: $vcFullPath" -ForegroundColor Cyan
    }
  }

  Write-Host "Output: $vcTemplatePath" -ForegroundColor Gray

  # CREATE BACKUP FIRST
  if ($script:RepoPath) {
    $backupFileName = $inputFileName -replace "\.json$", ".backup.json"
    $backupPath = Join-Path (Split-Path $vcTemplatePath -Parent) $backupFileName
    Copy-Item $InputFile $backupPath -Force
    Write-Host "Backup saved: $backupPath" -ForegroundColor Magenta
  }

  # Define symlink path in OBS scenes folder
  $symlinkPath = Join-Path $script:ObsScenesPath $templateFileName

  # Remove existing symlink BEFORE reading/writing anything
  if (Test-Path $symlinkPath) {
    Remove-Item $symlinkPath -Force
    Write-Host "Removed existing symlink in OBS scenes" -ForegroundColor Gray
  }

  # Read and transform content
  $content = Get-Content $InputFile -Raw

  # Replace paths in order of specificity (more specific first)
  if ($script:RepoPath) {
    $content = $content -replace [regex]::Escape($script:RepoPath), "{{STREAMING_REPO_PATH}}"
  }

  if ($script:DataPath) {
    $content = $content -replace [regex]::Escape($script:DataPath), "{{STREAMING_DATA_PATH}}"
  }

  # Write directly to VC location (no symlinks exist at this point)
  $content | Set-Content $vcTemplatePath -Encoding UTF8
  Write-Host "Template saved: $vcTemplatePath" -ForegroundColor Yellow

  # Create symlink in OBS scenes folder pointing to VC location
  if ($script:RepoPath) {
    New-Item -ItemType SymbolicLink -Path $symlinkPath -Target $vcTemplatePath | Out-Null
    Write-Host "Created symlink: $symlinkPath -> $vcTemplatePath" -ForegroundColor Green
  } else {
    Write-Host "Warning: STREAMING_REPO_PATH not set, symlink not created" -ForegroundColor Yellow
  }
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

  # Validate required variables
  if ($content -match "{{STREAMING_DATA_PATH}}" -and -not $script:DataPath) {
    throw "Template contains {{STREAMING_DATA_PATH}} but STREAMING_DATA_PATH environment variable is not set"
  }

  if ($content -match "{{STREAMING_REPO_PATH}}" -and -not $script:RepoPath) {
    throw "Template contains {{STREAMING_REPO_PATH}} but STREAMING_REPO_PATH environment variable is not set"
  }

  # Replace placeholders
  if ($script:RepoPath) {
    $content = $content -replace "{{STREAMING_REPO_PATH}}", $script:RepoPath
  }

  if ($script:DataPath) {
    $content = $content -replace "{{STREAMING_DATA_PATH}}", $script:DataPath
  }

  $content | Set-Content $OutputFile -Encoding UTF8
  Write-Host "Real config saved: $OutputFile" -ForegroundColor Yellow
}

Write-Host "OBS Templater functions loaded!" -ForegroundColor Green
Write-Host "Current paths:" -ForegroundColor Cyan
Write-Host "  Data Path: $($script:DataPath ?? 'Not set')" -ForegroundColor Gray
Write-Host "  Repo Path: $($script:RepoPath ?? 'Not set')" -ForegroundColor Gray
Write-Host "  OBS Scenes: $script:ObsScenesPath" -ForegroundColor Gray
Write-Host "  Default VC Path: $script:DefaultVcPath" -ForegroundColor Gray
Write-Host ""
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  ConvertTo-ObsTemplate 'Dota.json'                # Uses default VC path, creates symlink" -ForegroundColor Gray
Write-Host "  ConvertTo-ObsTemplate 'Dota.json' 'custom/path'  # Uses custom VC path" -ForegroundColor Gray
Write-Host "  ConvertFrom-ObsTemplate 'Dota.vc-template.json'" -ForegroundColor Gray

