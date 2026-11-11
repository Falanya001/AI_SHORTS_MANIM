from pathlib import Path

import numpy as np

from manim import PI, TAU
from manim.opengl import OpenGLSurface, OpenGLTexturedSurface


class EarthGlobe(OpenGLTexturedSurface):
    """NASA-textured 3D Earth."""

    def __init__(
        self,
        texture_path=None,
        radius=2.0,
        resolution=(256, 128),
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
            raise FileNotFoundError(texture_path)

        def sphere_point(u, v):
            return np.array([
                radius * np.sin(v) * np.cos(u),
                radius * np.sin(v) * np.sin(u),
                radius * np.cos(v),
            ])

        sphere = OpenGLSurface(
            uv_func=sphere_point,
            u_range=(0, TAU),
            v_range=(0, PI),
            resolution=resolution,
            gloss=0,
            shadow=0,
        )

        super().__init__(
            sphere,
            str(texture_path),
            **kwargs,
        )
