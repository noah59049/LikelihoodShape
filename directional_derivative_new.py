from manim import *
from MF_Tools import *
from N_Tools import *

def create_v(num_elements,
             orientation = "row",
             bracket = "bmatrix"):
    return latex_vector([f"v_{i}" for i in range(1, 1 + num_elements)], 
                        orientation=orientation,
                        bracket = bracket)

def create_grad(num_elements,
                orientation = "column",
                bracket = "bmatrix",
                func_name = "f"):
    return latex_vector([f"\\frac{{\\partial {func_name}}}{{\\partial x_{i}}}" for i in range(1, 1 + num_elements)],
                        orientation=orientation,
                        bracket = bracket)

def create_hess_row(num_elements,
                    i,
                    orientation = "row",
                    bracket = "bmatrix"):
    return latex_vector([f"\\frac{{\\partial^2{{f}}}}{{\\partial{{x_{i}}}\\partial{{x_{j}}}}}" for j in range(1, 1 + num_elements)], 
                        orientation=orientation,
                        bracket = bracket)


def hessian_latex(n, func_name="f"):
    rows = []
    
    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            entry = f"\\frac{{\\partial^2 {func_name}}}{{\\partial x_{i} \\partial x_{j}}}"
            row.append(entry)
        rows.append(" & ".join(row))
    
    matrix_body = " \\\\\n".join(rows)
    
    latex = (
        "\\begin{bmatrix}\n"
        f"{matrix_body}\n"
        "\\end{bmatrix}\n"
    )
    
    return latex

def make_directional(n=4, second=False):
    prefix = r"D^2_{\vec{v}} f(\vec{x})" if second else r"D_{\vec{v}} f(\vec{x})"
    frac_num = r"D_{\vec{v}} f(\vec{x})" if second else "f"
    parts = [prefix, "="]
    for i in range(1, n + 1):
        parts.append(rf"\frac{{\partial {frac_num}}}{{\partial x_{i}}}")
        parts.append(rf"v_{i}")
        if i < n:
            parts.append("+")
    return MathTex(*parts)

v_row = create_v(4, "row")
v_col = create_v(4, "column")
grad_row = create_grad(4, "row")
grad_col = create_grad(4, "column")

Dv = r"D_{\vec{v}} f(\vec{x})"
D2v = r"D^2_{\vec{v}} f(\vec{x})"

def make_expanded_D2v(n=4):
    v_row = create_v(n, "row")
    elements = [rf"\frac {{\partial}} {{\partial X_{i}}}" + grad_row + v_col for i in range(1, n + 1)]
    return D2v + "=" + v_row + latex_vector(elements)


class DirectionalDerivativeScene2(Scene):
    def construct(self):
        directional = make_directional(4)

        vTgrad = MathTex(Dv,
                         "=",
                         v_row,
                         grad_col)
        gradTv = MathTex(Dv,
                         "=",
                         grad_row,
                         v_col)
        
        first_order = VGroup(directional, vTgrad, gradTv).arrange(DOWN).to_edge(UP)

        dir_grad_col = create_grad(4, "col", func_name=Dv)
        second_directional = MathTex(D2v, "=", v_row, dir_grad_col)
        
        second_expanded = MathTex(make_expanded_D2v()).scale(0.77)
        
        # --- Animations ---
        self.add(directional)
        self.play(TransformMatchingShapes(directional.copy(), vTgrad))
        self.play(TransformMatchingShapes(vTgrad.copy(), gradTv))
        self.remove(directional, gradTv)
        self.play(TransformMatchingShapes(vTgrad, second_directional))
        self.play(TransformMatchingShapes(second_directional, second_expanded))
        self.wait(2)