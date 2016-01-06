#!/usr/bin/env python

import copy
import pygame
import random
import sys

from pygame.locals import *
from pygame import *

# colors
black = (0, 0, 0)
white = (255, 255, 255)
green  = (100, 140, 100)
red = (255, 0, 0)

class Othello:
    
    def __init__(self):
        self.size = 80
        self.length = 8
        self.displaySize = (self.size * self.length, self.size * self.length + 100)
        pygame.init()
        self.clock = pygame.time.Clock()
        display.set_caption("Othello")
        self.display = display.set_mode(self.displaySize)

        # True for player1, False for player2
        self.currentPlayer = True
        self.board = [[0 for x in range(self.length)] for x in range(self.length)]

        self.computerThinking = False
        
        self.mouseLoc = (0, 0)
        self.movePreview = (0, 0)
        self.player = 1 # 1 for white, 2 for black
        self.board[3][3] = 1
        self.board[3][4] = 2
        self.board[4][3] = 2
        self.board[4][4] = 1
        self.corners = [(0, 0), (0, self.length - 1), (self.length - 1, 0),\
                        (self.length - 1, self.length - 1)]
        self.almostCorners = [(0, 1), (1, 0), (1, 1), (self.length - 2, 0),\
                              (self.length - 2, 1), (self.length - 1, 1),\
                              (0, self.length - 2), (1, self.length - 2),\
                              (1, self.length - 1), (self.length - 1, self.length - 2),\
                              (self.length - 2, self.length - 2),\
                              (self.length - 2, self.length - 1)]
        self.gameOver = False
    def handleEvents(self):
        # Handle events, starting with the quit event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if not self.computerThinking:
                if event.type == MOUSEMOTION:
                    self.mouseLoc = event.pos
                    self.movePreview = (self.mouseLoc[0] / self.size,
                                        self.mouseLoc[1] / self.size)
                    if self.movePreview[1] >= self.length:
                        self.movePreview = (self.movePreview[0], self.length - 1)
                if event.type == MOUSEBUTTONDOWN:
                    if self.canFlip(self.movePreview, True):
                        print self.movePreview
                        self.board[self.movePreview[0]][self.movePreview[1]] = self.player
                        self.switchPlayers()
                        self.computerThinking = True
                        
                        if self.noMoveAvailable():
                            self.switchPlayers()
                            self.computerThinking = False
                        if self.noMoveAvailable():
                            print "GAME OVER"    

    def switchPlayers(self):
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def noMoveAvailable(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1 or self.board[i][j] == 2:
                    continue
                if self.canFlip((i, j), False):
                    return False
        return True

    def currentScore(self):
        white, black = 0, 0
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1:
                    white += 1
                if self.board[i][j] == 2:
                    black += 1
        return (white, black)

    # currently assuming that the ai is playing black pieces
    def aiMove(self):
        moveOptions = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == 1 or self.board[i][j] == 2:
                    continue
                oldBoard = copy.deepcopy(self.board)
                if self.canFlip((i, j), True):                    
                    moveOptions.append(((i, j), self.currentScore()[1]))
                self.board = oldBoard
        for option in moveOptions:
            if option[0] in self.corners:
                return option[0]
        moveOptions = sorted(moveOptions, reverse=True, key=lambda tup: tup[1])
        print moveOptions
        for option in moveOptions:
            if option[0] not in self.almostCorners:
                return option[0]
        
        return moveOptions[0][0]
                
    
    def canFlip(self, move, doFlips):
        if self.board[move[0]][move[1]] != 0:
            return False
        moveMade = False
        moveMade |= self.checkLeft(move, doFlips)
        moveMade |= self.checkUpLeft(move, doFlips)
        moveMade |= self.checkUp(move, doFlips)
        moveMade |= self.checkUpRight(move, doFlips)
        moveMade |= self.checkRight(move, doFlips)
        moveMade |= self.checkDownRight(move, doFlips)
        moveMade |= self.checkDown(move, doFlips)
        moveMade |= self.checkDownLeft(move, doFlips)
        return moveMade

    def checkLeft(self, move, doFlips):
        if move[0] <= 0:
            return False
        i = 1
        # go to the left until we hit one of our own tiles
        while self.board[move[0] - i][move[1]] != self.player:
            if self.board[move[0] - i][move[1]] == 0:
                return False
            if move[0] - i <= 0:
                return False    
            i += 1
        # same tile was next to us
        if i == 1:
            return False    
        if self.board[move[0] - i][move[1]] == self.player:
            # do flips
            if doFlips:
                while i > 0:
                    self.board[move[0] - i][move[1]] = self.player
                    i -= 1
            return True
        else:
            return False

    def checkUpLeft(self, move, doFlips):
        if move[0] <= 0 or move[1] <= 0:
            return False
        i, j = 1, 1
        # go to the up left until we hit one of our own tiles
        while self.board[move[0] - i][move[1] - j] != self.player:
            if self.board[move[0] - i][move[1] - j] == 0:
                return False
            if move[0] - i <= 0 or move[1] - j <= 0:
                return False    
            i += 1
            j += 1
        # same tile was next to us
        if i == 1 and j == 1:
            return False    
        if self.board[move[0] - i][move[1] - j] == self.player:
            # do flips
            if doFlips:
                while i > 0:
                    self.board[move[0] - i][move[1] - j] = self.player
                    i -= 1
                    j -= 1
            return True
        else:
            return False

    def checkUp(self, move, doFlips):
        if move[1] <= 0:
            return False
        j = 1
        # go up until we hit one of our own tiles
        while self.board[move[0]][move[1] - j] != self.player:
            if self.board[move[0]][move[1] - j] == 0:
                return False
            if move[1] - j <= 0:
                return False
            j += 1
        # same tile was next to us
        if j == 1:
            return False    
        if self.board[move[0]][move[1] - j] == self.player:
            # do flips
            if doFlips:
                while j > 0:
                    self.board[move[0]][move[1] - j] = self.player
                    j -= 1
            return True
        else:
            return False

    def checkUpRight(self, move, doFlips):
        if move[0] >= 7 or move[1] <= 0:
            return False
        i, j = 1, 1
        # go to the up right until we hit one of our own tiles
        while self.board[move[0] + i][move[1] - j] != self.player:
            if self.board[move[0] + i][move[1] - j] == 0:
                return False
            if move[0] + i >= 7 or move[1] <= 0:
                return False    
            i += 1
            j += 1
        # same tile was next to us
        if i == 1 and j == 1:
            return False    
        if self.board[move[0] + i][move[1] - j] == self.player:
            # do flips
            if doFlips:
                while i > 0:
                    self.board[move[0] + i][move[1] - j] = self.player
                    i -= 1
                    j -= 1
            return True
        else:
            return False


    def checkRight(self, move, doFlips):
        if move[0] >= 7:
            return False
        i = 1
        # go to the right until we hit one of our own tiles
        while self.board[move[0] + i][move[1]] != self.player:
            if self.board[move[0] + i][move[1]] == 0:
                return False
            if move[0] + i >= 7:
                return False    
            i += 1
        # same tile was next to us
        if i == 1:
            return False    
        if self.board[move[0] + i][move[1]] == self.player:
            # do flips
            if doFlips:
                while i > 0:
                    self.board[move[0] + i][move[1]] = self.player
                    i -= 1
            return True
        else:
            return False


    def checkDownRight(self, move, doFlips):
        if move[0] >= 7 or move[1] >= 7:
            return False
        i, j = 1, 1
        # go to the down right until we hit one of our own tiles
        while self.board[move[0] + i][move[1] + j] != self.player:
            if self.board[move[0] + i][move[1] + j] == 0:
                return False
            if move[0] + i >= 7 or move[1] + j >= 7:
                return False
            i += 1
            j += 1
        # same tile was next to us
        if i == 1 and j == 1:
            return False    
        if self.board[move[0] + i][move[1] + j] == self.player:
            # do flips
            if doFlips:
                while i > 0:
                    self.board[move[0] + i][move[1] + j] = self.player
                    i -= 1
                    j -= 1
            return True
        else:
            return False


    def checkDown(self, move, doFlips):
        if move[1] >= 7:
            return False
        j = 1
        # go down until we hit one of our own tiles
        while self.board[move[0]][move[1] + j] != self.player:
            if self.board[move[0]][move[1] + j] == 0:
                return False
            if move[1] + j >= 7:
                return False    
            j += 1
        # same tile was next to us
        if j == 1:
            return False    
        if self.board[move[0]][move[1] + j] == self.player:
            # do flips
            if doFlips:
                while j > 0:
                    self.board[move[0]][move[1] + j] = self.player
                    j -= 1
            return True
        else:
            return False


    def checkDownLeft(self, move, doFlips):
        if move[0] <= 0 or move[1] >= 7:
            return False
        i, j = 1, 1
        # go to the down left until we hit one of our own tiles
        while self.board[move[0] - i][move[1] + j] != self.player:
            if self.board[move[0] - i][move[1] + j] == 0:
                return False
            if move[0] - i <= 0 or move[1] + j >= 7:
                return False    
            i += 1
            j += 1
        # same tile was next to us
        if i == 1 and j == 1:
            return False    
        if self.board[move[0] - i][move[1] + j] == self.player:
            # do flips
            if doFlips:
                while i > 0:
                    self.board[move[0] - i][move[1] + j] = self.player
                    i -= 1
                    j -= 1
            return True
        else:
            return False

    
    def update(self):
        self.display.fill(green)
        self.drawSquares()
        if not self.computerThinking:
            self.drawPreview()
        self.drawScore()

    def drawScore(self):
        score = self.currentScore()
        font = pygame.font.Font(None, 50)
        text = font.render(str(score[0]), 1, (255, 255, 255))
        textpos = text.get_rect(centerx=100, centery=self.size*self.length + self.size / 2)
        self.display.blit(text, textpos)
        text = font.render(str(score[1]), 1, (0, 0, 0))
        textpos = text.get_rect(centerx=500, centery=self.size*self.length + self.size / 2)
        self.display.blit(text, textpos)
        
    def run(self):
        # Runs the game loop
        while True:
            self.handleEvents()
            self.update()
            # Update the full display surface to the screen
            display.update()
            if self.computerThinking and not self.gameOver:
                time.wait(1000)
                self.computerThinking = False
                computerMove = self.aiMove()
                self.canFlip(computerMove, True)
                self.board[computerMove[0]][computerMove[1]] = 2
                self.switchPlayers()
                if self.noMoveAvailable():
                    self.switchPlayers()
                    self.computerThinking = True
                if self.noMoveAvailable():
                    print "GAME OVER"
                    self.gameOver = True

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
