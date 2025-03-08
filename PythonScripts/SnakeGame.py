import pygame
import time
import random
import tkinter

tk = tkinter.Tk()
tk.geometry("300x150")
tk.title("Snake Game Size")

entry = tkinter.Entry(tk)
entry.pack(pady=10)

entry = tkinter.Entry(tk)
entry.pack(pady=10)

tk.mainloop()

# Initialize pygame
pygame.init()

# Set display width and height
width = 1000  # Double the width
height = 600  # Double the height 

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Snake block size
block_size = 20  # Double the block size
speed = 15

# Initialize display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Clock
clock = pygame.time.Clock()

# Font style
font_style = pygame.font.SysFont("bahnschrift", 60)  # Double the font size

# Font style for failure message
small_font_style = pygame.font.SysFont("bahnschrift", 40)  # Double the font size

# Large font style for "You Lost!" message
large_font_style = pygame.font.SysFont("bahnschrift", 90)  # Double the font size

class Raindrop:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = random.randint(-height, 0)
        self.speed = random.randint(5, 15) / 26  # Halve the speed and double the effect
        self.length = random.randint(10, 30)  # Double the length
    
    def fall(self):
        self.y += self.speed
        if self.y > height:
            self.y = random.randint(-height, 0)
            self.x = random.randint(0, width)
            self.speed = random.randint(5, 15) / 26  # Halve the speed and double the effect
            self.length = random.randint(10, 30)  # Double the length
    
    def draw(self):
        pygame.draw.line(screen, white, (self.x, self.y), (self.x, self.y + self.length), 2)  # Double the thickness

def generate_raindrops(num_drops):
    return [Raindrop() for _ in range(num_drops)]

def update_raindrops(raindrops):
    for drop in raindrops:
        drop.fall()
        drop.draw()

def message(msg, color, y, font=font_style):
    mesg = font.render(msg, True, color)
    x = (width - mesg.get_width()) / 2
    screen.blit(mesg, [x, y])

def draw_score(score):
    score_text = font_style.render(f"Score: {score}", True, white)
    screen.blit(score_text, (width - 420, 20))  # Adjusted for doubled size

def draw_eyes(snake_head, direction):
    eye_radius = 3
    eye_offset = 5
    if direction == 'UP':
        eye1_pos = (snake_head[0] + eye_offset, snake_head[1] + eye_offset)
        eye2_pos = (snake_head[0] + block_size - eye_offset, snake_head[1] + eye_offset)
    elif direction == 'DOWN':
        eye1_pos = (snake_head[0] + eye_offset, snake_head[1] + block_size - eye_offset)
        eye2_pos = (snake_head[0] + block_size - eye_offset, snake_head[1] + block_size - eye_offset)
    elif direction == 'LEFT':
        eye1_pos = (snake_head[0] + eye_offset, snake_head[1] + eye_offset)
        eye2_pos = (snake_head[0] + eye_offset, snake_head[1] + block_size - eye_offset)
    elif direction == 'RIGHT':
        eye1_pos = (snake_head[0] + block_size - eye_offset, snake_head[1] + eye_offset)
        eye2_pos = (snake_head[0] + block_size - eye_offset, snake_head[1] + block_size - eye_offset)
    else:
        return

    pygame.draw.circle(screen, black, eye1_pos, eye_radius)
    pygame.draw.circle(screen, black, eye2_pos, eye_radius)

def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    paused = False

        screen.fill(black)
        message("Paused", white, height / 2.3, font_style)
        message("Press F at any time to continue!", green, height / 1.7, small_font_style)
        pygame.display.update()
        clock.tick(5)

def start_screen():
    screen.fill(black)
    message("Press any direction to begin!", white, height / 2.3, font_style)
    message("Press F at any time to pause!", green, height / 1.7, small_font_style)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                    waiting = False

def gameLoop():
    game_over = False
    game_close = False

    x = width / 2
    y = height / 2
    
    x_change = 0
    y_change = 0
    
    snake = []
    length = 1
    
    food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0  # Adjusted for doubled size
    food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0  # Adjusted for doubled size
    
    current_direction = None
    
    raindrops = generate_raindrops(75)
    
    while not game_over:
        while game_close:
            screen.fill(black)
            update_raindrops(raindrops)
            message("You Lost MAX!", red, height / 4, large_font_style)
            message("Press Q-Quit or C-Play Again", green, height / 2.5, small_font_style)
            message("Your Score: " + str(length - 1), white, height / 2, font_style)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and current_direction != 'RIGHT':
                    x_change = -block_size
                    y_change = 0
                    current_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and current_direction != 'LEFT':
                    x_change = block_size
                    y_change = 0
                    current_direction = 'RIGHT'
                elif event.key == pygame.K_UP and current_direction != 'DOWN':
                    y_change = -block_size
                    x_change = 0
                    current_direction = 'UP'
                elif event.key == pygame.K_DOWN and current_direction != 'UP':
                    y_change = block_size
                    x_change = 0
                    current_direction = 'DOWN'
                elif event.key == pygame.K_f:
                    pause_game()
        
        if x >= width or x < 0 or y >= height or y < 0:
            game_close = True
        
        x += x_change
        y += y_change
        screen.fill(blue)
        pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])
        
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake.append(snake_head)
        if len(snake) > length:
            del snake[0]
        
        for segment in snake[:-1]:
            if segment == snake_head:
                game_close = True
        
        for segment in snake:
            pygame.draw.rect(screen, green, [segment[0], segment[1], block_size, block_size])
        
        draw_eyes(snake_head, current_direction)
        
        pygame.display.update()
        
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / 20.0) * 20.0  # Adjusted for doubled size
            food_y = round(random.randrange(0, height - block_size) / 20.0) * 20.0  # Adjusted for doubled size
            length += 1
        
        draw_score(length - 1)
        
        clock.tick(speed)
    
    pygame.quit()
    quit()
    
start_screen()
gameLoop()

