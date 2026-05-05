import numpy as np
import data # type: ignore
from manim import *
from N_Tools import create_likelihood_graph

X = np.array(range(100))
y = X % 2

class PlotSurfaceExample(ThreeDScene):
    def construct(self):
        for ses in 0.0001, 0.001:#, 0.003, 0.01, 0.03, 0.1, 3, 1, 3, 10, 30, 100:
            axes, surface = create_likelihood_graph(data.X[:,0], 
                                            data.y,
                                            x_ses = ses,
                                            y_ses = ses,
                                            use_loglik=True,
                                            resolution=21)

            if True:
                self.set_camera_orientation(
                    phi=55 * DEGREES,
                    theta=-45 * DEGREES,
                    zoom=0.55
                )

            label = MathTex(f"\\hat{{\\beta}}\\pm{ses}*SE").to_corner(UL)
            self.add_fixed_in_frame_mobjects(label)
            self.add(axes)
            self.add(surface)
            self.wait(1)
            self.begin_ambient_camera_rotation(rate=0.2)
            self.wait(6)
            self.clear()