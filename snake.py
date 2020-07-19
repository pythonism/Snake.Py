import random
import time
import tkinter


def teleport(coordinates):
    if coordinates[2] > 600:
        coordinates[2] = 10
        coordinates[0] = 0

    if coordinates[0] < 0:
        coordinates[0] = 590
        coordinates[2] = 600

    if coordinates[1] < 0:
        coordinates[1] = 390
        coordinates[3] = 400

    if coordinates[3] > 400:
        coordinates[3] = 10
        coordinates[1] = 0

    return coordinates


class Snake:
    def __init__(self, board):
        self.board = board
        self.snake_items = []

        x = 5
        y = 5

        for i in range(10):
            self.snake_items.append(self.board.create_rectangle(x, y, x + 10, y + 10, fill='green'))
            x += 10

        self.head = self.snake_items[-1]
        self.move_to = self.move_head_to_right
        self.apples = []

        for i in range(3):
            self.apples.append(self.board.create_rectangle(self.generate_apple_coords(), fill='red'))

    def generate_apple_coords(self):
        x1 = random.randint(0, 590)
        x2 = x1 + 10
        y1 = random.randint(0, 390)
        y2 = y1 + 10
        apple_coords = [x1, y1, x2, y2]

        for _ in self.snake_items:
            if self.board.coords == apple_coords:
                return self.generate_apple_coords()

        return apple_coords

    def eat_apple(self):
        x1, y1, x2, y2 = self.board.coords(self.head)

        for apple in self.apples:
            xx1, yy1, xx2, yy2 = self.board.coords(apple)

            if -10 < x1 - xx1 < 10 and -10 < yy1 - y1 < 10 and -10 < x2 - xx2 < 10 and -10 < y2 - yy2 < 10:
                self.add_item()
                self.board.coords(apple, self.generate_apple_coords())

    def move_head_to_right(self):
        coords = self.board.coords(self.head)
        coords[0] += 10
        coords[2] += 10
        coords = teleport(coords)
        self.board.coords(self.head, coords)

    def move_head_to_left(self):
        coords = self.board.coords(self.head)
        coords[0] -= 10
        coords[2] -= 10
        teleport(coords)
        self.board.coords(self.head, coords)

    def move_head_to_up(self):
        coords = self.board.coords(self.head)
        coords[1] -= 10
        coords[3] -= 10
        teleport(coords)
        self.board.coords(self.head, coords)

    def move_head_to_down(self):
        coords = self.board.coords(self.head)
        coords[1] += 10
        coords[3] += 10
        teleport(coords)
        self.board.coords(self.head, coords)

    def move_all(self):
        for i in range(len(self.snake_items) - 1):
            coords = self.board.coords(self.snake_items[i + 1])
            self.board.coords(self.snake_items[i], coords)
        self.move_to()
        self.eat_apple()

    def game_over(self):
        for i in range(len(self.snake_items) - 2):
            if self.board.coords(self.snake_items[-1]) == self.board.coords(self.snake_items[i]):
                return True
        return False

    def add_item(self):
        coords1 = self.board.coords(self.snake_items[1])
        coords2 = self.board.coords(self.snake_items[2])
        x1 = coords2[0] - coords1[0]
        x2 = coords2[2] - coords1[2]

        y1 = coords2[1] - coords1[1]
        y2 = coords2[3] - coords1[3]

        self.snake_items.insert(
            0,
            self.board.create_rectangle(
                coords1[0] - x1, coords1[1] - y1, coords1[2] - x2, coords1[3] - y2, fill='green'
            )
        )


class Game:
    def keyboard_manager(self, event):
        if event.keysym == "Right" and self.snake.move_to != self.snake.move_head_to_left:
            self.snake.move_to = self.snake.move_head_to_right

        elif event.keysym == "Left" and self.snake.move_to != self.snake.move_head_to_right:
            self.snake.move_to = self.snake.move_head_to_left

        elif event.keysym == "Up" and self.snake.move_to != self.snake.move_head_to_down:
            self.snake.move_to = self.snake.move_head_to_up

        elif event.keysym == "Down" and self.snake.move_to != self.snake.move_head_to_up:
            self.snake.move_to = self.snake.move_head_to_down

        elif event.keysym == "Return":
            self.game_loop()

        elif event.keysym == "Escape":
            self.app.destroy()

        elif event.keysym == 'e':
            self.snake.add_item()

        elif event.keysym == 'j':
            self.snake.move_all()

    def __init__(self, board, app):
        self.board = board
        self.app = app
        self.app.bind("<Key>", self.keyboard_manager)
        self.snake = Snake(board)

    def game_loop(self):
        while True:
            time.sleep(1 / 20)  # 20 FPS
            self.snake.move_all()
            self.board.update()
            if self.snake.game_over():
                for i in self.snake.snake_items[-10::-1]:
                    self.board.delete(i)
                    del self.snake.snake_items[self.snake.snake_items.index(i)]


root = tkinter.Tk()
root.resizable(False, False)
root.title("Snake.Py by Ilyosiddin Kalandar")
canvas = tkinter.Canvas(height=400, width=600, bg="black")
canvas.pack()
game = Game(canvas, root)
root.mainloop()
