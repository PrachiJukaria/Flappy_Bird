import random #for genrating random number
import sys #sys.exit() to exit the program
import pygame
from pygame.locals import *  # basic pygame import

#global game variable
FPS=32
SCREENWIDTH =289 
SCREENHEIGHT=511

SCREEN=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY= SCREENHEIGHT*0.8
GAME_SPRITES={}
GAME_SOUNDS ={}
PLAYER='gallery/sprites/bird.png'
BACKGROUND='gallery/sprites/background.png'
PIPE='gallery/sprites/pipe.png'

def welcomeScreen():        #shows welcome images on the screen
    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex=int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey=int(SCREENHEIGHT*0.13)
    basex=0
    while True:
        for event in pygame.event.get():
            #if user clcik on cross button close the game
            if event.type == pygame.QUIT or (event.type ==pygame.KEYDOWN and event.key ==pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if the user press space key or up key start the game
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
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
    playerx=int(SCREENWIDTH/5)
    playery=int(SCREENWIDTH/2)
    basex=0

    #create two pipe for blitting on screen
    newPipe1=getrandompipe()
    newPipe2=getrandompipe()

    #my list of upper pipes

    upperPipes=[
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[0]['y']},
    ]
    #my list of lower pipes
    lowerPipes=[
        {'x': SCREENWIDTH+200,'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2),'y':newPipe2[1]['y']},
    ]

    pipeVelX=-4
    playerVelY=-9
    playerMaxVelY=10
    playerMinVelY=-8
    playerAccY=1

    playerFlapAccv=-8   #velocity while flapping
    playerFlapped = False    #it is true only when bird is flapping

    while True:
        for event in pygame.event.get():
            #if user clcik on cross button close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key ==K_ESCAPE):
                pygame.quit()
                sys.exit()

            # if the user press space key or up key start the game
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        crashTest=isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return

        #check for score
        playerMidPos=playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos=pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<=playerMidPos and playerMidPos<pipeMidPos+4:
                score+=1
                print(f'your score is {score}')
                GAME_SOUNDS['point'].play()
        
            
        if (playerVelY<playerMaxVelY and not playerFlapped):
            playerVelY+=playerAccY

        if playerFlapped:
            playerFlapped = False
        playerheight=GAME_SPRITES['player'].get_height()
        playery=playery + min(playerVelY , GROUNDY - playery - playerheight)

            #move pipes to the left
        for upperpipe,lowerpipe in zip(upperPipes,lowerPipes):
            upperpipe['x']+=pipeVelX
            lowerpipe['x']+=pipeVelX

        #add a new pipe when the first pipe about to cross the screen
        if 0<upperPipes[0]['x']<5:
            newpipe=getrandompipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #if the pipe is out of the screen remove it
        if upperPipes[0]['x']< -(GAME_SPRITES['pipe'][0].get_width()):
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe, lowerpipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))

            SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
            SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
            myDigit=[int(x) for x in list(str(score))]
            width=0
        for digit in myDigit:
            width+=GAME_SPRITES['numbers'][digit].get_width()
            xoffset=(SCREENWIDTH-width)/2

        for digit in myDigit:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(xoffset,SCREENHEIGHT*0.12))
            xoffset+=GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)



def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False


            




            


def getrandompipe():
    '''
    genrate position of two pipe(one top straight and one rotated) for blitting on the screen
    '''
    pipeHeight=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREENHEIGHT/3
    y2=offset+random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height()-1.2*offset))
    pipex=SCREENWIDTH+10
    y1=pipeHeight-y2+offset
    pipe=[
        {'x':pipex , 'y':-y1},
        {'x':pipex, 'y':y2}
    ]
    return pipe

if __name__=="__main__":
    #this will be the main pouint from which our game will start
    pygame.init()   #initialise all pygame module
    FPSCLOCK=pygame.time.Clock()  #clock control the fps of game
    pygame.display.set_caption("Flappy bird by prachi jukaria")
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
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )
    GAME_SPRITES['message']=pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base']=pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe']=(
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )

    #game sonds
    GAME_SOUNDS['die']=pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit']=pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point']=pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh']=pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing']=pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert_alpha()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()

    while True:  #gaming loop
        welcomeScreen()   #shows the welcome screen to the user
        mainGame()  #this is the main game