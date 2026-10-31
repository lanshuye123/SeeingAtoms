#!/usr/bin/env bash
# Environment check for the science-video project.
# Usage: bash scripts/check_env.sh
set -u

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/environment_check.txt"
mkdir -p "$LOG_DIR" "$ROOT/.cache/numba"

# Keep a copy for the operator and show it on stdout.
exec > >(tee "$LOG") 2>&1

FAIL=0
WARN=0

pass() { printf '  [ OK ] %s\n' "$*"; }
warn() { printf '  [WARN] %s\n' "$*"; WARN=$((WARN + 1)); }
fail() { printf '  [FAIL] %s\n' "$*"; FAIL=$((FAIL + 1)); }
section() { printf '\n== %s ==\n' "$*"; }

section "Project"
printf 'root: %s\n' "$ROOT"
printf 'date: %s\n' "$(date -Iseconds)"
printf 'disk: %s\n' "$(df -h "$ROOT" | tail -1)"

section "Core tools"
for cmd in ffmpeg ffprobe uv python3 make; do
  if command -v "$cmd" >/dev/null 2>&1; then
    pass "$cmd: $(command -v "$cmd")"
  else
    fail "$cmd not found"
  fi
done

if ffmpeg -hide_banner -version >/dev/null 2>&1; then
  ffmpeg -hide_banner -version | head -1 | sed 's/^/         /'
fi
if ffmpeg -hide_banner -filters 2>/dev/null | grep -q 'loudnorm'; then
  pass "ffmpeg filter: loudnorm"
else
  fail "ffmpeg filter missing: loudnorm"
fi
if ffmpeg -hide_banner -filters 2>/dev/null | grep -q 'subtitles'; then
  pass "ffmpeg filter: subtitles/libass"
else
  warn "ffmpeg subtitles filter not found; SRT burn-in may need another path"
fi
if ffmpeg -hide_banner -encoders 2>/dev/null | grep -q 'libx264'; then
  pass "ffmpeg encoder: libx264"
else
  fail "ffmpeg encoder missing: libx264"
fi
if ffmpeg -hide_banner -encoders 2>/dev/null | grep -q ' aac '; then
  pass "ffmpeg encoder: aac"
else
  fail "ffmpeg encoder missing: aac"
fi

section "Manim environment"
MANIM="$ROOT/.venv/bin/manim"
if [ -x "$MANIM" ]; then
  pass "manim binary: $MANIM"
  if "$ROOT/.venv/bin/python" -c 'import manim; print(manim.__version__)' >/tmp/manim_version.$$ 2>&1; then
    pass "manim version: $(cat /tmp/manim_version.$$)"
  else
    fail "manim import failed"
  fi
  rm -f /tmp/manim_version.$$
else
  fail "manim binary missing: $MANIM (run uv venv + uv pip install manim)"
fi
TEX_BIN="/home/lanshuye/Apps/texlive/2025/bin/x86_64-linux"
if [ -x "$TEX_BIN/xelatex" ]; then
  pass "xelatex: $TEX_BIN/xelatex"
else
  fail "xelatex missing: $TEX_BIN/xelatex"
fi
for tool in latex dvisvgm; do
  if [ -x "$TEX_BIN/$tool" ]; then
    pass "TeX tool: $tool"
  else
    fail "TeX tool missing: $TEX_BIN/$tool"
  fi
done
if PATH="$TEX_BIN:$PATH" command -v xelatex >/dev/null 2>&1; then
  pass "TeX Live is usable when scripts/env.sh is sourced"
else
  fail "TeX Live not usable even with PATH override"
fi

section "Fonts"
for f in \
  SourceHanSansCN-Regular.otf \
  SourceHanSansCN-Bold.otf \
  SourceHanSerifCN-Regular.otf \
  SourceHanSerifCN-SemiBold.otf \
  LXGWWenKai-Regular.ttf; do
  if [ -s "$ROOT/assets/fonts/$f" ]; then
    pass "font: $f ($(du -h "$ROOT/assets/fonts/$f" | cut -f1))"
  else
    fail "font missing or empty: $f"
  fi
done
for f in LICENSE-SourceHanSans.txt LICENSE-SourceHanSerif.txt OFL-LXGWWenKai.txt; do
  if [ -s "$ROOT/assets/fonts/$f" ]; then
    pass "license: $f"
  else
    fail "license missing: $f"
  fi
done

section "TTS"
TTS_PY="/home/lanshuye/miniconda3/envs/qwen3-tts/bin/python"
MODEL="/home/lanshuye/Projects/QwenTTS/Qwen3-TTS-12Hz-0.6B-CustomVoice"
if [ -x "$TTS_PY" ]; then
  pass "TTS python: $TTS_PY"
  if "$TTS_PY" --version >/dev/null 2>&1; then
    printf '         %s\n' "$("$TTS_PY" --version 2>&1)"
  fi
else
  fail "TTS python missing: $TTS_PY"
fi
if [ -d "$MODEL" ]; then
  pass "TTS model: $MODEL"
else
  fail "TTS model missing: $MODEL"
fi
if [ -x "$TTS_PY" ] && [ -d "$MODEL" ]; then
  NUMBA_CACHE_DIR="$ROOT/.cache/numba" "$TTS_PY" - <<'PY' >/tmp/tts_check.$$ 2>&1
import torch
import qwen_tts
print("qwen_tts import: ok")
print("torch:", torch.__version__)
print("cuda:", torch.cuda.is_available())
print("device_count:", torch.cuda.device_count())
PY
  if [ $? -eq 0 ]; then
    pass "qwen_tts import: ok"
    grep -E 'torch:|cuda:|device_count:' /tmp/tts_check.$$ | sed 's/^/         /'
    if grep -q 'cuda: True' /tmp/tts_check.$$; then
      pass "CUDA available"
    else
      warn "CUDA unavailable; TTS will run on CPU (about 5-6x realtime)"
    fi
  else
    fail "qwen_tts import failed; see below"
    tail -12 /tmp/tts_check.$$ | sed 's/^/         /'
  fi
  rm -f /tmp/tts_check.$$
fi

section "Course notes"
for d in "X射线晶体学" "显微结构分析"; do
  if [ -d "/home/lanshuye/文档/课程电子笔记/$d" ]; then
    pass "notes: $d"
  else
    fail "notes missing: $d"
  fi
done

section "GPU (informational)"
if command -v nvidia-smi >/dev/null 2>&1; then
  if timeout 8 nvidia-smi --query-gpu=name,memory.total --format=csv,noheader 2>/dev/null; then
    pass "nvidia-smi responded"
  else
    warn "nvidia-smi present but not responding; CPU fallback expected"
  fi
else
  warn "nvidia-smi not found; CPU fallback expected"
fi

printf '\n== SUMMARY ==\n'
printf 'failures: %d\nwarnings: %d\n' "$FAIL" "$WARN"
printf 'log: %s\n' "$LOG"
if [ "$FAIL" -gt 0 ]; then
  printf 'RESULT: FAIL\n'
  exit 1
fi
printf 'RESULT: PASS (warnings are non-blocking)\n'
