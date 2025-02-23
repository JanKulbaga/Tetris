from pyray import *
from typing import Final
from .position import Position
from .color import Color


class Tetromino:
    def __init__(self, id: int) -> None:
        self.id = id
        self.rotation_state = 0
        self.cell_size: Final[int] = 30
        self.row_offset = 0
        self.col_offset = 0
        self.cells: dict[int, list[Position]] = {}
        self.colors: list[Color] = [color for color in Color]

    def on_render(self, offset_x: int, offset_y: int) -> None:
        tiles = self.get_cell_positions()
        for tile in tiles:
            x = tile.col * self.cell_size + offset_x
            y = tile.row * self.cell_size + offset_y
            color = self.colors[self.id].value
            draw_rectangle(x, y, self.cell_size - 1, self.cell_size - 1, color)

    def move(self, rows: int, cols: int) -> None:
        self.row_offset += rows
        self.col_offset += cols

    def rotate(self) -> None:
        self.rotation_state = (self.rotation_state + 1) % len(self.cells)

    def undo_rotate(self) -> None:
        self.rotation_state = (self.rotation_state - 1) % len(self.cells)

    def get_cell_positions(self) -> list[Position]:
        tiles = self.cells[self.rotation_state]
        return [
            Position(tile.row + self.row_offset, tile.col + self.col_offset)
            for tile in tiles
        ]
