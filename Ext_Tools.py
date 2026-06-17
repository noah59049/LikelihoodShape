###################################################################################
### This is a list of functions I find useful but were written by other people. ###
###################################################################################
from manim import * 

# Written by GniLudio
class Combine(AnimationGroup):
    """
    If you want to combine animations on the same object(s):
    """
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

# Written by nikolaj
def count_animations(scene : Scene, **config_kwargs):
    """
    Here's a stupid little utility function. I've got a scene which builds its list of animation depending on some starting input (for example, a BFS animation whose length depends on the actual graph input). The total number of animations can get quite large, and I needed to be able to count how many animations were being played for a given input without having to wait for the actual animation to render and play.
    """
    options = {
        "frame_size": (1,1),
        "frame_rate": 1,
        "save_last_frame": True,
        "dry_run": True,
        "verbosity": "ERROR",
        "progress_bar": "none",
    } | config_kwargs
    with tempconfig(options):
        if not isinstance(scene, Scene):
            scene = scene()
        scene.render()
        return scene.renderer.num_plays
    
