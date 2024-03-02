import pyxel
import sounddevice as sd
import soundfile as sf

from text import BDFRenderer

font_path = "assets/font/umplus_j12r.bdf"



class App:
    def __init__(self):
        # 画面サイズの設定
        self.width = 320
        self.height = 320
        self.state = "start"
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        #8x8の真ん中のところに白と黒の駒を配置 
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        
        self.cell_size = 30
        pyxel.init(self.width,self.height, title="オセロゲーム", display_scale=2)
        # フォントを日本語にする
        self.font = BDFRenderer(font_path)
        # マウスを使えるようにする
        pyxel.mouse(True)
        # 音のファイルを読み込む
        click_sound = "assets/othello_sound.wav"
        self.audio, self.sample_rate = sf.read(click_sound, always_2d=True)
        self.current_player = 1
        self.board_size = 8
        self.player_stones = [0, 0]
        self.pass_count = {1: 0, 2: 0}
        if not self.can_place_piece(1) and not self.can_place_piece(2) or self.is_board_full():
            self.check_game_over()

        # ゲーム開始
    
        pyxel.run(self.update, self.draw)
        
    def reset(self):
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        #8x8の真ん中のところに白と黒の駒を配置 
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        self.current_player = 1
        self.player_stones = [0, 0]
        self.pass_count = {1: 0, 2: 0}

    def update(self):
        cell_size=self.cell_size
        # ゲームのロジックを更新する関数
        if self.state == "start":
            self.reset()
            self.update_start()
        # クリックでオセロの駒を置く     
        if self.state == "play":
            self.place_koma()
            self.pass_turn()
            self.count_stones()
            if self.is_game_over():
                self.check_game_over()
        
        if self.state == "result":
            self.clear_game()
        

    def is_game_over(self):
        # 盤面に空きマスがないか、どちらかのプレイヤーの駒のみで埋まっているかをチェック
        black, white, empty = 0, 0, 0
        for row in self.board:
            for cell in row:
                if cell == 1:
                    black += 1
                elif cell == 2:
                    white += 1
                else:
                    empty += 1

        if empty == 0 or black == 0 or white == 0:
            return True
        return False
    
    def pass_turn(self):
        if pyxel.btnp(pyxel.KEY_P):
            if self.current_player == 1:
                if self.pass_count[self.current_player] < 3:
                    self.pass_count[self.current_player] += 1  # パス回数をインクリメント
                    self.switch_player()  # プレイヤーを切り替える
            
            elif self.current_player == 2:
                if self.pass_count[self.current_player] < 3:
                    self.pass_count[self.current_player] += 1  # パス回数をインクリメント
                    self.switch_player()  # プレイヤーを切り替える

    def show_winner(self):
        # 各プレイヤーの駒の数を数えて勝者を決定
        black, white = 0, 0
        for row in self.board:
            for cell in row:
                if cell == 1:
                    black += 1
                elif cell == 2:
                    white += 1

        winner = "引き分け"
        if black > white:
            winner = "黒の勝ち"
            
        elif white > black:
            winner = "白の勝ち"
        # 勝者を画面上に表示
        pyxel.text(50, 100, winner, 7)
        

# ...（メイン関数）
    def is_valid_move(self, row, col):
        # 有効な移動かチェックするロジック
        # "self.board"が0だったら置けるようにする
        if self.board[row][col] != 0:
            return False
        # 8方向のいずれかで相手のコマを挟めるかチェック
        for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    if self.can_flip(row, col, dx, dy):
                        return True
        return False
        
    def can_flip(self, row, col, dx, dy):
        # 特定の方向に対して相手の駒を挟めるかどうかをチェック
        x, y = col + dx, row + dy
        has_opponent_piece = False
        while 0 <= x < self.board_size and 0 <= y < self.board_size:
            if self.board[y][x] == 3 - self.current_player:
                has_opponent_piece = True
                x += dx
                y += dy
            elif self.board[y][x] == self.current_player and has_opponent_piece:
                return True
            else:
                break
        return False

    def place_koma(self):
        x, y = pyxel.MOUSE_POS_X, pyxel.MOUSE_POS_Y
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x - 40, pyxel.mouse_y - 40
            x, y = x // self.cell_size , y // self.cell_size
            if x < 0 or x >= 8:
                return
            
            if y < 0 or y >= 8:
                return
        
            if self.is_valid_move(y, x):
                self.board[y][x] = self.current_player
                self.flip_pieces(x, y)
                sd.play(self.audio, self.sample_rate)
                self.switch_player()
        
    def flip_pieces(self, x, y):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                self.flip_in_direction(x, y, dx, dy)
            
    def flip_in_direction(self, col, row, dx, dy):
        
        x, y = col + dx, row + dy
        pieces_to_flip = []
        print(x, y)
        while 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[y][x] == 3 - self.current_player:
            
            pieces_to_flip.append((y, x))
            x += dx
            y += dy
        if 0 <= x < self.board_size and 0 <= y < self.board_size and self.board[y][x] == self.current_player:
            for y, x in pieces_to_flip:
                print(x, y)
                self.board[y][x] = self.current_player
        
    def switch_player(self):
        self.current_player = 1 if self.current_player == 2 else 2
        
    def update_start(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = "play"
    #　ステートを"play"に変更する 
    
    def draw_count(self):
        self.font.draw_text(300, 0, str(self.player_stones[0]),7)
        self.font.draw_text(275, 0, "白")
        self.font.draw_text(300, 20, str(self.player_stones[1]),7)
        self.font.draw_text(275, 20, "黒")


        
    def draw(self):
        pyxel.cls(3)
        if self.state == "start":
            self.draw_start_screen()
        if self.state == "play":
            self.draw_play_screen()
            self.draw_koma()
            self.draw_count()
            self.draw_info()
        if self.state == "result":
            self.draw_result()
            
    def draw_start_screen(self):
        # スタート画面の描画
        self.font.draw_text(120, 50, "オセロゲーム", 7)
        self.font.draw_text(115, 100, "Spaceでスタート", 7)
        # オセロゲーム　spaceでスタートとでる
        
    
    
        
    def count_stones(self):
        self.player_stones = [0, 0]
        for row in self.board:
            for cell in row:
                if cell == 1:
                    self.player_stones[0] += 1
                elif cell == 2:
                    self.player_stones[1] += 1
                    print(self.player_stones)
            
    def draw_play_screen(self):

        cell_size = self.cell_size
        # オセロボードの描画
        for i in range(9):
            pyxel.line(40, 40 + i * cell_size, 280, 40 + i * cell_size, 7)
            # 垂直線
            pyxel.line(40 + i * cell_size, 40, 40 + i * cell_size, 280, 7)
        #オセロボードの描画
        
        
    def draw_koma(self):
        
        cell_size = self.cell_size
        for y, row in enumerate(self.board): #　マスの番号と中身をどちらも取り出す
            for x, koma in enumerate(row):
                if koma == 1:
                    pyxel.circ(self.cell_size +(x+0.83) * cell_size, self.cell_size + (y+0.83) * cell_size, 12,7)
                if koma == 2:
                    pyxel.circ(self.cell_size + (x+0.83) * cell_size, self.cell_size + (y+0.83) * cell_size, 12,0)
    
    def draw_info(self):
        if self.current_player == 1:
            self.font.draw_text(107, 10, "現在のターン：白", 7)
        else:
            self.font.draw_text(107, 10, "現在のターン：黒", 7)
        self.font.draw_text(50, 285, "Pキーでパス", 7)
        self.font.draw_text(120, 285, "パスは3回まで", 7)
        
    def can_place_piece(self, player):
        # playerが駒を置ける場所があるかどうかをチェック
        for row in range(8):
            for col in range(8):
                if self.is_valid_move(row, col):
                    return True
        return False

    def is_board_full(self):
        # 盤面がすべて埋まっているかどうかをチェック
        for row in range(8):
            for col in range(8):
                if self.board[row][col] == 0:
                    return False
        return True

    def check_game_over(self):
        # ゲーム終了時の勝敗判定と表示
        black, white = self.count_pieces()
        if black > white:
            winner = "白の勝ち"
        elif white > black:
            winner = "黒の勝ち"
        else:
            winner = "引き分け"
        self.winner = winner
        print(winner)  # またはpyxel.textを使用して画面に表示
        self.state = "result"

    def count_pieces(self):
        # 黒と白の駒の数をカウント
        black = sum(row.count(1) for row in self.board)
        white = sum(row.count(2) for row in self.board)
        return black, white
    
    def clear_game(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.state = "start"

    def draw_result(self):
        self.font.draw_text(130, 75 , self.winner, 7)
        self.font.draw_text(160, 95, str(self.player_stones[0]), 7)
        pyxel.circ(145, 100, 9, 7)
        self.font.draw_text(160, 115, str(self.player_stones[1]), 7)
        pyxel.circ(145, 120, 9, 0)
        self.font.draw_text(120, 150, "Spaceで再戦", 7)
            
if __name__ == "__main__":
    App()