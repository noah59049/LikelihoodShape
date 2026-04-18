from manim import *
from MF_Tools import *
from typing import Callable
from directional_derivative import latex_vector

def square_matrix_tex(n : int, 
                      generator: Callable[[int, int], str]):
    rows = []
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            entry = generator(i, j)
            row.append(entry)
        rows.append(" & ".join(row))
    
    matrix_body = " \\\\\n".join(rows)
    
    latex = (
        "\\begin{bmatrix}\n"
        f"{matrix_body}\n"
        "\\end{bmatrix}\n"
    )
    return latex

class LoglikSimplificationScene(Scene):
    def construct(self):
        # --- Part 1: The log likelihood ---

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
        
        # --- Part 2: The first derivative of the log likelihood ---

        grad_texes = [
            r"\frac{\partial l}{\partial \hat{\beta}_j}=",
            r"\sum_{i=1}^{n}",
            r"y_i X_{ij}",
            r"-",
            r"\frac{1}{e^{\hat{z}_i}+1}",
            r"e^{\hat{z}_i}",
            r"X_{ij}"
            ]

        grads = [MathTex(*grad_texes[0:i+1]) for i in range(len(grad_texes))]

        loglik17_broken = MathTex(r"l=",
                                  r"\sum_{i=1}^{n}",
                                  r"y_i\hat{z}_i",
                                  r"-",
                                  r"\ln(e^{\hat{z}_i}+1)",
                                  )
        self.play(TransformMatchingTex(loglik17, loglik17_broken, run_time = 0.001))

        grads[0].next_to(loglik17, DOWN, aligned_edge=LEFT)
        for grad in grads:
            grad.move_to(grads[0], aligned_edge=LEFT)

        
        self.play(Write(grads[0]))

        for i in range(1,5):
            self.play(ReplacementTransform(loglik17_broken[i].copy(), grads[i][i]))
            self.play(TransformMatchingTex(grads[i - 1], grads[i], run_time = 0.001))

        loglik17_broken2 = MathTex(r"l=",
                                  r"\sum_{i=1}^{n}",
                                  r"y_i\hat{z}_i",
                                  r"-",
                                  r"\ln(",
                                  r"e^{\hat{z}_i}",
                                  r"+1)",
                                  )
        self.play(TransformMatchingTex(loglik17_broken, loglik17_broken2, run_time = 0.001))
        self.play(ReplacementTransform(loglik17_broken2[5].copy(), grads[5][5]))
        self.play(TransformMatchingTex(grads[4], grads[5], run_time = 0.001))

        self.play(ReplacementTransform(loglik17_broken2[5][1:].copy(), grads[6][6]))
        self.play(TransformMatchingTex(grads[5], grads[6], run_time = 0.001))
        grad_together = MathTex("".join(grad_texes)).move_to(grads[0], aligned_edge=LEFT)
        self.play(TransformMatchingTex(grads[6], grad_together, run_time = 0.001))

        grad_together2 = MathTex(r"\frac{\partial l}{\partial \hat{\beta}_j}= \sum_{i=1}^{n} y_i X_{ij} - \frac{e^{\hat{z}_i}}{e^{\hat{z}_i}+1} X_{ij}").move_to(grads[0], aligned_edge=LEFT)
        self.play(TransformByGlyphMap(grad_together,grad_together2,
                                      ([27,28,29,30], [19,20,21,22]),
                                      ([19], FadeOut),
                                    ))
        grad_together3 = MathTex(r"\frac{\partial l}{\partial \hat{\beta}_j}= \sum_{i=1}^{n} y_i X_{ij} - \sigma(\hat{z}_i) X_{ij}").move_to(grads[0], aligned_edge=LEFT)
        self.play(TransformByGlyphMap(grad_together2,grad_together3,
                                      (range(19,30), range(19,25))
                                    ))
        
        # --- Part 3: The second derivative of the log likelihood ---
        self.play(LaggedStart(FadeOut(loglik17_broken2), grad_together3.animate.to_edge(UP), lag_ratio=0.5))
        hess_texes = [
            r"\frac{\partial^2 l}{\partial \hat{\beta}_j \partial \hat{\beta}_m}=",
            r"\sum_{i=1}^{n}",
            r".", # We will set this to 0 opacity
            r"- \sigma(\hat{z}_i)(1-\sigma(\hat{z}_i))",
            r"X_{im}",
            r"X_{ij}"
        ]
        hesses = [MathTex(*hess_texes[0:i+1]).next_to(grad_together3,DOWN,aligned_edge=LEFT) for i in range(len(hess_texes))]
        for hess in hesses[2:]:
            hess[2].set_opacity(0) # Jank solution but it works
        grad_parts = MathTex(r"\frac{\partial l}{\partial \hat{\beta}_j} = ",
                             r"\sum_{i=1}^{n}",
                             r"y_i X_{ij}",
                             r" - \sigma(\hat{z}_i)",
                             r" X_{ij}").move_to(grad_together3)
        self.play(TransformMatchingTex(grad_together3, grad_parts), run_time = 0.001)
        
        just_the_grad = grad_parts[0].copy()
        just_the_grad.generate_target()
        just_the_grad.target.next_to(grad_parts, DOWN, aligned_edge=LEFT)
        self.play(MoveToTarget(just_the_grad))
        just_the_grad2 = MathTex(r"\frac{\partial l}{\partial \hat{\beta}_j} = ")
        just_the_grad2.next_to(grad_parts, DOWN, aligned_edge = LEFT)
        self.play(TransformMatchingShapes(just_the_grad,just_the_grad2, run_time = 0.001))

        self.play(TransformByGlyphMap(just_the_grad2, hesses[0],
                                      (FadeIn, [1], {"delay":0.4, "run_time":0.7}),
                                      (FadeIn, [8,9,10,11])))
        for i in range(1,4):
            self.play(ReplacementTransform(grad_parts[i].copy(), hesses[i][i]))
            self.play(TransformMatchingTex(hesses[i - 1], hesses[i], run_time = 0.001))
        
        grad_parts2 = MathTex(r"\frac{\partial l}{\partial \hat{\beta}_j} = ",
                              r"\sum_{i=1}^{n}",
                              r"y_i X_{ij}",
                              r" - \sigma(",
                              r"\hat{z}_i",
                              r")",
                              r" X_{ij}").move_to(grad_together3)
        self.play(TransformMatchingTex(grad_parts, grad_parts2, run_time = 0.001))
        self.play(ReplacementTransform(grad_parts2[4].copy(), hesses[4][4]))
        self.play(TransformMatchingTex(hesses[3], hesses[4], run_time = 0.001))
        self.play(ReplacementTransform(grad_parts2[6].copy(), hesses[5][5]))
        self.play(TransformMatchingTex(hesses[4], hesses[5], run_time = 0.001))

        hess_joined = MathTex("".join(hess_texes)).next_to(grad_together3,DOWN,aligned_edge=LEFT)
        hess_joined[0][18].set_opacity(0) # That pesky dot again
        self.play(TransformMatchingTex(hesses[5], hess_joined, run_time = 0.55))
        hess_simplified = MathTex(r"\frac{\partial^2 l}{\partial \hat{\beta}_j \partial \hat{\beta}_m}=" +
            r"\sum_{i=1}^{n}" +
            r"- \hat{y}_i(1-\hat{y}_i)" +
            r"X_{im}" +
            r"X_{ij}").next_to(grad_together3,DOWN,aligned_edge=LEFT)
        self.play(TransformByGlyphMap(hess_joined, hess_simplified,
                                      ([18],FadeOut),
                                      (range(20,26), range(19,22)),
                                      (range(29,35), range(25,28)),
                                      ))
        
        hess_simplified2 = MathTex(r"\frac{\partial^2 l}{\partial \hat{\beta}_j \partial \hat{\beta}_m} = \sum_{i=1}^{n} - w_i X_{im} X_{ij}").next_to(grad_together3,DOWN,aligned_edge=LEFT)
        hess_simplified3 = MathTex(r"\frac{\partial^2 l}{\partial \hat{\beta}_j \partial \hat{\beta}_m} = - \sum_{i=1}^{n} X_{im} w_i X_{ij}").next_to(grad_together3,DOWN,aligned_edge=LEFT)
        self.play(TransformByGlyphMap(hess_simplified, hess_simplified2,
                                      (range(19,29),[19,20])))
        self.play(TransformByGlyphMap(hess_simplified2, hess_simplified3,
                                      ([18],[13], {"path_arc": -PI}),
                                      (range(13,18), range(14,19), {"path_arc": -PI}),
                                      ([19,20], [22,23], {"path_arc": -PI}),
                                      ([21,22,23], [19,20,21], {"path_arc": -PI}),
                                      show_indices=False))

        matrix_hess_tex = MathTex(square_matrix_tex(4, lambda m,j: r"-\sum_{i=1}^{n} X_{immm} w_i X_{ijjj}".replace("mmm",str(m-1)).replace("jjj",str(j-1)))
                                  ).scale(0.74).next_to(hess_simplified3,DOWN)
        self.play(Write(matrix_hess_tex))
        self.play(FadeOut(matrix_hess_tex))

        hess_simplified4 = MathTex(r"\frac{\partial^2 l}{\partial \hat{\beta}_j \partial \hat{\beta}_m} = -",
                                   r"\sum_{i=1}^{n} X_{im} w_i X_{ij}").next_to(grad_together3,DOWN,aligned_edge=LEFT)
        self.play(TransformMatchingTex(hess_simplified3, hess_simplified4, run_time = 0.001))

        self.play(LaggedStart(FadeOut(grad_parts2), 
                              hess_simplified4.animate.to_edge(UP), lag_ratio=0.5))

        # --- Part 4: Assembling the second order partials into the Hessian ---
        sum_with_w = hess_simplified4[1].copy()
        sum_with_w.generate_target()
        sum_with_w.target.next_to(hess_simplified4, DOWN)
        self.play(MoveToTarget(sum_with_w))
        sum_with_w2 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij}").next_to(hess_simplified4, DOWN)
        self.play(TransformMatchingShapes(sum_with_w,sum_with_w2, run_time = 0.001))

        sum_without_w = MathTex(r"\sum_{i=1}^{n} X_{im} X_{ij}").next_to(hess_simplified4, DOWN)
        self.play(TransformByGlyphMap(sum_with_w2,sum_without_w,
                                      ([8,9], FadeOut)))
        easy_dot1 = MathTex(r"\sum_{i=1}^{n} X_{im} X_{ij} = X_{\cdot m}\cdot X_{\cdot j}").next_to(hess_simplified4, DOWN)
        self.play(TransformByGlyphMap(sum_without_w, easy_dot1,
                                      (FadeIn, range(11,19))))
        easy_dot2 = MathTex(r"\sum_{i=1}^{n} X_{im} X_{ij} = X_{\cdot m}^T X_{\cdot j}").next_to(hess_simplified4, DOWN)
        self.play(TransformByGlyphMap(easy_dot1, easy_dot2,
                                      ([15],[13])))
        
        # --- Proving that that sum is a dot product with a diagonal matrix in between ---
        dot0 = hess_simplified4[1].copy()
        dot0.generate_target()
        dot0.target.next_to(easy_dot2, DOWN)
        self.play(MoveToTarget(dot0))
        dot1 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij}").next_to(easy_dot2, DOWN)
        self.play(TransformMatchingShapes(dot0,dot1, run_time = 0.001))
        
        dot2 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = X_{\cdot m}^T W X_{\cdot j}").next_to(easy_dot2, DOWN)
        self.play(TransformByGlyphMap(dot1, dot2,
                                      (FadeIn, range(13,22))))
        
        dot3 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = ",
        r"X_{\cdot m}^T",
        r"W",
        r"X_{\cdot j}").next_to(easy_dot2, DOWN)
        self.play(TransformMatchingTex(dot2, dot3, run_time = 0.001))
        W_generator = lambda i,j: f"w_{i}" if i == j else "0"
        W_tex = square_matrix_tex(4, W_generator)
        
        dot4 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = ",
        r"X_{\cdot m}^T",
        W_tex,
        r"X_{\cdot j}").next_to(easy_dot2, DOWN)
        self.play(*[ReplacementTransform(dot3[i], dot4[i]) for i in range(4)])
        
        dot5 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = ",
        latex_vector([f"X_{{{i}m}}" for i in range(1,5)], orientation = "row"),
        W_tex,
        latex_vector([f"X_{{{i}j}}" for i in range(1,5)], orientation = "column")
        ).next_to(easy_dot2, DOWN)
        dot5.scale(0.87)
        self.play(*[ReplacementTransform(dot4[i], dot5[i]) for i in range(4)])

        dot6 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = ",
        latex_vector([f"X_{{{i}m}}" for i in range(1,5)], orientation = "row"),
        W_tex+
        latex_vector([f"X_{{{i}j}}" for i in range(1,5)], orientation = "column")
        ).next_to(easy_dot2, DOWN)
        dot6.scale(0.87)
        self.play(TransformMatchingTex(dot5, dot6, run_time = 0.001))

        self.play(FadeOut(easy_dot2, hess_simplified4)) # We need the whole screen for this transformation
        dot7 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = ",
        latex_vector([f"X_{{{i}m}}" for i in range(1,5)], orientation = "row"),
        latex_vector([latex_vector([W_generator(i,j) for j in range(1,5)],"row") + 
                      latex_vector([f"X_{{{j}j}}" for j in range(1,5)], orientation = "column")
                        for i in range(1,5)])
        )
        dot7.scale(0.87)
        self.play(*[ReplacementTransform(dot6[i], dot7[i]) for i in range(2)],
                  TransformMatchingShapes(dot6[2], dot7[2]))
        

        