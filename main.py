import pygame
import os
from configparser import ConfigParser
pygame.font.init()
pygame.mixer.init()

config = ConfigParser()
config.read('difficulty.ini')

difficulty = {}
velocity, max_bullets, bullet_velocity, max_health = 0, 0, 0, 0

pos_num = 3
# difficulty -> config.ini
difficulty = {1: "lazy", 2: "easy", 3: "normal", 4: "hard", 5: "insane"}
velocity = int(config[difficulty[pos_num]]["VELOCITY"])
max_bullets = int(config[difficulty[pos_num]]["MAX_BULLETS"])
bullet_velocity = int(config[difficulty[pos_num]]["BULLET_VELOCITY"])
max_health = int(config[difficulty[pos_num]]["MAX_HEALTH"])

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Retro Beam")

SPACE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.jpg")), (WIDTH, HEIGHT))
SPACE_MENU_IMG = pygame.transform.scale(pygame.image.load(os.path.join("Assets","menu.jpg")), (WIDTH, HEIGHT))

MENU_NAV_SOUND = pygame.mixer.Sound(os.path.join("Assets", "menu_nav.wav"))
MENU_SELECT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "menu_select.wav"))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join("Assets", "explosion.wav"))
GAME_START_SOUND = pygame.mixer.Sound(os.path.join("Assets", "game_start.wav"))
GAME_PAUSE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "pause_in.wav"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join("Assets", "weapon_fire.wav"))
GAME_WIN_SOUND = pygame.mixer.Sound(os.path.join("Assets", "game_win.wav"))

BLACK = (0, 0, 0)
GREY = (125, 125, 125)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

HEALTH_FONT = pygame.font.Font(os.path.join("Assets","PublicPixel-0W5Kv.ttf"), 10, bold=False, italic=False)
WINNER_FONT = pygame.font.Font(os.path.join("Assets","PublicPixel-0W5Kv.ttf"), 24, bold=False, italic=False)
M_MENU_FONT1 = pygame.font.Font(os.path.join("Assets","PublicPixel-0W5Kv.ttf"), 36, bold=False, italic=False)
M_MENU_FONT2 = pygame.font.Font(os.path.join("Assets","PublicPixel-0W5Kv.ttf"), 12, bold=False, italic=False)

FPS = 60
MID_BORDER = pygame.Rect(WIDTH//2-5, 0, 4, HEIGHT)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40

YELLOW_SPACESHIP_IMG = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
RED_SPACESHIP_IMG = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))

YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

# CREATING USEREVENTS FOR BULLET HITS
HIT_YELLOW = pygame.USEREVENT + 1
HIT_RED = pygame.USEREVENT + 2

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.blit(SPACE_IMG, (0,0))
    pygame.draw.rect(WIN, WHITE, MID_BORDER)
    
    yellow_health_text = HEALTH_FONT.render("HEALTH: "  + str(yellow_health), 1, YELLOW)
    red_health_text = HEALTH_FONT.render("HEALTH: " + str(red_health), 1, RED)
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)    

    pygame.display.update()

def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_w] and yellow.y - velocity > 0: #YELLOW_UP
        yellow.y -= velocity
    if keys_pressed[pygame.K_s] and yellow.y + velocity < HEIGHT-yellow.height-15: #YELLOW_DOWN
        yellow.y += velocity
    if keys_pressed[pygame.K_a] and yellow.x - velocity > 0: #YELLOW_LEFT
        yellow.x -= velocity
    if keys_pressed[pygame.K_d] and yellow.x + velocity < MID_BORDER.x - yellow.width+6: #YELLOW_RIGHT
        yellow.x += velocity

def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_UP] and red.y - velocity > 0: #RED_UP
        red.y -= velocity
    if keys_pressed[pygame.K_DOWN] and red.y + velocity < HEIGHT-red.height-15: #RED_DOWN
        red.y += velocity
    if keys_pressed[pygame.K_LEFT] and red.x - velocity > MID_BORDER.x+MID_BORDER.width: #RED_LEFT
        red.x -= velocity
    if keys_pressed[pygame.K_RIGHT] and red.x + velocity < WIDTH-red.width+10: #RED_RIGHT
        red.x += velocity

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_velocity
        if bullet.colliderect(red):
            # posting and event when a yellow bullet was hit
            pygame.event.post(pygame.event.Event(HIT_RED))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_velocity
        if bullet.colliderect(yellow):
            # posting and event when a red bullet was hit
            pygame.event.post(pygame.event.Event(HIT_YELLOW))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(winner_text):
    color = winner_text.split()[0]
    if color == "YELLOW":
        color = YELLOW
    else:
        color = RED
    the_text = WINNER_FONT.render(winner_text, 1, color)
    WINNER_BG = pygame.Rect(
        WIDTH/2 - the_text.get_width()/2, HEIGHT/2 - the_text.get_height()/2, the_text.get_width(), the_text.get_height())
    pygame.draw.rect(WIN, BLACK, WINNER_BG)
    WIN.blit(the_text, (WIDTH/2 - the_text.get_width()/2, HEIGHT/2 - the_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def difficulty_menu():
    pos_num = 3
    pygame.display.set_caption("Retro Beam - Select difficulty")
    clock = pygame.time.Clock()

    # width for reference
    diff1 = M_MENU_FONT2.render("[ 1. LAZY    ]",1,GREEN)
    arrow = M_MENU_FONT2.render("-> ", 1, GREEN)
    
    pos_y = 300
    WIN.blit(arrow, (WIDTH//2 - diff1.get_width(), pos_y))
    pygame.display.update()

    run = True
    while run:
        clock.tick(FPS)
        WIN.blit(SPACE_MENU_IMG, (0,0))
        diff_text = M_MENU_FONT1.render("SELECT difficulty", 1, WHITE)
        diff1 = M_MENU_FONT2.render("[ 1. LAZY    ]",1,GREEN)
        diff2 = M_MENU_FONT2.render("[ 2. EASY    ]",1,GREEN)
        diff3 = M_MENU_FONT2.render("[ 3. NORMAL  ]",1,GREEN)
        diff4 = M_MENU_FONT2.render("[ 4. HARD    ]",1,GREEN)
        diff5 = M_MENU_FONT2.render("[ 5. INSANE! ]",1,GREEN)
        WIN.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, 200))
        WIN.blit(diff1, (WIDTH//2 - diff1.get_width()//2, 260))
        WIN.blit(diff2, (WIDTH//2 - diff1.get_width()//2, 280))
        WIN.blit(diff3, (WIDTH//2 - diff1.get_width()//2, 300))
        WIN.blit(diff4, (WIDTH//2 - diff1.get_width()//2, 320))
        WIN.blit(diff5, (WIDTH//2 - diff1.get_width()//2, 340))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                MENU_SELECT_SOUND.play()
                main_menu()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and pos_num < 5:
                pos_num += 1
                pos_y += 20
                MENU_NAV_SOUND.play()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and pos_num > 1:
                pos_num -= 1
                pos_y -= 20
                MENU_NAV_SOUND.play()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # print("Selected difficulty " + str(pos_num) + ": " + difficulty[pos_num])
                GAME_START_SOUND.play()
                return pos_num

        WIN.blit(arrow, (WIDTH//2 - diff1.get_width(), pos_y))
        pygame.display.update()

def pause_menu():
    GAME_PAUSE_SOUND.play()
    pygame.display.set_caption("Retro Beam - Pause")
    
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        WIN.blit(SPACE_MENU_IMG, (0,0))
        main_menu_text = M_MENU_FONT1.render("RETRO BEAM - PAUSED", 1, WHITE)
        info_text1 = M_MENU_FONT2.render("[Press Space to continue...]",1,GREEN)
        info_text2 = M_MENU_FONT2.render("[Press Esc for Main Menu...]",1,GREEN)      
        WIN.blit(info_text1, (WIDTH//2 - info_text1.get_width()//2, 300))
        WIN.blit(info_text2, (WIDTH//2 - info_text2.get_width()//2, 320))

        WIN.blit(main_menu_text, (WIDTH//2 - main_menu_text.get_width()//2, 200))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GAME_START_SOUND.play()
                run = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                MENU_SELECT_SOUND.play()
                main_menu()

def set_diff_parameters():
    global pos_num
    pos_num = difficulty_menu()
    global velocity
    velocity = int(config[difficulty[pos_num]]["VELOCITY"])
    global max_bullets 
    max_bullets = int(config[difficulty[pos_num]]["MAX_BULLETS"])
    global bullet_velocity 
    bullet_velocity = int(config[difficulty[pos_num]]["BULLET_VELOCITY"])
    global max_health 
    max_health = int(config[difficulty[pos_num]]["MAX_HEALTH"])

def game():
    set_diff_parameters()
    diff = difficulty[pos_num]
    yellow_bullets = list()
    red_bullets =  list()
    yellow = pygame.Rect(200, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(600, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow_health = red_health = max_health
    clock = pygame.time.Clock()
    draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width - yellow.width//2, yellow.y + yellow.height//2 +2, 20, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == pygame.KEYDOWN and len(red_bullets) < max_bullets:
                if event.key == pygame.K_RCTRL:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 +2, 20, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_menu()

            if event.type == HIT_YELLOW:
                yellow_health -= 1
                if diff == "insane":
                    red_health += 1
                BULLET_HIT_SOUND.play()

            if event.type == HIT_RED:
                red_health -= 1
                if diff == "insane":
                    yellow_health += 1
                BULLET_HIT_SOUND.play()

        keys_pressed = pygame.key.get_pressed()
        
        handle_yellow_movement(keys_pressed, yellow)
        handle_red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)
        
        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)
        
        winner_text = ""
        if yellow_health < 1:
            winner_text = "RED WON!"
        if red_health < 1:
            winner_text = "YELLOW WON!"
        if winner_text != "":
            pygame.time.delay(500)
            GAME_WIN_SOUND.play()
            draw_winner(winner_text)
            main_menu()

def main_menu():
    pygame.display.set_caption("Retro Beam - Menu")
    
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        WIN.blit(SPACE_MENU_IMG, (0,0))
        main_menu_text = M_MENU_FONT1.render("RETRO BEAM - MENU", 1, WHITE)
        info_text1 = M_MENU_FONT2.render("[Press Space to play...]",1,GREEN)
        info_text2 = M_MENU_FONT2.render("[Press Esc to Quit...]",1,GREEN)      
        WIN.blit(info_text1, (WIDTH//2 - info_text1.get_width()//2, 300))
        WIN.blit(info_text2, (WIDTH//2 - info_text2.get_width()//2, 320))

        WIN.blit(main_menu_text, (WIDTH//2 - main_menu_text.get_width()//2, 200))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                run = False
                MENU_SELECT_SOUND.play()
                game()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()

def main():
    main_menu()


if __name__ == "__main__":
    main()
