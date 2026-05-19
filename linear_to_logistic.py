from manim import *
from MF_Tools import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
import numpy as np
import pandas as pd
from N_Tools import simple_linear_regression, create_graph, TransformWithBoxes
from hat_matrix_logo import HMDialogBox
from tex_colors import *

df = pd.read_csv("breast_cancer_sklearn.csv")
X1 = np.array(df[df.columns[0]])
X2 = np.array(df[df.columns[1]])
X3 = np.array(df[df.columns[2]])
Y = np.array(df["target"])
# Here we don't need to use data.py because we don't care about order, and we want different Xs

class LinearLogisticScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService(r"/Users/noah/Convex/LikelihoodShape/podcasts/linear_to_logistic_podcast_1001.wav",
                cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
                min_silence_len=2000,
                keep_silence=(0,0)))
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        x1_norm = (X1 - X1.min()) / (X1.max() - X1.min())
        x2_norm = (X2 - X2.min()) / (X2.max() - X2.min())
        x3_norm = (X3 - X3.min()) / (X3.max() - X3.min())

        def make_3d_panel(ax, dots, x_lbl, y_lbl, z_lbl):
            # Rotate only axes + dots; labels are placed fresh after rotation so they stay upright.
            # add_fixed_orientation_mobjects can't fix this because the tilt is from VGroup rotation,
            # not camera rotation — labels must be created after the transform to stay readable.
            panel = VGroup(ax, dots)
            panel.rotate(-PI / 4, axis=Z_AXIS)
            panel.rotate(-PI / 3, axis=X_AXIS)
            # After rotation, ax.c2p() returns world coords in the rotated space.
            # x-axis tip goes lower-right, y-axis tip upper-right, z-axis tip upward.
            lx = ColoredMathTex(x_lbl).scale(1.5).next_to(ax.c2p(1, 0, 0), RIGHT + DOWN * 0.3, buff=0.05)
            ly = ColoredMathTex(y_lbl).scale(1.5).next_to(ax.c2p(0, 1, 0), UR, buff=0.05)
            lz = ColoredMathTex(z_lbl).scale(1.5).next_to(ax.c2p(0, 0, 1), UP, buff=0.05)
            return VGroup(panel, lx, ly, lz)
        
        # Panel A: Y vs X1, 2D (top-left)
        pA_ax = Axes(x_range=[0, 1, 0.5], y_range=[-0.2, 1.2, 0.5], x_length=5, y_length=3)
        pA_labels = pA_ax.get_axis_labels(x_label=r"X_1", y_label=r"Y")
        pA_dots = VGroup(*[Dot(pA_ax.c2p(x, y), color=DARK_BLUE, radius=0.05) for x, y in zip(x1_norm, Y)])
        panelA = VGroup(pA_ax, pA_labels, pA_dots)

        # Panel B: Y vs X1 and X2, 3D (top-right)
        pB_ax = ThreeDAxes(x_range=[0,1,0.5], y_range=[0,1,0.5], z_range=[-0.2,1.2,0.5], x_length=4, y_length=4, z_length=3)
        pB_dots = VGroup(*[
            Sphere(radius=0.05, resolution=(4, 4)).move_to(pB_ax.c2p(x1, x2, y)).set_color(DARK_BLUE)
            for x1, x2, y in zip(x1_norm, x2_norm, Y)
        ])
        panelB = make_3d_panel(pB_ax, pB_dots, r"X_1", r"X_2", r"Y").scale(0.5).move_to([3.5, 2.0, 0])

        # Legend for panels C and D (blue = Y=1, red = Y=0)
        legend = VGroup(
            VGroup(Dot(color=BLUE, radius=0.12), ColoredMathTex(r"Y=1").scale(0.9), Tex("Benign").scale(0.9)).arrange(RIGHT, buff=0.15),
            VGroup(Dot(color=RED,  radius=0.12), ColoredMathTex(r"Y=0").scale(0.9), Tex("Malignant").scale(0.9)).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([0, -3.5, 0])

        # Panel C: X1 vs X2 colored by Y, 2D (bottom-left)
        pC_ax = Axes(x_range=[0, 1, 0.5], y_range=[0, 1, 0.5], x_length=5, y_length=3)
        pC_labels = pC_ax.get_axis_labels(x_label=r"X_1", y_label=r"X_2")
        pC_dots = VGroup(*[
            Dot(pC_ax.c2p(x1, x2), color=BLUE if y == 1 else RED, radius=0.05)
            for x1, x2, y in zip(x1_norm, x2_norm, Y)
        ])
        panelC = VGroup(pC_ax, pC_labels, pC_dots).scale(0.6).move_to([-3.5, -2.0, 0])

        # Panel D: X1, X2, X3 colored by Y, 3D (bottom-right)
        pD_ax = ThreeDAxes(x_range=[0,1,0.5], y_range=[0,1,0.5], z_range=[0,1,0.5], x_length=4, y_length=4, z_length=4)
        pD_dots = VGroup(*[
            Sphere(radius=0.05, resolution=(4, 4)).move_to(pD_ax.c2p(x1, x2, x3)).set_color(BLUE if y == 1 else RED)
            for x1, x2, x3, y in zip(x1_norm, x2_norm, x3_norm, Y)
        ])
        panelD = make_3d_panel(pD_ax, pD_dots, r"X_1", r"X_2", r"X_3").scale(0.5).move_to([3.5, -2.0, 0])

        with self.voiceover("It’s always a good idea to graph your data, so here's a graph of Y versus X1.") as tracker:
            self.play(FadeIn(panelA))
            self.wait(tracker.duration - 2.1)
            self.play(panelA.animate.scale(0.6).move_to([-3.5, 2.0, 0]))
        with self.voiceover("And here's a 3D graph of Y vs X1 and X2") as tracker:
            self.play(FadeIn(panelB))
        with self.voiceover("And here's a graph of Y vs X1 and X2, with color representing Y") as tracker:
            self.play(FadeIn(panelC), FadeIn(legend))
        with self.voiceover("And here's a graph of Y vs X1, X2, and X3, with color representing Y. Now we need to make some kind of model, which will make some kind of assumption") as tracker:
            self.play(FadeIn(panelD))
        with self.voiceover(" about the distribution of Y. ") as tracker:
            lda_note = HMDialogBox(
                "Some models, like LDA, also make assumptions about the distribution of X.",
                text_width=5,
            )#.to_edge(DOWN, buff=0.3)
            self.play(FadeIn(lda_note))
            self.wait(max(0, tracker.duration - 1.5))
            self.play(FadeOut(lda_note))

        with self.voiceover("I could just state ") as tracker:
            ...

        with self.voiceover("the assumptions of logistic regression right here, but I think it's more helpful to try to derive it somewhat from scratch, so here goes.") as tracker:
            assumptions = ColoredMathTex(r"\ln\dfrac{p}{1-p} = \beta_0 + \beta_1 X_1 + \cdots + \beta_{k-1} X_{k-1}")
            self.play(FadeIn(assumptions))
            self.wait(max(0, tracker.duration - 2.1))
            self.play(FadeOut(assumptions), FadeOut(panelC), FadeOut(panelD), FadeOut(legend))

        tex0 = ColoredMathTex(r"P(Y=1) = \beta_0+\beta_1 X")
        tex1 = ColoredMathTex(r"p = \beta_0+\beta_1 X")
        tex_2pred = ColoredMathTex(r"p = \beta_0+\beta_1 X_1+\beta_2 X_2")
        tex2 = ColoredMathTex(r"p = \beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")
        tex3 = ColoredMathTex(r"f(p) = \beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")
        tex4 = ColoredMathTex(r"p = f^{-1}(\beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1})")
        tex5 = ColoredMathTex(r"\ln\frac{p}{1-p} = \beta_0+\beta_1 X_1+\beta_2 X_2+\ldots+\beta_{k-1} X_{k-1}")


        with self.voiceover("One model we could use is linear regression. So for 1 predictor variable, we’d assume that the probability that y is 1,") as tracker:
            beta0, beta1 = simple_linear_regression(X1, Y)
            # Regression line on panelA (x1_norm ∈ [0,1] scale)
            beta0_norm = beta0 + beta1 * X1.min()
            beta1_norm = beta1 * (X1.max() - X1.min())
            reg_line_A = pA_ax.plot(lambda x: beta0_norm + beta1_norm * x, x_range=[0, 1], color=RED)
            # Regression plane on panelB (multiple linear regression Y ~ X1_norm + X2_norm)
            A_mat = np.column_stack([np.ones(len(x1_norm)), x1_norm, x2_norm])
            b0_p, b1_p, b2_p = np.linalg.lstsq(A_mat, Y, rcond=None)[0]
            reg_plane_B = Surface(
                lambda u, v: pB_ax.c2p(u, v, b0_p + b1_p * u + b2_p * v),
                u_range=[0, 1], v_range=[0, 1],
                resolution=(8, 8),
                fill_color=RED, fill_opacity=0.5, stroke_width=0,
            )
            self.play(Create(reg_line_A), FadeIn(reg_plane_B))
            self.play(Write(tex0))

        with self.voiceover("notated p, is ") as tracker:
            self.play(TransformByGlyphMap(tex0, tex1,
                                          (range(6), [0])))
        
        with self.voiceover("a linear function of X with an unknown intercept and slope.") as tracker:
            # Intercept: vertical segment from x-axis up to y-intercept (β₀ = height)
            intercept_line = Line(
                pA_ax.c2p(0, 0), pA_ax.c2p(0, beta0_norm),
                color=YELLOW, stroke_width=4,
            )
            # Slope: Δx and Δy lines forming a right triangle on the regression line
            _xlo, _xhi = 0.35, 0.65
            _ylo = beta0_norm + beta1_norm * _xlo
            _yhi = beta0_norm + beta1_norm * _xhi
            dx_line = Line(pA_ax.c2p(_xlo, _ylo), pA_ax.c2p(_xhi, _ylo), color=GREEN, stroke_width=3)
            dy_line = Line(pA_ax.c2p(_xhi, _ylo), pA_ax.c2p(_xhi, _yhi), color=GREEN, stroke_width=3)
            slope_vis = VGroup(dx_line, dy_line)
            self.play(FadeIn(intercept_line), FadeIn(slope_vis))
            b0_highlight = VGroup(tex1[0][2], tex1[0][3]).copy()
            b1_highlight = VGroup(tex1[0][5], tex1[0][6]).copy()
            self.play(
                TransformFromCopy(intercept_line, b0_highlight),
                TransformFromCopy(slope_vis, b1_highlight),
            )
            self.wait(0.5)
            self.play(
                FadeOut(b0_highlight), FadeOut(b1_highlight),
                FadeOut(intercept_line), FadeOut(slope_vis),
            )

        with self.voiceover("With 2 predictors, we'd have an intercept and 2 slopes. With even more predictors,"):
            self.play(TransformByGlyphMap(tex1, tex_2pred, (FadeIn, range(8, 14))))

            # 3D intercept/slope visualization on panelB
            intercept_line_3d = Line(
                pB_ax.c2p(0, 0, 0), pB_ax.c2p(0, 0, b0_p),
                color=YELLOW, stroke_width=4,
            )
            # β₁: Δx₁ and Δz₁ right triangle along X₁ axis of the regression plane
            dx1_line = Line(pB_ax.c2p(0, 0, b0_p), pB_ax.c2p(0.5, 0, b0_p), color=GREEN, stroke_width=3)
            dz1_line = Line(pB_ax.c2p(0.5, 0, b0_p), pB_ax.c2p(0.5, 0, b0_p + b1_p * 0.5), color=GREEN, stroke_width=3)
            slope_vis_1 = VGroup(dx1_line, dz1_line)
            # β₂: Δx₂ and Δz₂ right triangle along X₂ axis of the regression plane
            dx2_line = Line(pB_ax.c2p(0, 0, b0_p), pB_ax.c2p(0, 0.5, b0_p), color=BLUE, stroke_width=3)
            dz2_line = Line(pB_ax.c2p(0, 0.5, b0_p), pB_ax.c2p(0, 0.5, b0_p + b2_p * 0.5), color=BLUE, stroke_width=3)
            slope_vis_2 = VGroup(dx2_line, dz2_line)
            self.play(FadeIn(intercept_line_3d), FadeIn(slope_vis_1), FadeIn(slope_vis_2))
            b0_highlight_3d = VGroup(tex_2pred[0][2], tex_2pred[0][3]).copy()
            b1_highlight_3d = VGroup(tex_2pred[0][5], tex_2pred[0][6]).copy()
            b2_highlight_3d = VGroup(tex_2pred[0][10], tex_2pred[0][11]).copy()
            self.play(
                TransformFromCopy(intercept_line_3d, b0_highlight_3d),
                TransformFromCopy(slope_vis_1, b1_highlight_3d),
                TransformFromCopy(slope_vis_2, b2_highlight_3d),
            )
            self.wait(0.5)
            self.play(
                FadeOut(b0_highlight_3d), FadeOut(b1_highlight_3d), FadeOut(b2_highlight_3d),
                FadeOut(intercept_line_3d), FadeOut(slope_vis_1), FadeOut(slope_vis_2),
            )

        with self.voiceover("we’d have 1 slope for each predictor. These are called the coefficients and they’re notated with beta 0 for the intercept and beta 1 and so on for the slopes.") as tracker:
            self.play(TransformByGlyphMap(tex_2pred, tex2,
                                          (FadeIn, range(14, 27))))
        
        with self.voiceover("However, this is not a good model. For some values of X, you’ll get probabilities ") as tracker:
            self.play(FadeOut(tex2))

        with self.voiceover("greater than 1 or less than 0, which is impossible. So what we want instead is to assume that some") as tracker:
            pA_hlines = {}
            pA_areas = {}
            for y_val in 0, 1:
                pA_hlines[y_val] = pA_ax.plot(lambda x, y=y_val: y, color=WHITE)
                self.add(pA_hlines[y_val])
                pA_areas[y_val] = pA_ax.get_area(
                    pA_hlines[y_val],
                    x_range=[0, 1],
                    bounded_graph=pA_ax.plot(lambda x, y=y_val: (y - 0.5) * 6),
                    color=RED,
                    opacity=0.2
                )
            # panelB: red planes at z=1 (above valid range) and z=0 (below valid range)
            pB_plane_top = Surface(
                lambda u, v: pB_ax.c2p(u, v, 1.2),
                u_range=[0, 1], v_range=[0, 1], resolution=(2, 2),
                fill_color=RED, fill_opacity=0.25, stroke_width=0,
            )
            pB_plane_bot = Surface(
                lambda u, v: pB_ax.c2p(u, v, -0.2),
                u_range=[0, 1], v_range=[0, 1], resolution=(2, 2),
                fill_color=RED, fill_opacity=0.25, stroke_width=0,
            )
            self.play(
                FadeIn(pA_areas[0]), FadeIn(pA_areas[1]),
                FadeIn(pB_plane_top), FadeIn(pB_plane_bot),
            )
            self.wait(tracker.duration - 2.1)
            # panelA.remove(pA_dots)
            # panelB.remove(pB_dots)
            self.play(
                # FadeOut(pA_dots), FadeOut(pB_dots),
                # FadeOut(panelA), FadeOut(panelB),
                FadeOut(reg_line_A), FadeOut(reg_plane_B),
                FadeOut(pA_hlines[0]), FadeOut(pA_hlines[1]),
                FadeOut(pA_areas[0]), FadeOut(pA_areas[1]),
                FadeOut(pB_plane_top), FadeOut(pB_plane_bot),
                FadeIn(tex2)
            )

        with self.voiceover("function of p is equal to that linear combination of the predictors. And we want this function to range from") as tracker:
            self.play(TransformByGlyphMap(tex2, tex3,
                                        (FadeIn, [0,1,3])))
            
        with self.voiceover("negative infinity to infinity as p ranges from 0 to 1. Or, sort of the INVERSE way to put it is that") as tracker:
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
        
        with self.voiceover("every real number to a legal probability between 0 and 1.") as tracker:
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
            graph_group.to_edge(DOWN)
            self.add(graph_group[0],graph_group[1])
            self.play(Create(graph_group[2]))
         
        with self.voiceover("Either way, no matter what the predictors are, we never get an impossible probability. We use the") as tracker:
            self.remove(graph_group[0], graph_group[1], graph_group[2])
            self.play(TransformByGlyphMap(tex4, tex3_original,
                ([2],[0], {"path_arc": PI}),
                ([5],[1], {"path_arc": PI}),
                ([31],[3], {"path_arc": PI/6}),
                ([3,4], FadeOut)
            ))
        
        with self.voiceover("logit function, ln p over 1 minus p. To isolate p, we do some algebra. We") as tracker:
            self.play(TransformByGlyphMap(tex3_original, tex5,
                                        (range(4), range(7))))
            
        sigmoid1 = ColoredMathTex(r"\frac{p}{1-p}=e^{\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1}}")
        sigmoid1a= ColoredMathTex(r"\frac{1-p}{p}=\frac{1}{e^{\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1}}}")
        sigmoid2 = ColoredMathTex(r"\frac{1-p}{p}=e^{-(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}")
        sigmoid3 = ColoredMathTex(r"\frac{1}{p}-\frac{p}{p}=e^{-(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}")
        sigmoid4 = ColoredMathTex(r"\frac{1}{p}-1=e^{-(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}")
        sigmoid5 = ColoredMathTex(r"\frac{1}{p}=1+e^{-(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}")
        sigmoid6 = ColoredMathTex(r"p=\frac{1}{1+e^{-(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}}")
        sigmoid7 = ColoredMathTex(r"p=\sigma(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})}")


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

        with self.voiceover("Take the reciprocal, and on the right hand side") as tracker:
            self.play(TransformByGlyphMap(sigmoid1, sigmoid1a,
                                ([0],[4], {"path_arc": PI * 0.5}),
                                ([2,3,4],[0,1,2], {"path_arc": PI * 0.5}),
                                (FadeIn, [6,7])
                                ))
            
        with self.voiceover("this negates the exponent,") as tracker:
            self.play(TransformByGlyphMap(sigmoid1a, sigmoid2,
                                          ([6,7], FadeOut),
                                          (FadeIn, [7,8]),
                                          (FadeIn, [34]),
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

        with self.voiceover("Take the reciprocal again, and you may recognize a sigmoid here.") as tracker:
            self.play(TransformByGlyphMap(sigmoid5, sigmoid6,
                                            ([0,1], [2,3])))
            self.wait(tracker.duration - 2.1)
            self.play(FadeOut(panelA), FadeOut(panelB))
            
        # Interlude, Part 1: Sigmoid definitions
        sigmoid_defn  = ColoredMathTex(r"\sigma(z)=\frac{1}{1+e^{-z}}").to_corner(UL)
        sigmoid_defn2 = ColoredMathTex(r"\sigma(z)=\frac{(1)e^{z}}{(1+e^{-z})e^{z}}").to_corner(UL)
        sigmoid_defn3 = ColoredMathTex(r"\sigma(z)=\frac{e^{z}}{e^{z}+e^{z}e^{-z}}").to_corner(UL)
        sigmoid_defn4 = ColoredMathTex(r"\sigma(z)=\frac{e^{z}}{e^{z}+1}").to_corner(UL)

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

        z_tracker = ValueTracker(-5)

        sliding_dot = always_redraw(lambda: Dot(
            axes.c2p(z_tracker.get_value(), sigmoid(z_tracker.get_value())),
            # color=YELLOW,
            radius=0.1,
        ))
        v_line = always_redraw(lambda: DashedLine(
            axes.c2p(z_tracker.get_value(), 0),
            axes.c2p(z_tracker.get_value(), sigmoid(z_tracker.get_value())),
            # color=YELLOW,
            stroke_width=2,
        ))
        h_line = always_redraw(lambda: DashedLine(
            axes.c2p(0, sigmoid(z_tracker.get_value())),
            axes.c2p(z_tracker.get_value(), sigmoid(z_tracker.get_value())),
            # color=YELLOW,
            stroke_width=2,
        ))

        # Compute fixed layout positions for all 4 formulas in a row at UL
        _layout = VGroup(
            ColoredMathTex(r"\sigma(z)=\frac{1}{1+e^{-(-5.0)}}"),
            ColoredMathTex(r"=\frac{1}{1+148.41}"),
            ColoredMathTex(r"=\frac{1}{149.41}"),
            ColoredMathTex(r"=0.0067"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_corner(UL)
        f_centers = [m.get_center().copy() for m in _layout]

        # Static versions for the TransformFromCopy introduction (at z = -5)
        f1_static = ColoredMathTex(r"\sigma(z)=\frac{1}{1+e^{-(-5.0)}}").move_to(f_centers[0])
        f2_static = ColoredMathTex(r"=\frac{1}{1+" + f"{np.exp(5):.2f}" + r"}").move_to(f_centers[1])
        f3_static = ColoredMathTex(r"=\frac{1}{" + f"{1+np.exp(5):.2f}" + r"}").move_to(f_centers[2])
        f4_static = ColoredMathTex(f"={sigmoid(-5):.4f}").move_to(f_centers[3])

        # Dynamic always_redraw versions (active during z animation)
        def _exp_str(z):
            return f"-({z:.1f})" if z < 0 else f"{-z:.1f}"

        formula = always_redraw(lambda: ColoredMathTex(
            r"\sigma(z)=\frac{1}{1+e^{" + _exp_str(z_tracker.get_value()) + r"}}",
            # color=YELLOW,
        ).move_to(f_centers[0]))
        f2_dyn = always_redraw(lambda: ColoredMathTex(
            r"=\frac{1}{1+" + f"{np.exp(-z_tracker.get_value()):.2f}" + r"}",
            # color=YELLOW,
        ).move_to(f_centers[1]))
        f3_dyn = always_redraw(lambda: ColoredMathTex(
            r"=\frac{1}{" + f"{1+np.exp(-z_tracker.get_value()):.2f}" + r"}",
            # color=YELLOW,
        ).move_to(f_centers[2]))
        f4_dyn = always_redraw(lambda: ColoredMathTex(
            f"={sigmoid(z_tracker.get_value()):.4f}",
            # color=YELLOW,
        ).move_to(f_centers[3]))

        with self.voiceover("To see why, if you plug in ") as tracker:
            self.play(FadeIn(sliding_dot), FadeIn(v_line), FadeIn(h_line))
        with self.voiceover("a small value of z, ") as tracker:
            self.play(TransformWithBoxes(sigmoid_defn, f1_static, ([11], [11,12,13,14,15,16])))
        with self.voiceover("the denominator becomes very large,") as tracker:
            self.play(TransformFromCopy(f1_static, f2_static))
            self.play(TransformFromCopy(f2_static, f3_static))
        with self.voiceover("and your function approaches 0 very fast.") as tracker:
            self.play(TransformFromCopy(f3_static, f4_static))
            self.remove(f1_static, f2_static, f3_static, f4_static)
            self.add(formula, f2_dyn, f3_dyn, f4_dyn)

        with self.voiceover("If z is large, then the exponential term becomes") as tracker:
            self.play(z_tracker.animate.set_value(5), run_time=tracker.duration, rate_func=linear)
        with self.voiceover("near zero, and the fraction") as tracker:
            near_zero_rect = SurroundingRectangle(f2_dyn[0][-4:], color = RED)
            if tracker.duration > 2:
                self.play(Create(near_zero_rect))
                self.wait(tracker.duration - 2)
                self.play(FadeOut(near_zero_rect))
            else:
                self.play(Create(near_zero_rect, run_time = tracker.duration / 2))
                self.play(FadeOut(near_zero_rect, run_time = tracker.duration / 2))
        with self.voiceover("evaluates to almost 1.") as tracker:
            almost_1_rect = SurroundingRectangle(f4_dyn, color = RED)
            if tracker.duration > 2:
                self.play(Create(almost_1_rect))
                self.wait(tracker.duration - 2)
                self.play(FadeOut(almost_1_rect))
            else:
                self.play(Create(almost_1_rect, run_time = tracker.duration / 2))
                self.play(FadeOut(almost_1_rect, run_time = tracker.duration / 2))

        with self.voiceover("If you multiply the top and bottom of the fraction by") as tracker:
            self.play(FadeOut(sliding_dot), FadeOut(v_line), FadeOut(h_line),
                      FadeOut(f2_dyn), FadeOut(f3_dyn), FadeOut(f4_dyn),
                      TransformMatchingTex(formula, sigmoid_defn))

        with self.voiceover("e to the z, ") as tracker:
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
        
        # End of interlude, back to the original equation
        with self.voiceover("So going back to our original equation, this formula just becomes") as tracker:
            self.play(FadeOut(axes), FadeOut(axis_labels), FadeOut(func), FadeOut(sigmoid_defn4), FadeIn(panelA, panelB))
            self.play(FadeIn(sigmoid6))
        
        with self.voiceover("p = sigmoid of the linear combination.") as tracker:
            self.play(TransformByGlyphMap(sigmoid6, sigmoid7,
                                        ([2,3], FadeOut),
                                        (range(4,8), [2])))