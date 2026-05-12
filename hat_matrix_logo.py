import math
from manim import *

class HatMatrixLogo(VGroup):
    def __init__(self):
        faint_elements = MathTex(
            r"\begin{bmatrix}"
            r"x_{11} & x_{12} \\"
            r"x_{21} & x_{22}"
            r"\end{bmatrix}", 
            font_size = 40
        ).set_stroke(color = GREEN_E, width = 4, background=False)
        faint_elements.scale(0.8)
        faint_elements.set_opacity(0.2)
        faint_elements[0][0].set_opacity(0)
        faint_elements[0][-1].set_opacity(0)

        brackets = MathTex(
            r"\begin{bmatrix}"
            r"\quad & \quad \\"
            r"\quad & \quad"
            r"\end{bmatrix}", 
            font_size = 40
        ).set_stroke(color = WHITE, width = 4, background=False)
        self.brackets = brackets
        self.original_brackets_width = brackets.width

        # Main triangle of the hat
        triangle = Triangle(color = PURPLE_E, 
                            fill_color = PURPLE_E, 
                            fill_opacity = 1,
                            )
        triangle.next_to(brackets, UP)
        triangle.stretch_to_fit_height(2)
        triangle.scale(0.9)
        triangle.shift(UP * 0.0)

        # Lower triangle with the brim of the hat
        triangle2 = triangle.copy()
        triangle2.stretch_to_fit_height(0.5)
        triangle2.stretch_to_fit_width(2.5)
        triangle2.move_to(triangle, aligned_edge=DOWN)

        # Brown strap with the buckle
        buckle_rect = Rectangle(width = triangle2.width * 2, height = triangle2.height * 0.65)
        buckle_rect.move_to(triangle, aligned_edge=DOWN)
        buckle_rect.shift(buckle_rect.height * UP)
        buckle_strap = Intersection(buckle_rect, triangle, color = DARK_BROWN, fill_opacity = 1)

        # Buckle
        buckle = RoundedRectangle(color = GRAY_A, width = triangle.width / 3.45, height = buckle_rect.height, corner_radius = buckle_rect.height / 10)
        buckle.set_stroke(width = buckle.height * 24)
        buckle.move_to(buckle_strap)

        hat_hidden = VGroup(triangle, triangle2, buckle_strap, buckle).next_to(brackets, UP)

        # Arms
        self.arm_length = ValueTracker(0.3)
        def get_hand(start_point, length = 0.13, theta = math.pi / 6):
            line1 = Line(start = start_point, end = start_point + math.cos(theta) * length * UP + math.sin(theta) * length * RIGHT)
            line2 = Line(start = start_point, end = start_point + length * UP)
            line3 = Line(start = start_point, end = start_point + math.cos(theta) * length * UP + math.sin(theta) * length * LEFT)
            return VGroup(line1, line2, line3).scale(self.get_scale())
        def get_left_arm():
            arc = Arc(start_angle = PI, angle = PI / 2, radius = 0.3).scale(self.get_scale())
            arc.stretch_to_fit_height(self.arm_length.get_value() * self.get_scale())
            arc.move_to(brackets.get_left())
            arc.shift(arc.width / 2 * LEFT + arc.height / 2 * UP)
            return arc
        def get_right_arm():
            arc = Arc(start_angle = 3 * PI / 2, angle = PI / 2, radius = 0.3).scale(self.get_scale())
            arc.stretch_to_fit_height(self.arm_length.get_value()* self.get_scale())
            arc.move_to(brackets.get_right())
            arc.shift(arc.width / 2 * RIGHT + arc.height / 2 * UP)
            return arc

        left_arm = always_redraw(get_left_arm)
        left_hand = always_redraw(lambda: get_hand(start_point = left_arm.get_corner(UL)))
        right_arm = always_redraw(get_right_arm)
        right_hand = always_redraw(lambda: get_hand(start_point = right_arm.get_corner(UR)))

        # Eyes
        eye1 = Circle(radius = brackets.width / 12, color = WHITE)
        eye1.move_to(brackets)
        eye1.shift(1.285 * eye1.width * RIGHT + eye1.height * UP)

        eye2 = eye1.copy()
        eye2.shift(1.285 * eye2.width * 2 * LEFT)

        # Nose
        nose = VGroup(Line(LEFT * 0.18, RIGHT * 0.18),
                      Line(RIGHT * 0.18, UP * 0.18 * 1.732))
        nose.scale(0.73)
        nose.shift(DOWN * 0.14)
        
        # Mouth
        mouth = Line(0.27 * LEFT, 0.27 * RIGHT, path_arc = PI / 4)
        mouth.shift(DOWN * 0.27)

        def get_hat():
            hat = hat_hidden.copy().scale(self.get_scale()).next_to(brackets)
            hat_bottom = right_hand.get_top() + hat.height / 2 * UP
            hat_bottom[0] = brackets.get_top()[0]
            hat_bottom[1] = max(hat_bottom[1], brackets.get_top()[1])
            hat.move_to(hat_bottom)
            return hat

        hat = always_redraw(get_hat)
        
        super().__init__(faint_elements, brackets, eye1, eye2, mouth, nose, left_arm, left_hand, right_arm, right_hand, hat)
    
    def adjust_hat(self, **kwargs):
        return Succession(
            ApplyMethod(self.arm_length.set_value, 0.6),
            ApplyMethod(self.arm_length.set_value, 0.3),
            **kwargs
        )
    
    def get_scale(self):
        return self.brackets.width / self.original_brackets_width

class HatMatrixScene(Scene):
    def construct(self):
        my_hat_matrix = HatMatrixLogo().scale(2).shift(DOWN * 0.4)
        self.add(my_hat_matrix)
        self.play(my_hat_matrix.adjust_hat(), run_time = 0.001)
        my_text = Text("The Hat Matrix").scale(2).to_edge(DOWN)
        self.wait(0.7)
        self.play(Write(my_text, run_time = 2))
        self.play(my_hat_matrix.adjust_hat(run_time = 2))
        self.wait(3)