from manim import *
from MF_Tools import *

class LoglikSimplificationScene(Scene):
    def construct(self):
        # We will probably start with loglik4, but it's nice to have these I guess
        loglik1  = MathTex(r"l=\ln\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        loglik2  = MathTex(r"l=\sum_{i=1}^{n}\ln[\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}]")
        loglik3  = MathTex(r"l=\sum_{i=1}^{n}\ln\hat{y}_i^{y_i}+\ln(1-\hat{y}_i)^{1-{y_i}}")
        loglik4  = MathTex(r"l=\sum_{i=1}^{n}y_i\ln\hat{y}_i+({1-{y_i}})\ln(1-\hat{y}_i)")
        loglik5  = MathTex(r"l=\sum_{i=1}^{n}y_i\ln\hat{y}_i+\ln(1-\hat{y}_i)-{y_i}\ln(1-\hat{y}_i)")
        loglik6  = MathTex(r"l=\sum_{i=1}^{n}y_i\ln\hat{y}_i-{y_i}\ln(1-\hat{y}_i)+\ln(1-\hat{y}_i)")
        loglik7  = MathTex(r"l=\sum_{i=1}^{n}y_i(\ln\hat{y}_i-\ln(1-\hat{y}_i))+\ln(1-\hat{y}_i)")
        loglik8  = MathTex(r"l=\sum_{i=1}^{n}y_i(\ln\frac{\hat{y}_i}{1-\hat{y}_i})+\ln(1-\hat{y}_i)")
        loglik9  = MathTex(r"l=\sum_{i=1}^{n}y_i(\hat{\beta_0}+\hat{\beta_1} X_{i,1}+\hat{\beta_2} X_{i,2}+\ldots+\hat{\beta}_{k-1} X_{i,k-1})+\ln(1-\hat{y}_i)")
        loglik10 = MathTex(r"l=\sum_{i=1}^{n}y_iz_i+\ln(1-\hat{y}_i)")
        loglik11 = MathTex(r"l=\sum_{i=1}^{n}y_i\hat{z}_i+\ln(1-\hat{y}_i)")
        loglik12 = MathTex(r"l=\sum_{i=1}^{n}y_i\hat{z}_i+\ln(1-\sigma(\hat{z}_i))")
        loglik13 = MathTex(r"l=\sum_{i=1}^{n}y_i\hat{z}_i+\ln(1-\frac{e^{\hat{z}_i}}{e^{\hat{z}_i}+1})")
        loglik14 = MathTex(r"l=\sum_{i=1}^{n}y_i\hat{z}_i+\ln(\frac{e^{\hat{z}_i}+1}{e^{\hat{z}_i}+1}-\frac{e^{\hat{z}_i}}{e^{\hat{z}_i}+1})")
        loglik15 = MathTex(r"l=\sum_{i=1}^{n}y_i\hat{z}_i+\ln(\frac{e^{\hat{z}_i}+1-e^{\hat{z}_i}}{e^{\hat{z}_i}+1})")
        loglik16 = MathTex(r"l=\sum_{i=1}^{n}y_i\hat{z}_i+\ln(\frac{1}{e^{\hat{z}_i}+1})")
        loglik17 = MathTex(r"l=\sum_{i=1}^{n}y_i\hat{z}_i-\ln(e^{\hat{z}_i}+1)")

        self.play(Write(loglik4))
        self.play(TransformByGlyphMap(loglik4, loglik5,
                                      (range(21,30), range(15,24), {"path_arc":PI}),
                                      (range(21,30), range(27,36)),
                                      ([15,20], FadeOut, {"run_time":0.5}),
                                      ([16], FadeOut),
                                      ([17,18,19], [24,25,26])))
        
        self.play(TransformByGlyphMap(loglik5, loglik6,
                                      (range(24,36), range(14,26), {"path_arc":PI}),
                                      (range(14,24), range(26,36), {"path_arc":PI})))
        
        self.play(TransformByGlyphMap(loglik6, loglik7,
                                      ([15,16], FadeOut),
                                      (FadeIn, [9,25])))
        
        self.play(TransformByGlyphMap(loglik7, loglik8,
                                      ([12,13,14], [12,13,14], {"path_arc": -PI/4}),
                                      (range(19,24), range(16,21), {"path_arc": -PI/4}),
                                      (FadeIn, [15]),
                                      ([15,16,17], FadeOut, {"run_time":0.5}),
                                      ([18,24], FadeOut, {"run_time":0.5})))
        
        self.play(TransformByGlyphMap(loglik8, loglik9,
                                      (range(10,21),range(10,45))))
        
        self.play(TransformByGlyphMap(loglik9, loglik10,
                                      (range(9,46), [10,11])))
        
        self.play(TransformByGlyphMap(loglik10, loglik11,
                                      (FadeIn, [9])))
        
        self.play(TransformByGlyphMap(loglik11, loglik12,
                                      (range(18,21), range(18,24))))
        
        self.play(TransformByGlyphMap(loglik12, loglik13,
                                      ([18,19,23], FadeOut, {"run_time":0.5}),
                                      (FadeIn, [18,22,23,27,28], {"delay":0.25, "run_time":0.73}),
                                      ([20,21,22],[19,20,21]),
                                      ([20,21,22],[24,25,26])))
        
        self.play(TransformByGlyphMap(loglik13,loglik14,
                                      ([16], range(16,29))))
        
        self.play(TransformByGlyphMap(loglik14, loglik15,
                                      (range(16,22), range(16,22)),
                                      ([29],[22]),
                                      (range(30,34), range(23,27)),
                                      (range(23,29), range(28,34), {"path_arc":PI/2}),
                                      (range(35,41), range(28,34), {"path_arc":-PI/2}),
                                      ([22,34],[27])))
        
        self.play(TransformByGlyphMap(loglik15, loglik16,
                                      (range(16,21), []),
                                      (range(22,27), [])))
        
        self.play(TransformByGlyphMap(loglik16, loglik17,
                                      ([16,17], FadeOut)))
        
        grad0 = MathTex(
            r"\frac{\partial l}{\partial \hat{\beta}_j}=",
        )

        grad1 = MathTex(
            r"\frac{\partial l}{\partial \hat{\beta}_j}=",
            r"\sum_{i=1}^{n}"
        )

        grad2 = MathTex(
             r"\frac{\partial l}{\partial \hat{\beta}_j}=",
            r"\sum_{i=1}^{n}",
            r"y_i X_{ij}"
        )

        grad3 = MathTex(
             r"\frac{\partial l}{\partial \hat{\beta}_j}=",
            r"\sum_{i=1}^{n}",
            r"y_i X_{ij}",
            r"-"
        )

        grad4 = MathTex(
            r"\frac{\partial l}{\partial \hat{\beta}_j}=",
            r"\sum_{i=1}^{n}",
            r"y_i X_{ij}",
            r"-",
            r"\frac{1}{e^{\hat{z}_i}+1}",
        )

        grad5 = MathTex(
            r"\frac{\partial l}{\partial \hat{\beta}_j}=",
            r"\sum_{i=1}^{n}",
            r"y_i X_{ij}",
            r"-",
            r"\frac{1}{e^{\hat{z}_i}+1}",
            r"e^{\hat{z}_i}",
        )

        grad6 = MathTex(
            r"\frac{\partial l}{\partial \hat{\beta}_j}=",
            r"y_i X_{ij}",
            r"+",
            r"\frac{1}{e^{\hat{z}_i}+1}",
            r"e^{\hat{z}_i}",
            r"X_{ij}"
        )

        loglik17_broken = MathTex(r"l=",
                                  r"\sum_{i=1}^{n}",
                                  r"y_i\hat{z}_i",
                                  r"-",
                                  r"\ln(e^{\hat{z}_i}+1)",
                                  )

        grad0.next_to(loglik17, DOWN, aligned_edge=LEFT)
        for grad in grad1,grad2,grad3,grad4,grad5:
            grad.move_to(grad0, aligned_edge=LEFT)

        self.play(TransformMatchingTex(loglik17, loglik17_broken, run_time = 0.001))
        self.play(Write(grad0))

        self.play(ReplacementTransform(loglik17_broken[1].copy(), grad1[1]))
        self.play(TransformMatchingTex(grad0, grad1, run_time = 0.001))

        self.play(ReplacementTransform(loglik17_broken[2].copy(), grad2[2]))
        self.play(TransformMatchingTex(grad1, grad2, run_time = 0.001))

        self.play(ReplacementTransform(loglik17_broken[3].copy(), grad3[3]))
        self.play(TransformMatchingTex(grad2, grad3, run_time = 0.001))

        self.play(ReplacementTransform(loglik17_broken[4].copy(), grad4[4]))
        self.play(TransformMatchingTex(grad3, grad4, run_time = 0.001))

        loglik17_broken2 = MathTex(r"l=",
                                  r"\sum_{i=1}^{n}",
                                  r"y_i\hat{z}_i",
                                  r"-",
                                  r"\ln(",
                                  r"e^{\hat{z}_i}+1",
                                  r")",
                                  )
        self.play(TransformMatchingTex(loglik17_broken, loglik17_broken2, run_time = 0.001))
        self.play(ReplacementTransform(loglik17_broken2[5].copy(), grad5[5]))
        self.play(TransformMatchingTex(grad4, grad5, run_time = 0.001))
