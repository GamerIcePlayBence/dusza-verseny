import pygame
import math

from src import game

swapAnimTime = 0.3
selectedOffset = 8

class CardSelectWrapper:
    # self.cardRect = a kártya maga
    def __init__(self, width:float, height:float, x:float, y:float, card:game.Card):
        self.cardRect:pygame.Rect = pygame.Rect(x,y,width,height)
        self.pos:list[float] = [x,y]
        self.destPos:tuple[float,float] = (-1,-1)
        self.speed:tuple = (-1,-1)
        self.card:game.Card = card
        self.selected = False

    def update(self,deltaTime):
        if self.destPos == (-1,-1):
            return 

        if self.speed[0] == -1:
            distancex = self.destPos[0] - self.pos[0] 
            self.speed = (distancex/swapAnimTime,self.speed[1])
        if self.speed[1] == -1:
            distancey = self.destPos[1] - self.pos[1] 
            self.speed = (self.speed[0],distancey/swapAnimTime)

        if self.destPos[0] != -1:
            if abs(self.pos[0] - self.destPos[0]) < 0.1:
                self.pos[0] = self.destPos[0]
                self.destPos = (-1,self.destPos[1])
                self.speed = (-1,self.speed[1])
            else:
                self.pos[0] += self.speed[0]*deltaTime
                if (self.pos[0] > self.destPos[0] and self.speed[0] > 0) or \
                    (self.pos[0] < self.destPos[0] and self.speed[0] < 0):
                    self.pos[0] = self.destPos[0]
                    self.destPos = (-1,self.destPos[1])
                    self.speed = (-1,self.speed[1])
            self.cardRect.x = int(self.pos[0])

        if self.destPos[1] != -1:
            if abs(self.pos[1] - self.destPos[1]) < 0.1:
                self.pos[1] = self.destPos[1]
                self.destPos = (self.destPos[0],-1)
                self.speed = (self.speed[0],-1)
            else:
                self.pos[1] += self.speed[1]*deltaTime
                if (self.pos[1] > self.destPos[1] and self.speed[1] > 0) or \
                    (self.pos[1] < self.destPos[1] and self.speed[1] < 0):
                    self.pos[1] = self.destPos[1]
                    self.destPos = (self.destPos[0],-1)
                    self.speed = (self.speed[0],-1)
            self.cardRect.y = int(self.pos[1])

    def draw(self,screen):
        if self.selected:
            pygame.draw.rect(screen,(255,255,0),(self.cardRect.x-selectedOffset//2,self.cardRect.y-selectedOffset//2,self.cardRect.w+selectedOffset,self.cardRect.h+selectedOffset),border_radius=10)
        pygame.draw.rect(screen,(255,0,0),self.cardRect,border_radius=10)


def swapCards(card1:CardSelectWrapper, card2:CardSelectWrapper, user:game.User):
    card1.destPos = (card2.cardRect.x,card2.cardRect.y)
    card2.destPos = (card1.cardRect.x,card1.cardRect.y)
    card1.selected = False
    card2.selected = False

    card1index = user.cardNames[card1.card.name]
    card2index = user.cardNames[card2.card.name]

    card1inselected = -1
    card2inselected = -1

    counter = 0
    for index in user.selected:
        if index == card1index:
            card1inselected = counter
        if index == card2index:
            card2inselected = counter
        counter +=1

    if card1inselected < 0:
        if card2inselected < 0:
            print("None selected")
            pass #ha egyik sincs a selected-be akkor teljesen mindegy hogy mi történik velük
        else:
            user.selected[card2inselected] = card1index
    else:
        if card2inselected < 0:
            user.selected[card1inselected] = card2index
        else:
            user.selected[card1inselected] = card2index
            user.selected[card2inselected] = card1index

    print(user.selected)

