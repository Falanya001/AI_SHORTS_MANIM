from manim import *
from manim.opengl import *

from core.earth import EarthGlobe


class EarthStillTest(ThreeDScene):

    def construct(self):

        self.camera.background_color = BLACK

        self.set_camera_orientation(
            phi=75 * DEGREES,
            theta=-90 * DEGREES,
        )

        earth = EarthGlobe(radius=2.5)

        self.add(earth)
        self.wait(1)
