import tkinter as tk
import random
import pygame
import time

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
SPEED = 10

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.snake = [(WIDTH/2, HEIGHT/2)]
        self.food = self.create_food()
        self.direction = "Right"
        self.score = 0

        self.game_over = False

        self.draw()


        self.master.bind("<KeyPress>", self.change_direction)
        self.update()

    def draw(self):
        self.canvas.delete("all")

        # Draw snake
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x+GRID_SIZE, y+GRID_SIZE, fill="green")

        # Draw food
        x, y = self.food
        self.canvas.create_oval(x, y, x+GRID_SIZE, y+GRID_SIZE, fill="red")

        # Draw score
        self.canvas.create_text(10, 10, text=f"Score: {self.score}", fill="white", anchor="nw")

        if self.game_over:
            self.canvas.create_text(WIDTH/2, HEIGHT/2, text="Game Over", fill="white", font=("Helvetica", 36))

    def create_food(self):
        x = random.randint(0, WIDTH - GRID_SIZE)
        y = random.randint(0, HEIGHT - GRID_SIZE)
        return x, y

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == "Up":
            new_head = (head_x, head_y - GRID_SIZE)
        elif self.direction == "Down":
            new_head = (head_x, head_y + GRID_SIZE)
        elif self.direction == "Left":
            new_head = (head_x - GRID_SIZE, head_y)
        elif self.direction == "Right":
            new_head = (head_x + GRID_SIZE, head_y)

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.create_food()
            self.score += 1
        else:
            self.snake.pop()

        if self.check_collision():
            self.game_over = True

    def check_collision(self):
        head_x, head_y = self.snake[0]

        # Check if snake hits walls
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True

        # Check if snake hits itself
        if (head_x, head_y) in self.snake[1:]:
            return True

        return False

    def update(self):
        if not self.game_over:
            self.move_snake()
            self.draw()
            self.master.after(1000 // SPEED, self.update)

    def change_direction(self, event):
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            if (event.keysym == "Up" and self.direction != "Down" or
                event.keysym == "Down" and self.direction != "Up" or
                event.keysym == "Left" and self.direction != "Right" or
                event.keysym == "Right" and self.direction != "Left"):
                self.direction = event.keysym

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
