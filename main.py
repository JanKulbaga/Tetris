from src.tetris_game import TetrisGame


def main() -> None:
    tetris_game = TetrisGame(500, 620, "Tetris")
    tetris_game.run()


if __name__ == "__main__":
    main()
