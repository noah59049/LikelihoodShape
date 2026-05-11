from manim import *

class HatMatrixScene(Scene):
    def construct(self):
        brackets = MathTex(
            r"\begin{bmatrix}"
            r"\quad & \quad \\"
            r"\quad & \quad"
            r"\end{bmatrix}", 
            font_size = 40
        ).set_stroke(color = WHITE, width = 4, background=False)
        self.add(brackets)

        triangle = Triangle(color = PURPLE, 
                            fill_color = PURPLE, 
                            fill_opacity = 1,
                            )
        triangle.next_to(brackets, UP)
        triangle.stretch_to_fit_height(2)
        triangle.scale(0.9)
        triangle.shift(UP * 0.4)
        self.add(triangle)

        print(brackets.get_right())
        print(brackets.get_center())

        arc1 = Arc(start_angle = 3 * PI / 2, angle = PI / 2, radius = 1).move_to(brackets.get_right())
        arc1.shift(arc1.width / 2 * RIGHT + arc1.height / 2 * UP)
        self.add(arc1)