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

def setPlayerBlock(x, y, width, height):
    posX = x
    posY = y
    print(x)
    print(y)
    block = Obstacle(posX, posY)
    block.setImg('block.bmp')
    block.setSize(width, height)
    block.setShape(x, y, width, height)

    return block


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
    timeout = time.time() + 10 
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
                        diffX = p[0] - block.x
                        diffY = p[1] - block.y
                        movingBlock.x = block.x + diffX
                        movingBlock.y = block.y + diffY
                       # block.setShape(p[0] - diffX, p[1] - diffY, width, height)
            elif event.type == MOUSEBUTTONUP:
                MOVING = False
        if MOVING == True:
            
            p = pygame.mouse.get_pos()
            movingBlock.setShape(p[0] - diffX, p[1] - diffY, width, height)
        screen.fill(black)
        for i in blocks:
            screen.blit(i.blockSize, i.blockShape)
        pygame.display.flip()


def connectWithPlayer(clientSocket, serverSocket):
    try:
        socket.connect('127.0.0.1', 3000)
        print('Connected with player')
        return 1
    except:
        print('Waiting for players....')
        c, addr = serverSocket.accept()
        print('Connected with player')
    
def passBoard(blocks, sock):
    boardState = {}
    boardState['num'] = len(blocks)
    blockList = []

    for block in blocks:
        blockList.append([block.x, block.y])
       
    sock.send(pickle.dumps(blockList))

def connectToServer(sock):
    try:
        sock.connect(('104.236.244.24', 8888))
    except:
        try:
            sock.connect(('104.236.244.24', 9999))
        except:
            try:
                sock.connect(('104.236.244.24', 1010))
            except:
                sys.exit()


'''
        for block in blocks:
            if block.moving == True:
                print('hello')
                p = pygame.mouse.get_pos()
                block.setShape(p[0] - diffX, p[1] - diffY, width, height)
                #block.moving = False
'''


