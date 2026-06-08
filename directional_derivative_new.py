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
        # HM TODO: We're doing a 4D vector, it can be any size though
        directional = MathTex(
            r"D_{\vec{v}} f(\vec{x})",
            "=",
            "\\frac{\\partial f}{\\partial x_1}",
            "v_1",
            "+",
            "\\frac{\\partial f}{\\partial x_2}",
            "v_2",
            "+",
            "\\frac{\\partial f}{\\partial x_3}",
            "v_3",
            "+",
            "\\frac{\\partial f}{\\partial x_4}",
            "v_4",
        )
        directional.to_edge(UP)

        self.add(directional)

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
        
        self.play(TransformMatchingShapes(directional.copy(), vTgrad))
        self.play(FadeOut(vTgrad))

        second_directional = MathTex(
            r"D^2_{\vec{v}} f(\vec{x})",
            r"=",
            r"\frac{\partial D_{\vec{v} f(\vec{x})}}{\partial x_1}",
            r"v_1",
            r"+",
            r"\frac{\partial D_{\vec{v} f(\vec{x})}}{\partial x_2}",
            r"v_2",
            r"+",
            r"\frac{\partial D_{\vec{v} f(\vec{x})}}{\partial x_3}",
            r"v_3",
            r"+",
            r"\frac{\partial D_{\vec{v} f(\vec{x})}}{\partial x_4}",
            r"v_4",
        )

        self.play(TransformMatchingShapes(directional.copy(), second_directional))