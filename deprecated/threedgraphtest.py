from manim import *
class YeetScene(ThreeDScene):
    def construct(self):
        formula = MathTex(r"p=\sigma(\beta_0+\beta_1 X_{1}+\beta_2 X_{2}+\ldots+\beta_{k-1} X_{k-1})").to_edge(DOWN)
        self.play(Write(formula))



        # --- Graph the likelihood ---
        self.move_camera(
            phi=60 * DEGREES,
            theta=-45 * DEGREES,
            run_time=1
        )

        # Function 
        def f(x, y):
            return np.exp(-0.5 * (x - 0.54)**2 - (y + 0.82)**2 - 0.2) # I just made this up because it's nice

        # Axes
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-3, 3],
        )

        x_label = MathTex(r"\hat{\beta}_0").next_to(axes.x_axis.get_end(), RIGHT, buff = 0.2)
        y_label = MathTex(r"\hat{\beta}_1").next_to(axes.y_axis.get_end(), UP, buff = 0.2)
        z_label = MathTex("L").next_to(axes.z_axis.get_end(), OUT, buff = 0.2)
        axis_labels = VGroup(x_label, y_label, z_label)
        self.add_fixed_orientation_mobjects(x_label, y_label, z_label)

        # Surface 
        surface = Surface(
            lambda u, v_: axes.c2p(u, v_, f(u, v_)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(12, 12), # TODO: Make this bigger again during production
            fill_opacity=0.35,
        )

        # point at the max
        max_coords = 0.54, -0.82, f(0.54, -0.82)
        max_point = Dot3D(axes.c2p(*max_coords))

        self.play(Create(axes), Create(surface), Write(axis_labels))
        self.play(FadeIn(max_point))



