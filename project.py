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
    
    playerInput = []

    while True:

        player.setShape(player.x, player.y, PLAYERWIDTH, PLAYERHEIGHT)
        getPlayerInput(player)

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
        if player.up == True:
            player.y -= 3 
        elif player.down == True:
                player.y += 3


if __name__ == '__main__':
    main()

