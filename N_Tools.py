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