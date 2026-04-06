from manim import *
import numpy as np

class DirectionalDerivativeSlice(ThreeDScene):
    def construct(self):
        # --- Function ---
        def f(x, y):
            return 0.5 * (x**2 + y**2)

        # --- Point and direction ---
        x0, y0 = 1, 1
        v = np.array([1, 2])
        v = v / np.linalg.norm(v)

        def gamma(t):
            return np.array([x0 + t * v[0], y0 + t * v[1]])

        def g(t):
            x, y = gamma(t)
            return f(x, y)

        # --- Axes ---
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[0, 10],
        )

        axes2d = Axes(
            x_range=[-2, 2],
            y_range=[0, 10],
            axis_config={"include_numbers": True},
        ).to_edge(DOWN)

        # --- Surface ---
        surface = Surface(
            lambda u, v_: axes.c2p(u, v_, f(u, v_)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(24, 24),
            fill_opacity=0.6,
        )

        # --- Camera ---
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        self.play(Create(axes), Create(surface))
        self.wait()

        # --- Point ---
        z0 = f(x0, y0)
        point = Dot3D(axes.c2p(x0, y0, z0), color=RED)
        self.play(FadeIn(point))

        # --- Directional derivative arrow ---
        grad = np.array([x0, y0])
        directional_derivative = np.dot(grad, v)

        arrow = Arrow3D(
            start=axes.c2p(x0, y0, z0),
            end=axes.c2p(
                x0 + v[0],
                y0 + v[1],
                z0 + directional_derivative
            ),
            color=YELLOW
        )

        self.play(Create(arrow))
        self.wait()

        # --- Slice curve data ---
        t_vals = np.linspace(-2, 2, 100)

        curve_3d_points = []
        curve_2d_points = []

        for t in t_vals:
            x, y = gamma(t)
            z = f(x, y)

            curve_3d_points.append(axes.c2p(x, y, z))
            curve_2d_points.append(axes2d.c2p(t, z))

        # --- Slice curve (3D) ---
        slice_curve = VMobject(color=ORANGE)
        slice_curve.set_points_smoothly(curve_3d_points)

        self.play(Create(slice_curve))
        self.wait()

        # --- Rotate camera top-down ---
        self.move_camera(phi=0, theta=-90 * DEGREES)
        self.wait()

        # --- Prepare transformed curve ---
        graph_curve = slice_curve.copy()
        graph_curve.set_points_smoothly(curve_2d_points)

        # Optional: shift to align nicely with axes2d
        # graph_curve.shift(DOWN * 1)

        # --- Transform curve into 2D graph ---
        self.play(
            Transform(slice_curve, graph_curve),
            FadeIn(axes2d),
            FadeOut(surface),
            FadeOut(arrow),
        )

        # --- Transform point to 2D ---
        dot2d = Dot(axes2d.c2p(0, g(0)), color=RED)

        self.play(
            Transform(point, dot2d)
        )

        self.wait()

        # --- Tangent line ---
        slope = directional_derivative

        tangent_line = axes2d.plot(
            lambda t: g(0) + slope * t,
            x_range=[-2, 2],
            color=GREEN
        )

        self.play(Create(tangent_line))
        self.wait(2)