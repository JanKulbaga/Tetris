from pyray import *
from .color import Color


class GameEngine:
    def __init__(self, width: int, height: int, title: str, fps: int = 10) -> None:
        init_window(width, height, title)
        set_target_fps(fps)

    def run(self) -> None:
        while not window_should_close():
            begin_drawing()

            clear_background(Color.Gray.value)
            self.on_update()
            self.on_render()

            end_drawing()
        close_window()

    def on_update(self) -> None:
        raise NotImplementedError("on_update(self)")

    def on_render(self) -> None:
        raise NotImplementedError("on_render(self)")
