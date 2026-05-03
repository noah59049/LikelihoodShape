#!/usr/bin/env python

# In order to have our example matrices be realistic, we are generating them from an actual logistic regression model on the sklearn breast cancer dataset

import numpy as np
from data import X, y # type: ignore
from manim import *
from N_Tools import logistic_regression, log_likelihood, as_row, as_col, compute_z_range, surface_from_function

X = as_col(X[:,0]) # We want to have only 2 parameters so we can graph the log-likelihood

def loglik_generator(X, y, add_intercept = True):
    def loglik(beta_hat0, beta_hat1):
        beta_hat = beta_hat0, beta_hat1
        beta_hat = np.array(beta_hat)
        result = log_likelihood(X, y, beta_hat, add_intercept=add_intercept)
        return result
    return loglik

def lik_generator(X, y, add_intercept = True):
    loglik = loglik_generator(X, y, add_intercept = True)
    def lik(beta_hat0, beta_hat1):
        return np.exp(loglik(beta_hat0, beta_hat1))
    return lik

def lik_scaled_generator(X, y, add_intercept = True):
    beta = logistic_regression(X, y, add_intercept = add_intercept, return_stats = False)
    loglik = loglik_generator(X, y)
    mle_loglik = log_likelihood(X, y, beta, add_intercept=add_intercept)
    def lik_scaled(beta_hat0, beta_hat1):
        return np.exp(loglik(beta_hat0, beta_hat1) - mle_loglik)
    return lik_scaled

def create_3d_graph(z_func,
                    x_range,
                    y_range,
                    z_range = "auto",
                    resolution = 32,
                    color = BLUE_C):
    
    z_range = compute_z_range(
        z_func=z_func,
        x_range=x_range,
        y_range=y_range,
        samples=resolution
    )

    axes = ThreeDAxes(
        x_range=(*x_range, (x_range[1] - x_range[0]) / 4),
        y_range=(*y_range, (y_range[1] - y_range[0]) / 4),
        z_range=z_range,
    )

    surface = surface_from_function(
        z_func=z_func,
        axes=axes,
        x_range=x_range,
        y_range=y_range,
        resolution=resolution,
        color=color,
    )

    return axes, surface
    

def create_likelihood_graph(X,
                            y,
                            x_ses = 1,
                            y_ses = 1,
                            add_intercept = True,
                            resolution = 32,
                            color = BLUE_C):
    beta, cov, se = logistic_regression(X, y, add_intercept = add_intercept, return_stats = True)
    beta0, beta1 = beta.flatten()
    se0, se1 = se.flatten()

    x_range = (beta0 - se0 * x_ses, beta0 + se0 * x_ses)
    y_range = (beta1 - se1 * y_ses, beta1 + se1 * y_ses)

    return create_3d_graph(z_func = lik_scaled_generator(X, y),
                           x_range=x_range,
                           y_range = y_range,
                           z_range = "auto",
                           resolution=resolution,
                           color = color)


class PlotSurfaceExample(ThreeDScene):
    def construct(self):
        axes, surface = create_likelihood_graph(X, 
                                         y,
                                         resolution=41)

        if True:
            self.set_camera_orientation(
                phi=55 * DEGREES,
                theta=-45 * DEGREES,
                zoom=0.55
            )

        self.add(axes)
        self.play(Create(surface))
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(6)