from manim import *
from MF_Tools import *

def _glyph_group(mobj, indices):
    return VGroup(*[mobj[0][i] for i in indices])


class TransformWithBoxes(AnimationGroup):
    def __init__(
        self,
        src,
        dst,
        *mappings,                 # same format as TransformByGlyphMap
        box_kwargs=None,
        create_boxes_anim=Create,
        remove_boxes_anim=FadeOut,
        lag_ratio=1.0,
        **kwargs                  # passed to AnimationGroup
    ):
        box_kwargs = box_kwargs or {"color": RED, "buff": 0.1}

        # Build boxes
        boxes = VGroup(*[
            SurroundingRectangle(
                _glyph_group(src, src_inds),
                **box_kwargs
            )
            for src_inds, _ in mappings
        ])

        # Core animation
        transform = TransformByGlyphMap(src, dst, *mappings)

        # Full animation sequence
        animations = [
            create_boxes_anim(boxes),
            transform,
            remove_boxes_anim(boxes),
        ]

        super().__init__(*animations, lag_ratio=lag_ratio, **kwargs)


class BoxesScene(Scene):
    def construct(self):
        failure1 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{y_i}(1-\hat{y}_i)^{1-{y_i}}")
        failure2 = MathTex(r"L=\prod_{i=1}^{n}\hat{y}_i^{0}(1-\hat{y}_i)^{1-{0}}")

        self.play(FadeIn(failure1))

        self.play(
            TransformWithBoxes(
                failure1, failure2,
                ([9,10], [9]),
                ([21,22], [20])
            )
        )

        self.wait(0.5)