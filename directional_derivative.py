from manim import *

class DirectionalDerivativeScene(Scene):
    def construct(self):

        # Step 1: Start with explicit function
        f_explicit = MathTex(
            "f(x_1, x_2, x_3, x_4)"
        )
        self.play(Write(f_explicit))
        self.wait()

        # Step 2: Transition to vector notation
        f_vector = MathTex("f(\\vec{x})")
        self.play(TransformMatchingTex(f_explicit, f_vector))
        self.wait()

        # Step 3: Directional derivative notation
        directional = MathTex("D_{\\vec{v}} f(\\vec{x})")
        directional.next_to(f_vector, DOWN, buff=1)

        self.play(Write(directional))
        self.wait()

        # Step 4: Introduce path x = a + tv
        path = MathTex("\\vec{x} = \\vec{a} + t\\vec{v}")
        path.to_edge(UP)

        self.play(Write(path))
        self.wait()

        # Step 5: Define g(t)
        g_def = MathTex(
            "g(t) = f(\\vec{a} + t\\vec{v}) = f(\\vec{x})"
        )
        g_def.next_to(directional, DOWN, buff=1)

        self.play(Write(g_def))
        self.wait()

        # Step 6: Relate directional derivative to g'(t)
        deriv_relation = MathTex(
            "D_{\\vec{v}} f(\\vec{x}) = g'(t)"
        )
        deriv_relation.next_to(g_def, DOWN, buff=1)

        self.play(TransformMatchingTex(directional.copy(), deriv_relation))
        self.wait()

        # Step 7: Chain rule expansion (long form)
        chain_rule = MathTex(
            "\\frac{\\partial g}{\\partial t} =",
            "\\frac{\\partial f}{\\partial x_1}\\frac{\\partial x_1}{\\partial t}",
            "+",
            "\\frac{\\partial f}{\\partial x_2}\\frac{\\partial x_2}{\\partial t}",
            "+",
            "\\frac{\\partial f}{\\partial x_3}\\frac{\\partial x_3}{\\partial t}",
            "+",
            "\\frac{\\partial f}{\\partial x_4}\\frac{\\partial x_4}{\\partial t}"
        )

        chain_rule.scale(0.8)
        chain_rule.to_edge(DOWN)

        self.play(Write(chain_rule))
        self.wait()

        # Step 8: Substitute dx/dt = v
        simplified = MathTex(
            "=",
            "\\frac{\\partial f}{\\partial x_1} v_1",
            "+",
            "\\frac{\\partial f}{\\partial x_2} v_2",
            "+",
            "\\frac{\\partial f}{\\partial x_3} v_3",
            "+",
            "\\frac{\\partial f}{\\partial x_4} v_4"
        )

        simplified.scale(0.8)
        simplified.next_to(chain_rule, DOWN)

        self.play(TransformMatchingTex(chain_rule.copy(), simplified))
        self.wait()

        # Step 9: Final compact dot product form
        final = MathTex(
            "\\nabla f(\\vec{x}) \\cdot \\vec{v}"
        )
        final.scale(1.2)
        final.to_edge(DOWN)

        self.play(TransformMatchingTex(simplified, final))
        self.wait(2)