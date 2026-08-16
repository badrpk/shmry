#!/usr/bin/env bash
set -euo pipefail

ROOT="${SHMRY_SOFTWARE_HOME:-$HOME/.local/share/shmry-software-inc}"
OWNER="badrpk"

products=(shmry xerus vps HuobzLang neuron nifdu sophyane)
branches=(main main main main main master main)

usage(){
  cat <<'EOF'
Shmry Software Inc universal downloader

Usage:
  install.sh [all|shmry|xerus|vps|huobzlang|neuron|nifdu|sophyane]

The downloader clones or fast-forwards clean repositories. Product installers
are invoked when a verified native installer is available.
EOF
}

choice="${1:-all}"
case "$choice" in
  all|shmry|xerus|vps|huobzlang|neuron|nifdu|sophyane) ;;
  -h|--help) usage; exit 0 ;;
  *) usage >&2; exit 2 ;;
esac

command -v git >/dev/null 2>&1 || { echo "git is required" >&2; exit 2; }
mkdir -p "$ROOT"

install_one(){
  local key="$1" repo="$2" branch="$3"
  local dest="$ROOT/$key"
  local url="https://github.com/$OWNER/$repo.git"

  echo "== $key =="
  if [ -d "$dest/.git" ]; then
    test -z "$(git -C "$dest" status --porcelain)" || { echo "Refusing update: $dest has local changes" >&2; return 3; }
    git -C "$dest" fetch origin --tags --prune
    git -C "$dest" checkout "$branch"
    git -C "$dest" pull --ff-only origin "$branch"
  elif [ -e "$dest" ]; then
    echo "Refusing overwrite: $dest exists and is not a Git repository" >&2
    return 3
  else
    git clone --branch "$branch" "$url" "$dest"
  fi

  case "$key" in
    sophyane)
      bash "$dest/install.sh"
      ;;
    nifdu)
      if [ -f "$dest/install-nifdu.sh" ]; then bash "$dest/install-nifdu.sh"; fi
      ;;
    neuron|vps)
      bash "$dest/install.sh"
      ;;
    *)
      echo "Source installed at $dest"
      echo "No universally verified native installer is advertised for $key yet."
      ;;
  esac
}

for i in "${!products[@]}"; do
  repo="${products[$i]}"
  branch="${branches[$i]}"
  key="${repo,,}"
  [ "$repo" = "HuobzLang" ] && key="huobzlang"
  if [ "$choice" = "all" ] || [ "$choice" = "$key" ]; then
    install_one "$key" "$repo" "$branch"
  fi
done

echo "Shmry Software Inc software root: $ROOT"
