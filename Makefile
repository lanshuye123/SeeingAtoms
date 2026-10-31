SHELL := /bin/bash
ROOT := $(CURDIR)
TEX_BIN := /home/lanshuye/Apps/texlive/2025/bin/x86_64-linux
UV_CACHE_DIR := $(ROOT)/.cache/uv
XDG_CACHE_HOME := $(ROOT)/.cache/xdg
MPLCONFIGDIR := $(ROOT)/.cache/mpl
NUMBA_CACHE_DIR := $(ROOT)/.cache/numba
TTS_PY := /home/lanshuye/miniconda3/envs/qwen3-tts/bin/python

export PATH := $(TEX_BIN):$(PATH)

.PHONY: env fonts smoke tex-smoke copy-check tts-dry tts-check patterns audio srt ass scenes credits cover concat final clean-preview

env:
	bash scripts/check_env.sh

fonts:
	bash scripts/fetch_fonts.sh

smoke:
	UV_CACHE_DIR="$(UV_CACHE_DIR)" XDG_CACHE_HOME="$(XDG_CACHE_HOME)" MPLCONFIGDIR="$(MPLCONFIGDIR)" \
	.venv/bin/manim -qh --fps 30 -s --media_dir media src/render/manim_smoke_test.py CJKSmokeTest

tex-smoke:
	UV_CACHE_DIR="$(UV_CACHE_DIR)" XDG_CACHE_HOME="$(XDG_CACHE_HOME)" MPLCONFIGDIR="$(MPLCONFIGDIR)" \
	.venv/bin/manim -qh --fps 30 -s --media_dir media src/render/tex_smoke_test.py TeXSmokeTest

copy-check:
	python3 scripts/check_copy.py chapters/s01/script/narration.txt

tts-dry:
	NUMBA_CACHE_DIR="$(NUMBA_CACHE_DIR)" "$(TTS_PY)" src/tts/generate_narration.py \
		--segments-json chapters/s01/script/segments.json \
		--out-dir chapters/s01/audio/segments --device auto --dry-run

tts-check:
	NUMBA_CACHE_DIR="$(NUMBA_CACHE_DIR)" "$(TTS_PY)" -c \
		"import torch, qwen_tts; print('qwen_tts ok; cuda=', torch.cuda.is_available(), 'device_count=', torch.cuda.device_count())"

patterns:
	.venv/bin/python scripts/build_xrd_patterns.py

audio:
	.venv/bin/python scripts/build_audio.py
	.venv/bin/python scripts/build_music.py --main-duration 508.2 --credits-duration 70.0
	.venv/bin/python scripts/mix_audio.py

srt:
	.venv/bin/python scripts/build_srt.py
	.venv/bin/python scripts/build_ass.py

scenes:
	mkdir -p chapters/s01/renders/segments
	for s in S00 S01 S02 S03 S04 S05 S06 S07 S08 S09; do \
		UV_CACHE_DIR="$(UV_CACHE_DIR)" XDG_CACHE_HOME="$(XDG_CACHE_HOME)" MPLCONFIGDIR="$(MPLCONFIGDIR)" \
		.venv/bin/manim -qh --fps 30 --media_dir media chapters/s01/manim/scenes.py $$s || exit 1; \
		cp "media/videos/scenes/1080p30/$$s.mp4" "chapters/s01/renders/segments/$$s.mp4"; \
	done

credits:
	UV_CACHE_DIR="$(UV_CACHE_DIR)" XDG_CACHE_HOME="$(XDG_CACHE_HOME)" MPLCONFIGDIR="$(MPLCONFIGDIR)" \
	.venv/bin/manim -qh --fps 30 --media_dir media chapters/s01/manim/credits.py S10Credits
	cp media/videos/credits/1080p30/S10Credits.mp4 chapters/s01/renders/segments/S10_credits.mp4

cover:
	UV_CACHE_DIR="$(UV_CACHE_DIR)" XDG_CACHE_HOME="$(XDG_CACHE_HOME)" MPLCONFIGDIR="$(MPLCONFIGDIR)" \
	.venv/bin/manim -qh --fps 30 -s --media_dir media chapters/s01/manim/cover.py S01Cover
	cp media/images/cover/S01Cover_ManimCE_v0.19.0.png chapters/s01/renders/cover.png
	ffmpeg -hide_banner -loglevel error -y -i chapters/s01/renders/cover.png \
		-vf "crop=1440:1080:240:0" chapters/s01/renders/cover_4x3_preview.png

concat:
	ffmpeg -hide_banner -y -f concat -safe 0 -i chapters/s01/renders/concat.txt -c copy chapters/s01/renders/s01_silent.mp4

final:
	ffmpeg -hide_banner -y -i chapters/s01/renders/s01_silent.mp4 -i chapters/s01/audio/s01_mix.wav \
		-vf "ass=chapters/s01/renders/s01_final.ass:fontsdir=assets/fonts" \
		-c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -r 30 \
		-c:a aac -b:a 192k -ar 48000 -ac 2 -movflags +faststart -shortest \
		-metadata title="看见原子 · 第一期" \
		chapters/s01/renders/s01_final.mp4

clean-preview:
	rm -rf media/images/manim_smoke_test media/images/tex_smoke_test media/texts
