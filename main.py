import pygame
import os
pygame.font.init()
pygame.mixer.init()

pygame.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH//2 -5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assests', 'collide.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assests', 'shoot.mp3'))
EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join('assests', 'explosion.wav'))

HEALTH_FONT = pygame.font.SysFont('comicscan', 40)
WINNER_FONT = pygame.font.SysFont('comiscan', 100)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assests', 'yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assests', 'red.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assests', 'space.png')), (WIDTH, HEIGHT))

def draw(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    # WIN.fill(WHITE) # fills the windows with the color given in parameter(rgb)
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y)) # .blit() is used to draw something on the win
    WIN.blit(RED_SPACESHIP, (red.x, red.y))


    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # left
            yellow.x -= VEL
        
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width - 15 < BORDER.x: # Right
        yellow.x += VEL
    
    if keys_pressed[pygame.K_w] and yellow.y - VEL - 15 > 0: # Up
        yellow.y -= VEL
    
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height + 15 < HEIGHT: # Down
        yellow.y += VEL

def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # left
            red.x -= VEL
        
    if keys_pressed[pygame.K_RIGHT] and red.x + red.width < WIDTH: # Right
        red.x += VEL
    
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # Up
        red.y -= VEL
    
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height + 15 < HEIGHT: # Down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    red = pygame.Rect(700, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 100, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    
    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health < 0:
            winner_text = "Yellow Wins!"

        if yellow_health < 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            EXPLOSION_SOUND.play()
            pygame.time.delay(500)
            winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed() # is used to check whether key stays being pressed
        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw(red, yellow, red_bullets, yellow_bullets,
                    red_health, yellow_health)

    pygame.quit()

if __name__ == '__main__':
    main()

