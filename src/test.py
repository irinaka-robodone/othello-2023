import pyxel

class OthelloGame:
    def __init__(self):
        self.board_size = 8
        self.cell_size = 30
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]  # 8x8の盤面
        self.current_player = 1  # 1: プレイヤー1, 2: プレイヤー2
        pyxel.init(self.board_size * self.cell_size, self.board_size * self.cell_size)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x, pyxel.mouse_y
            row, col = y // self.cell_size, x // self.cell_size
            if self.is_valid_move(row, col):
                self.place_piece(row, col)
                self.switch_player()

    def is_valid_move(self, row, col):
        # 有効な移動かチェックするロジック
        return self.board[row][col] == 0

    def place_piece(self, row, col):
        # 現在のプレイヤーに応じて駒を配置
        self.board[row][col] = self.current_player

    def switch_player(self):
        # プレイヤーを切り替える
        self.current_player = 1 if self.current_player == 2 else 2

    def draw(self):
        pyxel.cls(0)
        # 盤面と駒の描画
        for row in range(self.board_size):
            for col in range(self.board_size):
                x, y = col * self.cell_size, row * self.cell_size
                pyxel.rect(x, y, self.cell_size, self.cell_size, 11)  # グレーのセル
                if self.board[row][col] != 0:
                    color = 0 if self.board[row][col] == 1 else 7  # プレイヤー1は黒、プレイヤー2は白
                    pyxel.circ(x + self.cell_size // 2, y + self.cell_size // 2, self.cell_size // 2 - 2, color)


if __name__ == "__main__":
    OthelloGame()
