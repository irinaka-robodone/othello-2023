import pyxel
from text import BDFRenderer

font_path = "assets/font/umplus_j12r.bdf"



class App:
    def __init__(self):
        # 画面サイズの設定
        self.width = 256
        self.height = 256
        self.state = "start"
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        
        self.cell_size = 25
        pyxel.init(self.width,self.height, title="オセロゲーム")
        self.font = BDFRenderer(font_path)
        # フォントを日本語にする
        pyxel.mouse(True)
        # マウスを使えるようにする
        self.current_player = 1
        self.board_size = 8
        # ゲーム開始
    
        pyxel.run(self.update, self.draw)
        
        
        

    def update(self):
        # ゲームのロジックを更新する関数
        if self.state == "start":
            self.update_start()
    
        
        
        # クリックでオセロの駒を置く     
        if self.state == "play":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                x, y = pyxel.mouse_x - 28, pyxel.mouse_y - 28
                x, y = x // 25 , y // 25
                if self.is_valid_move(y, x):
                    self.place_koma(x, y)
                    self.switch_player()
                    
    
    def is_valid_move(self, row, col):
        # 有効な移動かチェックするロジック
        # "self.board"が0だったら置けるようにする
        return self.board[row][col] == 0
    


    def place_koma(self, x, y):
        self.board[y][x] = self.current_player
        self.flip_pieces(x, y)
            
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
    
    def draw(self):
        pyxel.cls(3)
        if self.state == "start":
            self.draw_start_screen()
        if self.state == "play":
            self.draw_play_screen()
            self.draw_koma()
            
    def draw_start_screen(self):
        # スタート画面の描画
        self.font.draw_text(90, 50, "オセロゲーム", pyxel.frame_count % 15)
        self.font.draw_text(85, 100, "Spaceでスタート", 7)
        # オセロゲーム　spaceでスタートとでる

            
    def draw_play_screen(self):

        cell_size = self.cell_size
        # オセロボードの描画
        for row in range(8):
            for i in range(9):  # 8x8グリッドのため、9本の線を描画
                # 水平線
                pyxel.line(28, (i+1) * cell_size, 228, (i+1) * cell_size, 7)
                # 垂直線
                pyxel.line((i+1) * cell_size, 28, (i+1) * cell_size, 228, 7)
        #オセロボードの描画 
    def draw_koma(self):
        
        cell_size = self.cell_size
        for y, row in enumerate(self.board): #　マスの番号と中身をどちらも取り出す
            for x, koma in enumerate(row):
                if koma == 1:
                    pyxel.circ(28 +(x+0.4) * cell_size, 28 + (y+0.37) * cell_size, 11,7)
                if koma == 2:
                    pyxel.circ(28 + (x+0.4) * cell_size, 28 + (y+0.37) * cell_size, 11,0)
            #8x8の真ん中のところに白と黒の駒を配置 
                    
                
if __name__ == "__main__":
    App()