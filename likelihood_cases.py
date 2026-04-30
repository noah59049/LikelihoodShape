from manim import *
from MF_Tools import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.stitcher import _StitcherService as StitcherService

def boxes_for_glyph_groups(mobj, groups, **kwargs):
    return VGroup(*[
        SurroundingRectangle(
            VGroup(*[mobj[0][i] for i in group]),
            **kwargs
        )
        for group in groups
    ])

def _glyph_group(mobj, indices):
    """
    Robust glyph extraction for Text, Tex, MathTex, etc.
    """
    try:
        return VGroup(*[mobj[i] for i in indices])
    except Exception:
        return VGroup(*[mobj[0][i] for i in indices])


class TransformWithBoxes(AnimationGroup):
    def __init__(
        self,
        src,
        dst,
        *mappings,                 # same format as TransformByGlyphMap
        box_kwargs=None,
        create_boxes_anim=Create,
        remove_boxes_anim=FadeOut,
        lag_ratio=1.0,
        **kwargs                  # passed to AnimationGroup
    ):
        box_kwargs = box_kwargs or {"color": RED, "buff": 0.1}

        # Build boxes
        boxes = VGroup(*[
            SurroundingRectangle(
                _glyph_group(src, src_inds),
                **box_kwargs
            )
            for src_inds, _ in mappings
        ])

        # Core animation
        transform = TransformByGlyphMap(src, dst, *mappings)

        # Full animation sequence
        animations = [
            create_boxes_anim(boxes),
            transform,
            remove_boxes_anim(boxes),
        ]

        super().__init__(*animations, lag_ratio=lag_ratio, **kwargs)
        
class LikelihoodCasesScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService(r"/Users/noah/Convex/LikelihoodShape/podcasts/likelihood_cases_podcast1.mp3",
        cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
        min_silence_len=2000,
        keep_silence=(0,0)))

        # Step 1: Write the piecewise expression for the likelihood
        base = MathTex(r"L=\prod_{i=1}^{n}")
        brace = MathTex(r"\left\{").scale(1.6).next_to(base, RIGHT)
        row1 = MathTex(r"\hat{y}_i \quad \quad \quad (y_i=1)")
        row2 = MathTex(r"1-\hat{y}_i \quad \thinspace \thinspace (y_i=0)") # This leads to the conditions being aligned somehow, probably not the best fix but it works
        rows = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(brace, RIGHT, aligned_edge = UP)
        cases = VGroup(base, brace, rows).to_edge(UP)

        row1_basic = MathTex(r"\hat{y} \quad \quad \quad (y=1)")
        row2_basic = MathTex(r"1-\hat{y} \quad \thinspace \thinspace (y=0)") # This leads to the conditions being aligned somehow, probably not the best fix but it works
        rows_basic = VGroup(row1_basic, row2_basic).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(brace, RIGHT, aligned_edge = UP)
        
        with self.voiceover("Now let’s write a formula for the likelihood. We’ll be taking a product, a product of the predicted probabilities of the observed outcomes.") as tracker:
            self.play(Write(base, run_time = 0.5))
            self.add(brace)
        with self.voiceover("So if y is 1, the predicted probability of y being 1 is y hat, ") as tracker:
            self.play(Write(row1_basic, run_time = 0.5))
        with self.voiceover("and if y is 0, the predicted probability of y being 0 is 1 - y hat. We should subscript all our ys with  ") as tracker:
            self.play(Write(row2_basic, run_time = 0.5))

        with self.voiceover("i because each element of this product is referring to the ith individual.") as tracker:
            self.play(TransformMatchingShapes(row1_basic, row1), TransformMatchingShapes(row2_basic, row2))


        # Step 2: Likelihood simplification for case y_i=1

        success1 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        success2 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{1}(1-\hat{y}_i)^{1-{1}}")
        success2a= MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{1}(1-\hat{y}_i)^{0}")
        success3 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{1}")
        success4 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i")

        with self.voiceover("So this formula is correct, but the likelihood is instead usually written as the product of yi hat to the yi times 1 minus yi hat to the 1 minus yi. And this is equivalent. ") as tracker:
            self.play(FadeIn(success1))

        box1 = SurroundingRectangle(row1, color = RED)
        with self.voiceover("if we look at the case where yi=1, the right hand term becomes 1-yi hat raised") as tracker:
            self.play(row1.animate.set_color(RED), Create(box1, run_time = 0.5))
            self.play(TransformWithBoxes(success1, success2,
                ([9,10], [9]),
                ([21,22], [20])))

        with self.voiceover(" to the power of 0,") as tracker:
            self.play(TransformByGlyphMap(success2, success2a,
                                          ([18,19,20], [18])))

        with self.voiceover("so it goes away, and the left hand term becomes yi hat, same as in the first formula") as tracker:
            self.play(TransformByGlyphMap(success2a, success3,
                (range(11), range(11), {"delay": 0.7}),
                (range(11,19), FadeOut)))

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
        
        with self.voiceover("If you look at the case where yi=0,") as tracker:
            box2 = SurroundingRectangle(row2, color = RED)
            self.play(row2.animate.set_color(RED), Create(box2))
            self.play(
                TransformWithBoxes(
                    failure1, failure2,
                    ([9,10], [9]),
                    ([21,22], [20])
                )
            )

        with self.voiceover("the left hand term becomes yi hat raised to the 0,") as tracker:
            pass

        with self.voiceover("so it goes away, ") as tracker:
            self.play(TransformByGlyphMap(failure2, failure3,
                ([7,8,9,10], FadeOut)))

        with self.voiceover("and the right hand term becomes 1 - yi hat, again, same as above. The log-likelihood, written lowercase l, is just the") as tracker:
            self.play(TransformByGlyphMap(failure3, failure4,
                ([7],FadeOut),
                ([13,14,15,16], FadeOut)))

            self.wait(tracker.duration - 3.1)
            self.play(FadeOut(failure4), row2.animate.set_color(WHITE), FadeOut(box2))
            self.play(FadeIn(failure1))
        
        # Step 4: Add log likelihood
        loglik1 = MathTex(r"l=ln\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        loglik2 = MathTex(r"l=\sum_{i=1}^{n}ln[\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}]")
        loglik3 = MathTex(r"l=\sum_{i=1}^{n}ln\hat{y}_i^{y_i}+ln(1-\hat{y}_i)^{1-{y_i}}")
        loglik4 = MathTex(r"l=\sum_{i=1}^{n}y_iln\hat{y}_i+({1-{y_i}})ln(1-\hat{y}_i)")

        with self.voiceover(" ln of the likelihood. If we simplify a bit, ") as tracker:
            self.play(TransformByGlyphMap(failure1, loglik1,
                                        ([0], [0]),
                                        ([], [2,3])))

        with self.voiceover("the ln of a product is the sum of the lns,") as tracker:
            self.play(TransformByGlyphMap(loglik1, loglik2,
                                        ([5], [3]),
                                        ([2,3], [7,8]),
                                        (FadeIn, [9,26])))

        with self.voiceover("do it again ") as tracker:
            self.play(TransformByGlyphMap(loglik2, loglik3,
                                        ([9,26], FadeOut),
                                        (FadeIn, [14]),
                                        ([7,8], [7,8]),
                                        ([7,8],[15,16], {"path_arc": PI * -0.7})))

        with self.voiceover("and then move the exponents. Maximizing the likelihood is equivalent to maximizing the log likelihood. But using the log likelihood makes the math easier.") as tracker:
            self.play(TransformByGlyphMap(loglik3, loglik4,
                                        ([11,12],[7,8],{"path_arc": PI * 0.7}),
                                        (range(24,28),range(16,20), {"path_arc": PI * 0.7}),
                                        (FadeIn, [15,21])))
        