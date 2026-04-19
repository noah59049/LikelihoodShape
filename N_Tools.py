from typing import Callable

def square_matrix_tex(n : int, 
                      generator: Callable[[int, int], str],
                      start_ij: int = 1):
    rows = []
    for i in range(start_ij, n + start_ij):
        row = []
        for j in range(start_ij, n + start_ij):
            entry = generator(i, j)
            row.append(entry)
        rows.append(" & ".join(row))
    
    matrix_body = " \\\\\n".join(rows)
    
    latex = (
        "\\begin{bmatrix}\n"
        f"{matrix_body}\n"
        "\\end{bmatrix}\n"
    )
    return latex