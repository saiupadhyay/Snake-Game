import pygame

pygame.mixer.init()
eat_sound = pygame.mixer.Sound("food_eat.wav")

from tkinter import *
import random
game_loop = None


GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 90
SPACE_SIZE = 30
BODY_PARTS = 5
SNAKE_COLOR = "blue"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

food_counter = 0
current_speed = SPEED

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    global game_loop, score, current_speed, food_counter

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        Label.config(text="Score: {}".format(score))
        canvas.delete("food")
        food = Food()

        eat_sound.play()
        food_counter += 1

        if food_counter % 5 ==0:
            current_speed = max(30, current_speed - 10)

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        snake.squares.pop()
    
    if check_collision(snake):
        game_over()
    
    else:
        game_loop = window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    
    global direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collision(snake):
    
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        print("Game Over")
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        print("Game Over")
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("Game Over")
            return True
        
    return False

def game_over():
    global restart_button
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 50, 
                       font=("consolas", 70), text="Game Over", fill="red", anchor=CENTER, tags="gameover")

    restart_button = Button(window, text="Replay", font= ("consolas", 20) , command=restart_game)
    restart_button.pack()

def restart_game():
    
    global snake, food, direction, score, restart_button, game_loop, current_speed, food_counter

    if game_loop is not None:
        window.after_cancel(game_loop)
        
    canvas.delete(ALL)
    score = 0
    Label.config(text="Score: {}".format(score))
    direction = "down"
    
    snake = Snake()
    food = Food()
    
    next_turn(snake, food)


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"

# Create a frame for the score bar on the left side
score_frame = Frame(window)
score_frame.pack(side=TOP, padx=10)

# Score label inside the frame
Label = Label(score_frame, text="Score: {}".format(score), font=("Arial", 20))
Label.pack()

# Replay button inside the frame (below score label)
restart_button = Button(score_frame, text="Replay", font=("Arial", 15), command=restart_game)
restart_button.pack(pady=10)  # Adds spacing below the button


canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2 )- (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind("<Left>", lambda event: change_direction('left'))
window.bind("<Right>", lambda event: change_direction('right'))
window.bind("<Up>", lambda event: change_direction('up'))
window.bind("<Down>", lambda event: change_direction('down'))
window.bind("<Return>", lambda event: restart_game())

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()