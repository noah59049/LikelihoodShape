import math
from manim import *
from MF_Tools import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.stitcher import _StitcherService as StitcherService

from manim import *
import numpy as np

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
                orientation = "row",
                bracket = "bmatrix"):
    return latex_vector([f"\\frac{{\\partial{{f}}}}{{\\partial{{x_{i}}}}}" for i in range(1, 1 + num_elements)], 
                        orientation=orientation,
                        bracket = bracket)

class SecondDerivativeScene(Scene):
    def construct(self):
        rowvector1 = latex_vector([f"v_{i}" for i in range(1,5)], orientation="row")
        colvector1 = latex_vector([f"\\frac{{\\partial{{f}}}}{{\\partial{{x_{i}}}}}" for i in range(1,5)])
        self.add(MathTex(rowvector1 + colvector1))
