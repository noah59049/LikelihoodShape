from manim import *
import numpy as np
import pandas as pd

df = pd.read_csv("breast_cancer_sklearn.csv")
X = np.array(df[df.columns[0]])
Y = np.array(df["target"])

def simple_linear_regression(X, Y):
    X = np.asarray(X)
    Y = np.asarray(Y)
    
    if X.shape != Y.shape:
        raise ValueError("X and Y must have the same shape")
    
    x_mean = X.mean()
    y_mean = Y.mean()
    
    # slope (beta_1)
    beta_1 = np.sum((X - x_mean) * (Y - y_mean)) / np.sum((X - x_mean)**2)
    
    # intercept (beta_0)
    beta_0 = y_mean - beta_1 * x_mean
    
    return beta_0, beta_1

class GraphDataScene(Scene):
    def construct(self):
        x_range = max(X) - min(X)
        axes = Axes(x_range = [min(X) - 0.1 * x_range, max(X) + 0.1 * x_range], y_range = [-0.2, 1.2])
        axis_labels = axes.get_axis_labels(x_label = "X1", y_label = "Y")
        dots = VGroup(*[Dot(axes.c2p(x, y), color = DARK_BLUE) for x, y in zip(X, Y)])
        
        self.play(DrawBorderThenFill(axes))
        self.play(Write(axis_labels))
        self.play(LaggedStart(*[Write(dot) for dot in dots], lag_ratio=0.005))

        # Regression coefficients
        beta0, beta1 = simple_linear_regression(X, Y)
        regression_line = axes.plot(lambda x : beta0 + beta1 * x,
                                    x_range = [(1.2 - beta0) / beta1, (-0.2 - beta0) / beta1],
                                    color = RED)
        self.play(Create(regression_line))