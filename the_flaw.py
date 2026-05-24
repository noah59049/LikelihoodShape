import numpy as np
import data # type: ignore
from manim import *
from manim_voiceover import *
from manim_voiceover.services.stitcher import _StitcherService as StitcherService
from N_Tools import *
from tex_colors import *

class FlawScene(ThreeDScene, VoiceoverScene):
    def construct(self):
        self.set_speech_service(StitcherService(r"/Users/noah/Convex/LikelihoodShape/podcasts/the_flaw_podcast2.wav",
        cache_dir="/Users/noah/Convex/LikelihoodShape/cache_dir",
        min_silence_len=2000,
        keep_silence=(0,0)))
        # --- Get our actual log likelihood ---
        X = as_col(data.X[:,0])
        y = data.y
        ses = 0.03
        beta, cov, se = logistic_regression(X, y, add_intercept = True, return_stats = True)
        _loglik = loglik_generator(X, y, add_intercept=True)

        def z_scores_to_betas(u, v):
            return (beta[0] + se[0] * ses * u, beta[1] + se[1] * ses * v)
        def loglik_centered(u, v):
            return _loglik(*z_scores_to_betas(u, v))
        
        z_range = compute_z_range(
            z_func=loglik_centered,
            x_range=[-1,1],
            y_range=[-1,1],
            samples=21
        )
        axes, surface = create_3d_graph(z_func = loglik_centered,
                                        x_range=[-1,1],
                                        y_range = [-1,1],
                                        z_range = z_range,
                                        resolution=21,
                                        color = TEAL_C)
        
        # --- Make the surface ---
        self.set_camera_orientation(
            phi=55 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.55
        )
        with self.voiceover("which is, how do you find the maximum of the log likelihood?") as tracker:
            self.add(axes)
            self.play(Create(surface))
            self.wait(1)
            self.begin_ambient_camera_rotation(rate=0.2)

        # --- Add the MLE dot ---
        mle_z = loglik_centered(0,0)
        start_u = 0.5
        start_v = 1
        start_z = loglik_centered(start_u, start_v)

        with self.voiceover("The standard explanation goes, you set all the derivatives to 0, the logic being, at the max, the derivative must be 0. But this explanation is incomplete. What if it's") as tracker:
            dot = Dot3D(axes.c2p(start_u, start_v, start_z), color=YELLOW)
            self.play(FadeIn(dot))

            u_tracker = ValueTracker(start_u)
            v_tracker = ValueTracker(start_v)

            def gradient(beta_vec): # Could be moved to N_Tools
                # returns [dl/db0, dl/db1] 
                return grad_log_likelihood(X, y, beta_vec, add_intercept=True)
            def gradient_centered(u,v):
                return gradient(np.array(z_scores_to_betas(u,v)))
            """
            def z_scores_to_betas(u, v):
                return (beta[0] + se[0] * ses * u, beta[1] + se[1] * ses * v)
            def loglik_centered(u, v):
                return _loglik(*z_scores_to_betas(u, v))
            """
            # d/du loglik_centered(u,v) = se[0] * ses * dl/dbhat0
            # d/dv loglik_centered(u,v) = se[1] * ses * dl/dbhat1
            def visual_gradient(u,v):
                return gradient_centered(u,v) * se * ses
            
            deriv_tex = always_redraw(lambda: VGroup(
                ColoredMathTex(
                    r"\frac{\partial \ell}{\partial \hat{\beta}_0} = "
                    f"{gradient_centered(u_tracker.get_value(), v_tracker.get_value())[0]:.3f}"
                ),
                ColoredMathTex(
                    r"\frac{\partial \ell}{\partial \hat{\beta}_1} = "
                    f"{gradient_centered(u_tracker.get_value(), v_tracker.get_value())[1]:.3f}"
                )
            ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL))
            self.add_fixed_in_frame_mobjects(deriv_tex)
            self.play(FadeIn(deriv_tex))
            
            dot.add_updater(lambda d: d.move_to(
                axes.c2p(
                    u_tracker.get_value(),
                    v_tracker.get_value(),
                    loglik_centered(u_tracker.get_value(), v_tracker.get_value())
                )
            ))

            initial_g = visual_gradient(start_u, start_v)
            initial_vis_g_norm = np.linalg.norm(initial_g)
            arrow_scale = 0.1 / initial_vis_g_norm

            def make_gradient_arrow():
                u = u_tracker.get_value()
                v = v_tracker.get_value()
                g = visual_gradient(u,v)
                start_pt = np.array(axes.c2p(u, v, loglik_centered(u, v)))
                end_u = u + g[0] * arrow_scale
                end_v = v + g[1] * arrow_scale
                end_pt = np.array(axes.c2p(end_u, end_v, loglik_centered(end_u, end_v)))
                if np.linalg.norm(end_pt - start_pt) < 1e-6:
                    end_pt = start_pt + np.array([1e-6, 0, 0])
                return Arrow3D(start=start_pt, end=end_pt, color=ORANGE)

            gradient_arrow = always_redraw(make_gradient_arrow)
            self.add(gradient_arrow)

            # Do gradient descent
            LR = 0.01
            curr = np.array((start_u, start_v))
            grad_steps = [curr]
            while np.linalg.norm(gradient_centered(*curr)) > 2.5e-5:
                curr = curr + LR * visual_gradient(*curr)
                grad_steps.append(curr)
                if len(grad_steps) > 10000:
                    print(f"We're not there yet {visual_gradient(*curr)=} {curr=}")
                    break
            grad_steps = np.vstack(grad_steps)
            

            path_alphas = np.linspace(0, 1, len(grad_steps))

            def update_trackers(mob, alpha):
                u_tracker.set_value(float(np.interp(alpha, path_alphas, grad_steps[:, 0])))
                v_tracker.set_value(float(np.interp(alpha, path_alphas, grad_steps[:, 1])))

            self.play(
                UpdateFromAlphaFunc(VMobject(), update_trackers),
                run_time=4,
                rate_func=linear
            )
            

            # --- Force a clean rebuild of the MathTex ---
            gradient_arrow.clear_updaters()
            self.remove(gradient_arrow)
            deriv_tex.clear_updaters()
            self.remove(deriv_tex)

            deriv_tex = VGroup(
                ColoredMathTex(
                    r"\frac{\partial \ell}{\partial \hat{\beta}_0} = "
                    f"{gradient_centered(u_tracker.get_value(), v_tracker.get_value())[0]:.3f}"
                ),
                ColoredMathTex(
                    r"\frac{\partial \ell}{\partial \hat{\beta}_1} = "
                    f"{gradient_centered(u_tracker.get_value(), v_tracker.get_value())[1]:.3f}"
                )
            ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)

            self.add_fixed_in_frame_mobjects(deriv_tex)

        return
        # --- Define the functions for what if the log likelihood is something else ---
        def upside_down_loglik(beta_hat0, beta_hat1):
            return 2 * mle_z - loglik(beta_hat0, beta_hat1)
        def saddle_loglik_centered(beta_hat0, beta_hat1):
            return loglik(beta_hat0, beta_hat1) - \
                   loglik(*rotate_90_cw(mle_x, mle_y, beta_hat0, beta_hat1, x_scale = se[0], y_scale = se[1])) + \
                   mle_z
        def bump(beta_hat0, beta_hat1):
            x0 = mle_x + se[0] * ses / 2 # I would rather do this with eigenvectors or something
            y0 = mle_y - se[1] * ses / 2 # I would rather do this with eigenvectors or something
            x_screen = (beta_hat0 - x0) / (se[0] * ses / 6)
            y_screen = (beta_hat1 - y0) / (se[1] * ses / 6)
            z_scale = (z_range[1] - z_range[0]) / 4
            exponential = np.exp(-(x_screen**2 + y_screen**2))
            return exponential * z_scale
        def bumped_loglik(beta_hat0, beta_hat1):
            return loglik(beta_hat0, beta_hat1) + bump(beta_hat0, beta_hat1)
        
        # --- Play the animations for what if it's a minimum, saddle, or local non global max ---
        for z_func in upside_down_loglik, saddle_loglik, bumped_loglik:
            with self.voiceover("a local minimum instead? Or") as tracker:
                _, surface2 = create_3d_graph(z_func = z_func,
                                            x_range=x_range,
                                            y_range = y_range,
                                            z_range = z_range,
                                            resolution=21,
                                            color = TEAL_C)
                surface.save_state()
                usable_time = tracker.duration - 0.1
                if usable_time > 2:
                    self.play(Transform(surface, surface2))
                    self.wait(usable_time - 2)
                    self.play(Restore(surface))
                else:
                    self.play(Transform(surface, surface2, run_time = usable_time / 2))
                    self.play(Restore(surface, run_time = usable_time / 2))

        if False:
            with self.voiceover("a saddle point? Or ") as tracker:
                pass
            with self.voiceover("a local maximum, but not the global maximum?") as tracker:
                pass