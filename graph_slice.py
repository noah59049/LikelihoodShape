from manim import *
import numpy as np

class DirectionalDerivativeSliceCopy(ThreeDScene):
    def construct(self):
        # --- Function ---
        def f(x, y):
            return 0.5 * (x**2 + y**2)

        # --- Point and direction ---
        x0, y0 = 1, 1
        v = np.array([0, 1])
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

        # 2D axes (fixed in frame)
        axes2d = Axes(
            x_range=[-2, 2],
            y_range=[0, 4],
            axis_config={"include_numbers": True},
        ).scale(0.7).to_corner(DR)

        # --- Surface ---
        surface = Surface(
            lambda u, v_: axes.c2p(u, v_, f(u, v_)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(24, 24),
            fill_opacity=0.35,
        )

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

        # =========================================================
        # Slice plane
        # =========================================================

        plane = Surface(
            lambda s, t: axes.c2p(
                x0 + s * v[0],
                y0 + s * v[1],
                z0 + t
            ),
            u_range=[-2, 2],
            v_range=[-3, 3],
            resolution=(10, 10),
            fill_opacity=0.6,
            checkerboard_colors=[RED_D, RED_E],
        )

        self.play(FadeIn(plane))
        self.wait()

        # =========================================================
        # Slice curve
        # =========================================================

        t_vals = np.linspace(-2, 2, 100)

        curve_3d_points = []
        curve_2d_points = []

        for t in t_vals:
            x, y = gamma(t)
            z = f(x, y)

            curve_3d_points.append(axes.c2p(x, y, z))
            curve_2d_points.append(axes2d.c2p(t, z))

        slice_curve = VMobject(color=ORANGE)
        slice_curve.set_points_as_corners(curve_3d_points)

        self.play(Create(slice_curve))
        self.wait()

        # =========================================================
        # Add 2D axes FIXED IN FRAME
        # =========================================================

        self.add_fixed_in_frame_mobjects(axes2d)
        self.play(FadeIn(axes2d))

        # =========================================================
        # Create 2D graph curve (target)
        # =========================================================

        graph_curve = VMobject(color=ORANGE)
        graph_curve.set_points_as_corners(curve_2d_points)

        self.add_fixed_in_frame_mobjects(graph_curve)

        # =========================================================
        # COPY animation
        # =========================================================

        slice_curve_2d_source = slice_curve.copy()
        slice_curve_2d_source.apply_function(
            lambda p: self.camera.project_point(p)
        )
        self.add_fixed_in_frame_mobjects(graph_curve)

        self.play(
            TransformFromCopy(slice_curve_2d_source, graph_curve),
            run_time=2
        )

        self.wait()

        # =========================================================
        # Copy the point too
        # =========================================================

        dot2d = Dot(axes2d.c2p(0, g(0)), color=RED)
        self.add_fixed_in_frame_mobjects(dot2d)

        self.play(
            Transform(point, dot2d)
        )

        self.wait()

        # =========================================================
        # Tangent line
        # =========================================================

        slope = directional_derivative

        tangent_line = axes2d.plot(
            lambda t: g(0) + slope * t,
            x_range=[-2, 2],
            color=GREEN
        )

        self.add_fixed_in_frame_mobjects(tangent_line)

        self.play(Create(tangent_line))
        self.wait(2)