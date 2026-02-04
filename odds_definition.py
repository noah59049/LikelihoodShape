#!/usr/bin/env python


from manim import *
from manim_voiceover import VoiceoverScene
from MF_Tools import *
from manim_voiceover.services.coqui import CoquiService

class DefinitionsScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(CoquiService())

        p1 = MathTex(r"P(y=1)")
        p2 = MathTex(r"p")
        odds1 = MathTex(r"Odds")
        odds2 = MathTex(r"Odds = \frac{p}{1-p}")
        logodds1 = MathTex(r"\ln\frac{p}{1-p}")
        logodds2 = MathTex(r"\ln\frac{p}{1-p}=\beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")
        logodds3 = MathTex(r"\ln\frac{p_i}{1-p_i}=\beta_0+\beta_1 X_{i,1}+\beta_2 X_{i,2}+\ldots+\beta_{k-1} X_{i,k-1}")

        logodds2colored = MathTex(r"\ln\frac{p}{1-p}=\beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}", substrings_to_isolate = [r"\beta_0"])

        # logodds2b0 = MathTex(r"ln\frac{p}{1-p}=\textcolor{red}{\beta_0}+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")

        with self.voiceover(text = "We are trying to look at how the probability that y is 1 depends on the Xs") as tracker:
            self.play(Write(p1))
        with self.voiceover(text = "So we denote that as p") as tracker:
            self.play(ReplacementTransform(p1, p2))
        self.play(FadeOut(p2))
        with self.voiceover(text = "Instead of directly looking at probability, we look at the odds. Now, people often use probability and odds interchangeably,"
                            "but here we mean odds in the sense where it's the probability of an event happening divided by the probability of it not happening"
                            "And you might have heard the term odds used in this sense. If someone says the odds of such and such event are 3 to 1,"
                            "They probably mean it's 3 times as likely to happen as not to happen, and this corresponds to a probability of 3/4") as tracker:
            self.play(FadeIn(odds1))
        with self.voiceover(text = "So we represent odds as p over 1 minus p") as tracker:
            self.play(TransformByGlyphMap(odds1, odds2,
                (FadeIn, range(4,10))))
        with self.voiceover(text = "So we actually look at the log odds, or just the ln of the odds") as tracker:
            self.play(TransformByGlyphMap(odds2, logodds1,
                ([0,1,2,3,4],[0,1])))
        with self.voiceover(text = "And the big assumption of logistic regression is that the log odds is equal to a linear combination of the Xs") as tracker:
            self.play(TransformByGlyphMap(logodds1, logodds2,
                (FadeIn, range(7, 33), {"delay":0.5, "run_time":1.4})))
        
        self.remove(logodds2)
        self.add(logodds2colored)
        logodds2colored.set_color_by_tex(r"\beta_0", RED)
        self.wait(0.7)
        self.remove(logodds2colored)
        self.add(logodds2)

        with self.voiceover(text = "And then we are looking at the Eye-Ith individual, so we subscript the p and the Xs with i") as tracker:
            self.play(TransformByGlyphMap(logodds2, logodds3,
                (FadeIn, [3]),
                (FadeIn, [8]),
                (FadeIn, [16,17]),
                (FadeIn, [23, 24]),
                (FadeIn, [36, 37])))