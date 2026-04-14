from manim import *
import numpy as np

class ShrinkingSecantScene(Scene):
    def construct(self):
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

        self.play(Create(axes), Write(labels))
        self.play(Create(graph))
        self.wait()

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
        self.wait()

        # -------------------------------------------------
        # Shrink Δx → 0
        # -------------------------------------------------
        self.play(
            dx_tracker.animate.set_value(0.05),
            run_time=4,
            rate_func=smooth,
        )
        self.wait()

        # Show tangent line
        self.play(
            FadeOut(secant_line),
            Create(tangent_line),
        )
        self.wait()

        # Final shrink for emphasis
        self.play(
            dx_tracker.animate.set_value(0.001),
            run_time=2,
        )
        self.wait()