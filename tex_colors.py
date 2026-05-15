import re
from manim import *

X_color = RED
beta_color = BLUE
Y_color = GREEN
z_color = YELLOW
p_color = GREEN
L_color = PINK


def color_math(tex: MathTex) -> MathTex:
    tex.set_color_by_tex(r"\beta", beta_color, substring=False)
    tex.set_color_by_tex("X", X_color, substring=False)
    tex.set_color_by_tex("Y", Y_color, substring=False)
    tex.set_color_by_tex("y", Y_color, substring=False)
    tex.set_color_by_tex("z", z_color, substring=False)
    tex.set_color_by_tex("p", p_color, substring=False)
    tex.set_color_by_tex("L", L_color, substring=False)
    tex.set_color_by_tex("l", L_color, substring=False)
    tex.set_color_by_tex(r"\ell", L_color, substring=False)
    return tex


_BASE_ISOLATE = [r"\beta", r"\ell", "X", "Y", "L", "y", "z"]


class ColoredMathTex(MathTex):
    def __init__(self, *args, **kwargs):
        full_tex = "".join(str(a) for a in args)
        isolate = _BASE_ISOLATE + ([] if re.search(r'\\[a-z]*p', full_tex) else ["p"])
        kwargs.setdefault('substrings_to_isolate', isolate)
        super().__init__(*args, **kwargs)
        color_math(self)
