import math
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

        # Main triangle of the hat
        triangle = Triangle(color = PURPLE, 
                            fill_color = PURPLE, 
                            fill_opacity = 1,
                            )
        triangle.next_to(brackets, UP)
        triangle.stretch_to_fit_height(2)
        triangle.scale(0.9)
        triangle.shift(UP * 0.4)
        self.add(triangle)

        # Lower triangle with the brim of the hat
        triangle2 = triangle.copy()
        triangle2.stretch_to_fit_height(0.5)
        triangle2.stretch_to_fit_width(2.5)
        triangle2.move_to(triangle, aligned_edge=DOWN)
        self.add(triangle2)

        def get_hand(start_point, length = 0.13, theta = math.pi / 6):
            line1 = Line(start = start_point, end = start_point + math.cos(theta) * length * UP + math.sin(theta) * length * RIGHT)
            line2 = Line(start = start_point, end = start_point + length * UP)
            line3 = Line(start = start_point, end = start_point + math.cos(theta) * length * UP + math.sin(theta) * length * LEFT)
            return VGroup(line1, line2, line3)

        # Right arm
        arc1 = Arc(start_angle = 3 * PI / 2, angle = PI / 2, radius = 0.3).move_to(brackets.get_right())
        arc1.shift(arc1.width / 2 * RIGHT + arc1.height / 2 * UP)
        self.add(arc1)

        hand1 = get_hand(start_point = arc1.get_corner(UR))
        self.add(hand1)

        # Left arm
        arc2 = Arc(start_angle = PI, angle = PI / 2, radius = 0.3).move_to(brackets.get_left())
        arc2.shift(arc2.width / 2 * LEFT + arc2.height / 2 * UP)
        self.add(arc2)

        hand2 = get_hand(start_point = arc2.get_corner(UL))
        self.add(hand2)
        
