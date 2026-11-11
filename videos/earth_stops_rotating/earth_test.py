from manim import *
from manim.opengl import *

from core.earth import EarthGlobe


class EarthRotationTest(ThreeDScene):

    def construct(self):

        self.camera.background_color = BLACK

        self.set_camera_orientation(
            phi=75 * DEGREES,
            theta=-90 * DEGREES,
        )

        earth = EarthGlobe(
            radius=2.0,
            resolution=(128, 64),
        )

        self.add(earth)

        def rotate_earth(mob, dt):
            mob.rotate(
                dt * TAU / 10,
                axis=UP,
                about_point=ORIGIN,
            )

        earth.add_updater(rotate_earth)

        self.wait(10)

        earth.clear_updaters()
        self.wait(1)
