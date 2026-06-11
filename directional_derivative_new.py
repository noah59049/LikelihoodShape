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
                bracket = "bmatrix"):
    return latex_vector([f"\\frac{{\\partial{{f}}}}{{\\partial{{x_{i}}}}}" for i in range(1, 1 + num_elements)], 
                        orientation=orientation,
                        bracket = bracket)

def create_hess_row(num_elements,
                    i,
                    orientation = "row",
                    bracket = "bmatrix"):
    return latex_vector([f"\\frac{{\\partial^2{{f}}}}{{\\partial{{x_{i}}}\\partial{{x_{j}}}}}" for j in range(1, 1 + num_elements)], 
                        orientation=orientation,
                        bracket = bracket)

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

class DirectionalDerivativeScene2(Scene):
    def construct(self):
        directional = make_directional(4)

        v_row = create_v(4, "row")
        v_col = create_v(4, "column")
        grad_row = create_grad(4, "row")
        grad_col = create_grad(4, "column")
        vTgrad = MathTex(r"D_{\vec{v}} f(\vec{x})",
                         "=",
                         v_row,
                         grad_col)
        gradTv = MathTex(r"D_{\vec{v}} f(\vec{x})",
                         "=",
                         grad_row,
                         v_col)
        
        first_order = VGroup(directional, vTgrad, gradTv).arrange(DOWN).to_edge(UP)
        
        self.add(directional)
        self.play(TransformMatchingShapes(directional.copy(), vTgrad))
        self.play(TransformMatchingShapes(vTgrad.copy(), gradTv))



        return

        second_directional = make_directional(4, second=True)

        self.play(TransformMatchingShapes(directional.copy(), second_directional))