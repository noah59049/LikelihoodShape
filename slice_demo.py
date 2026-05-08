from manim import *
import numpy as np
from slice_utils import make_graph_slice


class SliceDemo(ThreeDScene):
    def construct(self):
        def f(x, y):
            return 0.5 * (x**2 + y**2)

        def grad_f(x, y):
            return np.array([x, y])

        x0, y0 = -1.0, 1.0
        v = [1, 2]

        gs = make_graph_slice(
            f, grad_f, x0, y0, v,
            axes2d_y_range=[0, 4],
        )

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(gs.axes), Create(gs.surface))
        self.wait(0.5)

        base_dot = Dot3D(gs.axes.c2p(x0, y0, f(x0, y0)), color=RED)

        self.play(FadeIn(gs.slice_plane), Create(gs.slice_curve), FadeIn(base_dot))
        self.wait(0.5)

        gs.animate_copy(self, extra_3d_objects=[base_dot])
        self.wait(1)
