import random #for generating random numbers
import sys #we will sys.exit to exit the program
import pygame
from pygame.locals import * #Basic pygame imports

#global variable for the gameimport 
FPS=32
SCREENWIDTH=289
SCREENHEIGHT=511
SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY=SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='gallery/sprites/bird.png'
BACKGROUND='gallery/sprites/background.png'
PIPE='gallery/sprites/pipe.png'

def welcomeScreen():
    """
    shows welcome image on the screen
    """

    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_height())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex=0
    while True:
        for event in pygame.event.get(): # It tells which button you have pressed
            #if user press cross button,close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()

            #If the user presses the space or up key,start the game for them
            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score=0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex=0

    #create 2 pipes for blitting on the screen
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()

    #my list of upper pipes
    upperpipes=[
        {'x':SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']}
    ]
    #my list of lower pipes
    lowerpipes=[
        {'x':SCREENWIDTH+200,'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[1]['y']}
    ]

    pipeVelx = -4

    playervelY = -9
    playerMaxvelY = 10
    playerMinvely = -8
    playerAccY = 1

    playerFlapAccv = -8 #velocity while flapping
    playerFlapped = False #It is true only when the bird is flapping


    while True :
        for event in pygame.event.get():  
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery > 0:
                    playervelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
                
        
        crashTest = isCollide(playerx, playery, upperpipes, lowerpipes) #this fn will return true if the player is crashed
        if crashTest:
            return

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperpipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score+=1
                print(f"your score is {score}")
                try:
                    GAME_SOUNDS['point'].play()
                except:
                    print("point.wav sound error")


        if playervelY < playerMaxvelY and not playerFlapped:
            playervelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playervelY , GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperpipes , lowerpipes ):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx

            # add a new pipe when the first pipe is about to cross the leftmost part of the screen
        if 0 < upperpipes[0]['x'] < 5 :
            newpipe=getRandomPipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

             # if the pipe is out of the screen , remove it
        if upperpipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)        

                # let's blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],( 0,0 ))
        for upperPipe , lowerPipe in zip(upperpipes , lowerpipes ):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperPipe['x'] ,upperPipe['y'] ))
            SCREEN.blit(GAME_SPRITES['pipe'][1],( lowerPipe['x'],lowerPipe['y'] ))

            SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
            SCREEN.blit(GAME_SPRITES['player'],(playerx ,playery ))
        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in mydigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit] , (Xoffset, SCREENHEIGHT*0.12))
                Xoffset += GAME_SPRITES['numbers'][digit]. get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperpipes, lowerpipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperpipes:
        pipeheight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeheight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerpipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']
                and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe() : 
    """
    generate positions of two pipes(bottom one straight and top one rotated) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX=SCREENWIDTH+10
    y1=pipeHeight-y2+offset
    pipe=[
        {'x':pipeX,'y':-y1},#upper pipe
        {'x':pipeX,'y':y2}#lower pipe
    ]
    return pipe


if __name__=="__main__":
    #This will be the main point from where the game will start
    pygame.init() #Initialize all pygame's modules
    FPSCLOCK=pygame.time.Clock()
    pygame.display.set_caption('FLAPPY BIRD')
    GAME_SPRITES['numbers']=(
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )
    
    GAME_SPRITES['message']=pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe']= ( 
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )


    #Game sounds
    GAME_SOUNDS['die']=pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit']=pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point']=pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()

while True:
    welcomeScreen() #shows welcome screen until the user presses a button
    mainGame() #This is the main game function
