import math
from manim import *
from MF_Tools import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.stitcher import _StitcherService as StitcherService

def create_graph(func, 
                 x_range= None, 
                 y_range = None,
                 x_label = "x",
                 y_label = "y",
                 domain = None,
                 color = RED):
    
    # Step 0: Fill in ranges if they are not provided
    x_range = x_range or [-5,5,1]
    y_range = y_range or [-5,5,1]

    # Step 1: Determine tick mark length if it's not input already
    if len(x_range) == 2:
        x_range.append((x_range[1] - x_range[0]) * 0.1)
    assert len(x_range) == 3, "x_range must have length 2 or 3"
    if len(y_range) == 2:
        y_range.append((y_range[1] - y_range[0]) * 0.1)
    assert len(y_range) == 3, "y_range must have length 2 or 3"

    domain = domain or x_range[0:2]

    # Step 2: Create the axes
    axes = Axes(x_range = x_range, 
                    y_range = y_range,
                    ).add_coordinates()
    
    # Step 3: Make the axis labels
    axis_labels = axes.get_axis_labels(x_label = x_label,
                                        y_label = y_label)
    
    # Step 4: Add the function
    func = axes.plot(func, color = color, x_range = domain)

    # Step 5: Put it all together and return
    return VGroup(axes, axis_labels, func)


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
            self.play(FadeIn(graph_group))

        with self.voiceover("a") as tracker:
            hlines = {}
            areas = {}
            for y in 0,1:
                hlines[y] = axes.plot((lambda x : y), color = WHITE)
                self.add(hlines[y])
                graph_group.add(hlines[y])
                areas[y] = axes.get_area(
                    hlines[y],
                    x_range=[-5, 5],
                    bounded_graph=axes.plot(lambda x: (y - 0.5) * 6),  # goes up to y=3 for 1 and down to -3 for 0
                    color=RED,
                    opacity=0.2
                )
                self.add(areas[y])
                graph_group.add(areas[y])

        with self.voiceover("a") as tracker:
            self.play(FadeOut(graph_group))
            self.play(FadeIn(tex2))
        with self.voiceover("a") as tracker:
            self.play(TransformByGlyphMap(tex2, tex3,
                                        (FadeIn, [0,1,3])))
            graph_group = create_graph(lambda p : math.log(p / (1 - p)),
                                       x_range = [-1,2,3],
                                       x_label = "p",
                                       y_label = "f(p)",
                                       domain = [1e-6,1 - 1e-6],
                                       color = GREEN )
            self.play(FadeIn(graph_group))
            self.play(FadeOut(graph_group))
        tex3_original = tex3.copy()
        with self.voiceover("a") as tracker:
            self.play(TransformByGlyphMap(tex3, tex4,
                                         ([0],[2], {"path_arc":-PI}),
                                        ([1],[5], {"path_arc":-PI}),
                                        ([3],[31],{"path_arc":-PI/6}),
                                        (FadeIn, [3,4])))
            #Invert that transform because we want tex3
         
        with self.voiceover("a") as tracker:
            self.play(TransformByGlyphMap(tex4, tex3_original,
                ([2],[0], {"path_arc": PI}),
                ([5],[1], {"path_arc": PI}),
                ([31],[3], {"path_arc": PI/6}),
                ([3,4], FadeOut)
            ))
            self.play(TransformByGlyphMap(tex3_original, tex5,
                                        (range(4), range(7))))