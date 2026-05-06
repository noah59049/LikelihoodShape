import numpy as np
import data # type: ignore
from manim import *
from N_Tools import *

class FlawScene(ThreeDScene):
    def construct(self):
        # --- Get our actual log likelihood ---
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
        
        # --- Make the surface ---
        self.set_camera_orientation(
            phi=55 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.55
        )
        self.add(axes)
        self.play(Create(surface))
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)

        # --- Add the MLE dot ---
        mle_x, mle_y = beta
        mle_z = log_likelihood(X, y, beta, add_intercept = True)
        mle_dot = Dot3D(axes.c2p(mle_x, mle_y, mle_z), color = RED)
        self.play(FadeIn(mle_dot))

        # --- Define the functions for what if the log likelihood is something else ---
        def upside_down_loglik(beta_hat0, beta_hat1):
            return 2 * mle_z - loglik(beta_hat0, beta_hat1)
        def saddle_loglik(beta_hat0, beta_hat1):
            return loglik(beta_hat0, beta_hat1) - \
                   loglik(*rotate_90_cw(mle_x, mle_y, beta_hat0, beta_hat1, x_scale = se[0], y_scale = se[1])) + \
                   mle_z
        def bump(beta_hat0, beta_hat1):
            x0 = mle_x + se[0] * ses / 2 # I would rather do this with eigenvectors or something
            y0 = mle_y - se[1] * ses / 2 # I would rather do this with eigenvectors or something
            x_screen = (beta_hat0 - x0) / (se[0] * ses / 6)
            y_screen = (beta_hat1 - y0) / (se[1] * ses / 6)
            z_scale = (z_range[1] - z_range[0]) / 4
            exponential = np.exp(-(x_screen**2 + y_screen**2))
            return exponential * z_scale
        def bumped_loglik(beta_hat0, beta_hat1):
            return loglik(beta_hat0, beta_hat1) + bump(beta_hat0, beta_hat1)
        
        # --- Play the animations for what if it's a minimum, saddle, or local non global max ---
        for z_func in upside_down_loglik, saddle_loglik, bumped_loglik:
            _, surface2 = create_3d_graph(z_func = z_func,
                                        x_range=x_range,
                                        y_range = y_range,
                                        z_range = z_range,
                                        resolution=21,
                                        color = BLUE_C)
            surface.save_state()
            self.play(Transform(surface, surface2))
            self.play(Restore(surface))