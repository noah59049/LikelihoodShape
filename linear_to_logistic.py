import math
from manim import *
from MF_Tools import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.stitcher import _StitcherService as StitcherService

from manim import *
import numpy as np

def create_graph(
    func,
    x_range=None,
    y_range=None,
    x_label="x",
    y_label="y",
    domain=None,
    inverse_mode=False,
    inverse_func=None,   # maps y -> x (for inverse_mode mode)
    t_range=None,        # range in output space (y-space)
    n_points=1000,
    width = None,
    height = None,
    color=RED,
):
    # ---- defaults (avoid mutable args) ----
    x_range = x_range or [-5, 5, 1]
    y_range = y_range or [-5, 5, 1]

    if len(x_range) == 2:
        x_range = [*x_range, (x_range[1] - x_range[0]) * 0.1]
    if len(y_range) == 2:
        y_range = [*y_range, (y_range[1] - y_range[0]) * 0.1]

    domain = domain or x_range[0:2]
    if len(domain) == 2:
        step_size = (domain[1] - domain[0]) / n_points
        domain = [*domain, step_size]

    # ---- axes ----

    axes = Axes(
        x_range=x_range,
        y_range=y_range,
        x_length=width if width is not None else 6,
        y_length=height if height is not None else 6,
    ).add_coordinates()
    labels = axes.get_axis_labels(x_label=x_label, y_label=y_label)
    labels = axes.get_axis_labels(x_label=x_label, y_label=y_label)

    # ---- choose plotting mode ----
    if inverse_mode:
        if inverse_func is None:
            raise ValueError("inverse_mode=True requires inverse_func (mapping y -> x)")

        # default t_range from visible y-axis
        if t_range is None:
            t_range = y_range[0:2]
            # Apparently you can't control the step_size in t_range so never mind
            # step_size = (t_range[1] - t_range[0]) / n_points
            # t_range.append(step_size)

        def parametric(t):
            x = inverse_func(t)
            return axes.c2p(x, t)

        graph = ParametricFunction(
            parametric,
            t_range=t_range,
            color=color,
        )

    else:
        graph = axes.plot(
            func,
            x_range=domain,
            color=color,
        )

    return VGroup(axes, labels, graph)


class LinearLogisticScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService("/Users/noah/Convex/LikelihoodShape/linear_to_logistic.mp3",
                cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
                min_silence_len=2000,
                keep_silence=[0,0]))
        tex1 = MathTex(r"P(Y=1) = \beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")
        tex2 = MathTex(r"p = \beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")
        tex3 = MathTex(r"f(p) = \beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")
        tex4 = MathTex(r"p = f^{-1}(\beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1})")
        tex5 = MathTex(r"\ln\frac{p}{1-p} = \beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")

        with self.voiceover("a") as tracker:
            self.play(Write(tex1))
        with self.voiceover("a") as tracker:
            self.play(TransformByGlyphMap(tex1, tex2,
                                        ([0,1,2,3,4,5], [0])))
        
        # Graph the thing
        graph_group = create_graph((lambda x : 0.38 * (x  - 0.52)),
                                   x_range = [-5,5,1],
                                   y_range = [-3,3,1],
                                   x_label = "X",
                                   y_label = "p",
                                   color = GREEN)
        axes = graph_group[0]
        with self.voiceover("a") as tracker:
            self.play(FadeOut(tex2))
            self.add(graph_group[0],graph_group[1])
            self.play(Create(graph_group[2]))

        with self.voiceover("a") as tracker:
            hlines = {}
            areas = {}
            for y in 0,1:
                hlines[y] = axes.plot((lambda x : y), color = WHITE)
                # self.add(hlines[y])
                graph_group.add(hlines[y])
                areas[y] = axes.get_area(
                    hlines[y],
                    x_range=[-5, 5],
                    bounded_graph=axes.plot(lambda x: (y - 0.5) * 6),  # goes up to y=3 for 1 and down to -3 for 0
                    color=RED,
                    opacity=0.2
                )
                # self.add(areas[y])
                graph_group.add(areas[y])

        with self.voiceover("a") as tracker:
            self.play(FadeOut(graph_group))
            self.play(FadeIn(tex2))
        with self.voiceover("a") as tracker:
            self.play(TransformByGlyphMap(tex2, tex3,
                                        (FadeIn, [0,1,3])))
            
        with self.voiceover("a") as tracker:
            graph_group = create_graph(
                lambda p: np.log(p / (1 - p)),
                x_range=[0, 1.75, 1],
                y_range=[-6, 6, 2],
                x_label="p",
                y_label="f(p)",
                inverse_mode=True,
                inverse_func=lambda y: 1 / (1 + np.exp(-y)),  # sigmoid
                t_range=[-6, 6],
                width = 1,
                height = 5,
                color=GREEN,
            )
            graph_group.to_edge(RIGHT)
            self.add(graph_group[0],graph_group[1])
            self.play(Create(graph_group[2]))

        self.remove(graph_group[0], graph_group[1], graph_group[2])
        tex3_original = tex3.copy()
        with self.voiceover("a") as tracker:
            self.play(TransformByGlyphMap(tex3, tex4,
                                         ([0],[2], {"path_arc":-PI}),
                                        ([1],[5], {"path_arc":-PI}),
                                        ([3],[31],{"path_arc":-PI/6}),
                                        (FadeIn, [3,4])))
            graph_group = create_graph(
                lambda p: 1 / (1 + np.exp(-p)),
                x_range=[-6, 6, 2],
                y_range=[0, 1.75, 1],
                x_label=r"\beta^T X",
                y_label=r"f^-1(\beta^T X)",
                inverse_mode=False,
                width = 5,
                height = 1,
                color=GREEN,
            )
            graph_group.to_edge(UP)
            self.add(graph_group[0],graph_group[1])
            self.play(Create(graph_group[2]))
         
        with self.voiceover("a") as tracker:
            self.remove(graph_group[0], graph_group[1], graph_group[2])
            self.play(TransformByGlyphMap(tex4, tex3_original,
                ([2],[0], {"path_arc": PI}),
                ([5],[1], {"path_arc": PI}),
                ([31],[3], {"path_arc": PI/6}),
                ([3,4], FadeOut)
            ))
        
        with self.voiceover("a") as tracker:
            self.play(TransformByGlyphMap(tex3_original, tex5,
                                        (range(4), range(7))))