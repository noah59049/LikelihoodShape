import numpy as np
from manim import *
from MF_Tools import *

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

class SigmoidScene(Scene):
    def construct(self):
        # Part 1: Sigmoid definitions
        sigmoid_defn  = MathTex(r"\sigma(z)=\frac{1}{1+e^{-z}}").to_corner(UL)
        sigmoid_defn2 = MathTex(r"\sigma(z)=\frac{(1)e^z}{(1+e^{-z})e^z}").to_corner(UL)
        sigmoid_defn3 = MathTex(r"\sigma(z)=\frac{e^z}{e^z+e^ze^{-z}}").to_corner(UL)
        sigmoid_defn4 = MathTex(r"\sigma(z)=\frac{e^z}{e^z+1}").to_corner(UL)

        # Part 2: Graph
        axes = Axes(x_range = [-5,5,1], 
                    y_range = [-0,1,0.2],
                    ).add_coordinates()
        axis_labels = axes.get_axis_labels(x_label = "z",
                                           y_label = r"\sigma(z)")
        func = axes.plot(sigmoid, 
                         color = GREEN)
        graph_group = VGroup(axes, axis_labels, func)

        # Part 3: The animation
        self.play(Write(sigmoid_defn))
        self.play(DrawBorderThenFill(axes), Write(axis_labels), run_time = 0.5)
        self.play(Create(func))

        self.play(TransformByGlyphMap(sigmoid_defn, sigmoid_defn2,
                                      (FadeIn, [5,7,8,9]),
                                      (FadeIn, [11,17,18,19])))
        self.play(TransformByGlyphMap(sigmoid_defn2, sigmoid_defn3,
                                      ([5,6,7], FadeOut, {"run_time": 0.25}),
                                      ([11,17],FadeOut),
                                      ([14,15,16], [13,14,15]),
                                      ([18, 19], [11,12], {"path_arc": PI}),
                                      ([12], [8,9]),
                                      ([18,19], [8,9], {"path_arc": PI})))
        self.play(TransformByGlyphMap(sigmoid_defn3, sigmoid_defn4,
                                      ([11,12,13,14,15], [11], {"run_time": 0.75})))
        self.wait(0.25)
