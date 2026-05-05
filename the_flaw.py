import numpy as np
import data # type: ignore
from manim import *
from N_Tools import create_likelihood_graph

class FlawScene(ThreeDScene):
    def construct(self):
        axes, surface = create_likelihood_graph(data.X[:,0], 
                                            data.y,
                                            x_ses = 0.01,
                                            y_ses = 0.01,
                                            use_loglik=True,
                                            resolution=21)
        
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