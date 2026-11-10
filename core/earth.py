from pathlib import Path

from manim import Sphere
from manim.opengl import OpenGLTexturedSurface


class EarthGlobe(OpenGLTexturedSurface):
    """Reusable 3D Earth with a NASA image texture."""

    def __init__(
        self,
        texture_path=None,
        radius=2.0,
        resolution=(96, 48),
        **kwargs,
    ):
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

        sphere = Sphere(
            radius=radius,
            resolution=resolution,
        )

        super().__init__(
            sphere,
            str(texture_path),
            **kwargs,
        )
