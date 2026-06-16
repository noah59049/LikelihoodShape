from manim import *
from MF_Tools import *
from N_Tools import *
from manim_voiceover import *
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
import ls_config

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


def hessian_latex(n, func_name="f", row_sep=""):
    rows = []

    for i in range(1, n + 1):
        row = []
        for j in range(1, n + 1):
            entry = f"\\frac{{\\partial^2 {func_name}}}{{\\partial x_{i} \\partial x_{j}}}"
            row.append(entry)
        rows.append(" & ".join(row))

    sep = f" \\\\[{row_sep}]\n" if row_sep else " \\\\\n"
    matrix_body = sep.join(rows)

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


class DirectionalDerivativeScene2(VoiceoverScene):
    def construct(self):
        # --- Part 0: Set the speech service ---
        self.set_speech_service(StitcherService(ls_config.path_to_podcast("directional_derivative_new"),
        cache_dir=ls_config.get_cache_dir(),
        min_silence_len=2000,
        keep_silence=(0,0)))

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
        hess_str = hessian_latex(DIMS, row_sep = "12pt")
        D2v_col_only = MathTex(D2v_hess_rows.tex_strings[-1])
        Hv = MathTex(
            hess_str, 
            v_col, 
            "="
        )
        D2v_quadratic_form4 = MathTex(        
            D2v,
            "=",
            v_row,
            hess_str + v_col
        )
        D2v_quadratic_form5 = MathTex(        
            D2v,
            "=",
            v_row,
            hess_str,
            v_col
        )
        D2v_quadratic_form_hess = MathTex(        
            D2v,
            "=",
            v_row,
            "H",
            v_col
        )
        D2v_quadratic_form_compact1 = MathTex(        
            D2v,
            r"=",
            v_row,
            r"H",
            r"\vec{v}"
        )
        D2v_quadratic_form_compact2 = MathTex(        
            D2v,
            r"=",
            r"\vec{v}^T",
            r"H",
            r"\vec{v}"
        )
        element11_box = box_matrix_element(D2v_quadratic_form5[3], 0, 0)
        element12_box = box_matrix_element(D2v_quadratic_form5[3], 0, 1)

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
        with self.voiceover("You may recall that the directional derivative is equal to the sum of the partial derivatives times the components of the direction vector.") as tracker:
            self.add(Dv_sum)
        with self.voiceover("It's more convenient to write this as a product of the vector of components of v and of the partial derivatives.") as tracker:
            self.play(TransformMatchingShapes(Dv_sum.copy(), vTgrad))
        with self.voiceover("This is just v, except it's a row vector so it's v transpose. And this, as you may recall, is the gradient.") as tracker:
            ... # TODO: Draw an arrow pointing to each one of these
        with self.voiceover("The directional derivative is also equal to the gradient transposed times v.") as tracker:
            self.play(TransformMatchingShapes(vTgrad.copy(), gradTv))
        with self.voiceover("Now, the directional second derivative is just the directional derivative of the directional derivative.") as tracker:
            self.remove(Dv_sum, gradTv)
            self.play(TransformMatchingShapes(vTgrad, D2v_sub))
        with self.voiceover("we can plug the directional derivative definition into this formula") as tracker:
            self.play(TransformMatchingShapes(D2v_sub, D2v_partials))
        with self.voiceover("and the derivative just distributes with sums and scaling.") as tracker:
            self.play(TransformMatchingShapes(D2v_partials, D2v_hess_rows))
        with self.voiceover("This part here looks suspiciously like a matrix multiplication") as tracker:
            self.add(D2v_col_only)
            self.play(FadeOut(D2v_hess_rows))
        with self.voiceover("where we just glue all the row vectors into a matrix, and multiply it by v. It in fact is.") as tracker:
            self.play(TransformMatchingShapes(D2v_col_only.copy(), Hv))
        with self.voiceover("The first element of this product should be the first row times the vector, and what do you know, it is. The second element should be the second row times the column vector, etcetera.") as tracker:
            ... # TODO: Highlight the rows
        with self.voiceover("Now we can go back to the equation we had") as tracker:
            self.play(FadeOut(Hv))
            self.play(FadeIn(D2v_hess_rows))
            self.remove(D2v_col_only)
        with self.voiceover("and replace this messy vector with our matrix vector product.") as tracker:
            self.play(TransformIndices(
                D2v_hess_rows, 
                D2v_quadratic_form4,
                transform=TransformMatchingShapes
            ))
            self.remove(D2v_quadratic_form4)
        self.add(D2v_quadratic_form5)
        hess_transform = TransformIndicesWithBoxes(
            D2v_quadratic_form5, 
            D2v_quadratic_form_hess, 
            box_indices=[3]
        )
        with self.voiceover("The matrix is somewhat special. Recall how the gradient was the vector of all the first order partials? This is basically the second derivative version of that.") as tracker:
            self.play(hess_transform.animations[0])
        with self.voiceover("The element at 11, the first row and column, is the second order partial with respect to X1.") as tracker:
            self.play(Create(element11_box))
        with self.voiceover("The element at 12 is the mixed second order partial with respect to X1 and X2,") as tracker:
            self.play(Create(element12_box))
        with self.voiceover("and so on for all the other elements.") as tracker:
            self.play(FadeOut(element11_box, element12_box))
        with self.voiceover("This matrix is called the Hessian, written H.") as tracker:
            self.play(hess_transform.animations[1])
            self.play(hess_transform.animations[2])
        with self.voiceover("This vector here is just v,") as tracker:
            self.play(TransformIndicesWithBoxes(D2v_quadratic_form_hess,     D2v_quadratic_form_compact1, box_indices = [4]))
        with self.voiceover("and this vector is v transpose.") as tracker:
            self.play(TransformIndicesWithBoxes(D2v_quadratic_form_compact1, D2v_quadratic_form_compact2, box_indices = [2]))
        with self.voiceover("So we have arrived at a delightfully simple formula for the directional second derivative, and our next goal is to prove that it is negative. To do that, we need to calculate the Hessian.") as tracker:
            ...