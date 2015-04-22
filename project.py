import random
import json
import pygame
import time
import sys
import math
import socket
from player import Player, Obstacle 
from pygame.locals import *

def setBlocks(blocks, width, height, num):
    posX = 0
    posY = 0
    for x in range(num):
        block = Obstacle(posX, posY)
        block.setImg('block.bmp')
        block.setSize(width, height)
        block.setShape(block.x, block.y, width, height)
        blocks.append(block)
        posX += 60


def setPlayer(player, width, height):
    player.setImg('block.bmp')
    player.setSize(50, 50)


def reset(block, blocks):
    block.x = 0        
    block.y = 0
    del blocks[:]   
   # setBlocks(blocks) fix

def makeBoard(blocks, width, height, screen):

    MOVING = False
    diffX = 0 # Offset when moving blocks
    diffY = 0 # Offset when moving blocks
    timeout = time.time() + 5 
    black = 0,0,0

    while True:
        if time.time() > timeout:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mousePoint = pygame.mouse.get_pos()
                for block in blocks:
                    if block.blockShape.collidepoint(mousePoint):
                        MOVING = True
                        movingBlock = block
                        p = pygame.mouse.get_pos()
                        diffX = p[0] - movingBlock.x
                        diffY = p[1] - movingBlock.y
                        block.x = block.x + diffX
                        block.y = block.y + diffY
            elif event.type == MOUSEBUTTONUP:
                MOVING = False
        if MOVING == True:
            p = pygame.mouse.get_pos()
            movingBlock.setShape(p[0] - diffX, p[1] - diffY, width, height)
        screen.fill(black)
        for i in blocks:
            screen.blit(i.blockSize, i.blockShape)
        pygame.display.flip()

def connectToServer(sock):
    try:
        sock.connect((SERVER, PORTONE))
    except:
        try:
            sock.connect((SERVER, PORTTWO))
        except:
            try:
                sock.connect((SERVER, PORTTHREE))
            except:
                print('could not connect')
                sys.exit()




def connectWithPlayer(clientSocket, serverSocket):
    try:
        socket.connect('127.0.0.1', 3000)
        print('Connected with player')
        return 1
    except:
        print('Waiting for players....')
        c, addr = serverSocket.accept()
        print('Connected with player')
    
def passBoard(blocks):
    boardState = {}
    boardState['num'] = len(blocks)
    blockList = []

    for block in blocks:
        blockList.append([block.x, block.y])
       
    boardState['regular'] = blockList
    
    jsonBoardState = json.dumps(boardState)
    print(jsonBoardState)
#        sock.send(jsonBoardState)



def main():
    FPS = 30
    WINWIDTH = 640
    WINHEIGHT = 480
    BLOCKWIDTH = 50
    BLOCKHEIGHT = 50
    PLAYERWIDTH = 50
    PLAYERHEIGHT = 50
    NUMBLOCKS = 6
    BLACK = 0,0,0
    KEYPRESS_UP = False
    KEYPRESS_DOWN = False
    PAUSE = False
    MOVING = False
    PLAYER = False
    SERVER = '104.236.244.24'
    PORTONE = 8888
    PORTTWO = 9999
    PORTTHREE = 1010


    sock = socket.socket()
    try:
        connectToServer(sock)
    except:
        print('could not connect')

  
    pygame.init()
    FPS = pygame.time.Clock()
    pygame.display.set_caption('PY project')
    screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT)) 

    blocks = []
    setBlocks(blocks, BLOCKWIDTH, BLOCKHEIGHT, NUMBLOCKS)
    
    player = Player(0, 0)
    setPlayer(player, PLAYERWIDTH, PLAYERHEIGHT)

    makeBoard(blocks, BLOCKWIDTH, BLOCKHEIGHT, screen)

    if PLAYER == False:
        passBoard(blocks)

        

   
    while True:

        if PAUSE == True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_u:
                        PAUSE = False
        if PAUSE == True:
            continue
        player.setShape(player.x, player.y, PLAYERWIDTH, PLAYERHEIGHT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_q:
                    sys.exit()
                if event.key == pygame.K_DOWN or event.key == K_s:
                    KEYPRESS_DOWN = True
                elif event.key == pygame.K_UP: # not sure why 
                                               # event.key in (K_UP)        
                                               # doesnt work
                    KEYPRESS_UP = True
                elif event.key == pygame.K_p:
                    PAUSE = True
            elif event.type == KEYUP:
                if event.key in (K_UP, K_w):
                    KEYPRESS_UP = False
                elif event.key in (K_DOWN, K_s):
                    KEYPRESS_DOWN = False


        screen.fill(BLACK)
        screen.blit(player.blockSize, player.blockShape)
        for i in blocks:
            if player.blockShape.colliderect(i.blockShape):
                None
                #reset(player, blocks)
            screen.blit(i.blockSize, i.blockShape)
        pygame.display.flip()
        player.x += 1
        player.y += 1
        if KEYPRESS_UP == True:
            player.y -= 3 
        elif KEYPRESS_DOWN == True:
            player.y += 3








if __name__ == '__main__':
    main()

