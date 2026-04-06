from manim import *
import numpy as np

class DirectionalDerivativeSlice(ThreeDScene):
    def construct(self):
        # --- Function definition ---
        def f(x, y):
            return 0.5 * (x**2 + y**2)

        # --- Point and direction ---
        x0, y0 = 1, 1
        v = np.array([1, 2])
        v = v / np.linalg.norm(v)  # normalize

        # Parametric slice: (x(t), y(t))
        def gamma(t):
            return np.array([x0 + t * v[0], y0 + t * v[1]])

        def g(t):
            x, y = gamma(t)
            return f(x, y)

        # --- 3D Axes ---
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[0, 10],
        )

        # --- Surface ---
        surface = Surface(
            lambda u, v_: axes.c2p(u, v_, f(u, v_)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(24, 24),
            fill_opacity=0.6,
        )

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        self.play(Create(axes), Create(surface))
        self.wait()

        # --- Point on surface ---
        z0 = f(x0, y0)
        point = Dot3D(axes.c2p(x0, y0, z0), color=RED)
        self.play(FadeIn(point))

        # --- Directional derivative vector ---
        # gradient of f = (x, y)
        grad = np.array([x0, y0])
        directional_derivative = np.dot(grad, v)

        # Tangent direction lifted into 3D
        tangent_vec = np.array([v[0], v[1], directional_derivative])
        tangent_vec = tangent_vec / np.linalg.norm(tangent_vec)

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

        # --- Slice curve on surface ---
        t_vals = np.linspace(-2, 2, 100)
        slice_points = [
            axes.c2p(*(gamma(t)), f(*gamma(t)))
            for t in t_vals
        ]

        slice_curve = VMobject(color=ORANGE)
        slice_curve.set_points_smoothly(slice_points)

        self.play(Create(slice_curve))
        self.wait()

        # --- Transition to 2D slice graph ---
        self.move_camera(phi=0, theta=-90 * DEGREES)
        self.wait()

        # Fade out surface for clarity
        self.play(FadeOut(surface), FadeOut(slice_curve), FadeOut(arrow), FadeOut(point), FadeOut(axes))

        # --- 2D axes for g(t) ---
        axes2d = Axes(
            x_range=[-2, 2],
            y_range=[0, 10],
            axis_config={"include_numbers": True},
        ).to_edge(DOWN)

        graph = axes2d.plot(lambda t: g(t), color=BLUE)

        self.play(Create(axes2d), Create(graph))
        self.wait()

        # --- Point on 2D graph ---
        dot2d = Dot(axes2d.c2p(0, g(0)), color=RED)
        self.play(FadeIn(dot2d))

        # --- Tangent line ---
        # g'(0) = directional derivative
        slope = directional_derivative

        tangent_line = axes2d.plot(
            lambda t: g(0) + slope * (t - 0),
            color=GREEN,
            x_range=[-2, 2]
        )

        self.play(Create(tangent_line))
        self.wait(2)