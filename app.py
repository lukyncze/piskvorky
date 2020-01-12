from tkinter import *

WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE / 3
GRID_LINE_WIDTH = 2
SYMBOL_SIZE = 0.5
SYMBOL_WIDTH = WINDOW_SIZE/10

BG_COLOR = 'white'
TITLE_COLOR = 'black'
FONT = 'Franklin Gothic'
GRID_COLOR = 'light grey'
X_COLOR = 'dodger blue'
O_COLOR = 'firebrick1'
DRAW_SCREEN_COLOR = 'light sea green'

EMPTY = 0
X = 1
O = 2

FIRST_PLAYER = 1

STATE_TITLE_SCREEN = 0
STATE_X_TURN = 1
STATE_O_TURN = 2
STATE_GAME_OVER = 3


class Game(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.canvas = Canvas(height=WINDOW_SIZE, width=WINDOW_SIZE, bg=BG_COLOR)
        self.canvas.pack()

        self.canvas.bind('<Button-1>', self.click)
        self.bind('<Escape>', self.exit)

        self.gamestate=STATE_TITLE_SCREEN
        self.title_screen()

        self.board=[
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

    def title_screen(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, WINDOW_SIZE, WINDOW_SIZE, fill=TITLE_COLOR, outline='')
        self.canvas.create_text(WINDOW_SIZE/2, WINDOW_SIZE/3, text='TIC TAC TOE', fill=BG_COLOR, font=(FONT, int(-WINDOW_SIZE/12), 'bold'))
        self.canvas.create_text(int(WINDOW_SIZE/2), int(WINDOW_SIZE/2.5), text='[play]', fill=BG_COLOR, font=(FONT, int(-WINDOW_SIZE/25)))
        self.canvas.create_text(int(WINDOW_SIZE/2), int(WINDOW_SIZE/1.25), text='first move:', fill=BG_COLOR, font=(FONT, int(-WINDOW_SIZE/25)))
        self.canvas.create_text(int(WINDOW_SIZE/2), int(WINDOW_SIZE/1.15), text=('X' if FIRST_PLAYER==1 else 'O'), 
            fill=X_COLOR if FIRST_PLAYER==1 else O_COLOR, font=(FONT, int(-WINDOW_SIZE/12)))

    def new_board(self):
        self.canvas.delete('all')

        self.board=[
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

        for n in range(1, 3):
            # vertikálně
            self.canvas.create_line(CELL_SIZE*n, 0, CELL_SIZE*n, WINDOW_SIZE, width=GRID_LINE_WIDTH, fill=GRID_COLOR)
            # horizontálně
            self.canvas.create_line(0, CELL_SIZE*n, WINDOW_SIZE, CELL_SIZE*n, width=GRID_LINE_WIDTH, fill=GRID_COLOR)

    def gameover_screen(self, result):
        self.canvas.delete('all')
        if result == 'X WINS':
            result_text = 'X wins'
            result_color = X_COLOR
        elif result == 'O WINS':
            result_text = 'O wins'
            result_color = O_COLOR
        elif result == 'DRAW':
            result_text = 'Draw'
            result_color = DRAW_SCREEN_COLOR

        self.canvas.create_rectangle(0, 0, WINDOW_SIZE, WINDOW_SIZE, fill=result_color, outline='')
        self.canvas.create_text(int(WINDOW_SIZE/2), int(WINDOW_SIZE/2), text=result_text, fill=BG_COLOR, font=(FONT, int(-WINDOW_SIZE/6), 'bold'))
        self.canvas.create_text(int(WINDOW_SIZE/2), int(WINDOW_SIZE/1.65), text='[click to play again]', fill=BG_COLOR, font=(FONT, int(-WINDOW_SIZE/25)))

    # Logika hry
    def click(self, event):
        x = self.pixels_to_grid(event.x)
        y = self.pixels_to_grid(event.y)

        if self.gamestate == STATE_TITLE_SCREEN:
            self.new_board()
            self.gamestate = FIRST_PLAYER

        elif (self.gamestate == STATE_X_TURN and self.board[y][x] == EMPTY):
            self.new_move(X, x, y)

            if self.has_won(X):
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('X WINS')
            elif self.is_a_draw():
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('DRAW')
            else:
                self.gamestate = STATE_O_TURN

        elif (self.gamestate == STATE_O_TURN and self.board[y][x] == EMPTY):
            self.new_move(O, x, y)

            if self.has_won(O):
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('O WINS')
            elif self.is_a_draw():
                self.gamestate = STATE_GAME_OVER
                self.gameover_screen('DRAW')
            else:
                self.gamestate = STATE_X_TURN

        elif self.gamestate == STATE_GAME_OVER:
            self.new_board()
            self.gamestate = FIRST_PLAYER

        for i in self.board:
            print(i)
        print("---")

    # Logické vykonání tahu
    def new_move(self, player, grid_x, grid_y):
        if player == X:
            self.board[grid_y][grid_x] = X
            self.draw_X(grid_x, grid_y)

        elif player == O:
            self.board[grid_y][grid_x] = O
            self.draw_O(grid_x, grid_y)

    # Vykreslení daného symbolu do buňky, kterou hráč označil
    def draw_X(self, grid_x, grid_y):
        x = self.grid_to_pixels(grid_x)
        y = self.grid_to_pixels(grid_y)
        delta = CELL_SIZE/2*SYMBOL_SIZE

        self.canvas.create_line(x-delta, y-delta, x+delta, y+delta, width=SYMBOL_WIDTH, fill=X_COLOR)
        self.canvas.create_line(x+delta, y-delta, x-delta, y+delta, width=SYMBOL_WIDTH, fill=X_COLOR)

    def draw_O(self, grid_x, grid_y):
        x = self.grid_to_pixels(grid_x)
        y = self.grid_to_pixels(grid_y)
        delta = CELL_SIZE/2*SYMBOL_SIZE

        self.canvas.create_oval(x-delta, y-delta, x+delta, y+delta, width=SYMBOL_WIDTH, outline=O_COLOR)

    # Logika ukončení hry (výhra, remíza)
    def has_won(self, symbol):
        for x in range(3):
            if self.board[x] == [symbol, symbol, symbol]:
                return True
        
        for y in range(3):
            if self.board[0][y] == self.board[1][y] == self.board[2][y] == symbol:
                return True
        
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == symbol:
            return True
        
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] == symbol:
            return True
        
        return False

    def is_a_draw(self):
        for row in self.board:
            if EMPTY in row:
                return False
        return True

    # Funkce umožňující detekci buňky, na kterou zrovna hráč klikl
    def pixels_to_grid(self, pixel_coord):
        if pixel_coord >= WINDOW_SIZE:
            pixel_coord = WINDOW_SIZE - 1    

        grid_coord = int(pixel_coord / CELL_SIZE)
        return grid_coord

    # Funkce sloužící k úmístění symbolu do středu buňky
    def grid_to_pixels(self, grid_coord):
        pixel_coord = grid_coord * CELL_SIZE + CELL_SIZE / 2
        return pixel_coord

    def exit(self, event):
        self.destroy()

def main():
    root = Game()
    root.mainloop()

main()