param(
  [ValidateSet('all','shmry','xerus','vps','huobzlang','neuron','nifdu','sophyane')]
  [string]$Product = 'all'
)

$ErrorActionPreference = 'Stop'
$Root = if ($env:SHMRY_SOFTWARE_HOME) { $env:SHMRY_SOFTWARE_HOME } else { Join-Path $env:LOCALAPPDATA 'Shmry Software Inc' }
$Owner = 'badrpk'

$Products = @(
  @{ Key='shmry'; Repo='shmry'; Branch='main' },
  @{ Key='xerus'; Repo='xerus'; Branch='main' },
  @{ Key='vps'; Repo='vps'; Branch='main' },
  @{ Key='huobzlang'; Repo='HuobzLang'; Branch='main' },
  @{ Key='neuron'; Repo='neuron'; Branch='main' },
  @{ Key='nifdu'; Repo='nifdu'; Branch='master' },
  @{ Key='sophyane'; Repo='sophyane'; Branch='main' }
)

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git is required.' }
New-Item -ItemType Directory -Force -Path $Root | Out-Null

foreach ($p in $Products) {
  if ($Product -ne 'all' -and $Product -ne $p.Key) { continue }

  $dest = Join-Path $Root $p.Key
  $url = "https://github.com/$Owner/$($p.Repo).git"
  Write-Host "== $($p.Key) =="

  if (Test-Path (Join-Path $dest '.git')) {
    $dirty = git -C $dest status --porcelain
    if ($dirty) { throw "Refusing update: $dest has local changes" }
    git -C $dest fetch origin --tags --prune
    git -C $dest checkout $p.Branch
    git -C $dest pull --ff-only origin $p.Branch
  } elseif (Test-Path $dest) {
    throw "Refusing overwrite: $dest exists and is not a Git repository"
  } else {
    git clone --branch $p.Branch $url $dest
  }

  switch ($p.Key) {
    'sophyane' {
      & (Join-Path $dest 'install.ps1')
    }
    'neuron' {
      & (Join-Path $dest 'install.ps1')
    }
    'vps' {
      & (Join-Path $dest 'install.ps1')
    }
    default {
      Write-Host "Source installed at $dest"
      Write-Host "No universally verified Windows native installer is advertised for $($p.Key) yet."
    }
  }
}

Write-Host "Shmry Software Inc software root: $Root"
