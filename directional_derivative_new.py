from manim import *
from MF_Tools import *
from N_Tools import *

DIMS = 3

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

def make_directional(n=DIMS, second=False):
    prefix = r"D^2_{\vec{v}} f(\vec{x})" if second else r"D_{\vec{v}} f(\vec{x})"
    frac_num = r"D_{\vec{v}} f(\vec{x})" if second else "f"
    parts = [prefix, "="]
    for i in range(1, n + 1):
        parts.append(rf"\frac{{\partial {frac_num}}}{{\partial x_{i}}}")
        parts.append(rf"v_{i}")
        if i < n:
            parts.append("+")
    return MathTex(*parts)

v_row = create_v(DIMS, "row")
v_col = create_v(DIMS, "column")
grad_row = create_grad(DIMS, "row")
grad_col = create_grad(DIMS, "column")

Dv = r"D_{\vec{v}} f(\vec{x})"
D2v = r"D^2_{\vec{v}} f(\vec{x})"

def make_expanded_D2v(n=DIMS):
    elements = [rf"\frac {{\partial}} {{\partial X_{i}}}" + grad_row + v_col for i in range(1, n + 1)]
    return [
        D2v,
        "=",
        v_row,
        latex_vector(elements)
    ]


class DirectionalDerivativeScene2(Scene):
    def construct(self):
        # --- Part 1: Create the objects ---

        # Directional first derivatives
        Dv_sum = make_directional(DIMS)
        vTgrad = MathTex(
            Dv,
            "=",
            v_row,
            grad_col
        )
        gradTv = MathTex(
            Dv,
            "=",
            grad_row,
            v_col
        )

        # Directional second derivatives
        D2v_sub_str = create_grad(DIMS, "col", func_name=Dv) 
        D2v_sub = MathTex(
            D2v, 
            "=", 
            v_row, 
            D2v_sub_str
        ) # Plug f = Dv into the formula for Dv, getting D2v
        
        D2v_partials = MathTex(*make_expanded_D2v()) # Expand out D2v
        D2v_hess_rows = MathTex(        
            D2v,
            "=",
            v_row,
            latex_vector([create_hess_row(num_elements=DIMS, i=i) + v_col for i in range(1, DIMS + 1)])
        )
        D2v_col_only = MathTex(D2v_hess_rows.tex_strings[-1])
        Hv = MathTex(
            hessian_latex(DIMS), 
            v_col, 
            "="
        )
        D2v_quadratic_form = MathTex(        
            D2v,
            "=",
            v_row,
            hessian_latex(DIMS) + v_col
        )

        # --- Part 2a: Scale the objects ---
        desired_width = config.frame_width - 2 * DEFAULT_MOBJECT_TO_EDGE_BUFFER - DEFAULT_MOBJECT_TO_MOBJECT_BUFFER
        scale_factor = desired_width / (D2v_col_only.width + Hv.width)
        D2v_partials.scale(scale_factor)
        D2v_hess_rows.scale(scale_factor)
        D2v_col_only.scale(scale_factor)
        Hv.scale(scale_factor)

        # --- Part 2b: Move the objects ---
        VGroup(Dv_sum, vTgrad, gradTv).arrange(DOWN).to_edge(UP)
        D2v_partials.to_edge(RIGHT)
        D2v_hess_rows.to_edge(RIGHT)
        D2v_col_only.to_edge(RIGHT)
        Hv.to_edge(LEFT)

        # --- Part 3: Animations ---
        self.add(Dv_sum)
        self.play(TransformMatchingShapes(Dv_sum.copy(), vTgrad))
        self.play(TransformMatchingShapes(vTgrad.copy(), gradTv))
        self.remove(Dv_sum, gradTv)
        self.play(TransformMatchingShapes(vTgrad, D2v_sub))
        self.play(TransformMatchingShapes(D2v_sub, D2v_partials))
        self.play(TransformMatchingShapes(D2v_partials, D2v_hess_rows))
        self.add(D2v_col_only)
        self.play(FadeOut(D2v_hess_rows))
        self.play(TransformMatchingShapes(D2v_col_only.copy(), Hv))
        self.play(FadeOut(Hv))
        self.play(FadeIn(D2v_hess_rows))
        self.remove(D2v_col_only)
        self.play(ReplacementTransformGroup(
            D2v_hess_rows, 
            D2v_quadratic_form,
            transform=TransformMatchingShapes
        ))
        self.wait(2)