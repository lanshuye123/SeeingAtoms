"""Shared visual language for the series.

The palette and type choices are deliberately restrained: one dark ground,
one warm text colour, two accents for "beam" and "measurement".
"""
from pathlib import Path

from manim import Text
from manimpango import register_font

ROOT = Path(__file__).resolve().parents[2]
FONT_DIR = ROOT / "assets" / "fonts"

FONT_SANS_FILE = FONT_DIR / "SourceHanSansCN-Regular.otf"
FONT_SANS_BOLD_FILE = FONT_DIR / "SourceHanSansCN-Bold.otf"
FONT_SERIF_FILE = FONT_DIR / "SourceHanSerifCN-SemiBold.otf"
FONT_HAND_FILE = FONT_DIR / "LXGWWenKai-Regular.ttf"

FONT_SANS = "Source Han Sans CN"
FONT_SERIF = "Source Han Serif CN"
FONT_HAND = "LXGW WenKai"

COLORS = {
    "bg": "#0B1020",
    "ink": "#F4F1EA",
    "muted": "#98A2B3",
    "beam": "#6FD3C7",
    "measure": "#D8A657",
    "alert": "#E07A5F",
    "grid": "#263044",
}

_FONTS_REGISTERED = False


def register_fonts() -> None:
    """Register the bundled font files with Pango once per process."""
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    for path in (FONT_SANS_FILE, FONT_SANS_BOLD_FILE, FONT_SERIF_FILE, FONT_HAND_FILE):
        if not path.exists():
            raise FileNotFoundError(f"Bundled font missing: {path}")
        register_font(str(path))
    _FONTS_REGISTERED = True


def title(text: str, **kwargs) -> Text:
    register_fonts()
    defaults = dict(font=FONT_SANS, weight="MEDIUM", color=COLORS["ink"], font_size=64)
    defaults.update(kwargs)
    return Text(text, **defaults)


def body(text: str, **kwargs) -> Text:
    register_fonts()
    defaults = dict(font=FONT_SANS, color=COLORS["ink"], font_size=34, line_spacing=1.25)
    defaults.update(kwargs)
    return Text(text, **defaults)


def label(text: str, **kwargs) -> Text:
    register_fonts()
    defaults = dict(font=FONT_SANS, color=COLORS["muted"], font_size=24)
    defaults.update(kwargs)
    return Text(text, **defaults)


def credit(text: str, **kwargs) -> Text:
    register_fonts()
    defaults = dict(font=FONT_SANS, color=COLORS["muted"], font_size=20)
    defaults.update(kwargs)
    return Text(text, **defaults)
