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
        
        self.play(Write(base, run_time = 0.5))
        self.wait(13.5)
        self.add(brace)
        self.play(Write(row1, run_time = 0.5))
        self.wait(9.5)
        self.play(Write(row2, run_time = 0.5))
        self.wait(9.5)

        # Step 2: Likelihood simplification for case y_i=1

        success1 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        success2 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{1}(1-\hat{y}_i)^{1-{1}}")
        success3 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{1}")
        success4 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i")

        self.wait(5)
        self.play(FadeIn(success1, run_time = 0.5))
        self.wait(6.5)

        self.wait(3.7)
        box1 = SurroundingRectangle(row1, color = RED)
        self.play(row1.animate.set_color(RED), Create(box1, run_time = 0.5))
        self.wait(1.8)

        self.play(TransformByGlyphMap(success1, success2,
            ([9,10], [9]),
            ([21,22], [20])))
        self.wait(5)
        self.play(TransformByGlyphMap(success2, success3,
            (range(11), range(11), {"delay": 0.7}),
            (range(11,21), FadeOut)))
        self.wait(2.25)
        self.play(TransformByGlyphMap(success3, success4,
            (range(9), range(9), {"delay": 0.4}),
            (range(9,10), FadeOut)))
        self.wait(2)
        
        self.play(FadeOut(success4), row1.animate.set_color(WHITE), FadeOut(box1))
        
        # Step 3: Likelihood simplification for case y_i=0
        failure1 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        failure2 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{0}(1-\hat{y}_i)^{1-{0}}")
        failure3 = MathTex(r"L=\prod_{i=1}^{n}(1-\hat{y}_i)^{1-{0}}")
        failure4 = MathTex(r"L=\prod_{i=1}^{n}1-\hat{y}_i")

        self.play(FadeIn(failure1))
        box2 = SurroundingRectangle(row2, color = RED)
        self.play(row2.animate.set_color(RED), Create(box2))

        self.wait(2.5)
        self.play(TransformByGlyphMap(failure1, failure2,
            ([9,10], [9]),
            ([21,22], [20])))
        self.wait(1.95)
        self.play(TransformByGlyphMap(failure2, failure3,
            ([7,8,9,10], FadeOut)))
        self.wait(2.3)
        self.play(TransformByGlyphMap(failure3, failure4,
            ([7],FadeOut),
            ([13,14,15,16], FadeOut)))
        self.wait(4.7)
        
        self.play(FadeOut(failure4), row2.animate.set_color(WHITE), FadeOut(box2))
        self.play(FadeIn(failure1))
        
        # Step 4: Add log likelihood
        loglik1 = MathTex(r"l=ln\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        loglik2 = MathTex(r"l=\sum_{i=1}^{n}ln[\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}]")
        loglik3 = MathTex(r"l=\sum_{i=1}^{n}ln\hat{y}_i^{y_i}+ln(1-\hat{y}_i)^{1-{y_i}}")
        loglik4 = MathTex(r"l=\sum_{i=1}^{n}y_iln\hat{y}_i+({1-{y_i}})ln(1-\hat{y}_i)")

        self.wait(5.65)
        self.play(TransformByGlyphMap(failure1, loglik1,
                                      ([0], [0]),
                                      ([], [2,3])))
        self.wait(3)
        self.play(TransformByGlyphMap(loglik1, loglik2,
                                      ([5], [3]),
                                      ([2,3], [7,8]),
                                      (FadeIn, [9,26])))
        self.wait(1.3)
        self.play(TransformByGlyphMap(loglik2, loglik3,
                                      ([9,26], FadeOut),
                                      (FadeIn, [14]),
                                      ([7,8], [7,8]),
                                      ([7,8],[15,16], {"path_arc": PI * -0.7})))
        self.wait(3)
        self.play(TransformByGlyphMap(loglik3, loglik4,
                                      ([11,12],[7,8],{"path_arc": PI * 0.7}),
                                      (range(24,28),range(16,20), {"path_arc": PI * 0.7}),
                                      (FadeIn, [15,21])))
        