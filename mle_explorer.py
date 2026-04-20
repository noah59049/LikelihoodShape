import numpy as np
import pandas as pd
from manim import *
from MF_Tools import *
from N_Tools import as_row, as_col, numpy_to_latex, sigmoid, logistic_regression, round_sig
from intro_with_tables import yX_tex_numbered # TODO: Maybe move this to a data file

COLS_TO_KEEP = 4 # If we set this to a different number it would minorly break things
"""
colnames = list(load_breast_cancer().feature_names[0:COLS_TO_KEEP])
X, y = load_breast_cancer(return_X_y=True)
X = X[:,0:COLS_TO_KEEP]
yX = np.hstack([as_col(y.astype(X.dtype)), X])
"""
df = pd.read_csv("breast_cancer_sklearn.csv")
colnames = list(df.columns[0:COLS_TO_KEEP])
X = np.array(df[colnames])
y = np.array(df["target"])
yX = np.hstack([as_col(y.astype(X.dtype)), X])
yXyhat_tex = yX_tex_numbered.replace(r"\\", r"& \\").replace(r"c | }", r"c | c | }").replace("X4\n &", r"X4 & $\hat{y}$")

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
        formula4 = MathTex(*formula4_parts).to_edge(DOWN)
        self.play(TransformMatchingTex(formula3, formula4, run_time = 0.001))
        def formula4_beta_index(j):
            if j == 0: return 1
            else: return 3 * j
        def formula4_x_index(j):
            return 1 + 3 * j

        self.play(FadeIn(yX_table))
        yXyhat_table = Tex(yXyhat_tex).scale(0.66).to_corner(UL)
        self.play(FadeIn(yXyhat_table))
        self.remove(yX_table)

        # This happens for every estimate of the betas
        for _ in range(1):
            bhat0 = logistic_regression(X, y, add_intercept=True)
            bhat0 = round_sig(bhat0, 4)
            bhats_tex = VGroup(*[MathTex(r"\hat{\beta}_" + str(i) + f"={e}") for i,e in enumerate(bhat0)]).arrange(DOWN).to_corner(UR)
            self.play(FadeIn(bhats_tex))

            substituted_formula_parts = formula4_parts.copy()
            for j in range(COLS_TO_KEEP + 1):
                idx = formula4_beta_index(j)
                if j == 0 or bhat0[j] >= 0:
                    substituted_formula_parts[idx] = f"{bhat0[j]}"
                else: # For negative beta hats, we change the sign to a minus
                    substituted_formula_parts[idx] = f"{-bhat0[j]}"
                    substituted_formula_parts[idx - 1] = "-"

            substituted_formula = MathTex(*substituted_formula_parts).to_edge(DOWN)
            self.play(*[ReplacementTransform(formula4[i], substituted_formula[i])
                         for i in range(len(formula4_parts))])

            junk_table = Tex(numpy_to_latex(yX[0:4,:], make_table = True, colnames = ["X1"] * (COLS_TO_KEEP + 1))).scale(0.66).to_corner(UL)
            rect_height = junk_table.height / 5
            rect_width = yX_table.width
            highlight_rect = Rectangle(color = RED, width = rect_width, height = rect_height).set_opacity(0.3).to_corner(UL)
            self.play(FadeIn(highlight_rect))

            old_table_tex = yXyhat_tex
            old_table = yXyhat_table
            for i in range(1):
                self.play(highlight_rect.animate.shift(DOWN * highlight_rect.height))

                substituted_formula_parts2 = substituted_formula_parts.copy()
                row_np = X[i,:]
                for j, e in enumerate(row_np.reshape(-1)):
                    substituted_formula_parts2[formula4_x_index(j + 1)] = f"({e})"
                substituted_formula2 = MathTex(*substituted_formula_parts2).scale(0.83).to_edge(DOWN)
                self.play(*[ReplacementTransform(substituted_formula[i], substituted_formula2[i])
                         for i in range(len(substituted_formula_parts2))])

                new_table_tex = old_table_tex
                zi = np.sum(bhat0 * np.hstack([np.array([1.0]), row_np]))
                yhat_i = sigmoid(zi)
                new_table_tex = new_table_tex.replace(r"& \\", f"& {yhat_i:.4g} \\\\", count = 1)
                new_table = Tex(new_table_tex).scale(0.66).to_corner(UL)
                self.play(TransformMatchingTex(old_table, new_table))