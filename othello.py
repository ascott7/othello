#!/usr/bin/env python

import pygame
import sys
import random

from pygame.locals import *
from pygame import *

class Othello:
    
    def __init__(self):
        self.size = 80
        self.displaySize = (self.size * 8, self.size * 8)
        pygame.init()
        display.set_caption("Othello")
        self.display = display.set_mode(self.displaySize)
        #self.background = Background(self.displaySize)

        # True for player1, False for player2
        self.currentPlayer = True
        self.board = [[Square(80) for x in range(8)] for x in range(8)]

        self.mouseLoc = (0, 0)
        self.movePreview = (0, 0)
    def handleEvents(self):
        
        # Handle events, starting with the quit event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEMOTION:
                self.mouseLoc = event.pos
                self.movePreview = (self.mouseLoc[0] / self.size,
                                    self.mouseLoc[1] / self.size)
    def update(self):
        display.fill((100, 145, 100))
# The class for the background
#class Background:
    
#    def __init__(self, displaySize):
        
        # Set our image to a new surface, the size of the screen rectangle
#        self.image = Surface(displaySize)
        
        # Fill the image with a green colour (specified as R,G,B)
#        self.image.fill((27, 210, 57))
        
        # Get width proportionate to display size
#        lineWidth = displaySize[0] / 80
        
        # Create a rectangle to make the white line
 #       lineRect = Rect(0, 0, lineWidth, displaySize[1])
  #      lineRect.centerx  = displaySize[0] / 2
   #     draw.rect(self.image, (255, 255, 255), lineRect)
        
    #def draw(self, display):
            
        # Draw the background to the display that has been passed in
     #   display.blit(self.image, (0,0))


class Square:
    """
    Board square class. The color data member tells us what is in the square
    currently (0 = empty, 1 = white, 2 = black).
    """
    def __init__(self, size):
        self.color = 0
        self.size = size

    def getColor(self):
        return self.color

    def flip(self):
        if self.color == 1:
            self.color = 2
        else:
            self.color = 1

    def setColor(self, color):
        self.color = color
            
if __name__ == '__main__':
    game = Othello()
