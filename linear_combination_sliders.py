from manim import *

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

    def SlideTo(self, scene, new_value, run_time=1):
        # Clamp to allowed range (prevents nonsense values)
        new_value = max(self.min_val, min(self.max_val, new_value))
        scene.play(self.value.animate.set_value(new_value), run_time=run_time)


class SliderDemo(Scene):
    def construct(self):
        sliders = VGroup(*[
            VerticalSlider(label_text=f"X_{i+1}")
            for i in range(5)
        ])

        sliders.arrange(RIGHT, buff=1.2)

        self.add(sliders)

        self.wait()

        sliders[0].SlideTo(self, 0.8)
        sliders[1].SlideTo(self, 0.2)
        sliders[2].SlideTo(self, 1.0)
        sliders[3].SlideTo(self, 0.0)
        sliders[4].SlideTo(self, 0.6)

        self.wait()