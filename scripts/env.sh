# Source this file before rendering or generating narration:
#   source scripts/env.sh
#
# It centralizes the non-default paths used by this project.
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export PROJECT_ROOT
export PATH="/home/lanshuye/Apps/texlive/2025/bin/x86_64-linux:$PATH"
export UV_CACHE_DIR="$PROJECT_ROOT/.cache/uv"
export XDG_CACHE_HOME="$PROJECT_ROOT/.cache/xdg"
export MPLCONFIGDIR="$PROJECT_ROOT/.cache/mpl"
export NUMBA_CACHE_DIR="$PROJECT_ROOT/.cache/numba"

mkdir -p "$UV_CACHE_DIR" "$XDG_CACHE_HOME" "$MPLCONFIGDIR" "$NUMBA_CACHE_DIR"
