# In order to have our example matrices be realistic, we are generating them from an actual logistic regression model on the sklearn breast cancer dataset

import numpy as np
import pandas as pd
from N_Tools import as_row, as_col, numpy_to_latex
# from sklearn.datasets import load_breast_cancer
# from sklearn.linear_model import LogisticRegression
# import statsmodels.api as sm

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

x_names = [f"X{i + 1}" for i, e in enumerate(colnames)]
yX_tex_numbered = f"${numpy_to_latex(yX, make_table = True, colnames = ['Y'] + x_names)}$"
yX_lines = yX_tex_numbered.split(r"\hline")
yX_tex = f"${numpy_to_latex(yX, make_table = True, colnames = ['Y'] + colnames)}$"
y_tex = f"${numpy_to_latex(y, make_table = True, colnames = ['Y'])}$"
breast_cancer_tex = y_tex.replace("Y", "Breast Cancer")
y_labels_tex = y_tex.replace("0", "Malignant").replace("1", "Benign").replace("Y", "Breast Cancer")
yX_labels_tex = yX_tex.replace("    0 & ", "    Malignant & ").replace("    1 & ", "    Benign & ").replace("Y", "Breast Cancer")
yX_predict_tex = yX_labels_tex.replace(r"\end{tabular}", r"""
??? & 11.43 & 26.59 & 120.54 & 694.2 \\
\hline
\end{tabular}
                                """) # Ridiculous way to add another row, but it works.
# Many of these can be removed, but I'm not ready to remove them quite yet.

# ------------------------------
# Now actually animate the scene
# ------------------------------

if __name__ == "__main__":
    print(yX_labels_tex)

from manim import *
from manim_voiceover import VoiceoverScene
from MF_Tools import *
from manim_voiceover.services.stitcher import _StitcherService as StitcherService

class DefinitionsScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService("/Users/noah/Convex/LikelihoodShape/podcasts/intro_with_tables_podcast4.mp3",
                cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
                min_silence_len=2000,
                keep_silence=(0,0)))
        
        y_labels_table = Tex(y_labels_tex).scale(0.6)
        y_labels_table.shift(LEFT * y_labels_table.width * 1.4)
        breast_cancer_table = Tex(breast_cancer_tex).scale(0.6).align_to(y_labels_table, UL)
        yX_labels_table = Tex(yX_labels_tex).scale(0.6)
        yX_labels_table.align_to(y_labels_table,LEFT)
        yX_predict_table = Tex(yX_predict_tex).scale(0.6)
        yX_predict_table.align_to(y_labels_table,UL)

        y_table = Tex(y_tex).scale(0.6).align_to(y_labels_table, UL)
        yX_table = Tex(yX_tex).scale(0.6).align_to(y_labels_table, UL)
        yX_table_numbered = Tex(yX_tex_numbered).scale(0.6).align_to(y_labels_table, UL).to_edge(LEFT, buff = 0.4)
        # Many of these can be removed, but I'm not ready to remove them quite yet.
        
        with self.voiceover("We have a variable we’re interested in predicting, like the status of the tumor.") as tracker:
            self.play(Write(y_labels_table))


        with self.voiceover("It has many names, but here we’ll call it") as tracker:
            y_names = [
                "Response Variable",
                "Dependent Variable",
                "Outcome Variable"
            ]
            y_names_tex = VGroup(*[Text(name) for name in y_names]).arrange(DOWN)
            y_names_tex.to_edge(RIGHT)
            self.play(Write(y_names_tex))

        with self.voiceover("the response variable. And it’s dichotomous, it can only have 2 values, which here are benign and malignant, so we represent") as tracker:
            rect = SurroundingRectangle(y_names_tex[0], color=RED, buff=0.1)
            self.play(
                y_names_tex[0].animate.set_color(RED),
                Create(rect)
            )

        with self.voiceover("one of those values as 0 and the other as 1. ") as tracker:
            self.remove(y_names_tex, rect)
            dichotomous_text = Text("0 = Malignant\n1 = Benign")
            self.play(Write(dichotomous_text))
            self.wait(tracker.duration - 2.5)
            self.play(TransformMatchingTex(y_labels_table, breast_cancer_table))
            self.remove(dichotomous_text)

        with self.voiceover("We call it Y.") as tracker:
            self.play(TransformByGlyphMap(breast_cancer_table, y_table,
                                          (range(2,14), [2])))

        with self.voiceover("We have one ore more other variables we’re using to predict our response variable. ") as tracker:
            self.play(FadeIn(yX_table))
            self.remove(y_table)
            self.play(yX_table.animate.to_edge(LEFT, buff=0.4), run_time = tracker.duration - 1.3)
        
        with self.voiceover("They have many names too,") as tracker:
            x_names = [
                "Predictor Variables",
                "Independent Variables",
                "Explanatory Variables",
                "Regressors",
                "Covariates"
            ]
            x_names_tex = VGroup(*[Text(name) for name in x_names]).arrange(DOWN).scale(0.7)
            x_names_tex.to_edge(RIGHT)
            self.play(Write(x_names_tex), run_time = 0.73)
        
        with self.voiceover("but we’ll call them predictors. They can be any real number.") as tracker:
            rect = SurroundingRectangle(x_names_tex[0], color=RED, buff=0.1)
            self.play(
                x_names_tex[0].animate.set_color(RED),
                Create(rect)
            )

        with self.voiceover("We notate them X1, X2, etc.") as tracker:
            self.remove(x_names_tex, rect)
            self.play(TransformMatchingTex(yX_table, yX_table_numbered))