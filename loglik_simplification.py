from manim import *

class LoglikSimplificationScene(Scene):
    def construct(self):
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

        yeetgroup = VGroup(loglik12, loglik13, loglik14, loglik15, loglik16, loglik17).arrange(DOWN).scale(0.7).to_edge(UP)
        self.add(yeetgroup)