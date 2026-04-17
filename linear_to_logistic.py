from manim import *
from MF_Tools import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
import numpy as np
import pandas as pd

df = pd.read_csv("breast_cancer_sklearn.csv")
X = np.array(df[df.columns[0]])
Y = np.array(df["target"])

def simple_linear_regression(X, Y):
    X = np.asarray(X)
    Y = np.asarray(Y)
    
    if X.shape != Y.shape:
        raise ValueError("X and Y must have the same shape")
    
    x_mean = X.mean()
    y_mean = Y.mean()
    
    # slope (beta_1)
    beta_1 = np.sum((X - x_mean) * (Y - y_mean)) / np.sum((X - x_mean)**2)
    
    # intercept (beta_0)
    beta_0 = y_mean - beta_1 * x_mean
    
    return beta_0, beta_1

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
        self.set_speech_service(StitcherService(r"/Users/noah/Convex/LikelihoodShape/podcasts/linear_to_logistic_podcast_992.mp3",
                cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
                min_silence_len=2000,
                keep_silence=(0,0)))
        
        with self.voiceover("It’s always a good idea to graph your data, so here I’ve just graphed Y versus X1.") as tracker:
            x_range = max(X) - min(X)
            axes = Axes(x_range = [min(X) - 0.1 * x_range, max(X) + 0.1 * x_range], y_range = [-0.2, 1.2])
            axis_labels = axes.get_axis_labels(x_label = "X1", y_label = "Y")
            dots = VGroup(*[Dot(axes.c2p(x, y), color = DARK_BLUE) for x, y in zip(X, Y)])
            
            self.play(DrawBorderThenFill(axes))
            self.play(Write(axis_labels))
            self.play(LaggedStart(*[Write(dot) for dot in dots], lag_ratio=0.005))

            # Regression coefficients
            beta0, beta1 = simple_linear_regression(X, Y)
            regression_line = axes.plot(lambda x : beta0 + beta1 * x,
                                        x_range = [(1.2 - beta0) / beta1, (-0.2 - beta0) / beta1],
                                        color = RED)
            self.play(Create(regression_line))
            scatterplot = VGroup(axes, axis_labels, dots, regression_line)
            self.play(FadeOut(scatterplot))

        tex0 = MathTex(r"P(Y=1) = \beta_0+\beta_1 X")
        tex1 = MathTex(r"p = \beta_0+\beta_1 X")
        tex2 = MathTex(r"p = \beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")
        tex3 = MathTex(r"f(p) = \beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")
        tex4 = MathTex(r"p = f^{-1}(\beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1})")
        tex5 = MathTex(r"\ln\frac{p}{1-p} = \beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")

        with self.voiceover("So for just 1 predictor variable, we’d just assume that P(Y=1),") as tracker:
            self.play(Write(tex0))

        with self.voiceover("notated p, is a linear function of X with an unknown intercept and slope. And with more predictors,") as tracker:
            self.play(TransformByGlyphMap(tex0, tex1,
                                          (range(6), [0])))
        with self.voiceover("we’d just have a separate slope for each predictor. These are the coefficients and they’re notated with B0 for the intercept and B1 and so on for the slopes.") as tracker:
            self.play(TransformByGlyphMap(tex1, tex2,
                                          (FadeIn, range(8,27))))
        
        with self.voiceover("The reason that’s bad is that for some values of X, you’ll get probabilities ") as tracker:
            self.play(FadeOut(tex2))
            self.play(FadeIn(scatterplot))

        with self.voiceover("greater than 1 or less than 0, which is impossible. So what we want instead is to assume that some") as tracker:
            self.play(FadeOut(dots))
            hlines = {}
            areas = {}
            for y in 0,1:
                hlines[y] = axes.plot((lambda x : y), color = WHITE)
                self.add(hlines[y])
                scatterplot.add(hlines[y])
                areas[y] = axes.get_area(
                    hlines[y],
                    x_range=[min(X) - 0.1 * x_range, max(X) + 0.1 * x_range],
                    bounded_graph=axes.plot(lambda x: (y - 0.5) * 6),  # goes up to y=3 for 1 and down to -3 for 0 TODO: Maybe make a smaller range
                    color=RED,
                    opacity=0.2
                )
                self.add(areas[y])
                scatterplot.add(areas[y])
            self.wait(tracker.duration - 3.1) # BRITTLE but what else should I do
            self.play(FadeOut(scatterplot))
            self.play(FadeIn(tex2))

        with self.voiceover("function of p is equal to that linear combination of the predictors. And we want this function to give values that range from") as tracker:
            self.play(TransformByGlyphMap(tex2, tex3,
                                        (FadeIn, [0,1,3])))
            
        with self.voiceover("-∞ to ∞ as p ranges from 0 to 1. Or, sort of the INVERSE way to put it is that") as tracker:
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
        with self.voiceover("p is equal to some function of the linear combination of the predictors, some function that maps") as tracker:
            self.play(TransformByGlyphMap(tex3, tex4,
                                         ([0],[2], {"path_arc":-PI}),
                                        ([1],[5], {"path_arc":-PI}),
                                        ([3],[31],{"path_arc":-PI/6}),
                                        (FadeIn, [3,4])))
        
        with self.voiceover("every number from -∞ to ∞ to a legal probability between 0 and 1.") as tracker:
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
         
        with self.voiceover("Either way, no matter what the predictors are, we never get an impossible probability. The function we use is the ") as tracker:
            self.remove(graph_group[0], graph_group[1], graph_group[2])
            self.play(TransformByGlyphMap(tex4, tex3_original,
                ([2],[0], {"path_arc": PI}),
                ([5],[1], {"path_arc": PI}),
                ([31],[3], {"path_arc": PI/6}),
                ([3,4], FadeOut)
            ))
        
        with self.voiceover("logit, ln p over 1-p. If we want to put p in terms of the predictors, we just do a little algebra. We") as tracker:
            self.play(TransformByGlyphMap(tex3_original, tex5,
                                        (range(4), range(7))))
            
        sigmoid1 = MathTex(r"\frac{p}{1-p}=e^{\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1}}")
        sigmoid2 = MathTex(r"\frac{1-p}{p}=e^{-(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}")
        sigmoid3 = MathTex(r"\frac{1}{p}-\frac{p}{p}=e^{-(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}")
        sigmoid4 = MathTex(r"\frac{1}{p}-1=e^{-(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}")
        sigmoid5 = MathTex(r"\frac{1}{p}=1+e^{-(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}")
        sigmoid6 = MathTex(r"p=\frac{1}{1+e^{-(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}}")
        sigmoid7 = MathTex(r"p=\sigma(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}")


        with self.voiceover("exponentiate both sides") as tracker:
            # This would have been a simple TransformByGlyphMap(tex5, sigmoid1)
            # But that was warping/twisting some glyphs.
            # So we have a rigid transformation of the glyphs we don't want to twist, which is more annoying
            # x_src_idx = [13,18,29]
            # x_dst_idx = [12,17,28]
            x_src_idx = range(8,33)
            x_dst_idx = range(7,32)
            x_src = VGroup(*[tex5[0][i] for i in x_src_idx])
            x_dst = VGroup(*[sigmoid1[0][i] for i in x_dst_idx])
            rest_src = VGroup(*[
                m for i, m in enumerate(tex5)
                if i not in x_src
            ])
            rest_dst = VGroup(*[
                m for i, m in enumerate(sigmoid1)
                if i not in x_dst
            ])
            self.play(
                TransformByGlyphMap(
                    rest_src,
                    rest_dst,
                    ([0,1],[6], {"path_arc": -PI * 0.6}),
                ),
                *[
                    x_src[i].animate.move_to(x_dst[i])
                    for i in range(len(x_src))
                ]
            )

        with self.voiceover("Take the reciprocal, on the right hand side this negates the exponent,") as tracker:
            self.play(TransformByGlyphMap(sigmoid1, sigmoid2,
                                ([0],[4], {"path_arc": PI * 0.5}),
                                ([2,3,4],[0,1,2], {"path_arc": PI * 0.5}),
                                (FadeIn, [7,8]),
                                (FadeIn,[34])
                                ))
        
        with self.voiceover("Expand the fraction,") as tracker:
            self.play(TransformByGlyphMap(sigmoid2, sigmoid3,
                                        ([0,3,4],[0,1,2]),
                                        ([2,3,4],[4,5,6]),
                                        ([1],[3])
                                        ))

        with self.voiceover("P over p becomes 1,") as tracker:
            self.play(TransformByGlyphMap(sigmoid3, sigmoid4,
                                        ([4,5,6],[4])))
        

        with self.voiceover("Add one to both sides,") as tracker:
            self.play(TransformByGlyphMap(sigmoid4, sigmoid5,
                                            ([3],[5], {"path_arc": -PI}),
                                            ([5],[3], {"path_arc":-PI})))

        with self.voiceover("Take the reciprocal again, and If you’re familiar with machine learning, you may recognize a sigmoid here.") as tracker:
            self.play(TransformByGlyphMap(sigmoid5, sigmoid6,
                                            ([0,1], [2,3])))
            
        # Interlude, Part 1: Sigmoid definitions
        sigmoid_defn  = MathTex(r"\sigma(z)=\frac{1}{1+e^{-z}}").to_corner(UL)
        sigmoid_defn2 = MathTex(r"\sigma(z)=\frac{(1)e^z}{(1+e^{-z})e^z}").to_corner(UL)
        sigmoid_defn3 = MathTex(r"\sigma(z)=\frac{e^z}{e^z+e^ze^{-z}}").to_corner(UL)
        sigmoid_defn4 = MathTex(r"\sigma(z)=\frac{e^z}{e^z+1}").to_corner(UL)

        # Interlude, Part 2: Graph
        axes = Axes(x_range = [-5,5,1], 
                    y_range = [-0,1,0.2],
                    ).add_coordinates()
        axis_labels = axes.get_axis_labels(x_label = "z",
                                           y_label = r"\sigma(z)")
        func = axes.plot(sigmoid, 
                         color = GREEN)
        graph_group = VGroup(axes, axis_labels, func)

        # Interlude, Part 3: The animation
        self.remove(sigmoid6)
        with self.voiceover("The sigmoid, denoted sigma of z, is 1 over 1 + e to the negative z.") as tracker:
            self.play(Write(sigmoid_defn))
        with self.voiceover("It has this S shape. ") as tracker:
            self.play(DrawBorderThenFill(axes), Write(axis_labels), run_time = 0.5)
            self.play(Create(func))

        with self.voiceover("If you multiply the top and bottom of the fraction by e to the z, ") as tracker:
            self.play(TransformByGlyphMap(sigmoid_defn, sigmoid_defn2,
                                        (FadeIn, [5,7,8,9]),
                                        (FadeIn, [11,17,18,19])))
        with self.voiceover("and distribute, ") as tracker:
            self.play(TransformByGlyphMap(sigmoid_defn2, sigmoid_defn3,
                                        ([5,6,7], FadeOut, {"run_time": 0.25}),
                                        ([11,17],FadeOut),
                                        ([14,15,16], [13,14,15]),
                                        ([18, 19], [11,12], {"path_arc": PI}),
                                        ([12], [8,9]),
                                        ([18,19], [8,9], {"path_arc": PI})))
        with self.voiceover("and simplify, then you get this alternate formula, e to the z over e to the z + 1.") as tracker:
            self.play(TransformByGlyphMap(sigmoid_defn3, sigmoid_defn4,
                                        ([11,12,13,14,15], [11], {"run_time": 0.75})))
        
        with self.voiceover("So going back to our original equation, this formula just becomes") as tracker:
            self.play(FadeOut(axes), FadeOut(axis_labels), FadeOut(func), FadeOut(sigmoid_defn4))
            self.play(FadeIn(sigmoid6))
        
        with self.voiceover("p = sigmoid of the linear combination.") as tracker:
            self.play(TransformByGlyphMap(sigmoid6, sigmoid7,
                                        ([2,3], FadeOut),
                                        (range(4,8), [2])))