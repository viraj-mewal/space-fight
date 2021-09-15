import pygame
import os
import tkinter as tk
from tkinter import messagebox
from pygame.locals import *
pygame.font.init()
pygame.mixer.init()

class button():
    def __init__(self, color, x, y, width, height, text='', font_size=20):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.font_size)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True


class Game:
    def __init__(self):
        pygame.init()
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.pink = (232, 116, 242)
        self.light_blue = (140, 227, 237)
        self.qbhc = (237, 121, 226)
        self.qbc = (230, 223, 16)

        self.FPS = 60
        self.VEL = 5
        self.BULLET_VEL = 7
        self.MAX_BULLETS = 5
        self.SPACESHIP_WIDTH = 55
        self.SPACESHIP_HEIGHT = 40
        self.WIDTH = 900
        self.HEIGHT = 500
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Fight")
        
        self.YELLOW_HIT = pygame.USEREVENT + 1
        self.RED_HIT = pygame.USEREVENT + 2
        self.BORDER = pygame.Rect(self.WIDTH//2 -5, 0, 10, self.HEIGHT)

        self.BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assests', 'collide.mp3'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assests', 'shoot.mp3'))
        self.EXPLOSION_SOUND = pygame.mixer.Sound(os.path.join('assests', 'explosion.wav'))

        self.HEALTH_FONT = pygame.font.SysFont('comicscan', 40)
        self.WINNER_FONT = pygame.font.SysFont('comiscan', 100)

        self.SPACESHIP_WIDTH = 55
        self.SPACESHIP_HEIGHT = 40
        self.YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assests', 'yellow.png'))
        self.RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('assests', 'red.png'))
        self.YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(self.YELLOW_SPACESHIP_IMAGE, (self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)), 90)
        self.RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(self.RED_SPACESHIP_IMAGE, (self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)), 270)
        self.SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assests', 'space.png')), (self.WIDTH, self.HEIGHT))
        self.start_button = button((154, 237, 81),280,200,120,50,text='PLAY', font_size=60)
        self.quit_button = button((255,0,0),480,200,120,50,text='QUIT', font_size=60)
        self.start_button_hover_color = self.light_blue
        self.start_button_color = (154, 237, 81)
        self.quit_button_hover_color = self.qbhc
        self.quit_button_color = (255, 0, 0)
        self.info_button_color = (0, 245, 228)
        self.info_button_hover_color = (0, 255, 0)
        self.info_button_click_color = (240, 115, 240)
        self.info_button = button((0, 245, 228),self.WIDTH-80, 2, 80, 30, text="INFO", font_size=20)


    def info(self):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("INFORMATION", "Yellow Player Controls:-\n->Use 'W' - UP, 'A' - LEFT, 'S' - DOWN, 'D' - RIGHT\n->Use 'F' to fire\n\nRed Player Controls :-\n->Use arrow keys to move\n->Use 'RIGHT CTRL' to fire")


    def draw(self, red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        self.red = red
        self.yellow = yellow
        self.red_bulllets = red_bullets
        self.yellow_bullets = yellow_bullets
        self.red_health = red_health
        self.yellow_health = yellow_health
        self.WIN.fill(self.WHITE)
        self.WIN.blit(self.SPACE, (0, 0))
        # WIN.fill(WHITE) # fills the windows with the color given in parameter(rgb)
        pygame.draw.rect(self.WIN, self.BLACK, self.BORDER)
        red_health_text = self.HEALTH_FONT.render("Health: " + str(red_health), 1, self.WHITE)
        yellow_health_text = self.HEALTH_FONT.render("Health: " + str(yellow_health), 1, self.WHITE)
        self.WIN.blit(red_health_text, (self.WIDTH - red_health_text.get_width() - 10, 10))
        self.WIN.blit(yellow_health_text, (10, 10))

        self.WIN.blit(self.YELLOW_SPACESHIP, (self.yellow.x, self.yellow.y)) # .blit() is used to draw something on the win
        self.WIN.blit(self.RED_SPACESHIP, (self.red.x, self.red.y))

        for bullet in red_bullets:
            pygame.draw.rect(self.WIN, self.RED, bullet)

        for bullet in yellow_bullets:
            pygame.draw.rect(self.WIN, self.YELLOW, bullet)

        pygame.display.update()

    def writeText(self, string, coordx, coordy, fontSize):
        #set the font to write with
        self.font = pygame.font.SysFont('Roboto Slab', fontSize) 
        #(0, 0, 0) is black, to make black text
        self.text = self.font.render(string, True, (255, 215, 0))
        #get the rect of the text
        self.textRect = self.text.get_rect()
        #set the position of the text
        self.textRect.center = (coordx, coordy)
        #add text to window
        self.WIN.blit(self.text, self.textRect)
        #update wind

    def draw_start(self):
        try:
            self.WIN.blit(self.SPACE, (0, 0))
            self.start_button.draw(self.WIN, (1,1,1))
            self.quit_button.draw(self.WIN, (1,1,1))
            self.info_button.draw(self.WIN, (1,1,1))
            self.writeText("SPACE FIGHT", int(self.WIDTH/2), int(self.HEIGHT/2)-160, 100)
            self.WIN.blit(self.RED_SPACESHIP, (int(self.WIDTH/2)+300, int(self.HEIGHT-150)))
            self.WIN.blit(self.YELLOW_SPACESHIP, (int(self.WIDTH/2)-300, int(self.HEIGHT-150)))
            pygame.display.update()
        except:
            pass

    def start(self):
        self.run = True
        while self.run:
            try:
                for self.event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    if self.event.type == pygame.QUIT:
                        self.run = False
                    if self.event.type == pygame.MOUSEBUTTONDOWN:
                        if self.start_button.isOver(pos):
                            self.start_button.color = (203, 253, 90)
                            game = Game()
                            game.run()
                        if self.quit_button.isOver(pos):
                            self.quit_button.color = (237, 231, 140)
                            pygame.quit()
                        
                        if self.info_button.isOver(pos):
                            self.info_button.color = self.info_button_click_color
                            print("info button clicked")
                            self.info()
                            
                    if self.event.type == pygame.MOUSEMOTION:
                        if self.start_button.isOver(pos):
                            self.start_button.color = self.start_button_hover_color
                        else:
                            self.start_button.color = self.start_button_color

                        if self.quit_button.isOver(pos):
                            self.quit_button.color = self.quit_button_hover_color
                        else:
                            self.quit_button.color = self.quit_button_color
                        
                        if self.info_button.isOver(pos):
                            self.info_button.color = self.info_button_hover_color
                        else:
                            self.info_button.color = self.info_button_color
                    
                    
                    if self.event.type == pygame.KEYDOWN:
                        if self.event.key == pygame.K_ESCAPE:
                            self.run = False
                        
                        

                        
                self.draw_start()
            except:
                pass
        pygame.quit()
    
    def yellow_movement(self, keys_pressed, yellow):
        if keys_pressed[pygame.K_a] and yellow.x - self.VEL > 0: # left
                yellow.x -= self.VEL
            
        if keys_pressed[pygame.K_d] and yellow.x + self.VEL + yellow.width - 15 < self.BORDER.x: # Right
            yellow.x += self.VEL
        
        if keys_pressed[pygame.K_w] and yellow.y - self.VEL - 15 > 0: # Up
            yellow.y -= self.VEL
        
        if keys_pressed[pygame.K_s] and yellow.y + self.VEL + yellow.height + 15 < self.HEIGHT: # Down
            yellow.y += self.VEL

    def red_movement(self, keys_pressed, red):
        if keys_pressed[pygame.K_LEFT] and red.x - self.VEL > self.BORDER.x + self.BORDER.width: # left
                red.x -= self.VEL
            
        if keys_pressed[pygame.K_RIGHT] and red.x + red.width < self.WIDTH: # Right
            red.x += self.VEL
        
        if keys_pressed[pygame.K_UP] and red.y - self.VEL > 0: # Up
            red.y -= self.VEL
        
        if keys_pressed[pygame.K_DOWN] and red.y + self.VEL + red.height + 15 < self.HEIGHT: # Down
            red.y += self.VEL

    def handle_bullets(self, yellow_bullets, red_bullets, yellow, red):
        for bullet in yellow_bullets:
            bullet.x += self.BULLET_VEL
            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.RED_HIT))
                yellow_bullets.remove(bullet)
            elif bullet.x > self.WIDTH:
                yellow_bullets.remove(bullet)

        for bullet in red_bullets:
            bullet.x -= self.BULLET_VEL
            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.YELLOW_HIT))
                red_bullets.remove(bullet)
            elif bullet.x < 0:
                red_bullets.remove(bullet)

    def winner(self, text):
        draw_text = self.WINNER_FONT.render(text, 1, self.WHITE)
        self.WIN.blit(draw_text, (self.WIDTH/2 - draw_text.get_width()/2, self.HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(3000)
    
    def run(self):
            red = pygame.Rect(700, 100, self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)
            yellow = pygame.Rect(100, 100, self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)
            
            red_bullets = []
            yellow_bullets = []

            red_health = 10
            yellow_health = 10

            clock = pygame.time.Clock()
            self.run = True
            while self.run:
                clock.tick(self.FPS)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.run = False
                        if event.key == pygame.K_f and len(yellow_bullets) < self.MAX_BULLETS:
                            bullet = pygame.Rect(
                                yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                            yellow_bullets.append(bullet)
                            self.BULLET_FIRE_SOUND.play()
                        if event.key == pygame.K_RCTRL and len(red_bullets) < self.MAX_BULLETS:
                            bullet = pygame.Rect(
                                red.x, red.y + red.height//2 - 2, 10, 5)
                            red_bullets.append(bullet)
                            self.BULLET_FIRE_SOUND.play()

                    if event.type == self.RED_HIT:
                        red_health -= 1
                        self.BULLET_HIT_SOUND.play()

                    if event.type == self.YELLOW_HIT:
                        yellow_health -= 1
                        self.BULLET_HIT_SOUND.play()

                winner_text = ""
                if red_health == 0:
                    winner_text = "Yellow Wins!"

                if yellow_health == 0:
                    winner_text = "Red Wins!"

                if winner_text != "":
                    self.EXPLOSION_SOUND.play()
                    pygame.time.delay(1000)
                    Game.winner(self, winner_text)
                    break

                keys_pressed = pygame.key.get_pressed() # is used to check whether key stays being pressed
                Game.yellow_movement(self, keys_pressed, yellow)
                Game.red_movement(self, keys_pressed, red)

                Game.handle_bullets(self, yellow_bullets, red_bullets, yellow, red)

                Game.draw(self, red, yellow, red_bullets, yellow_bullets,
                            red_health, yellow_health)

            self.run = False
            pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.start()