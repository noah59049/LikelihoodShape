from manim import *
from MF_Tools import *

class LikelihoodDefinition(Scene):
    def construct(self):
        # Step 1: Write the piecewise expression for the likelihood
        base = MathTex(r"L=\prod_{i=1}^{n}")
        brace = MathTex(r"\left\{").scale(1.6).next_to(base, RIGHT)
        row1 = MathTex(r"\hat{y}_i \quad \quad \quad (y_i=1)")
        row2 = MathTex(r"1-\hat{y}_i \quad \thinspace \thinspace (y_i=0)") # This leads to the conditions being aligned somehow, probably not the best fix but it works
        rows = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(brace, RIGHT, aligned_edge = UP)
        cases = VGroup(base, brace, rows).to_edge(UP)
        
        self.play(Write(base))
        self.play(Write(brace))
        self.play(Write(row1))
        self.play(Write(row2))

        # Step 2: Likelihood simplification for case y_i=1

        success1 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        success2 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{1}(1-\hat{y}_i)^{1-{1}}")
        success3 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{1}")
        success4 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i")

        self.play(FadeIn(success1))
        box1 = SurroundingRectangle(row1, color = RED)
        self.play(row1.animate.set_color(RED), Create(box1))

        self.play(TransformByGlyphMap(success1, success2,
            ([9,10], [9]),
            ([21,22], [20])))
        self.play(TransformByGlyphMap(success2, success3,
            (range(11), range(11), {"delay": 0.7}),
            (range(11,21), FadeOut)))
        self.play(TransformByGlyphMap(success3, success4,
            (range(9), range(9), {"delay": 0.4}),
            (range(9,10), FadeOut)))
        
        self.play(FadeOut(success4), row1.animate.set_color(WHITE), FadeOut(box1))
        
        # Step 3: Likelihood simplification for case y_i=0
        failure1 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        failure2 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{0}(1-\hat{y}_i)^{1-{0}}")
        failure3 = MathTex(r"L=\prod_{i=1}^{n}(1-\hat{y}_i)^{1-{0}}")
        failure4 = MathTex(r"L=\prod_{i=1}^{n}1-\hat{y}_i")

        self.play(FadeIn(failure1))
        box2 = SurroundingRectangle(row2, color = RED)
        self.play(row2.animate.set_color(RED), Create(box2))

        self.play(TransformByGlyphMap(failure1, failure2,
            ([9,10], [9]),
            ([21,22], [20])))
        self.play(TransformByGlyphMap(failure2, failure3,
            ([7,8,9,10], FadeOut)))
        self.play(TransformByGlyphMap(failure3, failure4,
            ([7],FadeOut),
            ([13,14,15,16], FadeOut)))
        
        self.play(FadeOut(failure4), row2.animate.set_color(WHITE), FadeOut(box2))
        self.play(FadeIn(failure1))
        
