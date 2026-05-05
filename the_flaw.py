import numpy as np
import data # type: ignore
from manim import *
from N_Tools import *

class FlawScene(ThreeDScene):
    def construct(self):
        X = as_col(data.X[:,0])
        y = data.y
        ses = 0.03

        beta, cov, se = logistic_regression(X, y, add_intercept = True, return_stats = True)
        x_range = (beta[0] - se[0] * ses, beta[0] + se[0] * ses)
        y_range = (beta[1] - se[1] * ses, beta[1] + se[1] * ses)
        loglik = loglik_generator(X, y, add_intercept=True)
        z_range = compute_z_range(
            z_func=loglik,
            x_range=x_range,
            y_range=y_range,
            samples=21
        )
        axes, surface = create_3d_graph(z_func = loglik,
                                        x_range=x_range,
                                        y_range = y_range,
                                        z_range = z_range,
                                        resolution=21,
                                        color = BLUE_C)
        
        self.set_camera_orientation(
            phi=55 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.55
        )
        self.add(axes)
        self.play(Create(surface))
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        # self.wait(6)

        # --- What if it's a local minimum ---
        mle_x, mle_y = beta
        mle_z = log_likelihood(X, y, beta, add_intercept = True)
        
        mle_dot = Dot3D(axes.c2p(mle_x, mle_y, mle_z), color = RED)
        self.play(FadeIn(mle_dot))
        self.wait(1)

        def upside_down_loglik(beta_hat0, beta_hat1):
            return 2 * mle_z - loglik(beta_hat0, beta_hat1)
        
        print(f"loglik mle = {loglik(*beta)}")
        print(f"upside down loglik mle = {upside_down_loglik(*beta)}")
        
        _, surface2 = create_3d_graph(z_func = upside_down_loglik,
                                      x_range=x_range,
                                      y_range = y_range,
                                      z_range = z_range,
                                      resolution=21,
                                      color = BLUE_C)
        self.play(Transform(surface, surface2))
        self.play(Transform(surface2, surface))
        
        