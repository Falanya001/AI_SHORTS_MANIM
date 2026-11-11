from pathlib import Path

from manim import TAU
from manim.opengl import OpenGLSphere, OpenGLTexturedSurface


class EarthGlobe(OpenGLTexturedSurface):
    """Textured 3D Earth using Manim's native OpenGL sphere."""

    def __init__(
        self,
        texture_path=None,
        radius=2.0,
        resolution=(128, 64),
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

        sphere = OpenGLSphere(
            radius=radius,
            resolution=resolution,
        )

        super().__init__(
            sphere,
            str(texture_path),
            **kwargs,
        )
