from manim import *
from manim_voiceover import *
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
import numpy as np
from slice_utils import make_graph_slice
from N_Tools import shift_to_screen_corner


class GlobalMax(ThreeDScene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService(
            r"/Users/noah/Convex/LikelihoodShape/podcasts/global_max_podcast2.wav",
            cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
            min_silence_len=2000,
            keep_silence=(0, 0),
        ))
        # -------------------------------------------------------
        # Function: negative paraboloid + gaussian bump at (2, 0)
        #   P = (0, 0): dominated by the paraboloid, looks like a local max
        #   Q = (2, 0): gaussian peak, f(Q) = 1 > f(P) ≈ 0
        # -------------------------------------------------------
        def f(x, y):
            return -(x**2 + y**2) + 5 * np.exp(-(1.8 * (x - 2)**2 + 1.4 * y**2) / 0.5)

        def grad_f(x, y):
            ex = np.exp(-((x - 2)**2 + y**2) / 0.5)
            return np.array([
                -2*x + 5 * (-2*(x - 2) / 0.5) * ex,
                -2*y + 5 * (-2*y / 0.5) * ex,
            ])

        x0, y0 = 0.0, 0.0   # P
        t_search_Q = np.linspace(0.5, 3.5, 1000)
        t_Q = float(t_search_Q[np.argmax([f(t, 0.0) for t in t_search_Q])])
        x_Q, y_Q = t_Q, 0.0  # Q at actual maximum along y=0

        # -------------------------------------------------------
        # GraphSlice: P toward Q, direction v = (1, 0)
        # u_range controls both the surface x-extent and the 2D axes t-range.
        # P is at t=0, Q is at t=t_Q (actual max of f along y=0, near t≈1.9).
        # -------------------------------------------------------
        gs = make_graph_slice(
            f, grad_f,
            x0=x0, y0=y0,
            v=[1, 0],
            x_range=(-2.5, 2.5),
            y_range=(-2.5, 2.5),
            z_range=(-5, 2),
            u_range=(-2.3, 2.3),
            surface_v_range=(-2, 2),
            resolution=(18, 18),
            axes2d_y_range=(-4.5, 1.5),
            axes2d_scale=0.56,
            plane_u_range=(-0.2, 2.2),
            plane_v_range=(-5, 1.5),
            dot_color=RED,
        )
        gs.surface.set_fill(BLUE_B, opacity=0.35)

        # -------------------------------------------------------
        # Extra 3D/2D objects
        # -------------------------------------------------------
        Q_dot   = Dot3D(gs.axes.c2p(x_Q, y_Q, f(x_Q, y_Q)), color=GREEN)
        Q_dot2d = Dot(gs.axes2d.c2p(t_Q, gs.g(t_Q)), color=GREEN)

        P_label_3d = MathTex("P", color=RED,   font_size=36).next_to(gs.base_dot, OUT, buff=0.15)
        Q_label_3d = MathTex("Q", color=GREEN, font_size=36).next_to(Q_dot,       OUT, buff=0.15)
        # self.add_fixed_orientation_mobjects(P_label_3d, Q_label_3d)

        # -------------------------------------------------------
        # Find interior minimum M of g on (0, t_Q)
        # -------------------------------------------------------
        t_search = np.linspace(0.05, t_Q - 0.05, 500)
        t_M = float(t_search[np.argmin([gs.g(t) for t in t_search])])

        eps = 1e-5
        g_pp_P = (gs.g(eps) - 2*gs.g(0)   + gs.g(-eps))    / eps**2
        g_pp_M = (gs.g(t_M+eps) - 2*gs.g(t_M) + gs.g(t_M-eps)) / eps**2

        # -------------------------------------------------------
        # 2D concavity arcs
        # -------------------------------------------------------
        def concavity_arc_2d(t0, g_pp, width=None, height=None, visual_scale=6.0, color=RED):
            # g_pp = g'' (second derivative). Arc draws the local Taylor parabola:
            #   y = g(t0) + 0.5 * g_pp * visual_scale * (t - t0)^2
            # width:  half-range of t values sampled
            # height: if given instead of width, extends t until the arc is this far
            #         from g(t0) in y — solved as width = sqrt(2*height / (|g_pp|*visual_scale))
            if width is None:
                if height is not None:
                    width = np.sqrt(2 * height / (abs(g_pp) * visual_scale))
                else:
                    width = 0.32
            ts = np.linspace(t0 - width, t0 + width, 60)
            pts = [gs.axes2d.c2p(t, gs.g(t0) + 0.5 * g_pp * visual_scale * (t - t0)**2)
                   for t in ts]
            arc = VMobject(color=color, stroke_width=4)
            arc.set_points_as_corners(pts)
            return arc

        P_arc     = concavity_arc_2d(0,   g_pp_P, color=RED, height = 0.5)
        M_arc     = concavity_arc_2d(t_M, g_pp_M, color=RED, height = 0.5)
        M_dot_2d  = Dot(gs.axes2d.c2p(t_M, gs.g(t_M)), color=ORANGE, radius=0.07)
        M_label_2d = MathTex("M", color=ORANGE, font_size=24) \
                        .next_to(M_dot_2d, DOWN, buff=0.08)

        P_label_2d = MathTex("P", color=RED, font_size=24) \
                        .next_to(gs.dot2d, UL, buff=0.08)
        Q_label_2d = MathTex("Q", color=GREEN, font_size=24) \
                        .next_to(Q_dot2d, UR, buff=0.08)

        # -------------------------------------------------------
        # Proof text (right-center, fixed in frame)
        # -------------------------------------------------------
        def make_step(*lines, color=WHITE):
            rows = [Tex(line, font_size=40, color=color) for line in lines]
            group = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.25) \
                                 .to_corner(UL)
                                 # .move_to(np.array([-3.8, 1.5, 0]))
            group.set_stroke(color, width=1.5, background=False)
            return group

        t0_txt = make_step(r"$\nabla f(P) = 0$",
                           r"$f''_{\vec{v}} < 0$ everywhere")
        t1_txt = make_step(r"Suppose $g(Q) > g(P)$")
        t2_txt = make_step(r"By EVT, $\exists$ min on $[P, Q]$")
        t3_txt = make_step(r"Min $\neq P$", r"($P$ is a local max)")
        t4_txt = make_step(r"Min $\neq Q$", r"($g(Q) > g(P)$)")
        t5_txt = make_step(r"$\Rightarrow$ interior min: $M$")
        t6_txt = make_step(r"$M$ is a local min",
                           r"$\Rightarrow g''(M) \geq 0$")
        t7_txt = make_step(r"\textbf{Contradiction!}",
                           r"$g''(M) \geq 0$",
                           r"but $f''_{\vec{v}} < 0$ everywhere",
                           color=RED)
        t8_txt = make_step(r"$\therefore$ $P$ is the",
                           r"global maximum", color=GREEN)


        surf_small = Surface(
            lambda u, v: gs.axes.c2p(u, v, f(u,v)),
            u_range=(-1, 1),
            v_range=(-1, 1),
            resolution=(12, 12),
            fill_opacity=0.5,
        )
        surf_small.set_fill(BLUE_B, opacity=0.35)

        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        # -------------------------------------------------------
        # Phase 1: Small domain — paraboloid only, P looks like global max
        # -------------------------------------------------------
        with self.voiceover("Let's suppose we have a point P where all the first derivatives are zero. We know that this point is a local maximum in every direction.") as tracker:
            self.play(Create(gs.axes))
            self.add_fixed_orientation_mobjects(P_label_3d)
            self.play(FadeIn(gs.base_dot), FadeIn(P_label_3d))

            self.add_fixed_in_frame_mobjects(t0_txt)
            self.play(FadeIn(t0_txt))
            self.wait(0.5)

            # Draw arcs in 8 directions from P, showing it curves down in every direction
            arc_t_vals = np.linspace(-1.2, 1.2, 60)
            dir_arcs = VGroup()
            NUM_ARCS = 37
            for i in range(NUM_ARCS):
                th = i * PI / NUM_ARCS
                arc = VMobject(color=BLUE_B, stroke_width=2)
                arc.set_points_as_corners([
                    gs.axes.c2p(t * np.cos(th), t * np.sin(th),
                                f(t * np.cos(th), t * np.sin(th)))
                    for t in arc_t_vals
                ])
                dir_arcs.add(arc)
            self.play(LaggedStart(*[Create(arc, run_time = 2 / NUM_ARCS) for arc in dir_arcs],
                                  lag_ratio=2 / NUM_ARCS, run_time=2.5))
            self.wait(0.5)

            self.play(FadeIn(surf_small),
                      *[FadeOut(arc) for arc in dir_arcs],
                      run_time=1)
            # self.wait(tracker.duration - tracker.time_until_bookmark())

        # -------------------------------------------------------
        # Phase 2: Extend domain — gaussian bump appears, Q revealed
        # -------------------------------------------------------
        with self.voiceover("But we want to prove that it is the global maximum. We will do that by contradiction.") as tracker:
            ...

        with self.voiceover("Suppose there's some point Q with a higher log likelihood than P.") as tracker:
            self.add_fixed_in_frame_mobjects(t1_txt)
            self.play(FadeOut(t0_txt), FadeIn(t1_txt))

            self.play(
                FadeOut(surf_small),
                FadeIn(gs.surface),
                run_time=1.5,
            )
            self.remove(surf_small)
            self.add_fixed_orientation_mobjects(Q_label_3d)
            self.play(FadeIn(Q_dot), FadeIn(Q_label_3d))
            # self.wait(tracker.duration - tracker.time_until_bookmark())

        # -------------------------------------------------------
        # Phase 3: Slice plane and curve
        # -------------------------------------------------------
        with self.voiceover("We consider the log likelihood evaluated on the line segment between P and Q.") as tracker:
            self.play(FadeIn(gs.slice_plane))
            self.play(Create(gs.slice_curve))
            # self.wait(tracker.duration - tracker.time_until_bookmark())

            # -------------------------------------------------------
            # Phase 4: Copy to 2D
            # -------------------------------------------------------
            three_d_group = VGroup(gs.axes, gs.surface, gs.slice_plane, gs.slice_curve, gs.base_dot, Q_dot, P_label_3d, Q_label_3d)
            shift = shift_to_screen_corner(self, three_d_group, corner=UR, scale = 0.5)
            self.play(three_d_group.animate.shift(shift).scale(0.5), run_time=1.35)
            gs.animate_copy(self, extra_copy_pairs=[(Q_dot, Q_dot2d)], move_before_copy=False)

            # Highlight [P, Q] on the 2D graph, then fade out the outside portions.
            # Strategy: fade in a PQ-only segment while fading out the full curve.
            # Over [P,Q] the two cancel (opacity stays 1); outside just disappears.
            t_pq = np.linspace(0, t_Q, 80)
            pq_highlight = VMobject(color=YELLOW, stroke_width=6)
            pq_highlight.set_points_as_corners([gs.axes2d.c2p(t, gs.g(t)) for t in t_pq])
            self.add_fixed_in_frame_mobjects(pq_highlight)
            self.play(FadeIn(pq_highlight))
            self.wait(0.5)

            pq_seg = VMobject(color=ORANGE)
            pq_seg.set_points_as_corners([gs.axes2d.c2p(t, gs.g(t)) for t in t_pq])
            self.add_fixed_in_frame_mobjects(pq_seg)
            self.play(
                FadeOut(pq_highlight),
                FadeOut(gs.graph_curve),
                FadeIn(pq_seg),
            )

            # -------------------------------------------------------
            # Phase 5: 2D proof
            # -------------------------------------------------------
            self.add_fixed_in_frame_mobjects(P_label_2d, Q_label_2d)
            self.play(FadeIn(P_label_2d), FadeIn(Q_label_2d))

        with self.voiceover("By the Extreme Value Theorem, the log likelihood must have a minimum somewhere on this interval.") as tracker:
            self.add_fixed_in_frame_mobjects(t2_txt)
            self.play(FadeOut(t1_txt), FadeIn(t2_txt))
            # self.wait(tracker.duration - tracker.time_until_bookmark())

        with self.voiceover("The minimum is not at P because P is a local maximum.") as tracker:
            self.add_fixed_in_frame_mobjects(P_arc, t3_txt)
            self.play(FadeIn(P_arc), FadeOut(t2_txt), FadeIn(t3_txt))
            # self.wait(tracker.duration - tracker.time_until_bookmark())

        with self.voiceover("And the minimum is not at Q because it's higher than P.") as tracker:
            self.add_fixed_in_frame_mobjects(t4_txt)
            self.play(FadeOut(t3_txt), FadeIn(t4_txt), Indicate(Q_dot2d, scale_factor=1.5, color=GREEN, run_time=2))
            # self.wait(tracker.duration - tracker.time_until_bookmark())

        with self.voiceover("So the minimum on this line segment must be somewhere in the interior. Let's call that point M.") as tracker:
            self.add_fixed_in_frame_mobjects(M_dot_2d, M_label_2d, t5_txt)
            self.play(FadeIn(M_dot_2d), FadeIn(M_label_2d), FadeOut(t4_txt), FadeIn(t5_txt))
            # self.wait(tracker.duration - tracker.time_until_bookmark())

        with self.voiceover("So, M is a local minimum! And that means the directional second derivative at M is positive. But earlier we proved that the directional second derivative is negative everywhere. So we have a contradiction.") as tracker:
            self.add_fixed_in_frame_mobjects(M_arc, t6_txt)
            self.play(FadeIn(M_arc), FadeOut(t5_txt), FadeIn(t6_txt))
            self.wait(1)
            self.add_fixed_in_frame_mobjects(t7_txt)
            self.play(FadeOut(t6_txt), FadeIn(t7_txt))
            self.play(
                Flash(gs.axes2d.c2p(t_M, gs.g(t_M)), color=RED, flash_radius=0.3),
                M_arc.animate.set_color(YELLOW),
            )

        # Build conclusion targets: pure negative paraboloid, created after the 3D group
        # has been moved/scaled so gs.axes.c2p() gives the right coordinates.
        t_vals = np.linspace(-2.3, 2.3, 100)
        conclusion_surface = Surface(
            lambda u, v: gs.axes.c2p(u, v, -(u**2 + v**2)),
            u_range=(-2.3, 2.3),
            v_range=(-2, 2),
            resolution=(18, 18),
            fill_opacity=0.35,
        )
        conclusion_surface.set_fill(BLUE_B, opacity=0.35)

        conclusion_slice_3d = VMobject(color=ORANGE)
        conclusion_slice_3d.set_points_as_corners(
            [gs.axes.c2p(t, 0, -(t**2)) for t in t_vals]
        )

        conclusion_graph_2d = VMobject(color=ORANGE)
        conclusion_graph_2d.set_points_as_corners(
            [gs.axes2d.c2p(t, -(t**2)) for t in np.linspace(0, t_Q, 80)]
        )

        with self.voiceover("Therefore, our assumption that Q is higher than P is wrong. Therefore all points are lower than P.") as tracker:
            self.play(FadeOut(P_arc, M_arc, M_dot_2d, M_label_2d))
            self.add_fixed_in_frame_mobjects(t8_txt)
            new_q_2d = gs.axes2d.c2p(t_Q, -(t_Q**2))
            self.play(
                FadeOut(t7_txt), FadeIn(t8_txt),
                Transform(gs.surface, conclusion_surface),
                Transform(gs.slice_curve, conclusion_slice_3d),
                Transform(pq_seg, conclusion_graph_2d),
                Q_dot.animate.move_to(gs.axes.c2p(t_Q, 0, -(t_Q**2))),
                Q_dot2d.animate.move_to(new_q_2d),
                Q_label_2d.animate.next_to(new_q_2d, UR, buff=0.08),
            )
            # self.wait(tracker.duration - tracker.time_until_bookmark())
