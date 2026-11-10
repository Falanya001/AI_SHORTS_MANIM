from manim import *
from manim.opengl import *

from core.earth import EarthGlobe


class EarthRotationTest(ThreeDScene):

    def construct(self):

        self.camera.background_color = BLACK

        earth = EarthGlobe(radius=2.0)

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-90 * DEGREES,
        )

        self.add(earth)

        self.play(
            Rotate(
                earth,
                angle=TAU,
                axis=UP,
                run_time=10,
                rate_func=linear,
            )
        )

        self.wait(2)
