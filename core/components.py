"""
Reusable Manim components for AI Shorts.

Keep this module limited to components that are genuinely reusable. Video-
specific choreography belongs in videos/<video_id>/scene.py.

Manim is imported here because these classes inherit from or construct Manim
objects. Install Manim before importing this module.
"""

from __future__ import annotations

from datetime import datetime
from typing import Iterable, Optional

from manim import (
    Annulus,
    Arc,
    Arrow,
    Circle,
    Dot,
    DOWN,
    LEFT,
    Line,
    MathTex,
    ORIGIN,
    RIGHT,
    RoundedRectangle,
    Text,
    UP,
    VGroup,
    VMobject,
    WHITE,
    BLUE,
    YELLOW,
)

try:
    from .visual_style import COLORS, FONTS, FONT_SIZES, LAYOUT, STROKES
except ImportError:
    # Also supports direct imports when global/ is added to sys.path.
    from visual_style import COLORS, FONTS, FONT_SIZES, LAYOUT, STROKES


def log_progress(message: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [COMPONENTS] {message}", flush=True)


log_progress("Reusable Manim components module loaded.")


class StyledText(Text):
    """Text wrapper using the shared typography roles."""

    def __init__(
        self,
        text: str,
        role: str = "body",
        color: Optional[str] = None,
        **kwargs,
    ):
        log_progress(f"Creating StyledText: role={role}, text={text[:36]!r}")
        super().__init__(
            text,
            font=FONTS.get(role, FONTS["body"]),
            font_size=kwargs.pop("font_size", FONT_SIZES.get(role, FONT_SIZES["body"]) * 48),
            color=color or COLORS["text_primary"],
            **kwargs,
        )


class InfoCard(VGroup):
    """Simple reusable information card with a heading and supporting text."""

    def __init__(
        self,
        heading: str,
        body: str,
        accent: Optional[str] = None,
        width: float = 5.8,
        **kwargs,
    ):
        log_progress(f"Building InfoCard: {heading!r}")
        accent = accent or COLORS["accent"]

        panel = RoundedRectangle(
            width=width,
            height=1.65,
            corner_radius=LAYOUT["card_corner_radius"],
            stroke_color=accent,
            stroke_width=STROKES["thin"],
            fill_color=COLORS["surface"],
            fill_opacity=0.96,
        )
        panel.set_z_index(0)

        heading_text = Text(
            heading,
            font=FONTS["heading"],
            font_size=25,
            weight="BOLD",
            color=accent,
        )
        body_text = Text(
            body,
            font=FONTS["body"],
            font_size=19,
            color=COLORS["text_primary"],
            line_spacing=0.9,
        )

        content = VGroup(heading_text, body_text).arrange(
            DOWN, aligned_edge=LEFT, buff=0.16
        )
        content.move_to(panel.get_center())
        content.align_to(panel, LEFT).shift(RIGHT * 0.28)

        super().__init__(panel, content, **kwargs)


class DirectionArrow(Arrow):
    """Consistent directional arrow for movement and force explanations."""

    def __init__(
        self,
        start,
        end,
        color: Optional[str] = None,
        stroke_width: float = 5,
        **kwargs,
    ):
        log_progress("Creating DirectionArrow.")
        super().__init__(
            start,
            end,
            color=color or COLORS["accent"],
            stroke_width=stroke_width,
            buff=0,
            max_tip_length_to_length_ratio=0.18,
            **kwargs,
        )


class MotionTrail(VGroup):
    """A short series of fading dots indicating an object's direction of travel."""

    def __init__(
        self,
        start,
        end,
        dot_count: int = 7,
        color: Optional[str] = None,
        max_radius: float = 0.055,
        **kwargs,
    ):
        if dot_count < 2:
            raise ValueError("dot_count must be at least 2")

        log_progress(f"Creating MotionTrail with {dot_count} dots.")
        color = color or COLORS["warm"]
        dots = VGroup()

        for index in range(dot_count):
            alpha = index / (dot_count - 1)
            point = start + (end - start) * alpha
            dot = Dot(
                point,
                radius=max_radius * (0.35 + 0.65 * alpha),
                color=color,
            )
            dot.set_opacity(0.18 + 0.82 * alpha)
            dots.add(dot)

        super().__init__(*dots, **kwargs)


class RotationIndicator(VGroup):
    """Curved arrow and axis line indicating a sphere's rotation direction."""

    def __init__(
        self,
        radius: float = 1.35,
        arrow_color: Optional[str] = None,
        axis_color: Optional[str] = None,
        **kwargs,
    ):
        log_progress("Creating RotationIndicator.")
        arrow_color = arrow_color or COLORS["accent"]
        axis_color = axis_color or COLORS["text_secondary"]

        arc = Arc(
            radius=radius,
            start_angle=0.25,
            angle=4.8,
            color=arrow_color,
            stroke_width=STROKES["emphasis"],
        )
        # Add a small arrowhead at the end of the arc. A separate Arrow keeps
        # this indicator robust across Manim versions.
        end = arc.point_from_proportion(0.98)
        tangent = arc.point_from_proportion(0.96)
        tip = Arrow(
            tangent,
            end,
            color=arrow_color,
            stroke_width=STROKES["emphasis"],
            buff=0,
            max_tip_length_to_length_ratio=0.35,
        )
        axis = Line(UP * (radius + 0.35), DOWN * (radius + 0.35),
                    color=axis_color, stroke_width=STROKES["thin"])
        super().__init__(arc, tip, axis, **kwargs)


class MetricCallout(VGroup):
    """Large numeric value with a smaller explanatory label."""

    def __init__(
        self,
        value: str,
        label: str,
        accent: Optional[str] = None,
        **kwargs,
    ):
        log_progress(f"Creating MetricCallout: {value} — {label}")
        accent = accent or COLORS["warm"]

        number = Text(
            value,
            font=FONTS["numeric"],
            font_size=58,
            weight="BOLD",
            color=accent,
        )
        caption = Text(
            label,
            font=FONTS["label"],
            font_size=21,
            color=COLORS["text_secondary"],
        )
        group = VGroup(number, caption).arrange(DOWN, buff=0.08)
        super().__init__(*group, **kwargs)


class EarthGlobe(VGroup):
    """Procedural placeholder Earth globe made from vector primitives.

    This is intentionally a clean stylized globe, not a geographically exact
    map. It lets us develop and test scene composition before a polished
    reusable Earth SVG is selected or authored.

    Replace/extend this component later if the final SVG asset gives a better
    result. Keep the public constructor stable so video scenes need not change.
    """

    def __init__(
        self,
        radius: float = 1.8,
        show_atmosphere: bool = True,
        **kwargs,
    ):
        log_progress("Building procedural EarthGlobe...")
        ocean = Circle(
            radius=radius,
            stroke_color=COLORS["earth_ocean"],
            stroke_width=2,
            fill_color=COLORS["earth_ocean"],
            fill_opacity=1,
        )

        # Simplified continent-like shapes. They are intentionally abstract;
        # this is a temporary vector placeholder, not a map projection.
        land_a = VMobject()
        land_a.set_points_as_corners([
            (-0.72, 0.75, 0), (-0.28, 1.05, 0), (0.02, 0.82, 0),
            (0.12, 0.48, 0), (-0.12, 0.24, 0), (-0.28, -0.05, 0),
            (-0.55, 0.12, 0), (-0.78, 0.43, 0), (-0.72, 0.75, 0)
        ])
        land_a.scale(radius / 1.8).set_fill(COLORS["earth_land"], opacity=1)
        land_a.set_stroke(COLORS["earth_land_dark"], width=1)

        land_b = VMobject()
        land_b.set_points_as_corners([
            (0.28, 0.82, 0), (0.75, 0.72, 0), (0.95, 0.42, 0),
            (0.73, 0.18, 0), (0.48, 0.22, 0), (0.33, -0.08, 0),
            (0.08, -0.18, 0), (0.16, 0.28, 0), (0.28, 0.82, 0)
        ])
        land_b.scale(radius / 1.8).set_fill(COLORS["earth_land"], opacity=1)
        land_b.set_stroke(COLORS["earth_land_dark"], width=1)

        # Clip-like masking is not applied here; keep land inside the visible
        # globe by scaling it inward and placing the ocean circle above edges.
        land_group = VGroup(land_a, land_b).scale(0.88)
        land_group.set_z_index(2)
        ocean.set_z_index(1)

        globe = VGroup(ocean, land_group)

        if show_atmosphere:
            atmosphere = Circle(
                radius=radius * 1.045,
                stroke_color=COLORS["atmosphere"],
                stroke_width=5,
                fill_opacity=0,
            )
            atmosphere.set_opacity(0.42)
            atmosphere.set_z_index(3)
            globe.add(atmosphere)

        super().__init__(*globe, **kwargs)
        log_progress("EarthGlobe ready.")


def make_star_field(
    count: int = 45,
    width: float = 7.0,
    height: float = 12.0,
    color: Optional[str] = None,
    seed: int = 7,
) -> VGroup:
    """Create a deterministic sparse star field for a space background."""
    import random

    log_progress(f"Generating star field: {count} points.")
    rng = random.Random(seed)
    color = color or COLORS["text_primary"]
    stars = VGroup()

    for _ in range(count):
        x = rng.uniform(-width / 2, width / 2)
        y = rng.uniform(-height / 2, height / 2)
        radius = rng.uniform(0.008, 0.025)
        star = Dot((x, y, 0), radius=radius, color=color)
        star.set_opacity(rng.uniform(0.25, 0.8))
        stars.add(star)

    log_progress(f"Star field generated: {len(stars)} stars.")
    return stars


log_progress("Reusable component definitions are ready.")
