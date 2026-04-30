import numpy as np
import pandas as pd
from manim import *
from MF_Tools import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
from N_Tools import as_row, as_col, numpy_to_latex, sigmoid, logistic_regression, round_sig, get_matching_cell_map, TransformMatchingCells, latex_table_to_array, highlight_row, extract_table_grid, log_likelihood, FadeInRHS, FlashAround, latex_vector
from intro_with_tables import yX_tex_numbered # TODO: Maybe move this to a data file
from data import COLS_TO_KEEP, X, y, yX # type: ignore

yXyhat_tex = yX_tex_numbered.replace(r"\\", r"& \\").replace(r"c | }", r"c | c | }").replace("X4\n &", r"X4 & $\hat{y}$")
array_from_latex = latex_table_to_array(yX_tex_numbered)
array_from_latex = array_from_latex[1:] # The first row is the title row with just nans
y_latex = array_from_latex[:,0].reshape(-1)

TableTransform = TransformMatchingCells # TransformMatchingCells for production, FadeTransform for fast rendering

class MLEScene(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.set_speech_service(StitcherService(r"/Users/noah/Convex/LikelihoodShape/podcasts/mle_explorer_podcast14.mp3",
                cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
                min_silence_len=2000,
                keep_silence=(0,0)))
        yX_table = Tex(yX_tex_numbered).scale(0.66).to_corner(UL)
        formula = MathTex(r"p=\sigma(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})").to_edge(DOWN)
        with self.voiceover("If our assumptions are correct, these betas are unknown facts about the population our data is drawn from. So we need to estimate them, but how? The answer is") as tracker:
            self.play(Write(formula))
            mle_words = Text("Maximum Likelihood Estimation")
            tex1 = MathTex(r"L(\hat{\beta})")
            tex2 = MathTex(r"L(\hat{\beta})=P(Y|\hat{\beta})")
            mle_words.next_to(tex1, UP)

        with self.voiceover("maximum likelihood estimation. If we have an estimate of our betas, the") as tracker:
            self.play(FadeIn(mle_words), FlashAround(mle_words))
        with self.voiceover("likelihood, indicated L, of that estimate is the") as tracker:
            self.play(FadeIn(tex1))
        with self.voiceover("probability that it would produce the observed values of Y.") as tracker:
            self.play(FadeInRHS(tex1, tex2))
            self.wait(max(0, tracker.duration - 1.7))
            self.play(FadeOut(mle_words, tex2, run_time = 0.6))

        with self.voiceover("In order to indicate that they're estimated, we put a hat over the betas, and we use y hat to mean our estimate of p. In general a hat over something means an estimate from data.") as tracker:
            formula2 = MathTex(r"\hat{y}=\sigma(\hat{\beta_0}+\hat{\beta_1} X_{1}+\hat{\beta_2} X_{2}+\ldots+\hat{\beta}_{k-1} X_{k-1})").to_edge(DOWN)
            self.play(TransformByGlyphMap(formula, formula2,
                                        (FadeIn, [1]),
                                        (FadeIn, [5]),
                                        (FadeIn, [9]),
                                        (FadeIn, [15]),
                                        (FadeIn, [25]),
                                        ))

        with self.voiceover("Let's take a look at our data table") as tracker:
            self.play(FadeIn(yX_table))

        with self.voiceover("In this case we have 4 predictors. So let’s show that in our formula.") as tracker:
            formula3_tex = r"\hat{y}=\sigma(\hat{\beta_0}+" + "+".join(r"\hat{\beta_j} X_{j}".replace("j",str(j)) for j in range(1, 1 + COLS_TO_KEEP)) + ")"
            formula3 = MathTex(formula3_tex).to_edge(DOWN)
            self.play(TransformMatchingShapes(formula2, formula3))

        result = logistic_regression(X, y, add_intercept=True, return_stats=True)
        bhat_mle, cov, se = result
        rng = np.random.default_rng(seed = 186)
        
        all_bhats = []
        all_bhat_texes = []
        all_likelihood_strs = []
        all_likelihood_texes = []

        def arbitrarily_choose_bhat():
            bhat = bhat_mle + cov @ rng.normal(loc=0.0, scale=1.0, size=len(bhat_mle))
            bhat = round_sig(bhat, 4)
            return bhat

        # This loop happens for every estimate of the betas
        for m in range(3):
            # --- Choose beta hats for our example that are normally distributed with mean at the MLE and covariance equal to the covariance matrix of the model
            bhat = arbitrarily_choose_bhat()
            all_bhats.append(bhat.copy())

            # --- Add the beta hats to the corner ---
            with self.voiceover("Let’s look at a mostly arbitrarily chosen estimate of the betas.") as tracker:
                bhats_tex = VGroup(*[MathTex(r"\hat{\beta}_" + str(i) + f"={e}") for i,e in enumerate(bhat)]).set_color(BLUE).arrange(DOWN).to_corner(UR)
                all_bhat_texes.append(bhats_tex.copy().arrange(DOWN, aligned_edge = LEFT))
                self.play(FadeIn(bhats_tex))

                formula4_parts = [r"\hat{y}=\sigma(",r"\hat{\beta_0}"]
                for j in range(1, 1 + COLS_TO_KEEP):
                    formula4_parts.append("+")
                    formula4_parts.append(rf"\hat{{\beta_{j}}}")
                    formula4_parts.append(rf"X_{{{j}}}")
                formula4_parts.append(")")
                formula4 = MathTex(*formula4_parts).to_edge(DOWN)
                def formula4_beta_index(j):
                    if j == 0: return 1
                    else: return 3 * j
                def formula4_x_index(j):
                    return 1 + 3 * j

                # --- Substitute in the beta hats ---
                substituted_formula_parts = formula4_parts.copy()
                for j in range(COLS_TO_KEEP + 1):
                    idx = formula4_beta_index(j)
                    if j == 0 or bhat[j] >= 0:
                        substituted_formula_parts[idx] = f"{bhat[j]}"
                    else: # For negative beta hats, we change the sign to a minus
                        substituted_formula_parts[idx] = f"{-bhat[j]}"
                        substituted_formula_parts[idx - 1] = "-"
                substituted_formula = MathTex(*substituted_formula_parts).to_edge(DOWN)
                for j in range(COLS_TO_KEEP + 1):
                    substituted_formula[formula4_beta_index(j)].set_color(BLUE)

                if m == 0:
                    self.play(TransformMatchingTex(formula3, formula4, run_time = 0.001))
                    self.play(*[formula4[formula4_beta_index(j)].animate.set_color(BLUE) for j in range(COLS_TO_KEEP + 1)])
                    self.play(*[ReplacementTransform(formula4[i], substituted_formula[i])
                                for i in range(len(formula4_parts))])
                else:
                    self.play(FadeIn(substituted_formula))

            with self.voiceover("For each individual, we get an estimate of the probability of y being 1, which we call y hat.") as tracker:
                yXyhat_table = Tex(yXyhat_tex).scale(0.66).to_corner(UL)
                self.play(FadeIn(yXyhat_table, run_time = min(1, tracker.duration)))
                self.remove(yX_table)

            # --- add the y hats into the table one by one ---
            old_table_tex = yXyhat_tex
            old_table = yXyhat_table
            substituted_formula_old = substituted_formula
            substituted_formula_parts2 = substituted_formula_parts.copy()
            # This loop happens for every row
            with self.voiceover("In the first row, y hat is 0.9051. In the second row, y hat is 0.0001702, and so on.") as tracker:
                for i in range(array_from_latex.shape[0]):
                    # --- Determine the run times of transforms
                    if m == 0:
                        if i == 0:
                            rect_time = 2 # Determined from the audio
                            table_time = 3.2 # Determined from the audio
                            bundled = False
                        elif i == 1:
                            rect_time = 2 # Determined from the audio
                            table_time = 2.5 # Determined from the audio
                            bundled = False
                        else:
                            run_time = 0.8
                            bundled = True
                    else:
                        run_time = tracker.duration / array_from_latex.shape[0]
                        bundled = True


                    # --- Move the highlight rect down ---
                    highlight_rect_transforms = [FadeOut(highlight_rect)] if i > 0 else []
                    highlight_rect = highlight_row(yX_table, row_idx = i + 1)
                    highlight_rect_transforms.append(FadeIn(highlight_rect))

                    # --- Substitute stuff into the formula ---
                    row_np = array_from_latex[i, 1:]

                    for j, Xij in enumerate(row_np.reshape(-1)):
                        substituted_formula_parts2[formula4_x_index(j + 1)] = r"(\ldots)" if np.isnan(Xij) else f"({Xij})"
                    substituted_formula_new = MathTex(*substituted_formula_parts2).scale(0.83).to_edge(DOWN)
                    for j in range(COLS_TO_KEEP + 1):
                        substituted_formula_new[formula4_beta_index(j)].set_color(BLUE)
                        if j != 0: 
                            substituted_formula_new[formula4_x_index(j)].set_color(RED)
                    substituted_formula_transforms = [
                        ReplacementTransform(substituted_formula_old[i], 
                                            substituted_formula_new[i])
                            for i in range(len(substituted_formula_parts2))]
                    

                    # --- Add y hat ---
                    zi = np.sum(bhat * np.hstack([np.array([1.0]), row_np]))
                    yhat_i = sigmoid(zi)
                    new_table_tex = old_table_tex
                    new_table_tex = new_table_tex.replace(r"& \\", r"& \vdots \\" if np.isnan(yhat_i) else f"& {yhat_i:.4g} \\\\", count = 1)
                    new_table = Tex(new_table_tex).scale(0.66).to_corner(UL)
                    
                    # --- Play the animations ---
                    if bundled:
                        if run_time > 1:
                            self.play(*(highlight_rect_transforms + substituted_formula_transforms), TableTransform(old_table, new_table), run_time = 1)
                            self.wait(run_time - 1)
                        else:
                            self.play(*(highlight_rect_transforms + substituted_formula_transforms), TableTransform(old_table, new_table), run_time = run_time)
                    else:
                        if rect_time > 1:
                            self.play(*(highlight_rect_transforms + substituted_formula_transforms), run_time = 1)
                            self.wait(rect_time - 1)
                        else:
                            self.play(*(highlight_rect_transforms + substituted_formula_transforms), run_time = rect_time)
                        if table_time > 1:
                            self.play(TableTransform(old_table, new_table), run_time = 1)
                            self.wait(table_time - 1)
                        else:
                            self.play(TableTransform(old_table, new_table), run_time = table_time)

                    # --- Get ready for the next iteration of the loop ---
                    substituted_formula_old = substituted_formula_new
                    old_table_tex = new_table_tex
                    old_table = new_table

            # --- Add in the partial likelihoods ---
            with self.voiceover("Now we want to consider the probabilities the model assigned to the actual outcome.") as tracker:
                partial_likelihoods_tex_old = old_table_tex.replace(r"\\", r"& \\").replace(r"c | }", r"c | c | }").replace("& \\\\\n", "& $L_i$ \\\\\n", count = 1)
                print(partial_likelihoods_tex_old)
                partial_likelihoods_table_old = Tex(partial_likelihoods_tex_old).scale(0.66).to_corner(UL)
                self.play(FadeOut(highlight_rect), FadeIn(partial_likelihoods_table_old), run_time = min(1, tracker.duration))
                self.remove(new_table)
                partial_likelihoods = []
            with self.voiceover("So in the first row, y is 1, the predicted probability of y being 1 is y hat ,which is 0.9051. In the second row, y is 0, and the predicted probability of y being 0 is 1 - y hat, which is 0.9998. So now we continue that process for all of the rows. And then to get the overall likelihood,") as tracker:
                total_transforms = array_from_latex.shape[0] + np.sum(y_latex == 0)
                # This loop happens for every row
                for i in range(array_from_latex.shape[0]):
                    # --- Determine the run time
                    if m == 0:
                        if i == 0:
                            run_time = 10 # Determined from the audio
                            squish_time = None # We shouldn't need to use this
                        elif i == 1:
                            run_time = 8 # Determined from the audio
                            squish_time = 4 # Determined from the audio
                        else:
                            run_time = squish_time = 0.8
                    else:
                        run_time = squish_time = tracker.duration / total_transforms

                    row_np = array_from_latex[i, 1:]
                    zi = np.sum(bhat * np.hstack([np.array([1.0]), row_np]))
                    yhat_i = sigmoid(zi)
                    yi = y_latex[i]
                    if np.isnan(yhat_i):
                        Li_str1 = r"\vdots"
                    elif yi == 0:
                        Li_str1 = f"1-{yhat_i:.4g}"
                    else:
                        Li_str1 = f"{yhat_i:.4g}" 
                    Li = yhat_i ** yi * (1 - yhat_i) ** (1 - yi)
                    Li_str2 = r"\vdots" if np.isnan(Li) else f"{Li:.4g}"
                    partial_likelihoods.append(Li_str2)

                    partial_likelihoods_tex_new = partial_likelihoods_tex_old.replace(r"& \\", f"& {Li_str1} \\\\", count = 1)
                    partial_likelihoods_table_new = Tex(partial_likelihoods_tex_new).scale(0.66).to_corner(UL)
                    cell_map = get_matching_cell_map(partial_likelihoods_table_old, partial_likelihoods_table_new)
                    yhati_glyphs = extract_table_grid(partial_likelihoods_table_old)[(i + 1, COLS_TO_KEEP + 1)]
                    Li_glyphs    = extract_table_grid(partial_likelihoods_table_new)[(i + 1, COLS_TO_KEEP + 2)]
                    for start, end in cell_map.copy():
                        if end == Li_glyphs:
                            cell_map.remove((start, end))
                    if yi == 1 or np.isnan(Li):
                        cell_map.append((yhati_glyphs, Li_glyphs, {"path_arc": -PI / 5}))
                    else:
                        cell_map.append((yhati_glyphs, Li_glyphs[2:], {"path_arc": -PI / 5}))
                        cell_map.append(([], Li_glyphs[0:2], {"delay":0.35, "run_time": 0.6}))
                    if run_time > 1:
                        self.play(TransformByGlyphMap(partial_likelihoods_table_old, partial_likelihoods_table_new, *cell_map), run_time = 1)
                        self.wait(run_time - 1)
                    else:
                        self.play(TransformByGlyphMap(partial_likelihoods_table_old, partial_likelihoods_table_new, *cell_map), run_time = run_time)
                    if Li_str1 != Li_str2:
                        partial_likelihoods_tex_new = partial_likelihoods_tex_old.replace(r"& \\", f"& {Li_str2} \\\\", count = 1)
                        partial_likelihoods_table_new_simplified = Tex(partial_likelihoods_tex_new).scale(0.66).to_corner(UL)
                        if squish_time > 1:
                            self.play(TableTransform(partial_likelihoods_table_new, partial_likelihoods_table_new_simplified), run_time = 1)
                            self.wait(squish_time - 1)
                        else:
                            self.play(TableTransform(partial_likelihoods_table_new, partial_likelihoods_table_new_simplified), run_time = squish_time)
                        partial_likelihoods_table_old = partial_likelihoods_table_new_simplified
                    else:
                        partial_likelihoods_table_old = partial_likelihoods_table_new
                    partial_likelihoods_tex_old = partial_likelihoods_tex_new

            # --- Show the product of the partial likelihoods
            likelihood_together_tex = "L = " + "*".join(partial_likelihoods).replace(r"\vdots", r"\ldots")
            likelihood_together = MathTex(likelihood_together_tex).scale_to_fit_width(config.frame_width).next_to(substituted_formula_new, UP)

            # Transform the matching numbers
            table_grid = extract_table_grid(partial_likelihoods_table_old)
            glyph_map = [(FadeIn, [0,1])] # We start with fading in the "L="
            col_idx = COLS_TO_KEEP + 2
            eq_idx = 2
            used_table_glyphs = []
            for row_idx in range(array_from_latex.shape[0]):
                if row_idx != 0:
                    glyph_map.append((FadeIn, [eq_idx])) # The "*"
                    eq_idx += 1
                table_glyphs = table_grid[(row_idx + 1, col_idx)]
                eq_glyphs = range(eq_idx, eq_idx + len(table_glyphs))
                glyph_map.append((table_glyphs, eq_glyphs))
                used_table_glyphs += table_glyphs
                eq_idx += len(table_glyphs)

            # Fade out the entire table that's not involved
            unused_table_glyphs = [i for i in range(len(partial_likelihoods_table_old[0])) if i not in used_table_glyphs]
            glyph_map.append((unused_table_glyphs, FadeOut))
            
            print(f"{glyph_map=}")
            print(f"{len(likelihood_together[0])=}")

            # Play the transform yeet
            with self.voiceover("we multiply all the probabilities assigned to the actual outcome from each row together.") as tracker:
                self.play(TransformByGlyphMap(partial_likelihoods_table_old, likelihood_together,
                                            *glyph_map,
                                            run_time = 2.2))
            
            # Actually calculate the likelihood
            likelihood = np.exp(log_likelihood(X, y, bhat, add_intercept=True))
            likelihood_str = f"L={likelihood:.4g}"
            all_likelihood_strs.append(likelihood_str[2:]) # We don't want the "L="

            likelihood_final = MathTex(likelihood_str).next_to(substituted_formula_new, UP)
            all_likelihood_texes.append(likelihood_final.copy())
            with self.voiceover("And we get 3.394 times 10^-47. This might seem bad, but since we’re multiplying 569 things together, it’s not that bad.") as tracker:
                self.play(TransformByGlyphMap(likelihood_together, likelihood_final,
                                            (range(2, eq_idx), range(2, len(likelihood_str)))))
                self.wait(tracker.duration - 2.5)
                self.play(FadeOut(likelihood_final, bhats_tex, substituted_formula_old))


        # --- Show that we have a likelihood for every point and there's one MLE ---
        likelihood_grid = VGroup(*[VGroup(bhat_tex, likelihood_tex).arrange(DOWN) for bhat_tex, likelihood_tex in zip(all_bhat_texes, all_likelihood_texes)]).arrange(RIGHT)
        with self.voiceover("So for every set of beta hats, you get a likelihood for those betas.") as tracker:
            self.play(FadeIn(likelihood_grid))

        def l_function_tex(bhat):
            likelihood = np.exp(log_likelihood(X, y, bhat, add_intercept=True))
            likelihood_str = f"{likelihood:.4g}"
            likelihood_vector = numpy_to_latex(as_col(bhat))
            new_likelihood_tex = MathTex("L(",likelihood_vector, ")=", likelihood_str)
            new_likelihood_tex[1].set_color(BLUE)
            return new_likelihood_tex

        for m in range(100):
            all_bhats.append(arbitrarily_choose_bhat())
        with self.voiceover("In this way, you can think of the likelihood as a function of the beta hats. ") as tracker:
            l_vectors_old = likelihood_grid
            dims = (1,3),(3,3),(5,5),(7,7)
            for rows, cols in dims:
                l_vector_texes = [l_function_tex(bhat) for bhat in all_bhats[0:rows * cols]]
                l_vectors_new = VGroup(*l_vector_texes).arrange_in_grid(rows=rows, cols=cols).scale_to_fit_width(config.frame_width)
                self.play(TransformMatchingShapes(l_vectors_old, l_vectors_new), run_time = 0.8)
                l_vectors_old = l_vectors_new

            self.wait(max(tracker.duration - len(dims) * 0.8 - 1.1, 0))
            self.play(FadeOut(l_vectors_new))

        # --- Graph the likelihood ---
        with self.voiceover("Somewhere this function has a maximum, and the beta hats at the maximum are the beta hats that our model uses.") as tracker:
            self.move_camera(
                phi=60 * DEGREES,
                theta=-45 * DEGREES,
                run_time=1
            )
            # Function 
            def f(x, y):
                return np.exp(-0.5 * (x - 0.54)**2 - (y + 0.82)**2 - 0.2) # I just made this up because it's nice

            # Axes
            axes = ThreeDAxes(
                x_range=[-3, 3],
                y_range=[-3, 3],
                z_range=[-3, 3],
            )

            x_label = MathTex(r"\hat{\beta}_0").next_to(axes.x_axis.get_end(), RIGHT)
            y_label = MathTex(r"\hat{\beta}_1").next_to(axes.y_axis.get_end(), UP)
            z_label = MathTex("L").next_to(axes.z_axis.get_end(), OUT)
            axis_labels = VGroup(x_label, y_label, z_label)
            self.add_fixed_orientation_mobjects(x_label, y_label, z_label)

            # Surface 
            surface = Surface(
                lambda u, v_: axes.c2p(u, v_, f(u, v_)),
                u_range=[-2, 2],
                v_range=[-2, 2],
                resolution=(12, 12), # TODO: Make this bigger again during production
                fill_opacity=0.35,
            )

            # point at the max
            max_coords = 0.54, -0.82, f(0.54, -0.82)
            max_point = Dot3D(axes.c2p(*max_coords))
            self.play(Create(axes), Create(surface), Write(axis_labels))
            self.play(FadeIn(max_point))



