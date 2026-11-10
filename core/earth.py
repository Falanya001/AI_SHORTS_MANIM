from pathlib import Path

from manim import *
from manim.opengl import (
    OpenGLSphere,
    OpenGLTexturedSurface,
)


class EarthGlobe(VGroup):
    """Reusable, image-textured 3D Earth."""

    def __init__(
        self,
        texture_path=None,
        radius=2.0,
        resolution=(96, 48),
        **kwargs,
    ):
        super().__init__(**kwargs)

        if texture_path is None:
            project_root = Path(__file__).resolve().parent.parent
            texture_path = (
                project_root
                / "assets"
                / "textures"
                / "earth_august.jpg"
            )

        texture_path = Path(texture_path)

        if not texture_path.is_file():
            raise FileNotFoundError(
                f"Earth texture not found: {texture_path}"
            )

        sphere = OpenGLSphere(
            radius=radius,
            resolution=resolution,
        )

        self.surface = OpenGLTexturedSurface(
            sphere,
            str(texture_path),
        )

        self.add(self.surface)

    def rotate_earth(self, angle, axis=UP, **kwargs):
        """Rotate the Earth around an axis."""
        self.rotate(angle, axis=axis, **kwargs)
        return self
