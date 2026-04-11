from manim import *
from manim_voiceover import *
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
import numpy as np
from MF_Tools import *

class DirectionalDerivativeSliceCopy(ThreeDScene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService(r"/Users/noah/Convex/LikelihoodShape/podcasts/graph_slice_podcast2.mp3",
        cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
        min_silence_len=2000,
        keep_silence=(0,0)))
                # --- Step 1: First line at top ---
        f_explicit = MathTex("f(x_1, x_2, x_3, x_4)")
        f_explicit.to_edge(UP)

        # self.play(Write(f_explicit))
        # self.wait()

        # --- Step 2: Transform in place ---
        f_vector = MathTex("f(\\vec{x})")
        f_vector.move_to(f_explicit)

        # self.play(TransformByGlyphMap(f_explicit, f_vector,
        #                               (range(2,13), range(2,4))))
        # self.wait()

        # --- Step 3: Directional derivative ---
        directional = MathTex("D_{\\vec{v}} f(\\vec{x})")
        directional.next_to(f_vector, DOWN, buff=0.4)

        # self.play(Write(directional))
        # self.wait()

        # --- Step 4: Path ---
        path = MathTex("\\vec{x} = \\vec{a} + t\\vec{v}")
        path.next_to(directional, DOWN, buff=0.4)

        # --- Step 5: g(t) definition ---
        g_def = MathTex("g(t) = f(\\vec{a} + t\\vec{v}) = f(\\vec{x})")
        g_def.next_to(path, DOWN, buff=0.4)

        # self.play(Write(g_def))
        # self.wait()

        # --- Step 6: derivative relation ---
        deriv_relation = MathTex("D_{\\vec{v}} f(\\vec{x}) = g'(t)")
        deriv_relation.next_to(g_def, DOWN, buff=0.4)

        # self.play(TransformMatchingTex(directional.copy(), deriv_relation))
        # self.wait()

        self.add_fixed_in_frame_mobjects(f_explicit,
                                         f_vector,
                                         directional,
                                         path,
                                         g_def,
                                         deriv_relation)
        self.remove(f_explicit,
                    f_vector,
                    directional,
                    path,
                    g_def,
                    deriv_relation)


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

        with self.voiceover("So suppose we have a function f that inputs multiple variables, and it outputs a single value.") as tracker:
            # Yay tex
            self.play(Create(f_explicit))

            self.play(Create(axes), Create(surface))
            self.wait()

        with self.voiceover("We can think of it as inputting a vector.") as tracker:
            # Yay tex
            self.play(TransformByGlyphMap(f_explicit, f_vector,
                                    (range(2,13), range(2,4))))

        with self.voiceover("We consider the directional derivative in the direction of some vector v,") as tracker:
            # Yay tex
            self.play(Write(directional))

        # with self.voiceover(" the slope of the tangent line in that direction") as tracker:
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

        with self.voiceover("So the way we do that is we slice the graph along the vector, and that gives us a graph that’s just a function of 1 variable."):
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

        with self.voiceover("And the derivative of that function there is the directional derivative."):
            # =========================================================
            # Copy the point too
            # =========================================================

            # Get the 3D center of the point
            p3d = point.get_center()

            # Project it to screen space
            p2d = self.camera.project_point(p3d)

            # Create a proper 2D dot at that location
            point_2d_source = Dot(p2d, color=RED)

            # Hide it (so we only see the original)
            point_2d_source.set_opacity(0)
            self.add(point_2d_source)

            # Target dot (already correct)
            dot2d = Dot(axes2d.c2p(0, g(0)), color=RED)
            self.add_fixed_in_frame_mobjects(dot2d)

            # Animate
            self.play(
                TransformFromCopy(point_2d_source, dot2d)
            )

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
            self.play(Write(directional))

        # Yay tex
        with self.voiceover("So, the way I like to formalize this is by parameterizing our inputs. So our input x is equal to any initial state a plus our direction vector v times t.") as tracker:
            self.play(Write(path))
        with self.voiceover("And then we just let g(t) equal f(x), or f(a + tv).") as tracker:
            self.play(Write(g_def))
        with self.voiceover("So g is just the function sliced along that line. Then the directional derivative is just g’(t), the derivative of g with respect to t, which makes sense.") as tracker:
            self.play(Write(deriv_relation))