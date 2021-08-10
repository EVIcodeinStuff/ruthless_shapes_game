#Designed and Coded by Elliott Iannello
#Diddy-Kong Theme Remix by John Steadman
#Based off The Dodger Game in Al Sweigarts book Invent Your Own Computer Games with Python
#1/30/12


import pygame
import sys
import random
from pygame.locals import *

# colors
BLACK = [0, 0, 0]
WHITE = [255, 255, 255]
GREEN = [0, 255, 0]

# other constants
SHAPEMAXSIZE = 95
SHAPEMINSIZE = 30
HEIGHT = 700
WIDTH = 900
PLAYERMOVERATE = 5
SHAPEMOVEMIN = 1
SHAPEMOVEMAX = 6
SPAWNRATE = 45
FPS = 40
HIGHSCORE = 0


# funciton to see if player wants to quit
def gameQuit():
    pygame.quit()
    sys.exit()

#waits for player input and if input represents an exit command terminates the game
def waitForPlayer():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                gameQuit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    gameQuit()
                return

# handles all text display
def displayText(text, surf, font, posx, posy):
    t = font.render(text, 1, BLACK)
    trect = t.get_rect()
    trect.topleft = (posx, posy)
    surf.blit(t, trect)

def shapeCollision(pRect, shapesArray):
    for s in shapesArray:
        if pRect.colliderect(s['rect']):
            return True
    return False
    
# initialize Pygame
pygame.init()
mainClock = pygame.time.Clock()
myfont = pygame.font.SysFont(None, 36)

# set up the window
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Ruthless Shapes: The Game!')

#sound
pygame.mixer.music.load('Audio/RuthlessShapes.wav')

#player
playerAliveImage = pygame.image.load('Sprites/playerAlive.png')
shapeImageOne = pygame.image.load('Sprites/shapeone.png')
shapeImageTwo = pygame.image.load('Sprites/shapetwo.png')
shapeImageThree = pygame.image.load('Sprites/shapethree.png')
shapeImageFour = pygame.image.load('Sprites/shapefour.png')
shapeImage = shapeImageOne
pRect = playerAliveImage.get_rect()


#Start Screen
windowSurface.fill(GREEN)

displayText('RUTHLESS SHAPES: THE GAME!', windowSurface, myfont, 240, 50)
displayText('PRESS ANY KEY TO START', windowSurface, myfont, 240, 150)
displayText('RULES: Dodge as many shapes as you can', windowSurface, myfont, 60, 260)
displayText('         without getting hit. Difficulty goes up over time', windowSurface, myfont, 60, 350)
displayText('         and Radiation kills from range, so stay extra Clear!', windowSurface, myfont, 60, 450)

pygame.display.update()
waitForPlayer()

while True:
    #setup start conditions
    shapesArray = []
    score = 0
    pRect.topleft = ((WIDTH/2), (HEIGHT/2))
    mUp = False
    mDown = False
    mRight = False
    mLeft = False
    shapeCounter = 0
    difficulty = 0
    pygame.mixer.music.play(-1, 0.0)
    
    while True: # game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                gameQuit()

            #control with keyboard
           
            if event.type == KEYDOWN:
                if event.key == ord('w') or event.key == K_UP:
                    mDown = False
                    mUp = True
                if event.key == ord('s') or event.key == K_DOWN:
                    mUp = False
                    mDown = True
                if event.key == ord('a') or event.key == K_LEFT:
                    mRight = False
                    mLeft = True
                if event.key == ord('d') or event.key == K_RIGHT:
                    mLeft = False
                    mRight = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    gameQuit()
                if event.key == ord('w') or event.key == K_UP:
                    mUp = False
                if event.key == ord('s') or event.key == K_DOWN:
                    mDown = False
                if event.key == ord('a') or event.key == K_LEFT:
                    mLeft = False
                if event.key == ord('d') or event.key == K_RIGHT:
                    mRight = False

        shapeCounter = shapeCounter + 1
        if shapeCounter == SPAWNRATE:
            shapeCounter = 0
            difficulty = difficulty + 1
            if difficulty > 10 and SPAWNRATE > 7:
                SPAWNRATE = SPAWNRATE - 1
                difficulty = 0
            score = score + 1
            num = random.randint(1,24)
            if num < 4:
                shapeImage = shapeImageTwo
            if num >= 4 and num < 11:
                shapeImage = shapeImageThree
            if num >= 11 and num < 18:
                shapeImage = shapeImageOne
            if num >= 18:
                shapeImage = shapeImageFour
            shapeSize = random.randint(SHAPEMINSIZE, SHAPEMAXSIZE)
            newShape = {'rect': pygame.Rect(random.randint(0, WIDTH-shapeSize), 0 - shapeSize, shapeSize, shapeSize),
                        'speed': random.randint(SHAPEMOVEMIN, SHAPEMOVEMAX),
                        'surface' : pygame.transform.scale(shapeImage, (shapeSize, shapeSize)),
                        }
            shapesArray.append(newShape)
        
        #move player on screen
        if mUp and pRect.top > 0:
            pRect.move_ip(0, -1 * PLAYERMOVERATE)
        if mDown and pRect.bottom < HEIGHT:
            pRect.move_ip(0,PLAYERMOVERATE)
        if mLeft and pRect.left > 0:
            pRect.move_ip(-1*PLAYERMOVERATE, 0)
        if mRight and pRect.right < WIDTH:
            pRect.move_ip(PLAYERMOVERATE, 0)

        #move shapes
        for s in shapesArray:
            dirnum = random.randint(1,20)
            if dirnum < 11:
                s['rect'].move_ip(0, s['speed'])
            if dirnum >= 11 and dirnum < 16:
                s['rect'].move_ip(s['speed'], 0)
            if dirnum >= 16:
                s['rect'].move_ip(-s['speed'], 0)

        #remove dodged shapes
        for s in shapesArray[:]:
            if s['rect'].top > HEIGHT:
                shapesArray.remove(s)

        #draw display updates
        windowSurface.fill(WHITE)
        #draw player
        windowSurface.blit(playerAliveImage, pRect)
        #score
        displayText('Score: %s' %(score), windowSurface, myfont, 10, 0)
        displayText('High Score: %s' %(HIGHSCORE), windowSurface, myfont, 150, 0)
        #shapes
        for s in shapesArray:
            windowSurface.blit(s['surface'], s['rect'])

        pygame.display.update()

        #check for collisions
        if shapeCollision(pRect, shapesArray):
            if score > HIGHSCORE:
                HIGHSCORE = score
            break

        mainClock.tick(FPS)

    windowSurface.fill(GREEN)
    pygame.mixer.music.stop()
    SPAWNRATE = 45
    displayText('GAME OVER! Press Any Key to Have Another go', windowSurface, myfont, 140, 130)
    displayText('Designed by Elliott Iannello', windowSurface, myfont, 140, 330)
    displayText('Music by John Steadman', windowSurface, myfont, 140, 430)
    pygame.display.update()
    waitForPlayer()
                


  
    
    


            
