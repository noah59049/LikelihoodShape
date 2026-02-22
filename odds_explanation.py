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

        quote.animate.shift(quote.height * UP * 2)
        checks = VGroup(
            Text("✓", font_size=70).set_color(GREEN)
        )

        crosses = VGroup(*[
            Text("✗", font_size=70).set_color(RED)
            for _ in range(11)
        ])

        trials = VGroup(*checks, *crosses)
        trials.arrange_in_grid(rows=3, cols=4, buff=0.4)

        self.play(LaggedStart(*[FadeIn(t, scale=1.2) for t in trials], lag_ratio=0.05))

        # Part 3: 