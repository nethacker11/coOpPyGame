import random
import pickle
import json
import pygame
import time
import sys
import math
import socket
from functions import *
from player import Player, Obstacle 
from pygame.locals import *

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
 
    # Try to connect to the server
    sock = socket.socket()
    try:
        connectToServer(sock)
    except:
        print('Could not connect')

    
    # Connected, now wait for server to find a second player
    # If you are the player, then wait for the board.
    startState = sock.recv(1024)
    if startState == 'player':
        PLAYER = True
    else:
        pass
    

    # Start the player/maker game loop    
    blocks = []
    player = Player(0, 0)
    setPlayer(player, PLAYERWIDTH, PLAYERHEIGHT)

    if PLAYER == False:

        pygame.init()
        FPS = pygame.time.Clock()
        pygame.display.set_caption('Co-Op-Pyration')
        screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT)) 

        setBlocks(blocks, BLOCKWIDTH, BLOCKHEIGHT, NUMBLOCKS)
        makeBoard(blocks, BLOCKWIDTH, BLOCKHEIGHT, screen)
        passBoard(blocks, sock)
        sys.exit()
    else:    
        playBoard = sock.recv(1024)
        boardState = pickle.loads(playBoard)
        for x in range(NUMBLOCKS):
            blocks.append(setPlayerBlock(boardState[x][0], boardState[x][1], BLOCKWIDTH, BLOCKHEIGHT))

        pygame.init()
        FPS = pygame.time.Clock()
        pygame.display.set_caption('Co-Op-Pyration')
        screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT)) 


    # Start the single game loop 
   
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
                    break
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
                pass 
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
#            for i in range(boardState[u'num']):
#               print(newBlocks[i][0])
#               print(newBlocks[i][1])
#               block = Obstacle(newBlocks[i][0], newBlocks[i][1])
#               block.setImg('block.bmp')
#               block.setSize(BLOCKWIDTH, BLOCKHEIGHT)
#               block.setShape(block.x, block.y, BLOCKWIDTH, BLOCKHEIGHT)
#               blocks.append(block)
                
#
#        a = 0
#        print('these are the test prints')
#        for block in blocks:
#            block.x = newBlocks[a][0]
#            block.y = newBlocks[a][1]
#            block.setShape(block.x, block.y, BLOCKWIDTH, BLOCKHEIGHT)
#            a += 1
#
#        for i in blocks:
#            screen.blit(i.blockSize, i.blockShape)


