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
        triangle.shift(UP * 0.0)
        self.add(triangle)

        # Lower triangle with the brim of the hat
        triangle2 = triangle.copy()
        triangle2.stretch_to_fit_height(0.5)
        triangle2.stretch_to_fit_width(2.5)
        triangle2.move_to(triangle, aligned_edge=DOWN)
        self.add(triangle2)

        # Brown strap with the buckle
        buckle_rect = Rectangle(width = triangle2.width * 2, height = triangle2.height * 0.65)
        buckle_rect.move_to(triangle, aligned_edge=DOWN)
        buckle_rect.shift(buckle_rect.height * UP)
        buckle_strap = Intersection(buckle_rect, triangle, color = DARK_BROWN, fill_opacity = 1)
        self.add(buckle_strap)

        # Buckle
        buckle = RoundedRectangle(color = GRAY_A, width = triangle.width / 3.45, height = buckle_rect.height, corner_radius = buckle_rect.height / 10)
        buckle.move_to(buckle_strap)
        self.add(buckle)

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

        # Eyes
        eye1 = Circle(radius = brackets.width / 12, color = WHITE)
        eye1.move_to(brackets)
        eye1.shift(1.285 * eye1.width * RIGHT + eye1.height * UP)
        self.add(eye1)

        eye2 = eye1.copy()
        eye2.shift(1.285 * eye2.width * 2 * LEFT)
        self.add(eye2)

        # Nose
        nose = VGroup(Line(LEFT * 0.18, RIGHT * 0.18),
                      Line(RIGHT * 0.18, UP * 0.18 * 1.732))
        nose.scale(0.73)
        self.add(nose)
        nose.shift(DOWN * 0.14)
        
        # Mouth
        mouth = Line(0.27 * LEFT, 0.27 * RIGHT, path_arc = PI / 4)
        mouth.shift(DOWN * 0.27)
        self.add(mouth)