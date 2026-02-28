import numpy as np
from manim import *

class VerticalSlider(VGroup):
    def __init__(
        self,
        label_text="X_1",
        value_range=(0, 1),
        length=4,
        initial_value=0.5,
        **kwargs
    ):
        super().__init__(**kwargs)

        self.min_val, self.max_val = value_range

        # Value tracker
        self.value = ValueTracker(initial_value)

        # Vertical number line
        self.line = NumberLine(
            x_range=[self.min_val, self.max_val, 0.1],
            length=length,
            include_ticks=False,
            include_numbers=False,
        ).rotate(PI / 2)

        # Knob
        self.knob = Dot(color=BLUE)
        self.knob.add_updater(
            lambda m: m.move_to(self.line.n2p(self.value.get_value()))
        )

        # Label
        self.label = Tex(f"${label_text}$")
        self.label.next_to(self.line, DOWN, buff=0.3)

        self.add(self.line, self.knob, self.label)

    def getSlideTo(self, new_value):
        # Clamp to allowed range (prevents nonsense values)
        new_value = max(self.min_val, min(self.max_val, new_value))
        return self.value.animate.set_value(new_value)

class VerticalSliderGroup(VGroup):
    def __init__(
        self,
        labels,
        value_range=(0, 1),
        length=4,
        initial_values=None,
        **kwargs
    ):
        super().__init__(**kwargs)

        if initial_values == None:
            initial_values = [np.mean(value_range)] * len(labels)

        self.sliders = VGroup(*[VerticalSlider(label_text = label,
                                               value_range = value_range,
                                               length = length,
                                               initial_value = initial_value)
                                               for label, initial_value in zip(labels, initial_values)])
        self.sliders.arrange(RIGHT, buff=1.2)
        self.add(self.sliders)
    
    def slideTo(self, scene, values, run_time = 1):
        assert len(values) == len(self.sliders)
        animations = [self.sliders[i].getSlideTo(value) for i, value in enumerate(values)]
        scene.play(*animations, run_time = run_time)

class SliderDemo(Scene):
    def construct(self):
        sliders = VerticalSliderGroup(labels = [f"X_1", "X_2", "X_3", "X_4", r"\ln\frac{p}{1-p}"])

        self.add(sliders)

        self.wait()

        sliders.slideTo(self, (0,0.2,0.4,0.6,0.8))

        self.wait()


# Script:
"""
If you change one of the Xs, the change in the log odds will be proportional to how much the X changes. 
In other words, it will vary linearly.
If the beta associated with an X is small, then changing X leads to a small change in log odds.
If the beta associated with an X is large, then changing X leads to a large change in log odds.
If the beta is positive, then increasing X increases log odds.
If the beta is negative, then increasing X decreases log odds.
The betas are called regression coefficients, 
and each one determines how much its respective predictor variable affects the log odds.
The beta 0 is just a constant term. If we didn't have it, then our model would always assume that
the log odds are 0 when all the Xs are 0, which we don't want.

A word of caution though: talking about a small or a large change can be highly misleading
if you don't account for the units you're using.

Like, here the beta 1, the beta for the mean radius variable, is ____.
If I decide to measure mean radius in millimeters instead of centimeters [TODO: Check that we use cm right now]
the beta would be much lower. But that doesn't mean that the effect is smaller; it's literally the same data.

In practice this is not that big of a problem because of how we interpret the coefficients.
If we increase one of our predictors by 1, then the log odds will increase by the amount of that beta.
So hence, an interpretation could go something like this:
If mean radius increases by 1 cm, then the log odds of breast cancer being malignant increase by ____.

Except that's not quite how we do it, for the simple reason that statements like
"the log odds of breast cancer being malignant increase by ____" are hard to wrap your head around.

Instead we talk about odds ratios. To do that, we exponentiate this equation.
So then, if we increase, say, X1 by 1, that means you multiply the odds by e^beta 1.

"If mean radius increases by 1 cm, then the odds of breast cancer being malignant increase by a factor of ____."
And this is an odds ratio of _____.

This interpretation is also missing a little detail, 
which is that this is how you would interpret the coefficients if you knew them for sure.
But in real life, you almost never know the coefficients. You just have your best estimates of them.
So instead of the above, you would say something like,
"If mean radius increases by 1 cm, then THE MODEL PREDICTS THAT 
the odds of breast cancer being malignant increase by a factor of ____."
The "MODEL PREDICTS" part is important to clarify that it's a prediction your model made, 
not a fact about the world that you know for sure.

But how do we estimate the betas? That transitions nicely into the next point, 
which is maximum likelihood estimation.
In order to do maximum likelihood estimation, we need to rewrite the regression equation so we isolate p.
"""