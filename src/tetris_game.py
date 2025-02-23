from pyray import Font, Vector2
from .tetromino import Tetromino
from .tetrominos import (
    ITetromino,
    JTetromino,
    LTetromino,
    OTetromino,
    STetromino,
    TTetromino,
    ZTetromino,
)
from .game_engine import GameEngine
from .grid import Grid
import random
import os
from pyray import *
from raylib.defines import KEY_LEFT, KEY_RIGHT, KEY_DOWN, KEY_UP, GLFW_KEY_R
from .color import Color


class TetrisGame(GameEngine):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.reset()
        self.last_update_time = 0
        self.font: Font = load_font_ex(
            os.path.join("font", "monogram.ttf"), 64, None, 0
        )

    def on_update(self) -> None:
        self.handle_input()
        if self.event_triggered(0.2):
            self.move_block_down()

    def on_render(self):
        self.grid.on_render()
        self.current_block.on_render(11, 11)

        draw_text_ex(self.font, "Score", (360, 15), 38, 2, WHITE)
        draw_rectangle_rounded((320, 55, 170, 60), 0.3, 6, Color.LightBlack.value)
        text_size: Vector2 = measure_text_ex(self.font, str(self.score), 38, 2)
        draw_text_ex(
            self.font,
            str(self.score),
            (320 + (170 - text_size.x) / 2, 65),
            38,
            2,
            WHITE,
        )

        draw_text_ex(self.font, "Next", (370, 175), 38, 2, WHITE)
        draw_rectangle_rounded((320, 215, 170, 180), 0.3, 6, Color.LightBlack.value)
        if self.next_block.id == 3:  # ITetromino
            self.next_block.on_render(255, 290)
        elif self.next_block.id == 4:  # OTetromino
            self.next_block.on_render(255, 280)
        else:
            self.next_block.on_render(270, 270)

        if self.game_over:
            draw_text_ex(self.font, "GAME OVER", (320, 450), 38, 2, WHITE)
            draw_text_ex(self.font, "Press R to", (330, 510), 28, 2, WHITE)
            draw_text_ex(self.font, "restart", (355, 540), 28, 2, WHITE)

    def get_all_tetromino_blocks(self) -> list[Tetromino]:
        return [
            LTetromino(),
            JTetromino(),
            ITetromino(),
            OTetromino(),
            STetromino(),
            TTetromino(),
            ZTetromino(),
        ]

    def get_random_tetromino_block(self) -> Tetromino:
        if not self.tetromino_blocks:
            self.tetromino_blocks = self.get_all_tetromino_blocks()
        block: Tetromino = random.choice(self.tetromino_blocks)
        self.tetromino_blocks.remove(block)
        return block

    def handle_input(self) -> None:
        if self.game_over and is_key_pressed(GLFW_KEY_R):
            self.game_over = False
            self.reset()

        if is_key_down(KEY_LEFT) and not self.game_over:
            self.current_block.move(0, -1)
            if self.is_block_outside() or not self.block_fits():
                self.current_block.move(0, 1)
        elif is_key_down(KEY_RIGHT) and not self.game_over:
            self.current_block.move(0, 1)
            if self.is_block_outside() or not self.block_fits():
                self.current_block.move(0, -1)
        elif is_key_down(KEY_DOWN) and not self.game_over:
            self.move_block_down()
            self.update_score(0, 1)
        elif is_key_pressed(KEY_UP) and not self.game_over:
            self.current_block.rotate()
            if self.is_block_outside() or not self.block_fits():
                self.current_block.undo_rotate()

    def move_block_down(self) -> None:
        if self.game_over:
            return
        self.current_block.move(1, 0)
        if self.is_block_outside() or not self.block_fits():
            self.current_block.move(-1, 0)
            self.lock_block()

    def is_block_outside(self) -> bool:
        cells = self.current_block.get_cell_positions()
        for tile in cells:
            if self.grid.is_cell_outside(tile.row, tile.col):
                return True
        return False

    def lock_block(self) -> None:
        cells = self.current_block.get_cell_positions()
        for tile in cells:
            self.grid.set(tile.row, tile.col, self.current_block.id)
        self.current_block = self.next_block
        if not self.block_fits():
            self.game_over = True
        self.next_block = self.get_random_tetromino_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)

    def event_triggered(self, interval: float) -> bool:
        current_time = get_time()
        if current_time - self.last_update_time >= interval:
            self.last_update_time = current_time
            return True
        return False

    def block_fits(self) -> bool:
        cells = self.current_block.get_cell_positions()
        for tile in cells:
            if not self.grid.is_cell_empty(tile.row, tile.col):
                return False
        return True

    def reset(self) -> None:
        self.grid = Grid(20, 10)
        self.tetromino_blocks = self.get_all_tetromino_blocks()
        self.current_block = self.get_random_tetromino_block()
        self.next_block = self.get_random_tetromino_block()
        self.score = 0
        self.game_over = False

    def update_score(self, lines_cleared: int, move_down_points: int) -> None:
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points
