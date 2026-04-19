from manim import *

def animate_matrix_vector_product(scene, matrix_entries, vector_entries):
    n = int(len(matrix_entries) ** 0.5)

    rows = []
    idx = 0
    for i in range(n):
        row = VGroup(*matrix_entries[idx:idx+n])
        rows.append(row)
        idx += n

    scene.play(Write(matrix_entries), Write(vector_entries))
    scene.wait()

    result_entries = []

    for i, row in enumerate(rows):
        scene.play(
            row.animate.set_color(YELLOW),
            vector_entries.animate.set_color(BLUE)
        )

        terms = []
        for j in range(n):
            terms.append(row[j].copy())
            terms.append(MathTex(r"\cdot"))
            terms.append(vector_entries[j].copy())
            if j < n - 1:
                terms.append(MathTex("+"))

        dot_expr = VGroup(*terms).arrange(RIGHT)
        dot_expr.to_edge(RIGHT)

        scene.play(Write(dot_expr))

        result = MathTex(f"r_{i+1}")
        result.next_to(dot_expr, RIGHT)

        scene.play(Transform(dot_expr, result))

        result_entries.append(result)

        scene.play(
            row.animate.set_color(WHITE),
            vector_entries.animate.set_color(WHITE)
        )

    result_vector = VGroup(*result_entries).arrange(DOWN)
    scene.play(Write(result_vector))
    scene.wait()

class MatrixVectorTest(Scene):
    def construct(self):

        # Matrix entries
        matrix_entries = MathTex(
            "a_{11}", "a_{12}",
            "a_{21}", "a_{22}"
        ).arrange_in_grid(2, 2)
        matrix_entries.to_edge(LEFT)

        # Vector entries
        vector_entries = MathTex(
            "x_1", "x_2"
        ).arrange(DOWN)
        vector_entries.next_to(matrix_entries, RIGHT, buff=2)

        # Animate
        animate_matrix_vector_product(self, matrix_entries, vector_entries)