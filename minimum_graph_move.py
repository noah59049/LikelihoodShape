from manim import *

class Move3DGraph(ThreeDScene):
    def construct(self):
        def f(x, y):
            return -(x**2 + y**2)

        axes = ThreeDAxes(
            x_range=[-1,1],
            y_range=[-1,1],
            z_range=[-1,3]
        )

        surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u,v)),
            u_range=(-1, 1),
            v_range=(-1, 1),
            resolution=(12, 12),
            fill_opacity=0.5,
        )

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes), Create(surface))
        self.wait(1)

        three_d_group = VGroup(axes, surface)
        self.play(
            three_d_group.animate.scale(0.8).to_corner(UR, buff=0.5),
            run_time=1.35,
        )