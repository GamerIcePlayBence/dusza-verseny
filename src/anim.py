import pygame
import math

class SwordAnim:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.frame = 0
        self.pic = pygame.image.load("./src/img/sword.png").convert_alpha()
        self.finalangle = 60
        self.animtime = 3
        self.innerclock:float = 0
        self.done = False

    def _animtiming(self)->float:
        return math.sin(self.innerclock*math.pi/self.animtime)*self.finalangle

    def playAnim(self,deltaTime,screen):
        rotatedtext = pygame.transform.rotate(self.pic,self._animtiming())
        rect = rotatedtext.get_rect()

        screen.blit(rotatedtext,(self.height-rect.height,0))

        rotatedtext = pygame.transform.flip(rotatedtext,True,False)
        rect = rotatedtext.get_rect()

        screen.blit(rotatedtext,(self.height-rect.height,self.width-rect.width))

        self.innerclock+=deltaTime
        if self.innerclock >=self.animtime :
            self.done = True
