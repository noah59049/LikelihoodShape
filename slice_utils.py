from manim import *
import numpy as np
from dataclasses import dataclass
from typing import Callable, Tuple, List, Optional


@dataclass
class GraphSlice:
    axes: ThreeDAxes
    axes2d: Axes
    surface: Surface
    slice_plane: Surface        # red checkerboard plane cutting through (x0, y0)
    slice_curve: VMobject       # orange curve living on the 3D surface
    graph_curve: VMobject       # orange curve in the 2D axes (copy target)
    g: Callable                 # g(t) = f(gamma(t))
    g_prime: Callable           # g'(t) = dot(grad_f(gamma(t)), v)
    gamma: Callable             # gamma(t) -> array([x0 + t*v[0], y0 + t*v[1]])
    v: np.ndarray               # normalized direction vector
    x0: float
    y0: float

    def animate_copy(
        self,
        scene,
        extra_3d_objects: Optional[List] = None,
        run_time: float = 1.35,
    ):
        """
        Move the 3D scene to the right, reveal the 2D axes, and copy the
        slice curve from 3D into the 2D axes — matching the animation in
        graph_slice.py.

        Parameters
        ----------
        scene            : ThreeDScene — the active Manim scene
        extra_3d_objects : additional Mobjects to move with the 3D group
                           (e.g. an arrow, a base dot)
        run_time         : duration for each sub-animation
        """
        three_d_objects = [self.axes, self.surface, self.slice_plane, self.slice_curve]
        if extra_3d_objects:
            three_d_objects.extend(extra_3d_objects)
        three_d_group = VGroup(*three_d_objects)

        scene.play(
            three_d_group.animate.scale(0.8).to_edge(RIGHT, buff=0.5),
            run_time=run_time,
        )

        scene.add_fixed_in_frame_mobjects(self.axes2d)
        scene.play(FadeIn(self.axes2d))

        scene.add_fixed_in_frame_mobjects(self.graph_curve)

        # Project the 3D curve to screen space so TransformFromCopy starts
        # from the correct screen position.
        slice_curve_projected = self.slice_curve.copy()
        slice_curve_projected.apply_function(
            lambda p: scene.camera.project_point(p)
        )

        scene.play(
            TransformFromCopy(slice_curve_projected, self.graph_curve),
            run_time=run_time,
        )


def make_graph_slice(
    f: Callable,
    grad_f: Callable,
    x0: float,
    y0: float,
    v,
    x_range: Tuple = (-3, 3),
    y_range: Tuple = (-3, 3),
    z_range: Tuple = (0, 10),
    u_range: Tuple = (-2, 2),
    surface_v_range: Tuple = (-2, 2),
    resolution: Tuple = (12, 12),
    fill_opacity: float = 0.35,
    axes2d_y_range: Tuple = (0, 4),
    axes2d_scale: float = 0.56,
    slice_resolution: int = 100,
    slice_color=ORANGE,
    plane_u_range: Tuple = (-2, 2),
    plane_v_range: Tuple = (-3, 3),
    plane_resolution: Tuple = (10, 10),
    plane_fill_opacity: float = 0.6,
    plane_colors=None,
) -> GraphSlice:
    """
    Build a directed slice of a 3D graph f(x, y) together with a matching
    2D axes and copy-animation helpers.

    Parameters
    ----------
    f, grad_f        : function and its gradient
    x0, y0           : starting point of the slice in the xy-plane
    v                : direction vector (will be normalised)
    *_range          : axis/surface extent configuration
    resolution       : surface mesh resolution
    fill_opacity     : surface opacity
    axes2d_y_range   : y-range for the 2D axes (should cover g(t) values)
    axes2d_scale     : uniform scale applied to the 2D Axes object
    slice_resolution : number of sample points along the slice curve
    slice_color      : color for both the 3D and 2D slice curves

    Returns
    -------
    GraphSlice with:
      .axes        — ThreeDAxes
      .axes2d      — Axes (2D, scaled to DL corner)
      .surface     — Surface of f
      .slice_plane — checkerboard plane through (x0, y0) in direction v
      .slice_curve — VMobject on the 3D surface (orange by default)
      .graph_curve — VMobject in the 2D axes (orange by default)
      .g           — g(t) = f(x0 + t*v[0], y0 + t*v[1])
      .g_prime     — g'(t) = dot(grad_f(gamma(t)), v)
      .gamma       — gamma(t) = array([x0 + t*v[0], y0 + t*v[1]])
      .v           — normalised direction vector
      .x0, .y0     — starting point
    """
    if plane_colors is None:
        plane_colors = [RED_D, RED_E]
    v = np.array(v, dtype=float)
    v = v / np.linalg.norm(v)

    def gamma(t):
        return np.array([x0 + t * v[0], y0 + t * v[1]])

    def g(t):
        return f(*gamma(t))

    def g_prime(t):
        return float(np.dot(grad_f(*gamma(t)), v))

    axes = ThreeDAxes(
        x_range=list(x_range),
        y_range=list(y_range),
        z_range=list(z_range),
    )

    axes2d = (
        Axes(
            x_range=list(u_range),
            y_range=list(axes2d_y_range),
            axis_config={"include_numbers": True},
        )
        .scale(axes2d_scale)
        .to_corner(DL)
    )

    surface = Surface(
        lambda u, w: axes.c2p(u, w, f(u, w)),
        u_range=u_range,
        v_range=surface_v_range,
        resolution=resolution,
        fill_opacity=fill_opacity,
    )

    z0 = f(x0, y0)
    slice_plane = Surface(
        lambda s, t: axes.c2p(
            x0 + s * v[0],
            y0 + s * v[1],
            z0 + t,
        ),
        u_range=plane_u_range,
        v_range=plane_v_range,
        resolution=plane_resolution,
        fill_opacity=plane_fill_opacity,
        checkerboard_colors=plane_colors,
    )

    t_vals = np.linspace(u_range[0], u_range[1], slice_resolution)
    curve_3d_points = []
    curve_2d_points = []
    for t in t_vals:
        x, y = gamma(t)
        z = f(x, y)
        curve_3d_points.append(axes.c2p(x, y, z))
        curve_2d_points.append(axes2d.c2p(t, z))

    slice_curve = VMobject(color=slice_color)
    slice_curve.set_points_as_corners(curve_3d_points)

    graph_curve = VMobject(color=slice_color)
    graph_curve.set_points_as_corners(curve_2d_points)

    return GraphSlice(
        axes=axes,
        axes2d=axes2d,
        surface=surface,
        slice_plane=slice_plane,
        slice_curve=slice_curve,
        graph_curve=graph_curve,
        g=g,
        g_prime=g_prime,
        gamma=gamma,
        v=v,
        x0=x0,
        y0=y0,
    )
