#!/usr/bin/env python

# In order to have our example matrices be realistic, we are generating them from an actual logistic regression model on the sklearn breast cancer dataset

import numpy as np
from data import X, y # type: ignore
from manim import *
from N_Tools import logistic_regression, log_likelihood, as_row, as_col, compute_z_range, surface_from_function

X = as_col(X[:,0]) # We want to have only 2 parameters so we can graph the log-likelihood
beta, cov, se = logistic_regression(X, y, add_intercept = True, return_stats = True)
beta0, beta1 = beta.reshape(2)
se0, se1 = se.reshape(2)

def loglik(beta_hat0, beta_hat1):
    beta_hat = beta_hat0, beta_hat1
    beta_hat = np.array(beta_hat)
    result = log_likelihood(X, y, beta_hat, add_intercept=True)
    # print(f"loglik{float(beta_hat0), float(beta_hat1)}={float(result)}")
    return log_likelihood(X, y, beta_hat, add_intercept=True)

def lik(beta_hat0, beta_hat1):
    return np.exp(loglik(beta_hat0, beta_hat1))

mle_loglik = log_likelihood(X, y, beta, add_intercept = True)
mle_lik = np.exp(mle_loglik)
print(f"Log likelihood = {mle_loglik}")

def create_mle_graph(x_radius,
                     y_radius,
                     resolution = 32):
    beta0, beta1 = beta.reshape(-1)
    x_range = (beta0 - x_radius, beta0 + x_radius)
    y_range = (beta1 - y_radius, beta1 + y_radius)
    print(f"{x_range=}{y_range=}")

    loglik_range = compute_z_range(
        z_func=loglik,
        x_range=x_range,
        y_range=y_range,
        samples=30,
        padding = 0
    )
    loglik_offset = loglik_range[1]

    def lik_scaled(beta_hat0, beta_hat1):
        return np.exp(loglik(beta_hat0, beta_hat1) - loglik_offset)

    mle_lik_scaled = np.exp(mle_loglik - loglik_offset)

    z_range = compute_z_range(
        z_func=lik_scaled,
        x_range=x_range,
        y_range=y_range,
        samples=30
    )

    print(f"{x_range=} {y_range=} {z_range=}")

    axes = ThreeDAxes(
        x_range=(*x_range, (x_range[1] - x_range[0]) / 4),
        y_range=(*y_range, (y_range[1] - y_range[0]) / 4),
        z_range=z_range,
    )

    surface = surface_from_function(
        z_func=lik_scaled,
        axes=axes,
        x_range=x_range,
        y_range=y_range,
        resolution=resolution,
        color=BLUE_C,
    )

    return axes, surface


class PlotSurfaceExample(ThreeDScene):
    def construct(self):
        axes, surface = create_mle_graph(x_radius = se0 * 1,
                                         y_radius = se1 * 1,
                                         resolution=41)

        if True:
            self.set_camera_orientation(
                phi=55 * DEGREES,
                theta=-45 * DEGREES,
                zoom=0.55
            )

        self.add(axes)
        self.play(Create(surface))
        # mle_dot_scaled = Dot3D(axes.c2p(beta0, beta1, mle_lik_scaled), color = RED)
        # self.play(FadeIn(mle_dot_scaled))
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(6)