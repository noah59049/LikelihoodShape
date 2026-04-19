import numpy as np
import pandas as pd
from manim import *
from MF_Tools import *
from N_Tools import as_row, as_col, numpy_to_latex, sigmoid, logistic_regression
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

        self.play(FadeIn(yX_table))
        yXyhat_table = Tex(yXyhat_tex).scale(0.66).to_corner(UL)
        self.play(FadeIn(yXyhat_table))
        self.remove(yX_table)

        bhat0 = logistic_regression(X, y, add_intercept=True)
        bhats_tex = VGroup(*[MathTex(r"\hat{\beta}_" + str(i) + f"={e}") for i,e in enumerate(bhat0)]).arrange(DOWN).to_corner(UR)
        self.play(FadeIn(bhats_tex))

        substituted_formula_tex = formula3_tex
        for i,e in enumerate(bhat0):
            substituted_formula_tex = substituted_formula_tex.replace(r"\hat{\beta_" + str(i) + "}", f"{e:.{4}g}")
        substituted_formula = MathTex(substituted_formula_tex).to_edge(DOWN)
        self.play(TransformMatchingTex(formula3, substituted_formula))

        substituted_formula_tex2 = substituted_formula_tex
        row_np = X[0,:]
        for i, e in enumerate(row_np.reshape(-1)):
            substituted_formula_tex2 = substituted_formula_tex2.replace(f"X_{{{i+1}}}", f"({e})")
        substituted_formula2 = MathTex(substituted_formula_tex2).scale(0.83).to_edge(DOWN)
        self.play(TransformMatchingTex(substituted_formula, substituted_formula2))

        new_table_tex = yXyhat_tex
        zi = np.sum(bhat0 * np.hstack([np.array([1.0]), row_np]))
        yhat_i = sigmoid(zi)
        new_table_tex = new_table_tex.replace(r"& \\", f"& {yhat_i} \\\\", count = 1)
        new_table = Tex(new_table_tex).scale(0.66).to_corner(UL)
        self.play(TransformMatchingTex(yXyhat_table, new_table))
        

        junk_table = Tex(numpy_to_latex(yX[0:4,:], make_table = True, colnames = ["X1"] * (COLS_TO_KEEP + 1))).scale(0.66).to_corner(UL)
        rect_height = junk_table.height / 5
        rect_width = yXyhat_table.width
        highlight_rect = Rectangle(color = RED, width = rect_width, height = rect_height).set_opacity(0.3).to_corner(UL)
        self.play(FadeIn(highlight_rect))

