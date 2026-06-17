###################################################################################
### This is a list of functions I find useful but were written by other people. ###
###################################################################################
from manim import * 

# Written by GniLudio
class Combine(AnimationGroup):
    def _setup_scene(self, scene: Scene) -> None:
        super()._setup_scene(scene)
        self._scene = scene
        self._initial_mobjects = {
            animation.mobject: animation.mobject.copy() for animation in self.animations
        }

    def interpolate(self, alpha: float) -> None:
        for mobject, initial_mobject in self._initial_mobjects.items():
            mobject.become(initial_mobject)
        for animation in self.animations:
            animation._setup_scene(self._scene)
            animation.begin()
            animation.interpolate(alpha)