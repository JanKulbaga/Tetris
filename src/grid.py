from pyray import *
from typing import Final
from .color import Color


class Grid:
    def __init__(self, rows: int, cols: int) -> None:
        self.rows = rows
        self.cols = cols
        self.cell_size: Final[int] = 30
        self.grid: list[int] = [0] * (rows * cols)
        self.colors: list[Color] = [color for color in Color]

    def on_render(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + 11
                y = row * self.cell_size + 11
                value = self.get(row, col)
                color = self.colors[value].value
                draw_rectangle(x, y, self.cell_size - 1, self.cell_size - 1, color)

    def get(self, row: int, col: int) -> int:
        return self.grid[row * self.cols + col]

    def set(self, row: int, col: int, value: int) -> None:
        self.grid[row * self.cols + col] = value

    def is_cell_outside(self, row: int, col: int) -> bool:
        return not (0 <= row < self.rows and 0 <= col < self.cols)

    def is_cell_empty(self, row: int, col: int) -> bool:
        return self.get(row, col) == 0

    def is_row_full(self, row: int) -> bool:
        for col in range(self.cols):
            if self.get(row, col) == 0:
                return False
        return True

    def clear_row(self, row: int) -> None:
        for col in range(self.cols):
            self.set(row, col, 0)

    def move_row_down(self, row: int, num_rows: int) -> None:
        for col in range(self.cols):
            self.set(row + num_rows, col, self.get(row, col))
            self.set(row, col, 0)

    def clear_full_rows(self) -> int:
        completed = 0
        for row in range(self.rows - 1, -1, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed += 1
            elif completed > 0:
                self.move_row_down(row, completed)
        return completed
