import pygame
import random

pygame.init()

# Window Creation
WIDTH , HEIGHT = 1000 , 600
screen = pygame.display.set_mode((WIDTH , HEIGHT))

# Window Name
pygame.display.set_caption("Flappy Bird")

# Icon
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Variables
# Loading Sounds
flap_sound = pygame.mixer.Sound("sounds/bird/flap.wav")
game_over_sound = pygame.mixer.Sound("sounds/bird/gameover_sound.wav")
# Loading Images
# background
background_day = pygame.image.load("textures/background/background_day.png").convert()
background_night = pygame.image.load("textures/background/background_night.png").convert()
background = background_day
# pipe
pipe_up = pygame.image.load("textures/pipe/pipe_up.png").convert_alpha()
pipe_down = pygame.image.load("textures/pipe/pipe_down.png").convert_alpha()
pipe_up_copy = pygame.image.load("textures/pipe/pipe_up.png").convert_alpha()
pipe_down_copy = pygame.image.load("textures/pipe/pipe_down.png").convert_alpha()
# "bird"
flappy_bird = pygame.image.load("textures/bird/flappy_bird.png").convert_alpha()
flappy_bird_flap = pygame.image.load("textures/bird/flappy_bird_flap.png").convert_alpha()
flappy_bird_night = pygame.image.load("textures/bird/flappy_bird_night.png").convert_alpha()
flappy_bird_flap_night = pygame.image.load("textures/bird/flappy_bird_flap_night.png").convert_alpha()

# Must Have For Window
Running = True
clock = pygame.time.Clock()

# Bird Hitboxes
flappy_bird_flap_hitbox = flappy_bird_flap.get_rect(center=(100 , 100))
flappy_bird_hitbox = flappy_bird.get_rect(center=(100 , 100))
flappy_bird_flap_night_hitbox = flappy_bird_flap_night.get_rect(center=(100 , 100))
flappy_bird_night_hitbox = flappy_bird_night.get_rect(center=(100 , 100))
bird_hitbox = flappy_bird_hitbox
bird = flappy_bird

# Pipe 
# passed pipe
passed_pipe = False
passed_pipe_copy = False
# Randomized height of the pipe
pipe_height = random.randint(-150 , 125)
pipe_height_copy = random.randint(-150 , 125)
# Pipe hitboxes
pipe_up_hitbox = pipe_up.get_rect(center=(500 , pipe_height))
pipe_down_hitbox = pipe_down.get_rect(center=(500 , pipe_up_hitbox.bottom + 450))
pipe_up_copy_hitbox = pipe_up_copy.get_rect(center=(1000 , pipe_height_copy))
pipe_down_copy_hitbox = pipe_down_copy.get_rect(center=(1000 , pipe_up_copy_hitbox.bottom + 450))
pipe_tightness = 450

# Font
font = pygame.font.Font(None , 96)
text_color = (200 , 200 , 200)

# gravity
gravity = 0.5
bird_vel_y = 0
flap_strength = -10
# Score
score = 0
# score text
score_text = font.render(f"{score}", True, (text_color))
# game over mechanic
game_over = False
gameover_text = font.render("Game Over!", True, (text_color))
final_score_text = font.render(f"Your Score Is: {score}", True, (text_color))
restart_tuto_text = font.render("Press R to Restart", True, (text_color))
sound_played = 0
gameover_x_animation = 0
pipe_hit_side = False
pipe_hit_top = False
# day/night cycle
day = 0
night = 1
time = day
time_point = 0

# Command for rotating effect
def draw_rotated_bird():
    global bird, bird_hitbox, bird_vel_y
    angle = max(-30, min(90, bird_vel_y * 3))
    rotated_bird = pygame.transform.rotate(bird, -angle)
    rotated_rect = rotated_bird.get_rect(center=bird_hitbox.center)
    screen.blit(rotated_bird, rotated_rect)
# New Command For Rendering Text
def render_text():
    global font,gameover_text,final_score_text,score_text,restart_tuto_text
    gameover_text = font.render("Game Over!", True, (text_color))
    final_score_text = font.render(f"Your Score Is: {score}", True, (text_color))
    score_text = font.render(f"{score}", True, (text_color))
    restart_tuto_text = font.render("Press R to Restart", True, (text_color))
# New Command For Reseting Pipes
def pipe_reset():
    global pipe_height , pipe_up_hitbox , pipe_down_hitbox
    pipe_height = random.randint(-150 , 125)
    pipe_up_hitbox = pipe_up.get_rect(center=(500 , pipe_height))
    pipe_down_hitbox = pipe_down.get_rect(center=(500 , pipe_up_hitbox.bottom + pipe_tightness))
    pipe_up_hitbox.x= 1000
    pipe_down_hitbox.x = 1000
def pipe_copy_reset():
    global pipe_up_copy_hitbox , pipe_down_copy_hitbox , pipe_height_copy
    pipe_height_copy = random.randint(-150 , 125)
    pipe_up_copy_hitbox = pipe_up_copy.get_rect(center=(1000 , pipe_height_copy))
    pipe_down_copy_hitbox = pipe_down_copy.get_rect(center=(1000 , pipe_up_copy_hitbox.bottom + pipe_tightness))
    pipe_down_copy_hitbox.x = 1000
    pipe_up_copy_hitbox.x = 1000
# New command for score
def add_score():
    global font,final_score_text,score_text,score,time_point 
    score += 1
    time_point += 1
    final_score_text = font.render(f"Your Score Is: {score}", True, (text_color))
    score_text = font.render(f"{score}", True, (text_color))
# Render Textures
def render_textures():
    global pipe_up , pipe_up_copy , pipe_up_hitbox , pipe_up_copy_hitbox , pipe_down , pipe_down_copy ,pipe_down_hitbox , pipe_down_copy_hitbox, bird, bird_hitbox
    screen.blit(background, (0 , 0))
    draw_rotated_bird()
    screen.blit(pipe_up, pipe_up_hitbox)
    screen.blit(pipe_down, pipe_down_hitbox)
    screen.blit(pipe_up_copy, pipe_up_copy_hitbox)
    screen.blit(pipe_down_copy, pipe_down_copy_hitbox)
def restart_game():
    global pipe_up_hitbox,pipe_down_hitbox,pipe_down_copy_hitbox,pipe_up_copy_hitbox,game_over,bird,bird_hitbox,bird_vel_y,pipe_height,pipe_height_copy,score,score_text,time_point,time,sound_played,pipe_hit_top,pipe_hit_side
    sound_played = 0
    pipe_hit_top = False
    pipe_hit_side = False
    time = day
    pipe_up_hitbox = pipe_up.get_rect(center=(500 , pipe_height))
    pipe_down_hitbox = pipe_down.get_rect(center=(500 , pipe_up_hitbox.bottom + pipe_tightness))
    pipe_up_copy_hitbox = pipe_up_copy.get_rect(center=(1000 , pipe_height_copy))
    pipe_down_copy_hitbox = pipe_down_copy.get_rect(center=(1000 , pipe_up_copy_hitbox.bottom + pipe_tightness))
    bird_hitbox = flappy_bird.get_rect(center=(100 , 100))
    pipe_height = random.randint(-150 , 125)
    pipe_height_copy = random.randint(-150 , 125)
    bird_vel_y = 0
    score = 0
    time_point = 0
    render_text()
    screen.blit(score_text, (490 , 0))
    game_over = False
# main loop
while Running:
    # Loading Textures 
    render_textures()
    # Loading text
    screen.blit(score_text, (490 , 0))
    # Event Handling
    for event in pygame.event.get():
        # If tried to exit game via exit button
        if event.type == pygame.QUIT:
            Running = False
        # Flap Mechanic
        if event.type == pygame.KEYDOWN:
            # Check If Space Was Clicked  and game_over is false
            if event.key == pygame.K_SPACE and game_over == False:
                # Flap
                pygame.mixer.Sound.play(flap_sound)
                if time == day:
                    bird_vel_y = flap_strength
                    bird = flappy_bird_flap
                    bird_hitbox = flappy_bird_flap.get_rect(center=bird_hitbox.center)
                if time == night:
                    bird_vel_y = flap_strength
                    bird = flappy_bird_flap_night
                    bird_hitbox = flappy_bird_flap_night.get_rect(center=bird_hitbox.center)
            # Check If R Was Clicked and game_over is true
            if event.key == pygame.K_r and game_over == True:
               restart_game() 
    
    # gravity
    bird_vel_y += gravity
    bird_hitbox.y += bird_vel_y
    
    # day/night cycle
    if time_point < 50 or time_point == 0:
        time == day
    if time_point > 50:
        time = night
    if time_point > 100:
        time_point = 0
        time = day
    
    if time == day:
        text_color = (200 , 200 , 200)
        background = background_day
        bird = flappy_bird
        pipe_up = pygame.image.load("textures/pipe/pipe_up.png").convert_alpha()
        pipe_down = pygame.image.load("textures/pipe/pipe_down.png").convert_alpha()
        pipe_up_copy = pygame.image.load("textures/pipe/pipe_up.png").convert_alpha()
        pipe_down_copy = pygame.image.load("textures/pipe/pipe_down.png").convert_alpha()
        if bird_vel_y < 0:
            bird = flappy_bird_flap
        render_text
        gameover_text = font.render("Game Over!", True, (text_color))
        restart_tuto_text = font.render("Press R to Restart", True, (text_color))
    if time == night:
        text_color = (255 , 255 ,255)
        background = background_night
        bird = flappy_bird_night
        pipe_up = pygame.image.load("textures/pipe/pipe_up_night.png").convert_alpha()
        pipe_down = pygame.image.load("textures/pipe/pipe_down_night.png").convert_alpha()
        pipe_up_copy = pygame.image.load("textures/pipe/pipe_up_night.png").convert_alpha()
        pipe_down_copy = pygame.image.load("textures/pipe/pipe_down_night.png").convert_alpha()
        if bird_vel_y < 0:
            bird = flappy_bird_flap_night
        render_text
        gameover_text = font.render("Game Over!", True, (text_color))
        restart_tuto_text = font.render("Press R to Restart", True, (text_color))

    # Pipes Moving
    if game_over == False:
        pipe_up_hitbox.x -= 10
        pipe_down_hitbox.x -= 10
        pipe_down_copy_hitbox.x -= 10
        pipe_up_copy_hitbox.x -= 10
    
    # score based space between pipes
    if score >= 25:
        pipe_tightness = 440
    if score >= 50:
        pipe_tightness = 430
    if score >= 100:
        pipe_tightness = 420
    if score >= 150:
        pipe_tightness = 410
    if score >= 200:
        pipe_tightness = 400
    
    # bird texture change from flap to basic
    if time == day:  
        if bird_vel_y >= 0:
             bird = flappy_bird
             bird_hitbox = flappy_bird.get_rect(center=bird_hitbox.center)
    if time == night:
        if bird_vel_y >= 0:
             bird = flappy_bird_night
             bird_hitbox = flappy_bird_night.get_rect(center=bird_hitbox.center)

    # Collision With Ground Check
    if bird_hitbox.bottom >= 600 and game_over == False:
        bird_vel_y = flap_strength
        game_over = True
    if bird_hitbox.top < 0 and game_over == False:
        bird_vel_y = flap_strength
        game_over = True
    # Game Over mechanic
    if game_over == True:
        screen.blit(gameover_text, (300 , 200))
        screen.blit(final_score_text, (250 , 265))
        screen.blit(restart_tuto_text, (220 , 330))
        # Play game over sound
        if sound_played == 0:
            pygame.mixer.Sound.play(game_over_sound)
            sound_played = 1
    # If pipes went outside the screen they get back on other side of screen
    if pipe_down_hitbox.x and pipe_up_hitbox.x < -100:
        pipe_reset()
    if pipe_down_copy_hitbox.x and pipe_up_copy_hitbox.x < -100:
        pipe_copy_reset()
    
    # If bird hits pipes its game over
    if bird_hitbox.colliderect(pipe_up_hitbox) or bird_hitbox.colliderect(pipe_down_hitbox) or bird_hitbox.colliderect(pipe_up_copy_hitbox) or bird_hitbox.colliderect(pipe_down_copy_hitbox) and game_over == False:
        pipe_hit_side = True
        game_over = True
        render_text()
    # Bounce when bird hits top of a pipe 
        if bird_hitbox.colliderect(pipe_up_hitbox) and bird_hitbox.bottom <= pipe_up_hitbox.bottom + 10:
            pipe_hit_top = True
        elif bird_hitbox.colliderect(pipe_up_copy_hitbox) and bird_hitbox.bottom <= pipe_up_copy_hitbox.bottom + 10: 
            pipe_hit_top = True
        elif bird_hitbox.colliderect(pipe_down_hitbox) and bird_hitbox.top >= pipe_down_hitbox.top - 10:
            bird_vel_y = flap_strength * 1.5
            pipe_hit_top = True
        elif bird_hitbox.colliderect(pipe_down_copy_hitbox) and bird_hitbox.top >= pipe_down_copy_hitbox.top - 10:
            bird_vel_y = flap_strength * 1.5
            pipe_hit_top = True 
    
    if gameover_x_animation < 5 and pipe_hit_side == True and game_over == True:
        bird_hitbox.x -= 10
    elif gameover_x_animation < 5 and pipe_hit_top == True and game_over == True:
        bird_hitbox.x += 10
    
    # Score system - checks if bird passed pipes
    if not game_over:
    # For first pipe set
        if pipe_up_hitbox.right < bird_hitbox.left and not passed_pipe:
            add_score()
            passed_pipe = True
        elif pipe_up_hitbox.right >= bird_hitbox.left:
            passed_pipe = False
        
    # For second pipe set
        if pipe_up_copy_hitbox.right < bird_hitbox.left and not passed_pipe_copy:
            add_score()
            passed_pipe_copy = True
        elif pipe_up_copy_hitbox.right >= bird_hitbox.left:
            passed_pipe_copy = False

    # Screen Update
    pygame.display.update()
    # Frame Rate
    clock.tick(60)
