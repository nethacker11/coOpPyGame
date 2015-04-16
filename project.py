import projectClasses
import random
import pygame
import time
import sys
import math
from test import Player 
from pygame.locals import *



def setBlocks(blocks):
    loc = 0
    for x in range(6):
        block = Player(0, 0)
        block.setImg('block.bmp')
        block.setSize(50, 50)
        block.setShape(loc, 0, 50, 50)
        blocks.append(block)
        loc += 60

def reset(block, blocks):
    block.x = 0        
    block.y = 0
    del blocks[:]   
    setBlocks(blocks)

def main():
    FPS = 30
    WINWIDTH = 640
    WINHEIGHT = 480
    KEYPRESS_UP = False
    KEYPRESS_DOWN = False
    PAUSE = False
    MOVING = False
    

    
    pygame.init()
    FPS = pygame.time.Clock()
    pygame.display.set_caption('PY project')
    screen = pygame.display.set_mode((WINWIDTH, WINHEIGHT)) 

    timeout = time.time() + 5 
    black = 0,0,0

    blocks = []
    setBlocks(blocks)


    while True:
        if time.time() > timeout:
            break
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mousePoint = pygame.mouse.get_pos()
                for block in blocks:
                    if block.blockShape.collidepoint(mousePoint):
                        MOVING = True
                        movingBlock = block
            elif event.type == MOUSEBUTTONUP:
                MOVING = False
        
        if MOVING == True:
            p = pygame.mouse.get_pos()
            movingBlock.setShape(p[0], p[1], 50, 50)




        screen.fill(black)
        for i in blocks:
            screen.blit(i.blockSize, i.blockShape)
        pygame.display.flip()

    
    
    
    
    
    
    player = Player(0, 0)
    player.setImg('block.bmp')
    player.setSize(50, 50)
    player.x = 10
    player.y = 10
    width = 50
    height = 50
   # blockRect = pygame.Rect(x, y, width, height)
    
    while True:
        if PAUSE == True:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == pygame.K_u:
                        PAUSE = False
        if PAUSE == True:
            continue
        player.setShape(player.x, player.y, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            elif event.type == KEYDOWN:
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
            elif event.type == MOUSEBUTTONDOWN:
                p = pygame.mouse.get_pos()
                for i in blocks:
                    if i.blockShape.collidepoint(p):
                        MOVING = True
                        movingBlock = i
            elif event.type == MOUSEBUTTONUP:
                MOVING = False
        
        if MOVING == True:
            p = pygame.mouse.get_pos()
            movingBlock.setShape(p[0], p[1], 50, 50)




        screen.fill(black)
        screen.blit(player.blockSize, player.blockShape)
        for i in blocks:
            if player.blockShape.colliderect(i.blockShape):
                #reset(player, blocks)
                print('collision')
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
