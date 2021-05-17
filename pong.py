import pygame
import random

pygame.init()

# dimension variables
WIDTH = 800
HEIGHT = 600
SCORE_HEIGHT = 50
NEW_HEIGHT = HEIGHT - SCORE_HEIGHT


screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Colors in the format(Red, Green, Blue)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (255, 0, 255)
ORANGE = (255, 100, 100)
MY_COLOR = (10, 230, 200)

class Paddle(pygame.sprite.Sprite): #Paddle inherits from Sprite class
    def __init__(self, startX, startY, color=MY_COLOR):
        super().__init__() #Calls Sprite class constructor
        
        self.width = 10
        self.height = 100
        self.speed = 10

        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        
        pygame.draw.rect(self.image, color, (0, 0, self.width, self.height))
        self.rect = self.image.get_rect()

        self.rect.x = startX
        self.rect.y = startY

    def up(self):
        self.rect.y -= self.speed
        if self.rect.y < 53: # account for border on scoreboard
            self.rect.y = 53

    def down(self):
        self.rect.y += self.speed
        if self.rect.y > NEW_HEIGHT-50:
            self.rect.y = NEW_HEIGHT-50


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.width = 10
        self.height = 10
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, WHITE, (0, 0, self.width, self.height))
        self.rect = self.image.get_rect()

        self.rect.x = WIDTH / 2
        self.rect.y = NEW_HEIGHT / 2

        self.xSpeed = random.randint(5, 8)
        self.ySpeed = random.randint(-5, 5)
        
    def update(self):
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed

        # ball bounces off scoreboard and bottom
        if self.rect.y <= SCORE_HEIGHT or self.rect.y >= HEIGHT:
            self.ySpeed = -self.ySpeed            

    def bounce(self):
        if self.xSpeed < 0:
            self.xSpeed -= 1
        else:
            self.xSpeed += 1
            
        self.xSpeed = -self.xSpeed
        self.ySpeed = -self.ySpeed
        self.ySpeed += random.randint(-3, 3)

    def reset(self):
        self.rect.x = WIDTH / 2
        self.rect.y = NEW_HEIGHT / 2
        self.xSpeed = random.uniform(-5, 5) # float: decimal number
        self.ySpeed = random.randint(-5, 5) # int: integer whole number

player1 = Paddle(50, NEW_HEIGHT / 2, PURPLE)
player2 = Paddle(WIDTH - 50, NEW_HEIGHT / 2, ORANGE)
    
ball = Ball()

all_sprites = pygame.sprite.Group()

all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)

score1 = 0
score2 = 0
winScore = 3# first to 3 points wins


# clock used for frames per second
gameClock = pygame.time.Clock()

# game loop
running = True
while(running):

    # Handle Input Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Moves paddle when users press keyboard keys
    # player1: w, s
    # player2: up, down arrows

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1.up()
    if keys[pygame.K_s]:
        player1.down()
    if keys[pygame.K_UP]:
        player2.up()
    if keys[pygame.K_DOWN]:
        player2.down()
    if keys[pygame.K_RIGHT]:
        player2.down()


    # Main Game Functionality
    all_sprites.update()

    # Ball scores
    if ball.rect.x >= WIDTH: # player 1 scores
        score1 += 1
        ball.reset()
        if score1 > winScore:
            print("Player 1 Wins!")
            running = False
        
    elif ball.rect.x <= 0: # player 2 scores
        score2 += 1
        ball.reset()
        if score2 >= winScore:
            print("Player 2 Wins!")
            running = False

    # Collision with paddle
    collision = ball.rect.collidelist([player1, player2])
    if collision != -1:
        ball.bounce()
        
    # Drawing Code
    screen.fill(BLACK) # set background to black

    # draw the scoreboard outline
    pygame.draw.line(screen, WHITE, [0, SCORE_HEIGHT], [WIDTH, SCORE_HEIGHT], 4)
    pygame.draw.line(screen, WHITE, [WIDTH/2, 0], [WIDTH/2, SCORE_HEIGHT], 4)

    #Draw the scores
    font = pygame.font.Font(None, 64)
    text1 = font.render(str(score1), 1, PURPLE)
    screen.blit(text1, (WIDTH/4, 5))
    text2 = font.render(str(score2), 1, ORANGE)
    screen.blit(text2, (WIDTH*3/4, 5))

    all_sprites.draw(screen) # draw sprites

    pygame.display.flip() # update the window

    gameClock.tick(60) #60 fps

pygame.quit() # stop game engine, close window

