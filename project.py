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
    CONNECTED = False

    playAgain = pygame.image.load('playAgain.bmp')
    playAgainSize = pygame.transform.scale(playAgain, (200, 200))
    playAgainShape = pygame.Rect((WINWIDTH/2)-100, (WINHEIGHT/2)-100, 200, 200)


    # Try to connect to the server
    sock = socket.socket()
    try:
        connectToServer(sock)
        CONNECTED = True
    except:
        print('Could not connect')

    pygame.init()
    FPS = pygame.time.Clock()
    pygame.display.set_caption('Co-Op-Pyration')
    screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT)) 

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

    if CONNECTED == True:
        if PLAYER == False:
            setBlocks(blocks, BLOCKWIDTH, BLOCKHEIGHT, NUMBLOCKS)
            makeBoard(blocks, BLOCKWIDTH, BLOCKHEIGHT, screen)
            passBoard(blocks, sock)
            sys.exit()
        else:    
            playBoard = sock.recv(1024)
            boardState = pickle.loads(playBoard)
            for x in range(NUMBLOCKS):
                blocks.append(setPlayerBlock(boardState[x][0], boardState[x][1], BLOCKWIDTH, BLOCKHEIGHT))
    else:
        setBlocksRand(blocks, WINWIDTH, WINHEIGHT, BLOCKWIDTH, BLOCKHEIGHT, NUMBLOCKS)


    # Start the single game loop 
    
    playerInput = []
    
    mainLoop(player, PLAYERWIDTH, PLAYERHEIGHT, BLACK, blocks, screen, playAgainSize, playAgainShape, WINWIDTH, WINHEIGHT, NUMBLOCKS, BLOCKWIDTH, BLOCKHEIGHT)

if __name__ == '__main__':
    main()

