from manim import *
from manim_voiceover import *
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
import numpy as np
from MF_Tools import *

class DirectionalDerivativeSliceCopy(ThreeDScene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService(r"/Users/noah/Convex/LikelihoodShape/podcasts/graph_slice_podcast4.mp3",
        cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
        min_silence_len=2000,
        keep_silence=(0,0)))
        
        # --- Step 1: First line at top ---
        f_explicit = MathTex("f(x_1, x_2, x_3, x_4)")
        f_explicit.to_corner(UL)

        # --- Step 2: Transform in place ---
        f_vector = MathTex("f(\\vec{x})")
        f_vector.move_to(f_explicit)

        # --- Step 3: Directional derivative ---
        directional = MathTex(r"D_{\vec{v}} f(\vec{x})=\lim_{h \to 0}\frac{f(\vec{x}+h\vec{v})-f(\vec{x})}{h}")
        directional.next_to(f_vector, DOWN, buff=0.4)
        # TODO: Have directional added 1 at a time

        # --- Step 4: Path ---
        atv = MathTex("\\vec{x} = \\vec{a} + t\\vec{v}")
        atv.next_to(directional, DOWN, buff=0.4)

        # --- Step 5: g(t) definition ---
        g_def = MathTex("g(t) = f(\\vec{a} + t\\vec{v}) = f(\\vec{x})")
        g_def.next_to(atv, DOWN, buff=0.4)

        # --- Step 6: derivative relation ---
        deriv_relation = MathTex("D_{\\vec{v}} f(\\vec{x}) = g'(t)")
        deriv_relation.next_to(g_def, DOWN, buff=0.4)

        # Stuff that would go over the left edge needs to get sent to the left edge
        # But only after making everything else because otherwise we'd have misaligned things
        directional.to_edge(LEFT)
        g_def.to_edge(LEFT)


        self.add_fixed_in_frame_mobjects(f_explicit,
                                         f_vector,
                                         directional,
                                         atv,
                                         g_def,
                                         deriv_relation)
        self.remove(f_explicit,
                    f_vector,
                    directional,
                    atv,
                    g_def,
                    deriv_relation)


        # --- Function ---
        def f(x, y):
            return 0.5 * (x**2 + y**2)

        # --- Point and direction ---
        x0, y0 = -1, 1
        z0 = f(x0, y0)
        v = np.array([1,2])
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
        ).scale(0.56).to_corner(DL)

        # --- Surface ---
        surface = Surface(
            lambda u, v_: axes.c2p(u, v_, f(u, v_)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(24, 24),
            fill_opacity=0.35,
        )

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        with self.voiceover("If we have a function of a single variable f(x), the derivative is the change in the function value divided by the change in x, in the limit as the change in x goes to 0. And geometrically it’s the slope of the tangent line.") as tracker:
            pass # TODO: Have stuff in here

        with self.voiceover("If we have a function of multiple variables,") as tracker:
            # Yay tex
            self.play(Create(f_explicit))

            self.play(Create(axes), Create(surface))
            self.wait()

        with self.voiceover("f(vector x),") as tracker:
            # Yay tex
            self.play(TransformByGlyphMap(f_explicit, f_vector,
                                    (range(2,13), range(2,4))))

        with self.voiceover("f(vector x), the derivative in the direction of unit vector v is the change in the value of f divided by the distance in the direction of v,") as tracker:
            # Yay tex
            self.play(Write(directional))

            # =========================================================
            # Delta f / Delta x visualization on the 3D graph
            # =========================================================
            h_tracker = ValueTracker(1.0)

            # Helper to compute a point on the surface along the direction v
            def point_on_surface(t):
                x, y = gamma(t)
                z = f(x, y)
                return axes.c2p(x, y, z)

            # Base point
            base_dot = Dot3D(point_on_surface(0), color=RED)

            # Moving point
            moving_dot = always_redraw(
                lambda: Dot3D(
                    point_on_surface(h_tracker.get_value()),
                    color=BLUE
                )
            )

            # Secant line
            secant_line = always_redraw(
                lambda: Line3D(
                    start=point_on_surface(0),
                    end=point_on_surface(h_tracker.get_value()),
                    color=YELLOW
                )
            )

            # Δx: horizontal displacement along the slice direction
            delta_x_line = always_redraw(
                lambda: Line3D(
                    start=axes.c2p(x0, y0, z0),
                    end=axes.c2p(
                        x0 + h_tracker.get_value() * v[0],
                        y0 + h_tracker.get_value() * v[1],
                        z0
                    ),
                    color=GREEN
                )
            )

            # Δf: vertical displacement
            delta_f_line = always_redraw(
                lambda: Line3D(
                    start=axes.c2p(
                        x0 + h_tracker.get_value() * v[0],
                        y0 + h_tracker.get_value() * v[1],
                        z0
                    ),
                    end=point_on_surface(h_tracker.get_value()),
                    color=PURPLE
                )
            )

            # Labels for Δx and Δf
            delta_x_label = always_redraw(
                lambda: MathTex(r"\Delta x")
                .scale(0.5)
                .move_to(delta_x_line.get_center())
            )

            delta_f_label = always_redraw(
                lambda: MathTex(r"\Delta f")
                .scale(0.5)
                .move_to(delta_f_line.get_center())
            )

            self.add(
                base_dot,
                moving_dot,
                secant_line,
                delta_x_line,
                delta_f_line,
                delta_x_label,
                delta_f_label,
            )

            self.wait()

        with self.voiceover(
            "in the limit as the change in x goes to 0."
        ) as tracker:
            # Animate h shrinking to zero
            self.play(
                h_tracker.animate.set_value(0.001),
                run_time=3,
                rate_func=smooth
            )

        with self.voiceover("Geometrically it’s the slope of the tangent line in the direction of v.") as tracker:
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

        with self.voiceover("I like to think of it as taking a slice of the graph to get a function of 1 variable,"):
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

            # Move and shrink the 3D scene to make room for the 2D graph
            three_d_group = VGroup(
                axes,
                surface,
                plane,
                slice_curve,
                arrow,
                base_dot,
            )

            self.play(
                three_d_group.animate.scale(0.8).to_edge(RIGHT, buff=0.5),
                run_time=1.35
            )

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

            # =========================================================
            # Copy the point too
            # =========================================================

            # Get the 3D center of the point
            p3d = base_dot.get_center()

            # Project it to screen space
            p2d = self.camera.project_point(p3d)

            # Create a proper 2D dot at that location
            point_2d_source = Dot(p2d, color=BLUE)

            # Hide it (so we only see the original)
            point_2d_source.set_opacity(0)
            self.add(point_2d_source)

            # Target dot (already correct)
            dot2d = Dot(axes2d.c2p(0, g(0)), color=BLUE)
            self.add_fixed_in_frame_mobjects(dot2d)

            # Animate
            self.play(
                TransformFromCopy(slice_curve_2d_source, graph_curve),
                TransformFromCopy(point_2d_source, dot2d),
                run_time=1.35
            )

        with self.voiceover("and then taking the derivative of that function."):

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

        # Yay tex
        with self.voiceover("Algebraically that means you choose some initial value a, and then parameterize x as a + tv,") as tracker:
            self.play(Write(atv))
            # TODO: Add a and v to the z=0 plane of the 3D graph
        with self.voiceover("and define g(t) as equal to f(x).") as tracker:
            self.play(Write(g_def))
            # TODO: Add g(t) labels to the lower graph

            # --- Move the dots ---
            def point_on_graph(t):
                return axes2d.c2p(t, f(*gamma(t)))
            t_tracker = ValueTracker(0.0)
            parametric_dot2d = always_redraw(
                lambda: Dot(point_on_graph(t_tracker.get_value()), color=RED)
            )
            parametric_dot = always_redraw(
                lambda: Dot3D(
                    point_on_surface(t_tracker.get_value()),
                    color=RED
                )
            )
            # Ensure 2D objects remain fixed on screen
            self.add_fixed_in_frame_mobjects(parametric_dot2d)

            self.add(parametric_dot)
            self.add(parametric_dot2d)
            self.play(t_tracker.animate.set_value(1.0), run_time = 1.2)
            self.play(t_tracker.animate.set_value(0.0), run_time = 1.2)
        with self.voiceover("So the directional derivative is g’(t).") as tracker:
            self.play(Write(deriv_relation))
            # TODO: Move the tangent lines