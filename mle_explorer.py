import numpy as np
import pandas as pd
from manim import *
from MF_Tools import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
from N_Tools import as_row, as_col, numpy_to_latex, sigmoid, logistic_regression, round_sig, get_matching_cell_map, TransformMatchingCells, latex_table_to_array, highlight_row, highlight_cell, extract_table_grid, log_likelihood, FadeInRHS, FlashAround, latex_vector, create_likelihood_graph, get_graph_mle, surface_from_function, loglik_generator, TransformWithBoxes
from intro_with_tables import yX_tex_numbered # TODO: Maybe move this to a data file
from data import COLS_TO_KEEP, X, y, yX # type: ignore
from hat_matrix_logo import HMDialogBox
from tex_colors import *


yXyhat_tex = yX_tex_numbered.replace(r"\\", r"& \\").replace(r"c | }", r"c | c | }").replace("X4\n &", r"X4 & $\hat{y}$")
array_from_latex = latex_table_to_array(yX_tex_numbered)
array_from_latex = array_from_latex[1:] # The first row is the title row with just nans
y_latex = array_from_latex[:,0].reshape(-1)

TableTransform = TransformMatchingCells # TransformMatchingCells for production, FadeTransform for fast rendering

class MLEScene(VoiceoverScene, ThreeDScene):
    def construct(self):
        self.set_speech_service(StitcherService(r"/Users/noah/Convex/LikelihoodShape/podcasts/mle_explorer_podcast21.wav",
                cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
                min_silence_len=2000,
                keep_silence=(0,0)))
        yX_table = Tex(yX_tex_numbered).scale(0.66).to_corner(UL)
        mle_words = Text("Maximum Likelihood Estimation")
        tex1 = ColoredMathTex(r"L(\hat{\beta})")
        tex2 = ColoredMathTex(r"L(\hat{\beta})=P(Y|\hat{\beta})")
        mle_words.next_to(tex1, UP)
        formula = ColoredMathTex(r"p=\sigma(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})")
        
        self.add(formula)
        with self.voiceover("We still have a burning question though: how do we know what the betas are?") as tracker:
            pass
        with self.voiceover("Well, we don't. We estimate them using a technique called") as tracker:
            self.play(formula.animate.to_edge(DOWN))
        with self.voiceover("maximum likelihood estimation. If we have an estimate of our betas, the") as tracker:
            self.play(FadeIn(mle_words), FlashAround(mle_words))
        with self.voiceover("likelihood, indicated L, of that estimate is the") as tracker:
            self.play(FadeIn(tex1))
        with self.voiceover("probability that it would produce the observed values of Y. In order to indicate that they're estimated, we put a") as tracker:
            self.play(FadeInRHS(tex1, tex2))
            self.wait(max(0, tracker.duration - 1.7))
            self.play(FadeOut(mle_words, tex2, run_time = 0.6))

        with self.voiceover("hat over the betas, and we use y hat to mean our estimate of p.") as tracker:
            formula2 = ColoredMathTex(r"\hat{y}=\sigma(\hat{\beta_0}+\hat{\beta_1} X_{1}+\hat{\beta_2} X_{2}+\ldots+\hat{\beta}_{k-1} X_{k-1})").to_edge(DOWN)
            self.play(TransformByGlyphMap(formula, formula2,
                                        (FadeIn, [1]),
                                        (FadeIn, [5]),
                                        (FadeIn, [9]),
                                        (FadeIn, [15]),
                                        (FadeIn, [25]),
                                        ))
            hat_dialog = HMDialogBox("In most of statistics, having a hat over something means it's estimated from data")
            hat_dialog.to_corner(UR)
            self.play(FadeIn(hat_dialog))

        with self.voiceover("Let's look at our data table") as tracker:
            self.remove(hat_dialog)
            self.play(FadeIn(yX_table))

        with self.voiceover("In this case we have 4 predictors. So let’s show that in our formula.") as tracker:
            formula3_tex = r"\hat{y}=\sigma(\hat{\beta_0}+" + "+".join(r"\hat{\beta_j} X_{j}".replace("j",str(j)) for j in range(1, 1 + COLS_TO_KEEP)) + ")"
            formula3 = ColoredMathTex(formula3_tex).to_edge(DOWN)
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
            with self.voiceover("Let’s look at an estimate of the betas.") as tracker:
                bhats_tex = VGroup(*[ColoredMathTex(r"\hat{\beta}_" + str(i) + f"={e}") for i,e in enumerate(bhat)]).set_color(beta_color).arrange(DOWN).to_corner(UR)
                all_bhat_texes.append(bhats_tex.copy().arrange(DOWN, aligned_edge = LEFT))
                self.play(FadeIn(bhats_tex))

                if m == 0:
                    arbitrary_dialog = HMDialogBox("There's nothing special about these betas; they are chosen mostly arbitrarily.", 
                                                   text_width = 3,
                                                   text_scale=0.5)
                    arbitrary_dialog.to_corner(DR).shift(arbitrary_dialog.height * 0.8 * UP)
                    self.play(FadeIn(arbitrary_dialog))
                    self.play(FadeOut(arbitrary_dialog))

                formula4_parts = [r"\hat{y}=\sigma(",r"\hat{\beta_0}"]
                for j in range(1, 1 + COLS_TO_KEEP):
                    formula4_parts.append("+")
                    formula4_parts.append(rf"\hat{{\beta_{j}}}")
                    formula4_parts.append(rf"X_{{{j}}}")
                formula4_parts.append(")")
                formula4 = ColoredMathTex(*formula4_parts).to_edge(DOWN)
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
                substituted_formula = ColoredMathTex(*substituted_formula_parts).to_edge(DOWN)
                for j in range(COLS_TO_KEEP + 1):
                    substituted_formula[formula4_beta_index(j)].set_color(beta_color)

                if m == 0:
                    self.play(TransformMatchingTex(formula3, formula4, run_time = 0.001))
                    self.play(*[formula4[formula4_beta_index(j)].animate.set_color(beta_color) for j in range(COLS_TO_KEEP + 1)])
                    self.play(*[ReplacementTransform(formula4[i], substituted_formula[i])
                                for i in range(len(formula4_parts))])
                else:
                    self.play(FadeIn(substituted_formula))

            with self.voiceover("For each individual, we get a y hat.") as tracker:
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
                    substituted_formula_new = ColoredMathTex(*substituted_formula_parts2).scale(0.83).to_edge(DOWN)
                    for j in range(COLS_TO_KEEP + 1):
                        substituted_formula_new[formula4_beta_index(j)].set_color(beta_color)
                        if j != 0:
                            substituted_formula_new[formula4_x_index(j)].set_color(X_color)
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
                if m == 0:
                    Li_dialog = HMDialogBox("This column is Li because it's the contribution of the ith row to the likelihood. It will make more sense in a few seconds. But the notation for this column isn't important.",
                                            text_width = 5)
                    Li_dialog.to_corner(DR)
                    Li_dialog.shift(Li_dialog.height * 0.8 * UP)
                    self.play(FadeIn(Li_dialog))
                    self.play(FadeOut(Li_dialog))
            with self.voiceover("So in the first row, y is 1, the predicted probability of y being 1 is y hat ,which is 0.9051. In the second row, y is 0, and the predicted probability of y being 0 is 1 - y hat, which is 0.9998. So now we continue that process for all of the rows.") as tracker:
                if m == 0:
                    for i in range(array_from_latex.shape[0]):
                        # --- Determine the run time ---
                        if i == 0:
                            run_time = 10 # Determined from the audio
                            squish_time = None # We shouldn't need to use this
                        elif i == 1:
                            run_time = 8 # Determined from the audio
                            squish_time = 4 # Determined from the audio
                        else:
                            run_time = squish_time = 0.8

                        # --- Get the new latex table ---
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
                    
                        # --- Get the cell map for the transform ---
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
                else:
                    # Build intermediate table with all Li_str1 values; animate all arcs simultaneously
                    all_Li_str1 = []
                    all_Li_str2 = []
                    all_yi = []
                    all_Li = []
                    partial_likelihoods_tex_intermediate = partial_likelihoods_tex_old
                    for i in range(array_from_latex.shape[0]):
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
                        all_Li_str1.append(Li_str1)
                        all_Li_str2.append(Li_str2)
                        all_yi.append(yi)
                        all_Li.append(Li)
                        partial_likelihoods.append(Li_str2)
                        partial_likelihoods_tex_intermediate = partial_likelihoods_tex_intermediate.replace(r"& \\", f"& {Li_str1} \\\\", count=1)
                    partial_likelihoods_table_intermediate = Tex(partial_likelihoods_tex_intermediate).scale(0.66).to_corner(UL)

                    # Build combined cell map with arcs for all rows at once
                    cell_map = get_matching_cell_map(partial_likelihoods_table_old, partial_likelihoods_table_intermediate)
                    for i in range(array_from_latex.shape[0]):
                        yhati_glyphs = extract_table_grid(partial_likelihoods_table_old)[(i + 1, COLS_TO_KEEP + 1)]
                        Li_glyphs    = extract_table_grid(partial_likelihoods_table_intermediate)[(i + 1, COLS_TO_KEEP + 2)]
                        for entry in cell_map.copy():
                            if entry[1] == Li_glyphs:
                                cell_map.remove(entry)
                        if all_yi[i] == 1 or np.isnan(all_Li[i]):
                            cell_map.append((yhati_glyphs, Li_glyphs, {"path_arc": -PI / 5}))
                        else:
                            cell_map.append((yhati_glyphs, Li_glyphs[2:], {"path_arc": -PI / 5}))
                            cell_map.append(([], Li_glyphs[0:2], {"delay": 0.35, "run_time": 0.6}))
                    self.play(TransformByGlyphMap(partial_likelihoods_table_old, partial_likelihoods_table_intermediate, *cell_map), run_time=1)

                    # Squish all rows where Li_str1 != Li_str2 simultaneously
                    if any(s1 != s2 for s1, s2 in zip(all_Li_str1, all_Li_str2)):
                        partial_likelihoods_tex_final = partial_likelihoods_tex_old
                        for Li_str2 in all_Li_str2:
                            partial_likelihoods_tex_final = partial_likelihoods_tex_final.replace(r"& \\", f"& {Li_str2} \\\\", count=1)
                        partial_likelihoods_table_final = Tex(partial_likelihoods_tex_final).scale(0.66).to_corner(UL)
                        self.play(TableTransform(partial_likelihoods_table_intermediate, partial_likelihoods_table_final), run_time=1)
                        partial_likelihoods_table_old = partial_likelihoods_table_final
                        partial_likelihoods_tex_old = partial_likelihoods_tex_final
                    else:
                        partial_likelihoods_table_old = partial_likelihoods_table_intermediate
                        partial_likelihoods_tex_old = partial_likelihoods_tex_intermediate

            if m == 0:
                with self.voiceover("And then to get the overall likelihood,"):
                    pass

            # --- Show the product of the partial likelihoods
            likelihood_together_tex = "L = " + "*".join(partial_likelihoods).replace(r"\vdots", r"\ldots")
            likelihood_together = ColoredMathTex(likelihood_together_tex).scale_to_fit_width(config.frame_width).next_to(substituted_formula_new, UP)

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
                if m == 0:
                    independence_dialog = HMDialogBox("An assumption of logistic regression is that each individual (each row) is independent, so it's fine to simply multiply the probabilities from each row.")
                    independence_dialog.to_corner(UL)
                    self.play(FadeIn(independence_dialog))
                    self.play(FadeOut(independence_dialog))
            
            # Actually calculate the likelihood
            likelihood = np.exp(log_likelihood(X, y, bhat, add_intercept=True))
            likelihood_str = f"L={likelihood:.4g}"
            all_likelihood_strs.append(likelihood_str[2:]) # We don't want the "L="

            likelihood_final = ColoredMathTex(likelihood_str).next_to(substituted_formula_new, UP)
            all_likelihood_texes.append(likelihood_final.copy())
            with self.voiceover("And we get 3.394 times 10^-47. Let’s see how this compares to other beta hats.") as tracker:
                self.play(TransformByGlyphMap(likelihood_together, likelihood_final,
                                            (range(2, eq_idx), range(2, len(likelihood_str)))))
                self.wait(tracker.duration - 2.5)
                self.play(FadeOut(likelihood_final, bhats_tex, substituted_formula_old))
        
        if False:
            # IMPORTANT: DO NOT DELETE THESE!
            # We need them for insert_silences.py to correctly insert the silences.
            with self.voiceover("Here’s another estimate of the betas.") as tracker:
                pass
            with self.voiceover("So") as tracker:
                pass
            with self.voiceover("we get these y hats") as tracker:
                pass
            with self.voiceover("And") as tracker:
                pass
            with self.voiceover("these probabilities assigned to the actual outcome") as tracker:
                pass
            with self.voiceover("And we multiply them together to get the likelihood for that estimate.") as tracker:
                pass
            with self.voiceover("That’s 1.663 times 10^-63, a bit worse. ") as tracker:
                pass

            with self.voiceover("Now let’s choose a third estimate for the betas.") as tracker:
                pass
            with self.voiceover("We") as tracker:
                pass
            with self.voiceover("find the y hats,") as tracker:
                pass
            with self.voiceover("and") as tracker:
                pass
            with self.voiceover("the probabilities assigned to the actual outcome, and") as tracker:
                pass
            with self.voiceover("multiply them together to get the likelihood") as tracker:
                pass
            with self.voiceover("That’s 1.454 times 10^-47, so better but not as good as the first estimate") as tracker:
                pass


        # --- This part used to be likelihood_cases.py ---

        # Step 1: Write the piecewise expression for the likelihood
        base = ColoredMathTex(r"L=\prod_{i=1}^{n}")
        brace = ColoredMathTex(r"\left\{").scale(1.6).next_to(base, RIGHT)
        row1 = ColoredMathTex(r"\hat{y}_i \quad \quad \quad (y_i=1)")
        row2 = ColoredMathTex(r"1-\hat{y}_i \quad \thinspace \thinspace (y_i=0)") # This leads to the conditions being aligned somehow, probably not the best fix but it works
        rows = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(brace, RIGHT, aligned_edge = UP)
        cases = VGroup(base, brace, rows)
        cases.scale(0.8)
        cases.to_corner(UR)

        row1_basic = ColoredMathTex(r"\hat{y} \quad \quad \quad (y=1)")
        row2_basic = ColoredMathTex(r"1-\hat{y} \quad \thinspace \thinspace (y=0)") # This leads to the conditions being aligned somehow, probably not the best fix but it works
        rows_basic = VGroup(row1_basic, row2_basic).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(brace, RIGHT, aligned_edge = UP)
        
        with self.voiceover("By now, you can probably guess what the formula for the likelihood is going to be. We're") as tracker:
            self.play(*[FadeOut(mob) for mob in list(self.mobjects)])
            self.set_camera_orientation(
                phi=0,
                theta=-90 * DEGREES,
                gamma=0,
                zoom=1
            )
            self.wait(1)
            self.play(FadeIn(partial_likelihoods_table_old))
        with self.voiceover("multiplying all the rows together, ") as tracker:
            self.play(TransformByGlyphMap(partial_likelihoods_table_old, likelihood_together, *glyph_map, run_time=2.2))
        with self.voiceover("so it's a product.") as tracker:
            self.play(Write(base, run_time = 1))
            self.add(brace)
        # Reconstruct initial Li table (Li column header present but all values empty)
        partial_likelihoods_tex_initial = old_table_tex.replace(r"\\", r"& \\").replace(r"c | }", r"c | c | }").replace("& \\\\\n", "& $L_i$ \\\\\n", count=1)
        partial_likelihoods_table_initial = Tex(partial_likelihoods_tex_initial).scale(0.66).to_corner(UL)

        # Build y1-done table: Li filled for y=1 rows (and dots row), empty for y=0 rows
        parts, remaining = [], partial_likelihoods_tex_initial
        for _i in range(array_from_latex.shape[0]):
            before, _, remaining = remaining.partition(r"& \\")
            parts.append(before)
            parts.append(f"& {all_Li_str1[_i]} \\\\" if (all_yi[_i] == 1 or np.isnan(all_Li[_i])) else r"& \\")
        parts.append(remaining)
        partial_likelihoods_table_y1_done = Tex("".join(parts)).scale(0.66).to_corner(UL)

        # cell_map: initial → y1_done  (arcs for y=1 / dots rows only)
        y1_cell_map = get_matching_cell_map(partial_likelihoods_table_initial, partial_likelihoods_table_y1_done)
        for _i in range(array_from_latex.shape[0]):
            if all_yi[_i] == 1 or np.isnan(all_Li[_i]):
                yhati_glyphs = extract_table_grid(partial_likelihoods_table_initial)[(_i + 1, COLS_TO_KEEP + 1)]
                Li_glyphs    = extract_table_grid(partial_likelihoods_table_y1_done)[(_i + 1, COLS_TO_KEEP + 2)]
                for entry in y1_cell_map.copy():
                    if entry[1] == Li_glyphs:
                        y1_cell_map.remove(entry)
                y1_cell_map.append((yhati_glyphs, Li_glyphs, {"path_arc": -PI / 5}))

        # cell_map: y1_done → intermediate  (arcs for y=0 rows only)
        y0_cell_map = get_matching_cell_map(partial_likelihoods_table_y1_done, partial_likelihoods_table_intermediate)
        for _i in range(array_from_latex.shape[0]):
            if all_yi[_i] == 0 and not np.isnan(all_Li[_i]):
                yhati_glyphs = extract_table_grid(partial_likelihoods_table_y1_done)[(_i + 1, COLS_TO_KEEP + 1)]
                Li_glyphs    = extract_table_grid(partial_likelihoods_table_intermediate)[(_i + 1, COLS_TO_KEEP + 2)]
                for entry in y0_cell_map.copy():
                    if entry[1] == Li_glyphs:
                        y0_cell_map.remove(entry)
                y0_cell_map.append((yhati_glyphs, Li_glyphs[2:], {"path_arc": -PI / 5}))
                y0_cell_map.append(([], Li_glyphs[0:2], {"delay": 0.35, "run_time": 0.6}))

        with self.voiceover("So if y is 1, the predicted probability of y being 1 ") as tracker:
            self.remove(likelihood_together)
            self.add(partial_likelihoods_table_initial)
            y1_highlights = VGroup(*[highlight_cell(partial_likelihoods_table_y1_done, row_idx=i+1, col_idx=j) for i in range(array_from_latex.shape[0]) if y_latex[i] == 1 for j in (0, COLS_TO_KEEP + 1, COLS_TO_KEEP + 2)])
            self.play(TransformByGlyphMap(partial_likelihoods_table_initial, partial_likelihoods_table_y1_done, *y1_cell_map), FadeIn(y1_highlights))
        with self.voiceover("is y hat, "):
            self.play(Write(row1_basic, run_time = 0.5))
        with self.voiceover("and if y is 0, the predicted probability of y being 0 ") as tracker:
            y0_highlights = VGroup(*[highlight_cell(partial_likelihoods_table_intermediate, row_idx=i+1, col_idx=j) for i in range(array_from_latex.shape[0]) if y_latex[i] == 0 for j in (0, COLS_TO_KEEP + 1, COLS_TO_KEEP + 2)])
            self.play(TransformByGlyphMap(partial_likelihoods_table_y1_done, partial_likelihoods_table_intermediate, *y0_cell_map), FadeOut(y1_highlights), FadeIn(y0_highlights))
        with self.voiceover("is 1 - y hat. We should subscript all our ys with") as tracker:
            self.play(Write(row2_basic, run_time = 0.5))
            self.wait(tracker.duration - 1.1)
            self.play(FadeOut(y0_highlights, partial_likelihoods_table_intermediate), run_time = 0.5)

        with self.voiceover("i because each element of this product is referring to the ith individual.") as tracker:
            self.play(TransformMatchingShapes(row1_basic, row1), TransformMatchingShapes(row2_basic, row2))


        # Step 2: Likelihood simplification for case y_i=1

        success1 = ColoredMathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        success2 = ColoredMathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{1}(1-\hat{y}_i)^{1-{1}}")
        success2a= ColoredMathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{1}(1-\hat{y}_i)^{0}")
        success3 = ColoredMathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{1}")
        success4 = ColoredMathTex(r"L=\prod_{i=1}^{n}\hat{y}_i")

        with self.voiceover("So this formula is correct, but the likelihood is instead usually written as the product of yi hat to the yi times 1 minus yi hat to the 1 minus yi. And this is equivalent. ") as tracker:
            self.play(FadeIn(success1))

        box1 = SurroundingRectangle(row1, color = RED)
        with self.voiceover("if yi=1, the right term is raised") as tracker:
            self.play(Create(box1, run_time = 0.5))
            self.play(TransformWithBoxes(success1, success2,
                ([9,10], [9]),
                ([21,22], [20])))

        with self.voiceover(" to the power of 0,") as tracker:
            self.play(TransformByGlyphMap(success2, success2a,
                                          ([18,19,20], [18])))

        with self.voiceover("so it goes away, and the left hand term ") as tracker:
            self.play(TransformByGlyphMap(success2a, success3,
                (range(11), range(11), {"delay": 0.7}),
                (range(11,19), FadeOut)))

        with self.voiceover("becomes yi hat, same as in the first formula") as tracker:
            self.play(TransformByGlyphMap(success3, success4,
                (range(9), range(9), {"delay": 0.4}),
                (range(9,10), FadeOut)))

            self.wait(tracker.duration - 2.1)        
            self.play(FadeOut(success4), FadeOut(box1))
        
        # --- Step 3: Likelihood simplification for case y_i=0 ---

            failure1 = ColoredMathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
            failure2 = ColoredMathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{0}(1-\hat{y}_i)^{1-{0}}")
            failure3 = ColoredMathTex(r"L=\prod_{i=1}^{n}(1-\hat{y}_i)^{1-{0}}")
            failure4 = ColoredMathTex(r"L=\prod_{i=1}^{n}1-\hat{y}_i")
            
            self.play(FadeIn(failure1))
        
        with self.voiceover("If yi=0, the left term is raised to the 0,") as tracker:
            box2 = SurroundingRectangle(row2, color = RED)
            self.play(Create(box2))
            self.play(
                TransformWithBoxes(
                    failure1, failure2,
                    ([9,10], [9]),
                    ([21,22], [20])
                )
            )

        with self.voiceover("so it goes away, ") as tracker:
            self.play(TransformByGlyphMap(failure2, failure3,
                ([7,8,9,10], FadeOut)))

        with self.voiceover("and we're left with 1 - yi hat, again, same as above. ") as tracker:
            self.play(TransformByGlyphMap(failure3, failure4,
                ([7],FadeOut),
                ([13,14,15,16], FadeOut)))

            # self.wait(tracker.duration - 2.1) # TODO: Figure out why this line is giving errors
            self.play(FadeOut(failure4), FadeOut(box2))

        # --- Graph the likelihood ---
        with self.voiceover("It's hopefully clear now that you can think of the likelihood as a ") as tracker:
            self.play(FadeIn(failure1))

        with self.voiceover("function of the beta hats.") as tracker:
            L_as_function = ColoredMathTex(r"L(\hat{\beta})=\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
            self.play(TransformByGlyphMap(failure1, L_as_function, (FadeIn, [1,2,3,4])))
            self.add_fixed_in_frame_mobjects(L_as_function)
            self.play(L_as_function.animate.to_corner(UL))

        with self.voiceover("Here's a graph of the likelihood vs the betas for one predictor.") as tracker:
            axes, surface = create_likelihood_graph(X[:,0],
                                            y,
                                            x_ses = 1,
                                            y_ses = 1,
                                            use_loglik=False,
                                            resolution=21)

            x_label = ColoredMathTex(r"\hat{\beta}_0").next_to(axes.x_axis.get_end(), RIGHT)
            y_label = ColoredMathTex(r"\hat{\beta}_1").next_to(axes.y_axis.get_end(), UP)
            z_label = ColoredMathTex("L").next_to(axes.z_axis.get_end(), OUT)
            axis_labels = VGroup(x_label, y_label, z_label)
            graph_group = VGroup(axes, surface, axis_labels)
            # Replicate zoom=0.4 and phi=60° without moving the camera.
            # scale(0.4) compensates for zoom; rotate(PI/3, RIGHT) tilts the L-axis
            # 60° from the camera direction so the surface is visible from the side.
            graph_group.scale(0.4, about_point=ORIGIN)
            graph_group.rotate(-PI / 3, axis=RIGHT, about_point=ORIGIN)

            self.play(Create(axes), Create(surface), Write(axis_labels))
            # Remove individual mobs and re-add as a group so that graph_group
            # is in self.mobjects and its updater gets called each frame.
            self.remove(axes, surface, axis_labels)
            self.add(graph_group)
            spin_axis = np.array([0, np.sin(PI / 3), np.cos(PI / 3)])
            graph_group.add_updater(lambda g, dt: g.rotate(0.2 * dt, axis=spin_axis, about_point=ORIGIN))

        with self.voiceover("At the maximum of the liklihood function, that's the MLE, that's the beta hats we use.") as tracker:
            beta_2d, se_2d, z_func_2d = get_graph_mle(axes, X[:,0], y)
            start_x = beta_2d[0] - se_2d[0]
            start_y = beta_2d[1] - se_2d[1]
            t = ValueTracker(0)
            def _dot_pos(tv):
                x  = start_x + tv * (beta_2d[0] - start_x)
                yc = start_y + tv * (beta_2d[1] - start_y)
                return axes.c2p(x, yc, z_func_2d(x, yc))
            mle_dot = Dot3D(_dot_pos(0), color=YELLOW, radius=0.08)
            mle_dot.add_updater(lambda d: d.move_to(_dot_pos(t.get_value())))
            self.add(mle_dot)
            self.play(t.animate.set_value(1), run_time=min(2, tracker.duration - 0.1))

        # Step 4: Add log likelihood
        loglik1 = ColoredMathTex(r"\ell(\hat{\beta})=\ln\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}").to_corner(UL)
        loglik2 = ColoredMathTex(r"\ell(\hat{\beta})=\sum_{i=1}^{n}\ln[\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}]").to_corner(UL)
        loglik3 = ColoredMathTex(r"\ell(\hat{\beta})=\sum_{i=1}^{n}\ln\hat{y}_i^{y_i}+ln(1-\hat{y}_i)^{1-{y_i}}").to_corner(UL)
        loglik4 = ColoredMathTex(r"\ell(\hat{\beta})=\sum_{i=1}^{n}y_i\ln\hat{y}_i+({1-{y_i}})ln(1-\hat{y}_i)").to_corner(UL)

        with self.voiceover("The log likelihood, denoted little l, is the ln of the likelihood. If we simplify a bit, ") as tracker:
            self.play(TransformByGlyphMap(L_as_function, loglik1,
                                        ([0], [0]),
                                        ([], [6,7])))

        with self.voiceover("the ln of a product is the sum of the lns,") as tracker:
            self.play(TransformByGlyphMap(loglik1, loglik2,
                                        ([9], [7]),
                                        ([6,7], [11,12]),
                                        (FadeIn, [13,30])))

        with self.voiceover("do it again ") as tracker:
            self.play(TransformByGlyphMap(loglik2, loglik3,
                                        ([13,30], FadeOut),
                                        (FadeIn, [18]),
                                        ([11,12], [11,12]),
                                        ([11,12],[19,20], {"path_arc": PI * -0.7})))

        with self.voiceover("and then move the exponents. Maximizing the likelihood is equivalent to maximizing the log likelihood. But using the log likelihood makes the math easier.") as tracker:
            self.play(TransformByGlyphMap(loglik3, loglik4,
                                        ([15,16],[11,12],{"path_arc": PI * 0.7}),
                                        (range(28,32),range(20,24), {"path_arc": PI * 0.7}),
                                        (FadeIn, [19,25])))

        with self.voiceover("So here's the graph of the log likelihood. The maximum is in the same place, but the graph is slightly nicer, and more importantly, it's easier to take the derivative of, which ties into our next idea.") as tracker:
            # Normalize the log-likelihood to [0, 1] so the peak stays at z=1
            # and the shape change is visible with the same axes.
            x_range_plot = (beta_2d[0] - se_2d[0], beta_2d[0] + se_2d[0])
            y_range_plot = (beta_2d[1] - se_2d[1], beta_2d[1] + se_2d[1])
            xs = np.linspace(*x_range_plot, 20)
            ys = np.linspace(*y_range_plot, 20)
            loglik_func = loglik_generator(as_col(X[:, 0]), y)
            loglik_max = loglik_func(beta_2d[0], beta_2d[1])  # == MLE log-likelihood
            loglik_min = min(loglik_func(x, yc) for x in xs for yc in ys)

            def loglik_norm(x, yc):
                return (loglik_func(x, yc) - loglik_min) / (loglik_max - loglik_min)

            # Morph surface in-place while it keeps spinning.  The updater rebuilds
            # surface each frame via axes.c2p(), which always reflects the current
            # rotation — so the spin updater (which runs first on graph_group) and
            # this morph updater (which runs next on the submobject) compose cleanly.
            morph = ValueTracker(0)

            def _morph_surface(mob):
                a = morph.get_value()
                new_surf = surface_from_function(
                    lambda x, yc: (1 - a) * z_func_2d(x, yc) + a * loglik_norm(x, yc),
                    axes, x_range_plot, y_range_plot, resolution=21,
                    color=interpolate_color(BLUE_C, TEAL_C, a),
                )
                mob.become(new_surf)

            surface.add_updater(_morph_surface)
            self.play(morph.animate.set_value(1), run_time=min(3, tracker.duration - 0.1))
            surface.remove_updater(_morph_surface)