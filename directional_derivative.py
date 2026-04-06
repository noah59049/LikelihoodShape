from manim import *
from MF_Tools import *

def latex_vector(elements, orientation="column", bracket="bmatrix"):
    """
    Convert a list of strings into a LaTeX vector.

    Parameters:
        elements (list of str): The entries of the vector.
        orientation (str): "column" or "row".
        bracket (str): LaTeX matrix environment (e.g., "pmatrix", "bmatrix", "vmatrix").

    Returns:
        str: LaTeX string representing the vector.
    """
    if not elements:
        raise ValueError("elements list cannot be empty")

    if orientation == "col":
        orientation = "column"

    if orientation not in {"column", "row"}:
        raise ValueError("orientation must be 'column' or 'row'")

    if orientation == "column":
        body = " \\\\ ".join(elements)
    else:  # row
        body = " & ".join(elements)

    return f"\\begin{{{bracket}}}{body}\\end{{{bracket}}}"

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

class DirectionalDerivativeScene(Scene):
    def construct(self):

        # --- Step 1: First line at top ---
        f_explicit = MathTex("f(x_1, x_2, x_3, x_4)")
        f_explicit.to_edge(UP)

        self.play(Write(f_explicit))
        self.wait()

        # --- Step 2: Transform in place ---
        f_vector = MathTex("f(\\vec{x})")
        f_vector.move_to(f_explicit)

        self.play(TransformByGlyphMap(f_explicit, f_vector,
                                      (range(2,13), range(2,4))))
        self.wait()

        # --- Step 3: Directional derivative ---
        directional = MathTex("D_{\\vec{v}} f(\\vec{x})")
        directional.next_to(f_vector, DOWN, buff=0.4)

        self.play(Write(directional))
        self.wait()

        # --- Step 4: Path ---
        path = MathTex("\\vec{x} = \\vec{a} + t\\vec{v}")
        path.next_to(directional, DOWN, buff=0.4)

        self.play(Write(path))
        self.wait()

        # --- Step 5: g(t) definition ---
        g_def = MathTex("g(t) = f(\\vec{a} + t\\vec{v}) = f(\\vec{x})")
        g_def.next_to(path, DOWN, buff=0.4)

        self.play(Write(g_def))
        self.wait()

        # --- Step 6: derivative relation ---
        deriv_relation = MathTex("D_{\\vec{v}} f(\\vec{x}) = g'(t)")
        deriv_relation.next_to(g_def, DOWN, buff=0.4)

        self.play(TransformMatchingTex(directional.copy(), deriv_relation))
        self.wait()

        # --- Step 7: Chain rule ---
        chain_rule = MathTex(
            "\\frac{\\partial g}{\\partial t} =",
            "\\frac{\\partial f}{\\partial x_1}",
            "\\frac{\\partial x_1}{\\partial t}",
            "+",
            "\\frac{\\partial f}{\\partial x_2}",
            "\\frac{\\partial x_2}{\\partial t}",
            "+",
            "\\frac{\\partial f}{\\partial x_3}",
            "\\frac{\\partial x_3}{\\partial t}",
            "+",
            "\\frac{\\partial f}{\\partial x_4}",
            "\\frac{\\partial x_4}{\\partial t}",
        )
        chain_rule.scale(0.8)
        chain_rule.next_to(deriv_relation, DOWN, buff=0.4)

        self.play(Write(chain_rule))
        self.wait()

        # --- Step 8: Substitute v ---
        simplified = MathTex(
            "\\frac{\\partial g}{\\partial t} =",
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
        simplified.scale(0.8)
        simplified.align_to(chain_rule, UP)

        self.play(
            *[ReplacementTransform(chain_rule[i], simplified[i]) for i in range(12)]
        )

        # --- Step 9: Clear out the rest of the scene except for simplified ---
        self.play(FadeOut(Group(*[m for m in self.mobjects if m is not simplified])))
        self.play(simplified.animate.to_edge(UP))

        # --- Step 10: Vector form ---
        v_row = create_v(4, "row")
        v_col = create_v(4, "column")
        grad_row = create_grad(4, "row")
        grad_col = create_grad(4, "column")
        vTgrad = MathTex("\\frac{\\partial g}{\\partial t} =",
                         v_row,
                         grad_col)
        gradTv = MathTex("\\frac{\\partial g}{\\partial t} =",
                         grad_row,
                         v_col)

        self.play(TransformMatchingShapes(simplified.copy(), vTgrad))
        self.play(TransformMatchingShapes(vTgrad, gradTv))
        self.play(TransformMatchingShapes(gradTv, vTgrad))

        # --- Step 11: Making the Giga Hess ---

        giga_hess0_list = [
            "\\frac{\\partial^2 g}{\\partial t^2} =",
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
            ]

        giga_hess0 = MathTex(
            *giga_hess0_list.copy()
        )
        giga_hess0.scale(0.8)
        giga_hess0.align_to(simplified, UP)

        self.play(
            *[ReplacementTransform(simplified[i], giga_hess0[i]) for i in range(12)]
        )

        for i in (1,2,3,4):
            giga_hess0_list[3 * i - 2] = create_hess_row(4, i) + v_col
            giga_hess1 = MathTex(*giga_hess0_list.copy())
            giga_hess1.scale([None, 0.8, 0.55, 0.4, 0.34][i])
            giga_hess1.align_to(giga_hess0, UP)
            self.play(
                *[ReplacementTransform(giga_hess0[i], giga_hess1[i]) for i in range(12)]
            )
            giga_hess0 = giga_hess1

        self.play(FadeOut(giga_hess0)) # I don't like this but I need to do it to give hess_vec more room

        hess_vec0 = MathTex("\\frac{\\partial^2 g}{\\partial t^2} =",
                         v_row,
                         grad_col)
        hess_vec0.align_to(vTgrad, UP)
        self.play(*[ReplacementTransform(vTgrad[i], hess_vec0[i]) for i in range(3)])

        # Change hess_vec0 into one that's identical, but only 1 part
        hess_vec0new = MathTex("\\frac{\\partial^2 g}{\\partial t^2} =" +
                         v_row +
                         grad_col)
        hess_vec0new.align_to(vTgrad, UP)
        self.play(TransformMatchingTex(hess_vec0, hess_vec0new))
        # We may need to change this to one that transforms smoothly
        
        hess_v = [f"\\frac{{\\partial{{f}}}}{{\\partial{{x_{i}}}}}" for i in (1,2,3,4)]
        glyph_index_transforms = [
            [
                (range(18,23), range(18,29)), # Left bracket
                (range(23, 23 + 6), range(29, 29 + 58)), # Hess row
                (range(47,52), range(105,116)) # Right bracket
            ],
            [
                (range(18,29), range(18,34)), # Left bracket
                (range(87, 87 + 6), range(92, 92 + 58)), # Hess row
                (range(105,116), range(162, 178)) # Right bracket
            ],
            [
                (range(18, 34), range(18, 40)), # Left bracket
                (range(150, 150 + 6), range(156, 156 + 58)), # Center row
                (range(162, 178), range(220, 242)) # Right bracket
            ],
            [
                (range(18, 40), range(18, 46)), # Left bracket
                (range(220 - 6, 220), range(278 - 58, 278)), # Center row
                (range(220, 242), range(278, 306)) # Right bracket
            ]
        ]
        for i in (1,2,3,4):
            hess_v[i - 1] = create_hess_row(4, i) + v_col
            hess_vec1 = MathTex("\\frac{\\partial^2 g}{\\partial t^2} =" +
                         v_row + 
                         latex_vector(hess_v.copy()))
            hess_vec1.scale(0.77)
            self.play(TransformByGlyphMap(hess_vec0new, hess_vec1,
                                          *glyph_index_transforms[i-1],
                                          ))
            hess_vec0new = hess_vec1

        # --- Step 12: Showing that this is equal to the quadratic form of a matrix ---
        # Switch the number of groups in here 
        hess_vec1_split = MathTex("\\frac{\\partial^2 g}{\\partial t^2} =" +
                v_row,
                latex_vector(hess_v.copy()))
        hess_vec1_split.scale(0.77)
        self.play(TransformMatchingTex(hess_vec1,hess_vec1_split))

        # Replace the 4 different dot products with the Hessian
        hess_vec2 = MathTex("\\frac{\\partial^2 g}{\\partial t^2} =" +
                         v_row,
                         hessian_latex(4) + 
                         v_col)
        hess_vec2.scale(0.77)
        
        self.play(ReplacementTransform(hess_vec1_split[0], hess_vec2[0]),
                  TransformMatchingShapes(hess_vec1_split[1], hess_vec2[1]))
        
        # Split it into 4 groups
        hess_vec2_split = MathTex("\\frac{\\partial^2 g}{\\partial t^2} =",
                         v_row,
                         hessian_latex(4),
                         v_col)
        hess_vec2_split.scale(0.77)
        self.play(TransformMatchingTex(hess_vec2,hess_vec2_split))
        
        # Interlude showing that matrix is correct
        # Move it over to the left and get rid of everything except the matmul
        hess_mat0 = MathTex(
            hessian_latex(4),
            v_col
        )
        hess_mat0.scale(0.77)
        hess_mat0.to_edge(LEFT)

        self.play(
            FadeOut(VGroup(*hess_vec2_split[0:2]), run_time = 0.6),
            ReplacementTransform(
                VGroup(hess_vec2_split[2], hess_vec2_split[3]),
                hess_mat0,
                run_time = 1.3
            ),
        )

        # Change it into just 1 object
        hess_mat1 = MathTex(
            hessian_latex(4) +
            v_col
        )
        hess_mat1.scale(0.77)
        hess_mat1.to_edge(LEFT)
        self.play(TransformMatchingTex(hess_mat0, hess_mat1))

        # Add a right hand side to the equation with an empty matrix
        rhs_tex = r"""=\begin{bmatrix}
            \phantom{0} \\
            \phantom{0} \\
            \phantom{0} \\
            \phantom{0}
            \end{bmatrix}"""
        hess_mat2 = MathTex(
            hessian_latex(4) +
            v_col + 
            rhs_tex
        )
        hess_mat2.scale(0.77)
        hess_mat2.to_edge(LEFT)
        self.play(TransformByGlyphMap(hess_mat1, hess_mat2,
                                      (FadeIn, range(188,197))))

        # Before we add the dot products, we need to scale this down
        hess_mat2.animate.scale(0.66)

        # Add the dot products one by one
        left_bracket_ranges  = [range(189, 193), range(189, 199), range(189,205),range(189, 211),range(189,217)]
        right_bracket_ranges = [range(193, 197), range(257, 267), range(321,337),range(385,407),range(449,477)]
        for i in (1,2,3,4):
            rhs_tex = rhs_tex.replace(r"\phantom{0}", 
                                      create_hess_row(4, i) + v_col, 
                                      count = 1)
            hess_mat3 = MathTex(
                hessian_latex(4) +
                v_col + 
                rhs_tex
            )
            # Compute a bunch of indices for the TransormByGlyphMap
            left_old = left_bracket_ranges[i - 1]
            left_new = left_bracket_ranges[i]
            right_old = right_bracket_ranges[i - 1]
            right_new = right_bracket_ranges[i]
            new_v_range = range(min(right_new) - 16, min(right_new))
            left_hess_row_range = range(40 * i - 34, 40 * i + 6)
            right_hess_row_range = range(min(right_new) - 57, min(right_new) - 17)
            
            

            hess_mat3.scale(0.66)
            hess_mat3.to_edge(LEFT)
            self.play(TransformByGlyphMap(hess_mat2, hess_mat3,
                                            (range(189), range(189)), # The LHS and equals sign stay fixed
                                            (left_old, left_new), # Enlarge the left bracket
                                            (right_old, right_new), # Enlarge the right bracket
                                            (range(172, 188), new_v_range), # Copy v_col over to the RHS matrix
                                            (left_hess_row_range, right_hess_row_range), # Move a hess row from LHS to RHS 
                                            (FadeIn, [min(right_new) - 58, min(right_new) - 17]), # Fade in the brackets of the hess row
                                        ))
            hess_mat2 = hess_mat3

        return # TODO: Remove this

        # Replace the whole Hessian with H
        hess_vec3 = MathTex("\\frac{\\partial^2 g}{\\partial t^2} =",
                         v_row,
                         "H",
                         v_col)
        self.play(*[ReplacementTransform(hess_vec2_split[i], hess_vec3[i]) for i in range(4)])

        # Replace the v1,v2,v3,v4 with \vec{v}
        hess_vec4 = MathTex("\\frac{\\partial^2 g}{\\partial t^2} =",
                         r"\vec{v}^T",
                         "H",
                         r"\vec{v}")
        self.play(*[ReplacementTransform(hess_vec3[i], hess_vec4[i]) for i in range(4)])

        # Replace the g''(t) with a directional second derivative using D^2
        hess_vec5 = MathTex(r"D^2_{\vec{v}}f(\vec{x}) =",
                         r"\vec{v}^T",
                         "H",
                         r"\vec{v}")
        self.play(*[ReplacementTransform(hess_vec4[i], hess_vec5[i]) for i in range(4)])


if __name__ == "__main__":
    print(hessian_latex(4))