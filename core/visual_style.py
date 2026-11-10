"""
Shared visual design system for AI Shorts.

This file contains visual constants and small style helpers only. It does not
depend on Manim, so it can be imported by storyboard validation, asset tools,
and rendering code without loading the animation engine.

Fonts are referenced by family name. Install the font files in assets/fonts
and register them with the runtime environment when rendering in Manim.
"""

from __future__ import annotations

from datetime import datetime


def log_progress(message: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [STYLE] {message}", flush=True)


log_progress("Loading shared visual style...")

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

COLORS = {
    "background": "#080D19",
    "background_secondary": "#101A2B",
    "surface": "#142238",
    "surface_highlight": "#1C304A",
    "text_primary": "#F5F7FA",
    "text_secondary": "#AAB6C8",
    "text_muted": "#718096",
    "accent": "#42C8F5",
    "accent_secondary": "#8A7CFF",
    "warm": "#FFB547",
    "danger": "#FF5263",
    "success": "#54D6A0",
    "earth_ocean": "#176B9B",
    "earth_land": "#6F9B65",
    "earth_land_dark": "#426B50",
    "earth_cloud": "#EAF4F8",
    "atmosphere": "#55CFFF",
    "water": "#087EBD",
}

log_progress(f"Loaded {len(COLORS)} colour tokens.")

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------

FONTS = {
    "title": "Space Grotesk",
    "heading": "Space Grotesk",
    "body": "Inter",
    "label": "Inter",
    "numeric": "Space Grotesk",
}

# Sizes are Manim logical font sizes, not pixel values. Adjust after the first
# 1080x1920 test render rather than assuming one size fits every scene.
FONT_SIZES = {
    "hero": 0.78,
    "title": 0.62,
    "section": 0.48,
    "body": 0.34,
    "label": 0.25,
    "small": 0.20,
    "numeric": 0.90,
}

FONT_WEIGHTS = {
    "title": "BOLD",
    "heading": "BOLD",
    "body": "NORMAL",
    "label": "MEDIUM",
    "numeric": "BOLD",
}

log_progress("Typography tokens loaded.")

# ---------------------------------------------------------------------------
# Layout and shape language
# ---------------------------------------------------------------------------

LAYOUT = {
    "safe_margin_x": 0.55,
    "safe_margin_top": 0.65,
    "safe_margin_bottom": 1.85,
    "content_width": 6.45,
    "card_corner_radius": 0.16,
    "card_padding": 0.22,
    "element_gap": 0.16,
    "title_to_content_gap": 0.30,
}

STROKES = {
    "thin": 1.2,
    "regular": 2.0,
    "emphasis": 3.2,
    "outline": 1.5,
}

ANIMATION = {
    "quick": 0.25,
    "standard": 0.45,
    "emphasis": 0.75,
    "transition": 0.55,
}

# These values are visual defaults, not mandatory values. Individual scenes
# can override them when a specific shot needs a different treatment.
EFFECTS = {
    "subtle_glow_opacity": 0.18,
    "highlight_opacity": 0.22,
    "shadow_opacity": 0.25,
}

log_progress("Layout, stroke, animation and effect tokens loaded.")


def color(name: str) -> str:
    """Return a named palette colour with a useful error for unknown names."""
    try:
        return COLORS[name]
    except KeyError as exc:
        available = ", ".join(sorted(COLORS))
        raise KeyError(f"Unknown colour {name!r}. Available: {available}") from exc


def font(role: str) -> str:
    """Return a font family for a semantic typography role."""
    try:
        return FONTS[role]
    except KeyError as exc:
        available = ", ".join(sorted(FONTS))
        raise KeyError(f"Unknown font role {role!r}. Available: {available}") from exc


def font_size(role: str) -> float:
    """Return a logical Manim font size for a semantic role."""
    try:
        return FONT_SIZES[role]
    except KeyError as exc:
        available = ", ".join(sorted(FONT_SIZES))
        raise KeyError(f"Unknown font-size role {role!r}. Available: {available}") from exc


log_progress("Shared visual style ready.")
