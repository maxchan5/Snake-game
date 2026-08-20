import tkinter
import random

rows = 25
cols = 25
tile_size = 25

window_height = rows * tile_size
window_width = cols * tile_size

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


#game window
window = tkinter.Tk()
window.title("Snaketris")
window.resizable(False, False) #stops the game dimensions from changing by changing the window 

canvas = tkinter.Canvas(window, bg = "black", width = window_width, height = window_height, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#center the window to the middle of the screen

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

#geometry has to be in the format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialise game
snake = Tile(11*tile_size, 11*tile_size)
food = Tile(random.randint(0, cols-1)*tile_size, 0)
snake_body = []
velocityX = 0
velocityY = 0
gameover = False
score = 0
fall_counter = 0
fall_speed = 5
prev_score = 0

def change_direction(e): 
    global velocityX, velocityY, snake, food, gameover, snake_body, score, fall_counter, fall_speed

    #reset game by pressing space
    if gameover and e.keysym == "space":
            snake = Tile(11*tile_size, 11*tile_size)
            food = Tile(random.randint(0, cols-1)*tile_size, 0)
            snake_body = []
            velocityX = 0
            velocityY = 0
            gameover = False
            score = 0
            fall_counter = 0
            fall_speed = 5
            return

    #inputs not registered while gameover
    if gameover:
        return
    

    if (e.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (e.keysym == "Down" and velocityY != -1):
        velocityX = 0 
        velocityY = 1
    elif (e.keysym == "Left" and velocityX != 1):
        velocityX = -1 
        velocityY = 0
    elif (e.keysym == "Right" and velocityX != -1):
        velocityX = 1 
        velocityY = 0

def move():
    global snake, food, snake_body, gameover, fall_counter, fall_speed, score, prev_score

    if (gameover):
        return
    
    #hits the walls
    if (snake.x < 0 or snake.x >= window_width or snake.y < 0 or snake.y >= window_height):
        gameover = True
        return

    #hits itself
    #for tile in snake_body:
    #    if (snake.x == tile.x and snake.y == tile.y):
    #        gameover = True
    #        return

    #makes the food fall and speed up after eevry 10 points
    fall_counter += 1
    if fall_counter >= fall_speed:
        if score % 10 == 0 and score != 0 and score != prev_score:
            fall_speed -= 1
            prev_score = score
        food.y += tile_size
        fall_counter = 0

    #if food reaches the bottom, gameover
    if food.y >= window_height - tile_size:
        gameover = True
        return
    


    #eating food
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, cols-1) * tile_size
        #food.y = random.randint(0, rows-1) * tile_size
        food.y = 0 * tile_size
        score += 1

    #updates the snakes body
    for i in range(len(snake_body) - 1, -1, -1):
        tile = snake_body[i]
        if (i == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i - 1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * tile_size
    snake.y += velocityY * tile_size

def draw():
    global snake, food, snake_body, gameover, score

    move()

    #clears prev frame 
    canvas.delete("all")

    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + tile_size, food.y + tile_size, fill = "red")

    #draws snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + tile_size, snake.y + tile_size, fill = "lime green")

    #draw body
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + tile_size, tile.y + tile_size, fill = "lime green")

    #draw score counter
    canvas.create_text(40, 20, font = "Arial 15", text = f"Score: {score}", fill = "white")

    #draw gameover
    if gameover:
        canvas.create_text(window_width/2, window_height/2, font = "Arial 20", text = f"GAMEOVER", fill = "white")

    window.after(100, draw) # 100ms = 1/10 second, 10 frames/second

draw()

window.bind("<KeyRelease>", change_direction)
window.mainloop()