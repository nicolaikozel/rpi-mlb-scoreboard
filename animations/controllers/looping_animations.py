import time
from typing import Dict, List

from animations.base_animations import BaseAnimation


class LoopingAnimationsController(BaseAnimation):
    def __init__(
        self,
        animations: List[BaseAnimation],
        max_cycles: int = None,
        wait_until_armed: bool = False,
    ):
        super().__init__(max_cycles, wait_until_armed)
        self._animations = animations
        self._animation_index = 0
        self._current_animation = self._animations[self._animation_index]

    def _reset(self):
        self._animation_index = 0
        for animation in self._animations:
            animation.reset()
        self._current_animation = self._animations[self._animation_index]

    def _advance_frame(self, canvas):
        if self._current_animation.finished:
            self._animation_index += 1
            if self._animation_index >= len(self._animations):
                self.reset()
            else:
                self._current_animation = self._animations[self._animation_index]
                self._current_animation.reset()

    def _render_frame(self, canvas):
        self._current_animation.render(canvas)
