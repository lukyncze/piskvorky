from tkinter import *

WINDOW_SIZE = 600
CELL_SIZE = WINDOW_SIZE / 3
GRID_LINE_WIDTH = 2

BG_COLOR = 'white'
TITLE_COLOR = 'black'
FONT = 'Franklin Gothic'
GRID_COLOR = 'light grey'

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

        self.gamestate=STATE_TITLE_SCREEN
        self.title_screen()

        self.board=[
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

    def title_screen(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(0, 0, WINDOW_SIZE, WINDOW_SIZE, fill=TITLE_COLOR, outline='')
        self.canvas.create_text(WINDOW_SIZE/2, WINDOW_SIZE/3, text='TIC TAC TOE', fill='white', font=(FONT, int(-WINDOW_SIZE/12), 'bold'))
        self.canvas.create_text(int(WINDOW_SIZE/2), int(WINDOW_SIZE/2.5), text='[play]', fill='white', font=(FONT, int(-WINDOW_SIZE/25)))

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

    def gameover_screen(self):
        pass

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
            elif self.is_a_draw():
                self.gamestate = STATE_GAME_OVER
            else:
                self.gamestate = STATE_O_TURN

        elif (self.gamestate == STATE_O_TURN and self.board[y][x] == EMPTY):
            self.new_move(O, x, y)

            if self.has_won(O):
                self.gamestate = STATE_GAME_OVER
            elif self.is_a_draw():
                self.gamestate = STATE_GAME_OVER
            else:
                self.gamestate = STATE_X_TURN

        for i in self.board:
            print(i)
        print("---")

    # Logické vykonání tahu
    def new_move(self, player, grid_x, grid_y):
        if player == X:
            self.board[grid_y][grid_x] = X

        elif player == O:
            self.board[grid_y][grid_x] = O

    def draw_X(self):
        pass

    def draw_O(self):
        pass

    def has_won(self, symbol):
        pass

    def is_a_draw(self):
        pass

    # Funkce umožňující detekci buňky, na kterou zrovna hráč klikl
    def pixels_to_grid(self, pixel_coord):
        grid_coord = int(pixel_coord / CELL_SIZE)
        return grid_coord

def main():
    root = Game()
    root.mainloop()

main()