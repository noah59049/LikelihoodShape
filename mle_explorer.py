import numpy as np
import pandas as pd
from manim import *
from MF_Tools import *
from N_Tools import as_row, as_col, numpy_to_latex, sigmoid, logistic_regression, round_sig, get_matching_cell_map, TransformMatchingCells, latex_table_to_array, highlight_row, extract_table_grid, log_likelihood
from intro_with_tables import yX_tex_numbered # TODO: Maybe move this to a data file
from data import COLS_TO_KEEP, X, y, yX # type: ignore

yXyhat_tex = yX_tex_numbered.replace(r"\\", r"& \\").replace(r"c | }", r"c | c | }").replace("X4\n &", r"X4 & $\hat{y}$")
array_from_latex = latex_table_to_array(yX_tex_numbered)
array_from_latex = array_from_latex[1:] # The first row is the title row with just nans

class MLEScene(Scene):
    def construct(self):
        yX_table = Tex(yX_tex_numbered).scale(0.66).to_corner(UL)
        formula = MathTex(r"p=\sigma(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})").to_edge(DOWN)
        self.play(Write(formula))
        formula2 = MathTex(r"\hat{y}=\sigma(\hat{\beta_0}+\hat{\beta_1} X_{1}+\hat{\beta_2} X_{2}+\ldots+\hat{\beta}_{k-1} X_{k-1})").to_edge(DOWN)
        self.play(TransformByGlyphMap(formula, formula2,
                                      (FadeIn, [1]),
                                      (FadeIn, [5]),
                                      (FadeIn, [9]),
                                      (FadeIn, [15]),
                                      (FadeIn, [25]),
                                      ))
        formula3_tex = r"\hat{y}=\sigma(\hat{\beta_0}+" + "+".join(r"\hat{\beta_j} X_{j}".replace("j",str(j)) for j in range(1, 1 + COLS_TO_KEEP)) + ")"
        formula3 = MathTex(formula3_tex).to_edge(DOWN)
        self.play(TransformMatchingShapes(formula2, formula3))

        formula4_parts = [r"\hat{y}=\sigma(",r"\hat{\beta_0}"]
        for j in range(1, 1 + COLS_TO_KEEP):
            formula4_parts.append("+")
            formula4_parts.append(rf"\hat{{\beta_{j}}}")
            formula4_parts.append(rf"X_{{{j}}}")
        formula4_parts.append(")")
        formula4 = MathTex(*formula4_parts).to_edge(DOWN)
        self.play(TransformMatchingTex(formula3, formula4, run_time = 0.001))
        def formula4_beta_index(j):
            if j == 0: return 1
            else: return 3 * j
        def formula4_x_index(j):
            return 1 + 3 * j
        
        self.play(*[formula4[formula4_beta_index(j)].animate.set_color(BLUE) for j in range(COLS_TO_KEEP + 1)])
        self.play(*[formula4[formula4_x_index(j)].animate.set_color(RED) for j in range(1, COLS_TO_KEEP + 1)])

        self.play(FadeIn(yX_table))
        yXyhat_table = Tex(yXyhat_tex).scale(0.66).to_corner(UL)
        self.play(FadeIn(yXyhat_table))
        self.remove(yX_table)

        result = logistic_regression(X, y, add_intercept=True, return_stats=True)
        bhat_mle, cov, se = result
        rng = np.random.default_rng(seed = 186)

        # This loop happens for every estimate of the betas
        for _ in range(1):
            # --- Choose beta hats for our example that are normally distributed with mean at the MLE and covariance equal to the covariance matrix of the model
            bhat = bhat_mle + cov @ rng.normal(loc=0.0, scale=1.0, size=len(bhat_mle))
            bhat = round_sig(bhat, 4)

            # --- Add the beta hats to the corner ---
            bhats_tex = VGroup(*[MathTex(r"\hat{\beta}_" + str(i) + f"={e}") for i,e in enumerate(bhat)]).set_color(BLUE).arrange(DOWN).to_corner(UR)
            self.play(FadeIn(bhats_tex))

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
                if j != 0: 
                    substituted_formula[formula4_x_index(j)].set_color(RED)
            self.play(*[ReplacementTransform(formula4[i], substituted_formula[i])
                         for i in range(len(formula4_parts))])

            # --- add the y hats into the table one by one ---
            old_table_tex = yXyhat_tex
            old_table = yXyhat_table
            substituted_formula_old = substituted_formula
            substituted_formula_parts2 = substituted_formula_parts.copy()
            # This loop happens for every row
            for i in range(array_from_latex.shape[0]):
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
                
                # Play the formula that moves the highlight rect and substitutes
                self.play(*(highlight_rect_transforms + substituted_formula_transforms))

                # --- Add y hat ---
                zi = np.sum(bhat * np.hstack([np.array([1.0]), row_np]))
                yhat_i = sigmoid(zi)
                new_table_tex = old_table_tex
                new_table_tex = new_table_tex.replace(r"& \\", r"& \vdots \\" if np.isnan(yhat_i) else f"& {yhat_i:.4g} \\\\", count = 1)
                new_table = Tex(new_table_tex).scale(0.66).to_corner(UL)
                self.play(TransformMatchingCells(old_table, new_table))

                substituted_formula_old = substituted_formula_new
                old_table_tex = new_table_tex
                old_table = new_table

            # --- Add in the partial likelihoods ---
            self.play(FadeOut(highlight_rect))
            partial_likelihoods_tex_old = old_table_tex.replace(r"\\", r"& \\").replace(r"c | }", r"c | c | }").replace("& \\\\\n", "& $L_i$ \\\\\n", count = 1)
            print(partial_likelihoods_tex_old)
            partial_likelihoods_table_old = Tex(partial_likelihoods_tex_old).scale(0.66).to_corner(UL)
            self.play(FadeIn(partial_likelihoods_table_old))
            self.remove(new_table)
            partial_likelihoods = []
            # This loop happens for every row
            for i in range(array_from_latex.shape[0]):
                row_np = array_from_latex[i, 1:]
                zi = np.sum(bhat * np.hstack([np.array([1.0]), row_np]))
                yhat_i = sigmoid(zi)
                yi = y[i]
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
                    cell_map.append(([], Li_glyphs[0:2]))
                self.play(TransformByGlyphMap(partial_likelihoods_table_old, partial_likelihoods_table_new, *cell_map))
                partial_likelihoods_tex_old = partial_likelihoods_tex_new
                partial_likelihoods_table_old = partial_likelihoods_table_new

            return 
            # --- Show the product of the partial likelihoods
            likelihood_together_tex = "L = " + "*".join(partial_likelihoods).replace(r"\vdots", r"\ldots")
            likelihood_together = MathTex(likelihood_together_tex).scale_to_fit_width(config.frame_width).next_to(substituted_formula_new, UP)

            # Transform the matching numbers
            table_grid = extract_table_grid(partial_likelihoods_table_new)
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
            unused_table_glyphs = [i for i in range(len(partial_likelihoods_table_new[0])) if i not in used_table_glyphs]
            glyph_map.append((unused_table_glyphs, FadeOut))
            
            print(f"{glyph_map=}")
            print(f"{len(likelihood_together[0])=}")

            # Play the transform yeet
            self.play(TransformByGlyphMap(partial_likelihoods_table_new, likelihood_together,
                                          *glyph_map))
            
            # Actually calculate the likelihood
            likelihood = np.exp(log_likelihood(X, y, bhat, add_intercept=True))
            likelihood_str = f"L={likelihood:.4g}"

            likelihood_final = MathTex(likelihood_str).next_to(substituted_formula_new, UP)
            self.play(TransformByGlyphMap(likelihood_together, likelihood_final,
                                          (range(2, eq_idx), range(2, len(likelihood_str)))))
            
            self.play(FadeOut(likelihood_final, bhats_tex))

