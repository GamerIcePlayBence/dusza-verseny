import pygame
import math

from src import game

swapAnimTime = 1
selectedOffest = 4

class CardSelectWrapper:
    # self.cardRect = a kártya maga
    def __init__(self, width:float, height:float, x:float, y:float, card:game.Card):
        self.cardRect:pygame.Rect = pygame.Rect(x,y,width,height)
        self.pos:list[float] = [x,y]
        self.destPos:tuple[float,float] = (0,0)
        self.speed = -1
        self.card:game.Card = card

    def update(self,deltaTime):
        if self.speed == -1:
            distance:float = math.sqrt((self.destPos[0]-self.cardRect.x)**2 + (self.destPos[1]-self.cardRect.y)**2)
            self.speed = distance/swapAnimTime

        if self.pos[0] < self.destPos[0]:
            self.pos[0] += self.speed*deltaTime
        elif abs(self.pos[0] - self.destPos[0]) > 0.1:
            self.pos[0] -= self.speed*deltaTime

        if self.pos[1] < self.destPos[1]:
            self.pos[1] += self.speed*deltaTime
        elif abs(self.pos[1] - self.destPos[1]) > 0.1:
            self.pos[1] -= self.speed*deltaTime
    def select(self):
        self.pos[0] -= selectedOffest//2
        self.pos[1] -= selectedOffest//2
        self.cardRect.x -= selectedOffest//2
        self.cardRect.y -= selectedOffest//2
        self.cardRect.width += selectedOffest
        self.cardRect.height += selectedOffest
    def deselect(self):
        self.pos[0] += selectedOffest//2
        self.pos[1] += selectedOffest//2
        self.cardRect.x += selectedOffest//2
        self.cardRect.y += selectedOffest//2
        self.cardRect.width -= selectedOffest
        self.cardRect.height -= selectedOffest

def swapCards(card1:CardSelectWrapper, card2:CardSelectWrapper):
    card1.destPos = (card2.cardRect.x,card2.cardRect.y)
