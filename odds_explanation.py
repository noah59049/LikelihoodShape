import numpy as np
from manim import *
from MF_Tools import *


class OddsScene(Scene):
    def construct(self):
        # Part 1: Tex
        tex1 = MathTex(r"Odds=\frac{P(Y=1)}{P(Y=0)}")
        tex2 = MathTex(r"p=P(Y=1)")
        tex2.shift(tex2.height * UP * 3)
        tex3 = MathTex(r"Odds=\frac{P(Y=1)}{1-P(Y=1)}")
        tex4 = MathTex(r"Odds=\frac{p}{1-p}}")

        self.play(Write(tex1))
        self.play(Write(tex2))
        self.play(TransformByGlyphMap(tex1, tex3,
                                      (FadeIn, [12,13])))
        self.play(TransformByGlyphMap(tex3, tex4,
                                      (range(5,11), [5]),
                                      (range(14,20), [9])))
        
        # Part 2: Example from poker
        self.remove(tex2, tex4)

        avatar = Square()
        self.add(avatar)
        self.wait(1)
        self.remove(avatar)

        quote = Text('"The odds of hitting a gutshot straight draw on the turn is 8.5%,\nor 10.75-to-1 odds against"', font_size = 32)
        self.add(quote)
        quote.shift(quote.height * UP * 2)

        full_xs = VGroup(*[
            Text("✗", font_size=70).set_color(RED)
            for _ in range(10)
        ])

        partial_x = Text("✗", font_size=70).set_color(RED)

        # Compute cutoff position (75% from left)
        left = partial_x.get_left()[0]
        right = partial_x.get_right()[0]
        cutoff = left + 0.75 * (right - left)

        # Keep only points left of cutoff
        partial_x.set_points(
            partial_x.points[
                partial_x.points[:, 0] <= cutoff
            ]
        )

        check = Text("✓", font_size=70).set_color(GREEN)

        trials = VGroup(*full_xs, partial_x, check)
        trials.arrange(RIGHT, buff=0.3)

        self.play(FadeIn(trials))

        # Part 3: 