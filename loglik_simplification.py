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
        loglik9 = MathTex(r"l=\sum_{i=1}^{n}y_i(\ln(\hat{\beta_0}+\hat{\beta_1} X_{i,1}+\hat{\beta_2} X_{i,2}+\ldots+\hat{\beta}_{k-1} X_{i,k-1}))+\ln(1-\hat{y}_i)")

        yeetgroup = VGroup(loglik4, loglik5, loglik6, loglik7, loglik8, loglik9).arrange(DOWN).scale(0.7).to_edge(UP)
        self.add(yeetgroup)