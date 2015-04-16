import pygame

class Player():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def setImg(self, image):
        self.image = pygame.image.load(image)

    def setSize(self, width, height):
        self.blockSize = pygame.transform.scale(self.image, (width, height))

    def setShape(self, x, y, width, height):
        self.blockShape = pygame.Rect(x, y, width, height)


