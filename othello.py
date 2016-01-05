#!/usr/bin/env python

import pygame
import sys
import random

from pygame.locals import *
from pygame import *

# colors
black = (0, 0, 0)
white = (255, 255, 255)
green  = (100, 140, 100)

class Othello:
    
    def __init__(self):
        self.size = 80
        self.displaySize = (self.size * 8, self.size * 8)
        pygame.init()
        self.clock = pygame.time.Clock()
        display.set_caption("Othello")
        self.display = display.set_mode(self.displaySize)
        #self.background = Background(self.displaySize)

        # True for player1, False for player2
        self.currentPlayer = True
        self.board = [[0 for x in range(8)] for x in range(8)]

        self.mouseLoc = (0, 0)
        self.movePreview = (0, 0)
        self.player = 1 # 1 for white, 2 for black
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        
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

            if event.type == MOUSEBUTTONDOWN:
                if self.canFlip(self.player, self.movePreview):
                    self.board[self.movePreview[0]][self.movePreview[1]] = self.player
                    if self.player == 1:
                        self.player = 2
                    else:
                        self.player = 1



    def canFlip(self, player, movePreview):
        return True

    def update(self):
        self.display.fill(green)
        self.drawSquares()
        self.drawPreview()
        
    def run(self):
        # Runs the game loop
        while True:
            self.handleEvents()
            self.update()
            # Update the full display surface to the screen
            display.update()            
            # Limit the game to 30 frames per second
            self.clock.tick(30)

    def drawPreview(self):
        if self.board[self.movePreview[0]][self.movePreview[1]] == 0:               
            center = (self.movePreview[0] * self.size + self.size / 2,
                      self.movePreview[1] * self.size + self.size / 2)
            if self.player == 1:
                draw.circle(self.display, white, center, self.size / 2)
            else:
                draw.circle(self.display, black, center, self.size / 2)
            
    def drawSquares(self):
        for i in range(8):
            for j in range(8):
                square = Rect(i * self.size, j * self.size, self.size, self.size)
                draw.rect(self.display, black, square, 1)
                center = (i * self.size + self.size / 2, j * self.size +
                          self.size / 2)
                if self.board[i][j] == 1:
                    draw.circle(self.display, white, center, self.size / 2)
                if self.board[i][j] == 2:
                    draw.circle(self.display, black, center, self.size / 2)
            
if __name__ == '__main__':
    game = Othello()
    game.run()
