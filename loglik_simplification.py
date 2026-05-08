from manim import *
from MF_Tools import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
from N_Tools import latex_vector, square_matrix_tex, ReplacementTransformGroup

class LoglikSimplificationScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService("/Users/noah/Convex/LikelihoodShape/podcasts/loglik_simplification_podcast.mp3",
        cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
        min_silence_len=2000,
        keep_silence=(0,0)))
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

        with self.voiceover("So now we want to find the Hessian and directional second derivatives of our log likelihood. So let’s take a look at our log likelihood again. We are going to simplify it.") as tracker:
            self.play(Write(loglik4))

        with self.voiceover("We expand (1 - yi)") as tracker:
            self.play(TransformByGlyphMap(loglik4, loglik5,
                                        (range(21,30), range(15,24), {"path_arc":PI}),
                                        (range(21,30), range(27,36)),
                                        ([15,20], FadeOut, {"run_time":0.5}),
                                        ([16], FadeOut),
                                        ([17,18,19], [24,25,26])))
        
        with self.voiceover("Rearrange terms") as tracker:
            self.play(TransformByGlyphMap(loglik5, loglik6,
                                        (range(24,36), range(14,26), {"path_arc":PI}),
                                        (range(14,24), range(26,36), {"path_arc":PI})))
        
        with self.voiceover("Factor out the yi") as tracker:
            self.play(TransformByGlyphMap(loglik6, loglik7,
                                        ([15,16], FadeOut),
                                        (FadeIn, [9,25])))
        
        with self.voiceover("Simplify the difference of lns into the ln of a ratio") as tracker:
            self.play(TransformByGlyphMap(loglik7, loglik8,
                                        ([12,13,14], [12,13,14], {"path_arc": -PI/4}),
                                        (range(19,24), range(16,21), {"path_arc": -PI/4}),
                                        (FadeIn, [15]),
                                        ([15,16,17], FadeOut, {"run_time":0.5}),
                                        ([18,24], FadeOut, {"run_time":0.5})))
        
        with self.voiceover("If you remember the original definition we gave, this part becomes the linear combination of the predictors") as tracker:
            self.play(TransformByGlyphMap(loglik8, loglik9,
                                        (range(10,21),range(10,45))))
        
        with self.voiceover("We are going to call that zi to simplify things.") as tracker:
            self.play(TransformByGlyphMap(loglik9, loglik10,
                                        (range(9,46), [10,11])))
        
        with self.voiceover("And since it’s estimated we use z hat i instead") as tracker:
            self.play(TransformByGlyphMap(loglik10, loglik11,
                                        (FadeIn, [9])))
        
        with self.voiceover("So that yi hat just becomes sigmoid of zi hat") as tracker:
            self.play(TransformByGlyphMap(loglik11, loglik12,
                                        (range(18,21), range(18,24))))
        
        with self.voiceover("And we use the definition of sigmoid") as tracker:
            self.play(TransformByGlyphMap(loglik12, loglik13,
                                        ([18,19,23], FadeOut, {"run_time":0.5}),
                                        (FadeIn, [18,22,23,27,28], {"delay":0.25, "run_time":0.73}),
                                        ([20,21,22],[19,20,21]),
                                        ([20,21,22],[24,25,26])))
        
        with self.voiceover("Expand 1 so that we’re under a common denominator") as tracker:
            self.play(TransformByGlyphMap(loglik13,loglik14,
                                        ([16], range(16,29))))
        
        with self.voiceover("Combine both sides of the fraction") as tracker:
            self.play(TransformByGlyphMap(loglik14, loglik15,
                                        (range(16,22), range(16,22)),
                                        ([29],[22]),
                                        (range(30,34), range(23,27)),
                                        (range(23,29), range(28,34), {"path_arc":PI/2}),
                                        (range(35,41), range(28,34), {"path_arc":-PI/2}),
                                        ([22,34],[27])))
        
        with self.voiceover("Cancel out e^zi hat on top of the fraction") as tracker:
            self.play(TransformByGlyphMap(loglik15, loglik16,
                                        (range(16,21), []),
                                        (range(22,27), [])))
        
        with self.voiceover("And ln of 1 over something equals negative ln of that") as tracker:
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
        with self.voiceover("NOW we want to find the derivative of the likelihood with respect to beta hat j") as tracker:
            self.play(TransformMatchingTex(loglik17, loglik17_broken, run_time = 0.001))

            grads[0].next_to(loglik17, DOWN, aligned_edge=LEFT)
            for grad in grads:
                grad.move_to(grads[0], aligned_edge=LEFT)

            
            self.play(Write(grads[0]))

        for i in range(1,5):
            with self.voiceover([
            "",
            "It’s going to be a sum as above",
            "The yi zi hat turns into yi Xij [WHY WHY WHY]",
            "And then we subtract the derivative of the thing on the right, using the chain rule",
            "The ln becomes a reciprocal"
            ][i]) as tracker:
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
        
        with self.voiceover("The exponential plus 1 just becomes the exponential") as tracker:
            self.play(TransformMatchingTex(loglik17_broken, loglik17_broken2, run_time = 0.001))
            self.play(ReplacementTransform(loglik17_broken2[5].copy(), grads[5][5]))
            self.play(TransformMatchingTex(grads[4], grads[5], run_time = 0.001))

        with self.voiceover("And the zi becomes Xij") as tracker:
            self.play(ReplacementTransform(loglik17_broken2[5][1:].copy(), grads[6][6]))
            self.play(TransformMatchingTex(grads[5], grads[6], run_time = 0.001))
            grad_together = MathTex("".join(grad_texes)).move_to(grads[0], aligned_edge=LEFT)
            self.play(TransformMatchingTex(grads[6], grad_together, run_time = 0.001))

        grad_together2 = MathTex(r"\frac{\partial l}{\partial \hat{\beta}_j}= \sum_{i=1}^{n} y_i X_{ij} - \frac{e^{\hat{z}_i}}{e^{\hat{z}_i}+1} X_{ij}").move_to(grads[0], aligned_edge=LEFT)
        with self.voiceover("Now if we just put this in one fraction") as tracker:
            self.play(TransformByGlyphMap(grad_together,grad_together2,
                                        ([27,28,29,30], [19,20,21,22]),
                                        ([19], FadeOut),
                                        ))
        
        grad_together3 = MathTex(r"\frac{\partial l}{\partial \hat{\beta}_j}= \sum_{i=1}^{n} y_i X_{ij} - \sigma(\hat{z}_i) X_{ij}").move_to(grads[0], aligned_edge=LEFT)
        with self.voiceover("That fraction becomes sigmoid of zi") as tracker:
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
        
        with self.voiceover("Now we want the second order partial with respect to beta hat j and beta hat m [I wanted to use k but we’re already using it]") as tracker:
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
            with self.voiceover([
            "Again it's a sum",
            "This yi Xij is a constant, and on the right side we use a chain rule",
            "The derivative of the sigmoid is equal to sigmoid times 1 minus sigmoid, and I’ll leave up on screen the derivation of that, though I won’t go into it.",
            ][i-1]) as tracker:
                self.play(ReplacementTransform(grad_parts[i].copy(), hesses[i][i]))
                self.play(TransformMatchingTex(hesses[i - 1], hesses[i], run_time = 0.001))

        grad_parts2 = MathTex(r"\frac{\partial l}{\partial \hat{\beta}_j} = ",
                              r"\sum_{i=1}^{n}",
                              r"y_i X_{ij}",
                              r" - \sigma(",
                              r"\hat{z}_i",
                              r")",
                              r" X_{ij}").move_to(grad_together3)
        with self.voiceover("The derivative of zi hat is Xim") as tracker:
            self.play(TransformMatchingTex(grad_parts, grad_parts2, run_time = 0.001))
            self.play(ReplacementTransform(grad_parts2[4].copy(), hesses[4][4]))
        
        with self.voiceover("And then the Xij is just a constant, so we multiply by it") as tracker:
            self.play(TransformMatchingTex(hesses[3], hesses[4], run_time = 0.001))
            self.play(ReplacementTransform(grad_parts2[6].copy(), hesses[5][5]))
            self.play(TransformMatchingTex(hesses[4], hesses[5], run_time = 0.001))
    
        hess_joined = MathTex("".join(hess_texes)).next_to(grad_together3,DOWN,aligned_edge=LEFT)
        hess_joined[0][18].set_opacity(0) # That pesky dot again
        with self.voiceover("Now let’s turn those sigmoids of zi hat into yi hat") as tracker:
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
        with self.voiceover("And let’s define wi as yi hat times 1 minus yi hat") as tracker:
            self.play(TransformByGlyphMap(hess_simplified, hess_simplified2,
                                        (range(19,29),[19,20])))
        with self.voiceover("And rearrange the sum a little bit, which will be useful later.") as tracker:
            self.play(TransformByGlyphMap(hess_simplified2, hess_simplified3,
                                        ([18],[13], {"path_arc": -PI}),
                                        (range(13,18), range(14,19), {"path_arc": -PI}),
                                        ([19,20], [22,23], {"path_arc": -PI}),
                                        ([21,22,23], [19,20,21], {"path_arc": -PI}),
                                        show_indices=False))

        matrix_hess_tex = MathTex(square_matrix_tex(4, lambda m,j: r"-\sum_{i=1}^{n} X_{immm} w_i X_{ijjj}".replace("mmm",str(m)).replace("jjj",str(j)), start_ij=0)
                                  ).scale(0.74).next_to(hess_simplified3,DOWN)
        with self.voiceover("So now if we try to construct the entire Hessian matrix from these second order partials, we get this, and it’s not clear how that’s helpful to us.") as tracker:
            self.play(Write(matrix_hess_tex))
        with self.voiceover("So let’s try a different approach.") as tracker:
            self.play(FadeOut(matrix_hess_tex))

        hess_simplified4 = MathTex(r"\frac{\partial^2 l}{\partial \hat{\beta}_j \partial \hat{\beta}_m} = -",
                                   r"\sum_{i=1}^{n} X_{im} w_i X_{ij}").next_to(grad_together3,DOWN,aligned_edge=LEFT)
        with self.voiceover("Let’s look at this sum") as tracker:
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
        with self.voiceover("I notice that if the wi were not there,") as tracker:
            self.play(TransformByGlyphMap(sum_with_w2,sum_without_w,
                                        ([8,9], FadeOut)))
        easy_dot1 = MathTex(r"\sum_{i=1}^{n} X_{im} X_{ij} = X_{\cdot m}\cdot X_{\cdot j}").next_to(hess_simplified4, DOWN)
        with self.voiceover("It would be the dot product of the mth and jth columns of X.") as tracker:
            self.play(TransformByGlyphMap(sum_without_w, easy_dot1,
                                        (FadeIn, range(11,19))))
        easy_dot2 = MathTex(r"\sum_{i=1}^{n} X_{im} X_{ij} = X_{\cdot m}^T X_{\cdot j}").next_to(hess_simplified4, DOWN)
        with self.voiceover("Or the mth column transposed times the jth column.") as tracker:
            self.play(TransformByGlyphMap(easy_dot1, easy_dot2,
                                        ([15],[13])))
        
        # --- Proving that that sum is a dot product with a diagonal matrix in between ---
        with self.voiceover("But we do have the wi in there.") as tracker:
            dot0 = hess_simplified4[1].copy()
            dot0.generate_target()
            dot0.target.next_to(easy_dot2, DOWN)
            self.play(MoveToTarget(dot0))
            dot1 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij}").next_to(easy_dot2, DOWN)
            self.play(TransformMatchingShapes(dot0,dot1, run_time = 0.001))
        
        with self.voiceover("I claim that this sum, with the wi, is equal to the mth column transposed times the matrix W, times the jth column.") as tracker:
            dot2 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = X_{\cdot m}^T W X_{\cdot j}").next_to(easy_dot2, DOWN)
            self.play(TransformByGlyphMap(dot1, dot2,
                                        (FadeIn, range(13,22))))
        
        with self.voiceover("Where W is just a nxn diagonal matrix with the elements of wi on the diagonal.") as tracker:
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
            self.play(ReplacementTransformGroup(dot3, dot4))
        
        with self.voiceover("So let’s explicitly write out the vectors.") as tracker:
            dot5 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = ",
            latex_vector([f"X_{{{i}m}}" for i in range(1,5)], orientation = "row"),
            W_tex,
            latex_vector([f"X_{{{i}j}}" for i in range(1,5)], orientation = "column")
            ).next_to(easy_dot2, DOWN)
            dot5.scale(0.87)
            self.play(ReplacementTransformGroup(dot4, dot5))

        with self.voiceover("The product of the matrix and the jth column is just the product of each row with that column vector.") as tracker:
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
        
        with self.voiceover("And everything is multiplied with 0 except wi times Xij.") as tracker:
            dot8 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = ",
            latex_vector([f"X_{{{i}m}}" for i in range(1,5)], orientation = "row"),
            latex_vector([f"w_{j} X_{{{j}j}}" for j in range(1,5)], orientation = "column")
            )
            dot8.scale(0.87)
            self.play(*[ReplacementTransform(dot7[i], dot8[i]) for i in range(2)],
                    TransformMatchingShapes(dot7[2], dot8[2]))
        
        with self.voiceover("And now you expand out the matrix vector product, and you see that my claim was correct. The sum is equal to the mth column transposed times the matrix W, times the jth column.") as tracker:
            dot9 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = ",
            latex_vector([f"X_{{{i}m}}" for i in range(1,5)], orientation = "row") +
            latex_vector([f"w_{j} X_{{{j}j}}" for j in range(1,5)], orientation = "column")
            )
            dot9.scale(0.87)
            self.play(TransformMatchingTex(dot8, dot9, run_time = 0.001))

            dot10 = MathTex(r"\sum_{i=1}^{n} X_{im} w_i X_{ij} = ",
            r"X_{1m}w_1X_{1j}+X_{2m}w_2X_{2j}+X_{3m}w_3X_{3j}+X_{4m}w_4X_{4j}"
            )
            dot10.scale(0.87)
            self.play(ReplacementTransform(dot9[0], dot10[0]), TransformMatchingShapes(dot9[1], dot10[1]))
        
        with self.voiceover("So we return to the formula and plug that in. And now we want to find the full Hessian.") as tracker:
            self.play(FadeIn(hess_simplified4), FadeOut(dot10))
            hess_simplified5 = MathTex(r"\frac{\partial^2 l}{\partial \hat{\beta}_j \partial \hat{\beta}_m} = -",
                                    r"X_{\cdot m}^T W X_{\cdot j}").move_to(hess_simplified4, aligned_edge=LEFT)
            self.play(ReplacementTransformGroup(hess_simplified4, hess_simplified5))

            hess_simplified6 = MathTex(r"\frac{\partial^2 l}{\partial \hat{\beta}_j \partial \hat{\beta}_m} = -"+
                                    r"X_{\cdot m}^T W X_{\cdot j}").move_to(hess_simplified4, aligned_edge=LEFT)
            self.play(TransformMatchingTex(hess_simplified5, hess_simplified6, run_time = 0.001))
        
        # --- Gluing the partials together into the Hessian
        with self.voiceover("I claim that it is equal to -X transpose times W times X.") as tracker:
            big_claim = MathTex("H=-X^T W X")
            self.play(Write(big_claim))
            self.wait(tracker.duration - 2.1)
            self.play(FadeOut(big_claim))

        with self.voiceover("To see that, let’s just look at the mth row of the Hessian, which is just caused by gluing all the columns of X together at the right.") as tracker:
            hess_row_tex = latex_vector([r"\frac{\partial^2 l}{\partial \hat{\beta}_j \partial \hat{\beta}_m}".replace("j",str(j)) for j in range(4)], "row")
            glued_row = MathTex(hess_row_tex + r"= -X_{\cdot m}^T W " + latex_vector([r"X_{\cdot j}".replace("j",str(j)) for j in range(4)], "row")).scale(0.9)
            self.play(TransformByGlyphMap(hess_simplified6.copy(), glued_row,
                                        (range(12), range(1 ,13)),
                                        (range(12), range(13,25)),
                                        (range(12), range(25,37)),
                                        (range(12), range(37,49)),
                                        (FadeIn, [0,49]), # Brackets on the left
                                        (range(12,19), range(50,57)), # Middle stuff with W
                                        (FadeIn, [57,70]), # Brackets on the right
                                        (range(19,22), range(58,61)),
                                        (range(19,22), range(61,64)),
                                        (range(19,22), range(64,67)),
                                        (range(19,22), range(67,70)),
                                        ))
        
        with self.voiceover("And the entire Hessian is just gluing the rows together at the beginning.") as tracker:
            entire_hess_tex = square_matrix_tex(4, 
                                                lambda m, j: r"\frac{\partial^2 l}{\partial \hat{\beta}_j \partial \hat{\beta}_m}".replace("j",str(j)).replace("m", str(m)), start_ij = 0)
            glued_hess = MathTex(entire_hess_tex + 
                                "=-" +
                                latex_vector([r"X_{\cdot m}^T".replace("m",str(m)) for m in range(4)], "col") + 
                                " W " + 
                                latex_vector([r"X_{\cdot j}".replace("j",str(j)) for j in range(4)], "row")
                                ).scale(0.89).next_to(glued_row, DOWN)
            self.play(TransformByGlyphMap(glued_row.copy(),glued_hess,
                                        ([0], range(7)), # Left bracket of hess
                                        (range(1,49), range(7,55)),
                                        (range(1,49), range(55,103)),
                                        (range(1,49), range(103,151)),
                                        (range(1,49), range(151,199)),
                                        ([49], range(199,206)), # Right bracket of hess
                                        ([50,51], [206,207]), # Equals sign and minus sign
                                        (FadeIn, range(208,212)), # Left bracket of XT
                                        (range(52,56), range(212,216)),
                                        (range(52,56), range(216,220)),
                                        (range(52,56), range(220,224)),
                                        (range(52,56), range(224,228)),
                                        (FadeIn, range(228, 232)) # Right bracket of XT
                                        ))
        
        with self.voiceover("So now if you use the definitions for Hessian and X, you’ll see that my claim was correct, the Hessian is -X transpose W X") as tracker:
            quadratic0 = MathTex("H=-X^T W X").move_to(glued_hess)
            self.play(TransformByGlyphMap(glued_hess, quadratic0,
                                        (range(206), [0]),
                                        (range(208,232), [3,4]),
                                        (range(233, 247), [6])))
            self.play(LaggedStart(FadeOut(glued_row, hess_simplified6), quadratic0.animate.move_to(ORIGIN), lag_ratio=0.3))
        
        with self.voiceover("So now we want to find the directional second derivative in the direction of column vector v.") as tracker:
            quadratic1 = MathTex(r"\vec{v}^T H \vec{v} = -\vec{v}^TX^T W X \vec{v}")
            self.play(TransformByGlyphMap(quadratic0,quadratic1,
                                        (FadeIn, [0,1,2]),
                                        (FadeIn, [4,5]),
                                        (FadeIn, [8,9,10]),
                                        (FadeIn, [15,16]),
                                        ))
        
        with self.voiceover("It’s v transpose H v, which if we plug the definition of the Hessian in,") as tracker:
            quadratic2 = MathTex(r"D_{\vec{v}}^2(l) = -\vec{v}^TX^T W X \vec{v}")
            self.play(TransformByGlyphMap(quadratic1, quadratic2,
                                        (range(6), range(7))))
        
        with self.voiceover("Use the formula for the transpose of a product.") as tracker:
            quadratic3 = MathTex(r"D_{\vec{v}}^2(l) = -(X\vec{v})^T W X \vec{v}")
            self.play(TransformByGlyphMap(quadratic2, quadratic3,
                                        ([12],[10]),
                                        ([9,10],[11,12]),
                                        (FadeIn, [9,13]),
                                        ([11],[14]),
                                        ([13],[14]),
                                        ))
        
        with self.voiceover("And then let’s define Xv as u. It doesn’t really matter what u is.") as tracker:
            quadratic4 = MathTex(r"D_{\vec{v}}^2(l) = -\vec{u}^T W \vec{u}")
            self.play(TransformByGlyphMap(quadratic3,quadratic4,
                                        (range(9,14), [9,10]),
                                        (range(16,19), [13,14]),
                                        ))
        
        with self.voiceover("Now let’s use a result we got from earlier. This product is the sum of ui times wi times ui. Now we don’t really care what this is, we just care that it’s negative") as tracker:
            quadratic5 = MathTex(r"D_{\vec{v}}^2(l) = -\sum_{i=1}^{n} u_i w_i u_i")
            self.play(TransformByGlyphMap(quadratic4, quadratic5,
                                        (FadeIn, range(9,14)),
                                        ([9,11], [15]),
                                        (FadeIn, [17]),
                                        show_indices=False))
        

        with self.voiceover("It’s equal to wi times ui squared") as tracker:
            quadratic6 = MathTex(r"D_{\vec{v}}^2(l) = -\sum_{i=1}^{n} w_i u_i^2")
            self.play(TransformByGlyphMap(quadratic5, quadratic6,
                                        ([14,15],[17], {"path_arc": -PI/3})))
            
        with self.voiceover("This sum will always be positive. Because all the elements of wi are positive, and ui squared is always positive or 0.") as tracker:
            quadratic7 = MathTex(r"D_{\vec{v}}^2(l) =",
                                             r"-",
                                             r"\sum_{i=1}^{n}", 
                                             r"w_i",
                                             r"u_i^2")
            self.play(TransformMatchingTex(quadratic6,quadratic7, run_time = 0.001))

            # Boxes
            w_box = SurroundingRectangle(quadratic7[3], buff=0.08, color = RED)
            u_box = SurroundingRectangle(quadratic7[4], buff=0.08, color = RED)

            # Labels + arrows
            w_text = Tex("Always positive").scale(0.6)
            w_text.next_to(quadratic7, UP + RIGHT, buff=0.6)

            w_arrow = Arrow(
                w_text.get_bottom(),
                w_box.get_top(),
                buff=0.1,
                stroke_width=4,
            )

            u_text = Tex("Always nonnegative").scale(0.6)
            u_text.next_to(quadratic7, DOWN + RIGHT, buff=0.6)

            u_arrow = Arrow(
                u_text.get_top(),
                u_box.get_bottom(),
                buff=0.1,
                stroke_width=4,
            )

            self.play(
                Create(w_box),
                Write(w_text),
                GrowArrow(w_arrow),

                Create(u_box),
                Write(u_text),
                GrowArrow(u_arrow),
            )

        with self.voiceover("Because this sum is positive, the directional second derivative must be negative.") as tracker:
            # Highlight the whole sum term
            sum_box = SurroundingRectangle(quadratic7[2:], buff=0.12)

            positive_text = Tex("Positive").scale(0.7)
            positive_text.next_to(sum_box, UP, buff=0.35)

            positive_arrow = Arrow(
                positive_text.get_bottom(),
                sum_box.get_top(),
                buff=0.08,
                stroke_width=4,
            )

            # Highlight the negative sign
            minus_box = SurroundingRectangle(quadratic7[1:], buff=0.08)

            negative_text = Tex("Therefore negative").scale(0.7)
            negative_text.next_to(minus_box, DOWN, buff=0.35)

            negative_arrow = Arrow(
                negative_text.get_top(),
                minus_box.get_bottom(),
                buff=0.08,
                stroke_width=4,
            )

            self.play(
                FadeOut(w_box, w_text, w_arrow, u_box, u_text, u_arrow),
                Create(sum_box),
                Write(positive_text),
                GrowArrow(positive_arrow),
            )

            self.play(
                Create(minus_box),
                Write(negative_text),
                GrowArrow(negative_arrow),
            )