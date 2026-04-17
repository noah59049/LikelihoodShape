from manim import *

class LoglikSimplificationScene(Scene):
    def construct(self):
        # We will probably start with loglik4, but it's nice to have these I guess
        loglik1 = MathTex(r"l=\ln\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        loglik2 = MathTex(r"l=\sum_{i=1}^{n}\ln[\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}]")
        loglik3 = MathTex(r"l=\sum_{i=1}^{n}\ln\hat{y}_i^{y_i}+\ln(1-\hat{y}_i)^{1-{y_i}}")
        loglik4 = MathTex(r"l=\sum_{i=1}^{n}y_i\ln\hat{y}_i+({1-{y_i}})\ln(1-\hat{y}_i)")
        loglik5 = MathTex(r"l=\sum_{i=1}^{n}y_i\ln\hat{y}_i+\ln(1-\hat{y}_i)-{y_i}\ln(1-\hat{y}_i)")
        loglik6 = MathTex(r"l=\sum_{i=1}^{n}y_i\ln\hat{y}_i-{y_i}\ln(1-\hat{y}_i)+\ln(1-\hat{y}_i)")
        loglik7 = MathTex(r"l=\sum_{i=1}^{n}y_i(\ln\hat{y}_i-\ln(1-\hat{y}_i))+\ln(1-\hat{y}_i)")
        loglik8 = MathTex(r"l=\sum_{i=1}^{n}y_i(\ln\frac{\hat{y}_i}{1-\hat{y}_i})+\ln(1-\hat{y}_i)")

        yeetgroup = VGroup(loglik4, loglik5, loglik6, loglik7, loglik8).arrange(DOWN).to_edge(UP)
        self.add(yeetgroup)