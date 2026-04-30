from manim import *
import numpy as np
from manim_voiceover import *
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
from MF_Tools import *
from N_Tools import FadeInRHS


class ShrinkingSecantScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService(r"/Users/noah/Convex/LikelihoodShape/podcasts/shrinking_secant_podcast0.mp3",
        cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
        min_silence_len=2000,
        keep_silence=(0,0)))

        # -------------------------------------------------
        # Tex definitions of the derivative
        # -------------------------------------------------      
        derivs = [
        MathTex(r"f'(x)"),
        MathTex(r"f'(x) = \frac{\Delta{f}}{\Delta{x}}"),
        MathTex(r"f'(x) = \lim_{\Delta{x} \to 0} \frac{\Delta{f}}{\Delta{x}}"),
        MathTex(r"f'(x) = \lim_{\Delta{x} \to 0} \frac{f(x + \Delta{x}) - f(x)}{\Delta{x}}"),
        MathTex(r"f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}"),
        ]

        for deriv in derivs:
            deriv.to_corner(UL)

        # -------------------------------------------------
        # Function definition
        # -------------------------------------------------
        def f(x):
            return 0.5 * x**2

        # -------------------------------------------------
        # Axes and graph
        # -------------------------------------------------
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-1, 5, 1],
            axis_config={"include_numbers": True},
        )

        labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        graph = axes.plot(f, x_range=[-3, 3], color=BLUE)

        with self.voiceover("If we have a function of a single variable f(x), the derivative is the ") as tracker:
            self.play(Create(axes), Write(labels))
            self.play(Create(graph))
            self.play(Write(derivs[0]))


        # -------------------------------------------------
        # Base point and tracker for Δx
        # -------------------------------------------------
        x0 = 1
        dx_tracker = ValueTracker(1.5)

        # Helper functions
        def point_on_graph(x):
            return axes.c2p(x, f(x))

        # Fixed base point
        dot_a = always_redraw(
            lambda: Dot(point_on_graph(x0), color=RED)
        )

        # Moving point
        dot_b = always_redraw(
            lambda: Dot(
                point_on_graph(x0 + dx_tracker.get_value()),
                color=YELLOW
            )
        )

        # Vertical projection for Δf
        dot_proj = always_redraw(
            lambda: Dot(
                axes.c2p(
                    x0 + dx_tracker.get_value(),
                    f(x0)
                ),
                radius=0.04,
                color=WHITE
            )
        )

        # -------------------------------------------------
        # Δx and Δf segments
        # -------------------------------------------------
        delta_x = always_redraw(
            lambda: Line(
                axes.c2p(x0, f(x0)),
                axes.c2p(
                    x0 + dx_tracker.get_value(),
                    f(x0)
                ),
                color=GREEN
            )
        )

        delta_f = always_redraw(
            lambda: Line(
                axes.c2p(
                    x0 + dx_tracker.get_value(),
                    f(x0)
                ),
                point_on_graph(
                    x0 + dx_tracker.get_value()
                ),
                color=PURPLE
            )
        )

        # Labels
        label_dx = always_redraw(
            lambda: MathTex(r"\Delta x")
            .scale(0.6)
            .next_to(delta_x, DOWN, buff=0.1)
        )

        label_df = always_redraw(
            lambda: MathTex(r"\Delta f")
            .scale(0.6)
            .next_to(delta_f, RIGHT, buff=0.1)
        )

        # -------------------------------------------------
        # Secant line
        # -------------------------------------------------
        secant_line = always_redraw(
            lambda: Line(
                point_on_graph(x0),
                point_on_graph(
                    x0 + dx_tracker.get_value()
                ),
                color=ORANGE
            )
        )

        # Tangent line
        slope = x0  # derivative of 0.5x^2 is x

        tangent_line = axes.plot(
            lambda x: f(x0) + slope * (x - x0),
            x_range=[-3, 3],
            color=BLUE,
        )

        # -------------------------------------------------
        # Animate appearance
        # -------------------------------------------------
        with self.voiceover("change in the function value divided by the change in x, ") as tracker:
            self.play(
                FadeIn(dot_a),
                FadeIn(dot_b),
                FadeIn(dot_proj),
                Create(secant_line),
                Create(delta_x),
                Create(delta_f),
                Write(label_dx),
                Write(label_df),
            )
            self.play(FadeInRHS(derivs[0], derivs[1]))

        # -------------------------------------------------
        # Shrink Δx → 0
        # -------------------------------------------------
        with self.voiceover("in the limit as the change in x goes to 0. And geometrically it’s ") as tracker:
            self.play(
                dx_tracker.animate.set_value(0.001),
                run_time=4,
                rate_func=smooth,
            )
            self.play(TransformByGlyphMap(derivs[1], derivs[2],
                                      (FadeIn, range(6,13))))
            self.play(TransformByGlyphMap(derivs[2], derivs[3],
                                        ([13,14], range(13,25))))
            self.play(TransformByGlyphMap(derivs[3], derivs[4],
                                        ([9,10], [9]),
                                        ([17,18], [16]),
                                        ([26,27], [24]),
                                        ))

        # Show tangent line
        with self.voiceover("the slope of the tangent line.") as tracker:
            self.play(
                FadeOut(secant_line),
                Create(tangent_line),
            )