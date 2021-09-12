import pygame
import os
from pygame.constants import USEREVENT

pygame.font.init() #initialize the font in pygame
pygame.mixer.init() #initialize the sound

RED_HIT = pygame.USEREVENT + 0
YELLOW_HIT = pygame.USEREVENT + 1

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Spaceship Battle')
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 10,  HEIGHT)

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

#SPACESHIPS VARS AND CONSTANTS
VEL = 5
BULLET_VEL = 7
MAX_BULLET_NUM = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
red =  pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
yellow =  pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", 'spaceship_yellow.png'))
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", 'spaceship_red.png'))
RED_SPACESHIP_IMAGE = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    WIN.fill(WHITE)
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_score_txt = HEALTH_FONT.render("Health: " + str(yellow_health), 1, BLACK)
    yellow_score_txt = HEALTH_FONT.render("Health: " + str(red_health), 1, BLACK)

    WIN.blit(red_score_txt, (WIDTH - red_score_txt.get_width() - 10, 10))
    WIN.blit(yellow_score_txt, (10, 10))
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)  
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    pygame.display.update()

def draw_winner(txt):
    draw_txt = WINNER_FONT.render(txt, 1, BLACK)
    WIN.blit(draw_txt, (WIDTH/2 - draw_txt.get_width()/2, HEIGHT/2 - draw_txt.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)


def yellow_handle_movement(keys):
        if keys[pygame.K_a] and (yellow.x - VEL > 0): #LEFT
            yellow.x -= VEL
        if keys[pygame.K_d] and (yellow.x + VEL + SPACESHIP_WIDTH < BORDER.x): #RIGHT
            yellow.x += VEL
        if keys[pygame.K_s] and (yellow.y + SPACESHIP_HEIGHT + VEL < HEIGHT - 15): #DOWN, I don't know why the -5 was needed...
            yellow.y += VEL
        if keys[pygame.K_w] and (yellow.y - VEL) > 0: #UP
            yellow.y -= VEL

def red_handle_movement(keys):
        if keys[pygame.K_LEFT] and (red.x - VEL > BORDER.x + BORDER.width): #LEFT
            red.x -= VEL
        if keys[pygame.K_RIGHT] and (red.x + VEL + SPACESHIP_WIDTH < WIDTH): #RIGHT
            red.x += VEL
        if keys[pygame.K_DOWN] and (red.y + SPACESHIP_HEIGHT + VEL < HEIGHT - 15): #DOWN
            red.y += VEL
        if keys[pygame.K_UP] and (red.y - VEL) > 0: #UP
            red.y -= VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if(yellow.colliderect(bullet)):
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        if(bullet.x < 0):
            red_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if(red.colliderect(bullet)):
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        if(bullet.x > WIDTH):
            yellow_bullets.remove(bullet)
        


def main():
    red_bullets = []
    yellow_bullets = []
    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock() 
    run = True

    while run:
        clock.tick(FPS) #at max FPS cycles p second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and (len(yellow_bullets) < MAX_BULLET_NUM):
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2 + 4, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_KP_0 and (len(red_bullets) < MAX_BULLET_NUM):
                    bullet = pygame.Rect(red.x, red.y + red.height/2 + 5, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed)
        red_handle_movement(keys_pressed)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

        winner_txt = ''
        if(red_health <= 0):
            winner_txt = 'Red wins!!'
        if(yellow_health <= 0):
            winner_txt = 'Yellow wins!!'
        if(winner_txt != ''):
            draw_winner(winner_txt)
            break
    
    main()

if __name__ == '__main__':
    main()
