from manim import *
from manim_voiceover import *
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
import numpy as np
from MF_Tools import *
from slice_utils import make_graph_slice

class DirectionalDerivativeSliceCopy(ThreeDScene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService(r"/Users/noah/Convex/LikelihoodShape/podcasts/graph_slice_podcast5.mp3",
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
        pre_directional = MathTex(r"D_{\vec{v}} f(\vec{x})")
        pre_directional.move_to(f_vector)
        directional = MathTex(r"D_{\vec{v}} f(\vec{x})=\lim_{h \to 0}\frac{f(\vec{x}+h\vec{v})-f(\vec{x})}{h}")
        directional.to_corner(UL)

        # --- Step 4: Path ---
        atv = MathTex("\\vec{x} = \\vec{a} + t\\vec{v}")
        atv.next_to(directional, DOWN, buff=0.4, aligned_edge=LEFT)

        # --- Step 5: g(t) definition ---
        g_def = MathTex(r"g(t) = f(\vec{a} + t\vec{v})")
        g_def.next_to(atv, DOWN, buff=0.4, aligned_edge=LEFT)

        g_def2 = MathTex(r"g(t) = f(\vec{x})")
        g_def2.next_to(atv, DOWN, buff=0.4, aligned_edge=LEFT)

        # --- Step 6: derivative relation ---
        deriv_relation = MathTex("D_{\\vec{v}} f(\\vec{x}) = g'(t)")
        deriv_relation.next_to(g_def, DOWN, buff=0.4, aligned_edge=LEFT)

        self.add_fixed_in_frame_mobjects(f_explicit,
                                         f_vector,
                                         pre_directional,
                                         directional,
                                         atv,
                                         g_def,
                                         g_def2,
                                         deriv_relation)
        self.remove(f_explicit,
                    f_vector,
                    pre_directional,
                    directional,
                    atv,
                    g_def,
                    g_def2,
                    deriv_relation)

        # --- Function and GraphSlice ---
        def f(x, y):
            return 0.5 * (x**2 + y**2)

        def grad_f(x, y):
            return np.array([x, y])

        gs = make_graph_slice(
            f, grad_f,
            x0=-1, y0=1,
            v=[1, 2],
            axes2d_y_range=[0, 4],
        )

        x0, y0 = gs.x0, gs.y0
        z0 = gs.g(0)

        # Helper to compute a point on the surface along the direction v
        def point_on_surface(t):
            x, y = gs.gamma(t)
            return gs.axes.c2p(x, y, gs.g(t))

        # --- Time to actually animate the scene ---
        with self.voiceover("If we have a function of multiple variables,") as tracker:
            self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
            # Yay tex
            self.play(Create(f_explicit))

            self.play(Create(gs.axes), Create(gs.surface))
            self.wait()

        with self.voiceover("f(vector x),") as tracker:
            # Yay tex
            self.play(TransformByGlyphMap(f_explicit, f_vector,
                                    (range(2,13), range(2,4))))

        with self.voiceover("f(vector x), the derivative in the direction of unit vector v is the change in the value of f divided by the distance in the direction of v,") as tracker:
            # Yay tex
            self.play(TransformByGlyphMap(f_vector,pre_directional,
                                          (FadeIn, range(3)),
                                          ))
            self.play(TransformByGlyphMap(pre_directional,directional,
                                          (FadeIn, range(8,32))))

            # =========================================================
            # Delta f / Delta x visualization on the 3D graph
            # =========================================================
            h_tracker = ValueTracker(1.0)

            # Base point
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
                    start=gs.axes.c2p(x0, y0, z0),
                    end=gs.axes.c2p(
                        x0 + h_tracker.get_value() * gs.v[0],
                        y0 + h_tracker.get_value() * gs.v[1],
                        z0
                    ),
                    color=GREEN
                )
            )

            # Δf: vertical displacement
            delta_f_line = always_redraw(
                lambda: Line3D(
                    start=gs.axes.c2p(
                        x0 + h_tracker.get_value() * gs.v[0],
                        y0 + h_tracker.get_value() * gs.v[1],
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
                gs.base_dot,
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
            self.play(
                h_tracker.animate.set_value(0.001),
                run_time=3,
                rate_func=smooth
            )

        with self.voiceover("Geometrically it's the slope of the tangent line in the direction of v.") as tracker:
            # --- Directional derivative arrow ---
            arrow = Arrow3D(
                start=gs.axes.c2p(x0, y0, z0),
                end=gs.axes.c2p(
                    x0 + gs.v[0],
                    y0 + gs.v[1],
                    z0 + gs.g_prime(0)
                ),
                color=YELLOW
            )

            self.play(Create(arrow))
            self.wait()

        # =========================================================
        # Slice plane
        # =========================================================

        with self.voiceover("I like to think of it as taking a slice of the graph to get a function of 1 variable,"):
            self.play(FadeIn(gs.slice_plane))
            self.play(Create(gs.slice_curve))
            gs.animate_copy(self, extra_3d_objects=[arrow])

        with self.voiceover("and then taking the derivative of that function."):
            tangent_line = gs.axes2d.plot(
                lambda t: gs.g(0) + gs.g_prime(0) * t,
                x_range=[-2, 2],
                color=GREEN
            )

            self.add_fixed_in_frame_mobjects(tangent_line)
            self.play(Create(tangent_line))

        # Yay tex
        with self.voiceover("Algebraically that means you choose some initial value a, and then parameterize x as a + tv,") as tracker:
            self.play(Write(atv))
            # TODO: Add a and v to the z=0 plane of the 3D graph

            self.play(FadeOut(tangent_line), FadeOut(arrow), run_time=0.7)

        with self.voiceover("and define g(t) as equal to f(x).") as tracker:
            self.play(Write(g_def))
            self.play(TransformByGlyphMap(g_def, g_def2,
                                          (range(8,14), [8,9])))

            # Add g(t) labels to the lower graph
            axis_labels = gs.axes2d.get_axis_labels(
                MathTex("t").scale(0.7),
                MathTex("g(t)").scale(0.7)
            )

            self.add_fixed_in_frame_mobjects(axis_labels)
            self.play(Write(axis_labels), run_time=0.5)

            # --- Move the dots ---
            def point_on_graph(t):
                return gs.axes2d.c2p(t, gs.g(t))

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
            self.play(t_tracker.animate.set_value(1.0), run_time=1.2)
            self.play(t_tracker.animate.set_value(0.0), run_time=1.2)

        with self.voiceover("So the directional derivative is g'(t).") as tracker:
            self.play(Write(deriv_relation))
            # Move the tangent lines
            tangent_line_2d = always_redraw(
                lambda: gs.axes2d.plot(
                    lambda tau: (
                        gs.g(t_tracker.get_value())
                        + gs.g_prime(t_tracker.get_value())
                        * (tau - t_tracker.get_value())
                    ),
                    x_range=[
                        t_tracker.get_value() - 0.75,
                        t_tracker.get_value() + 0.75
                    ],
                    color=GREEN,
                )
            )
            tangent_line_3d = always_redraw(
                lambda: Line3D(
                    start=gs.axes.c2p(
                        gs.gamma(t_tracker.get_value())[0] - 0.5 * gs.v[0],
                        gs.gamma(t_tracker.get_value())[1] - 0.5 * gs.v[1],
                        gs.g(t_tracker.get_value())
                        - 0.5 * gs.g_prime(t_tracker.get_value())
                    ),
                    end=gs.axes.c2p(
                        gs.gamma(t_tracker.get_value())[0] + 0.5 * gs.v[0],
                        gs.gamma(t_tracker.get_value())[1] + 0.5 * gs.v[1],
                        gs.g(t_tracker.get_value())
                        + 0.5 * gs.g_prime(t_tracker.get_value())
                    ),
                    color=GREEN,
                )
            )

            self.add_fixed_in_frame_mobjects(tangent_line_2d)
            self.add(tangent_line_2d)
            self.add(tangent_line_3d)

            self.play(
                t_tracker.animate.set_value(1.0),
                run_time=2,
                rate_func=linear
            )
            self.play(
                t_tracker.animate.set_value(0.0),
                run_time=2,
                rate_func=linear
            )
