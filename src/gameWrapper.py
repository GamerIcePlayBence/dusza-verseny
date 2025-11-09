import pygame
import math

from src import game

swapAnimTime = 0.3
selectedOffset = 8

dungeonAnimTime = 0.1
selectedDungonOffset = 0.4

class DungeonSelectWrapper:
    def __init__(self, width:float, height:float, x:float, y:float, dungeon:game.Dungeon):
        self.cardRect:pygame.Rect = pygame.Rect(x,y,width,height)
        self.pos:list[float] = [x,y]
        self.destPos:float = -1
        self.speed:float = -1
        self.dungeon:game.Dungeon = dungeon
        self.selected = False

        self.title_render1 = ""
        self.title_render2 = ""
        if self.dungeon.name.count(" ") >= 1 and self.dungeon.name.count(" ") < 2:
            self.space_dungeon_name1 = self.dungeon.name.split(" ")[0]
            self.space_dungeon_name2 = self.dungeon.name.split(" ")[1]
            self.title_render1 = pygame.font.Font("src/font/Minister Std Bold.otf", 60).render( self.space_dungeon_name1, True, (255,255,255))
            self.title_render2 = pygame.font.Font("src/font/Minister Std Bold.otf", 60).render(self.space_dungeon_name2, True, (255,255,255))
            self.title_render1k = pygame.font.Font("src/font/Minister Std Bold.otf", 30).render( self.space_dungeon_name1, True, (255,255,255))
            self.title_render2k = pygame.font.Font("src/font/Minister Std Bold.otf", 30).render(self.space_dungeon_name2, True, (255,255,255))
        elif self.dungeon.name.count(" ") == 2:
            self.space_dungeon_name1 = self.dungeon.name.split(" ")[0]
            self.space_dungeon_name2 = self.dungeon.name.split(" ")[1] + " " + self.dungeon.name.split(" ")[2]
            self.title_render1 = pygame.font.Font("src/font/Minister Std Bold.otf", 60).render( self.space_dungeon_name1, True, (255,255,255))
            self.title_render2 = pygame.font.Font("src/font/Minister Std Bold.otf", 37).render(self.space_dungeon_name2, True, (255,255,255))
            self.title_render1k = pygame.font.Font("src/font/Minister Std Bold.otf", 30).render( self.space_dungeon_name1, True, (255,255,255))
            self.title_render2k = pygame.font.Font("src/font/Minister Std Bold.otf", 26).render(self.space_dungeon_name2, True, (255,255,255))

    def update(self,deltaTime):
        if self.destPos == -1:
            return 

        if self.speed == -1:
            distancex = self.destPos - self.pos[0] 
            self.speed = distancex/dungeonAnimTime

        if self.destPos != -1:
            if abs(self.pos[0] - self.destPos) < 0.1:
                self.pos[0] = self.destPos
                self.destPos = -1
                self.speed = -1
            else:
                self.pos[0] += self.speed*deltaTime
                if (self.pos[0] > self.destPos and self.speed > 0) or \
                    (self.pos[0] < self.destPos and self.speed < 0):
                    self.pos[0] = self.destPos
                    self.destPos = -1
                    self.speed = -1
            self.cardRect.x = int(self.pos[0])

    def draw(self,screen):
        widthoffset = self.cardRect.w*selectedDungonOffset
        if self.selected:
            pygame.draw.rect(screen,(255,0,0),(self.cardRect.x-widthoffset//2,self.cardRect.y-widthoffset,self.cardRect.w+widthoffset,self.cardRect.h+widthoffset),border_radius=10)
            if self.dungeon.name.count(" ") >= 1 and self.dungeon.name.count(" ") < 2:
                screen.blit(self.title_render1, (self.cardRect.centerx-200+len(self.dungeon.name)*5, self.cardRect.centery-150))
                screen.blit(self.title_render2, (self.cardRect.centerx-200+len(self.dungeon.name)*5, self.cardRect.centery-50))
            elif self.dungeon.name.count(" ") == 2:
                screen.blit(self.title_render1, (self.cardRect.centerx-140+len(self.dungeon.name)*5, self.cardRect.centery-150))
                screen.blit(self.title_render2, (self.cardRect.centerx-270+len(self.dungeon.name)*5, self.cardRect.centery-50))

        else:
            pygame.draw.rect(screen,(255,0,0),self.cardRect,border_radius=10)
            if self.dungeon.name.count(" ") >= 1 and self.dungeon.name.count(" ") < 2:
                screen.blit(self.title_render1k, (self.cardRect.centerx-140+len(self.dungeon.name)*5, self.cardRect.centery-50))
                screen.blit(self.title_render2k, (self.cardRect.centerx-140+len(self.dungeon.name)*5, self.cardRect.centery))
            elif self.dungeon.name.count(" ") == 2:
                screen.blit(self.title_render1k, (self.cardRect.centerx-120+len(self.dungeon.name)*5, self.cardRect.centery-50))
                screen.blit(self.title_render2k, (self.cardRect.centerx-215+len(self.dungeon.name)*5, self.cardRect.centery))

class CardSelectWrapper:
    def __init__(self, width:float, height:float, x:float, y:float, card:game.Card):
        self.cardRect:pygame.Rect = pygame.Rect(x,y,width,height)
        self.pos:list[float] = [x,y]
        self.destPos:tuple[float,float] = (-1,-1)
        self.speed:tuple = (-1,-1)
        self.card:game.Card = card
        self.selected = False

        self.font = pygame.font.Font("src/font/Minister Std Bold.otf", 35)
        self.title_render = pygame.font.Font("src/font/Minister Std Bold.otf", 25-(len(self.card.name)-6)).render(self.card.name, True, (255,255,255))
        self.space_card_name1 = ""
        self.space_card_name2 = ""
        self.title_render1 = ""
        self.title_render2 = ""
        if self.card.name.find(" ") >= 1:
            self.space_card_name1 = self.card.name.split(" ")[0]
            self.space_card_name2 = self.card.name.split(" ")[1]
            self.title_render1 = pygame.font.Font("src/font/Minister Std Bold.otf", 25-(len(self.space_card_name1)-6)).render( self.space_card_name1, True, (255,255,255))
            self.title_render2 = pygame.font.Font("src/font/Minister Std Bold.otf", 25-(len(self.space_card_name2)-6)).render(self.space_card_name2, True, (255,255,255))
            
        self.stats_render = self.font.render(str(self.card.baseDmg) + "/"+ str(self.card.baseHp), True, (255,255,255))
        self.type_render = self.font.render(self.card.type, True, (255,255,255))

    def update(self,deltaTime,animtime:float):
        if self.destPos == (-1,-1):
            return 

        if animtime == -1:
            animtime = swapAnimTime

        if self.speed[0] == -1:
            distancex = self.destPos[0] - self.pos[0] 
            self.speed = (distancex/animtime,self.speed[1])
        if self.speed[1] == -1:
            distancey = self.destPos[1] - self.pos[1] 
            self.speed = (self.speed[0],distancey/animtime)

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
        if self.card.name.find(" ") >= 1:
            if len(self.space_card_name1) <= 4:
                screen.blit(self.title_render1, (self.cardRect.centerx-35, self.cardRect.top+11))
            else:
                screen.blit(self.title_render1, (self.cardRect.centerx-45, self.cardRect.top+11))
            screen.blit(self.title_render2, (self.cardRect.centerx-35, self.cardRect.top+35))
        else:
            screen.blit(self.title_render, (self.cardRect.centerx-35, self.cardRect.top+11))

        screen.blit(self.stats_render, (self.cardRect.centerx-28, self.cardRect.centery-8))
        if self.card.type == "levego":
            screen.blit(self.type_render, (self.cardRect.centerx-55, self.cardRect.centery+27))
        else:
            screen.blit(self.type_render, (self.cardRect.centerx-30, self.cardRect.centery+27))


def putInORtakeOut(card1:CardSelectWrapper, user:game.User):
    card1index = user.cardNames[card1.card.name]

    card1inselected = -1

    counter = 0
    for index in user.selected:
        if index == card1index:
            card1inselected = counter
            break
        counter +=1

    # the card has to be put in
    if card1inselected < 0:
        user.addCardToPack(card1.card.name)
    else:
        user.removeCardFromPack(card1.card.name)

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



