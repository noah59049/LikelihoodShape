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
        z_func = loglik_generator(X, y, add_intercept=True)
        axes, surface = create_3d_graph(z_func = z_func,
                                        x_range=x_range,
                                        y_range = y_range,
                                        z_range = "auto",
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
        self.wait(6)
        self.clear()