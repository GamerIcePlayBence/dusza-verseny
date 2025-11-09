import pygame
import math

class SwordAnim:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.pic = pygame.image.load("./src/img/sword.png").convert_alpha()
        self.pic = pygame.transform.scale_by(self.pic,1.75)
        self.finalangle = 60
        self.animtime = 1.5
        self.innerclock:float = 0
        self.done = False

    def _animtiming(self)->float:
        return math.sin(self.innerclock*math.pi/self.animtime)*self.finalangle

    def playAnim(self,deltaTime,screen):
        self.finalangle = 60
        rotatedtext = pygame.transform.rotate(self.pic,self._animtiming()-90)
        rect = rotatedtext.get_rect()
        self.finalangle = 150
        rect.x = int(self._animtiming())*2-int(self.finalangle)
        rect.y = self.height-rect.h+30

        screen.blit(rotatedtext,(rect))

        rotatedtext = pygame.transform.flip(rotatedtext,True,False)
        rect = rotatedtext.get_rect()
        rect.x = self.width-rect.width-int(self._animtiming())*2+int(self.finalangle)
        rect.y = self.height-rect.h+30

        screen.blit(rotatedtext,(rect))

        if self.innerclock >= self.animtime:
            self.done = True
        self.innerclock+=deltaTime

class Projectileanim:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.y = 0
        self.startx = 0
        self.pic = pygame.image.load("./src/img/projectile.png").convert_alpha()
        #self.pic = pygame.transform.scale_by(self.pic,1.75)
        self.animtime = 2
        self.innerclock:float = 0
        self.done = True
        self.distance = 0

    def _animtiming(self)->float:
        return self.innerclock**2*(self.distance/(self.animtime**2))

    def playAnim(self,deltaTime,screen):
        transformed = self.pic
        if self.distance < 0:
            transformed = pygame.transform.flip(transformed,True,False)

        rect = transformed.get_rect()
        rect.x = int(self.startx + self._animtiming())
        rect.y = int(self.y-rect.h/2)

        if self.distance < 0:
            rect.x -= rect.w

        screen.blit(transformed,(rect))

        if self.innerclock >= self.animtime:
            self.done = True
        self.innerclock+=deltaTime

