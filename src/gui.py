import pygame
import random
from src import gameWrapper
from src import game

width, height = 1280, 720

user = None

#card selection menu
cardlayer = None
scrollamount = 0
cardsInPack:list[gameWrapper.CardSelectWrapper] = []
cards:list[gameWrapper.CardSelectWrapper] = []

def select_kazamata(screen, mode):
    pygame.display.set_caption("Kazamata választás")
    screen.fill((255, 255, 255))
    BP_Color = (0, 255, 0)
    OSZ_Color = (255, 0, 0)
    MK_Color = (0, 0, 255)

    pygame.draw.line(screen, (0, 0, 0), (0, 450), (1280, 450), width=10)

    if mode == "BP":
        for i in game.availableDungeons:
            if i.name == "Barlangi Portya":
                K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02, K_COLOR = 480, 40, 300, 400, BP_Color
            elif i.name == "Osi Szentely":
                K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02, K_COLOR = 100, 140, 200, 300, OSZ_Color
            elif i.name == "A melyseg kiralynoje":
                K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02, K_COLOR = 980, 140, 200, 300, MK_Color
            else:
                continue
        
            Dungeons_Rect = pygame.Rect(K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02)
            K_Rect = pygame.Rect(560, 500, 150, 200)
            pygame.draw.rect(screen, K_COLOR, Dungeons_Rect, border_radius=10)
            pygame.draw.rect(screen, BP_Color, K_Rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), K_Rect, width=4, border_radius=10)

    elif mode == "OSZ":
        for i in game.availableDungeons:
            if i.name == "Barlangi Portya":
                K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02, K_COLOR = 980, 140, 200, 300, BP_Color
            elif i.name == "Osi Szentely":
                K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02, K_COLOR = 480, 40, 300, 400, OSZ_Color
            elif i.name == "A melyseg kiralynoje":
                K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02, K_COLOR = 100, 140, 200, 300, MK_Color
            else:
                continue
        
            Dungeons_Rect = pygame.Rect(K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02)
            pygame.draw.rect(screen, K_COLOR, Dungeons_Rect, border_radius=10)

        for i in range(len(game.availableDungeons[1].cards)):
            K_POS_X = 760 - i*200
            K_Rect = pygame.Rect(K_POS_X, 500, 150, 200)
            pygame.draw.rect(screen, OSZ_Color, K_Rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), K_Rect, width=4, border_radius=10)

    elif mode == "MK":   
        for i in game.availableDungeons:
            if i.name == "Barlangi Portya":
                K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02, K_COLOR = 100, 140, 200, 300, BP_Color
            elif i.name == "Osi Szentely":
                K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02, K_COLOR = 980, 140, 200, 300, OSZ_Color
            elif i.name == "A melyseg kiralynoje":
                K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02, K_COLOR = 480, 40, 300, 400, MK_Color
            else:
                continue
        
            Dungeons_Rect = pygame.Rect(K_POS_X, K_POS_Y, K_SIZE_01, K_SIZE_02)
            pygame.draw.rect(screen, K_COLOR, Dungeons_Rect, border_radius=10)

        for i in range(len(game.availableDungeons[2].cards)):
            K_POS_X = 1050 - i*200
            K_Rect = pygame.Rect(K_POS_X, 500, 150, 200)
            pygame.draw.rect(screen, MK_Color, K_Rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), K_Rect, width=4, border_radius=10)
    
    #Borders
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(480, 40, 300, 400), width=4, border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(100, 140, 200, 300), width=4, border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(980, 140, 200, 300), width=4, border_radius=10)





def create():
    game.newDungeon("Barlangi Portya", "Egyszerű kazamata", ["Nerun"], "sebzés")
    game.newDungeon("Osi Szentely", "Kis kazamata", ["Arin", "Emera", "Selia", "Lord Torak"], "életerő")
    game.newDungeon("A melyseg kiralynoje", "Nagy kazamata", ["Liora", "Arin", "Selia", "Nerun", "Torak", "Priestess Selia"], "")

    game.newCard("Arin", 2, 5, "föld")
    game.newCard("Liora", 2, 4, "levegő")
    game.newCard("Selia", 2, 6, "víz")
    game.newCard("Nerun", 3, 3, "tűz")
    game.newCard("Torak", 3, 4, "föld")
    game.newCard("Emera", 2, 5, "levegő")
    game.newCard("Kael", 3, 5, "tűz")
    game.newCard("Myra", 3, 6, "föld")
    game.newCard("Thalen", 3, 5, "levegő")
    game.newCard("Isara", 2, 6, "víz")

    #TEST
    for i in range(30):
        game.newCard(str(i)+"TEST",2,5,"tuz")


    global user
    user = game.User()

    user.addCard("Arin")
    user.addCard("Liora")
    user.addCard("Selia")
    user.addCard("Nerun")
    user.addCard("Torak")

    #TEST
    for i in range(30):
        user.addCard(str(i)+"TEST")

    user.addCardToPack("Arin")
    user.addCardToPack("Liora")
    user.addCardToPack("Selia")

    #TEST
    for i in range(20):
        user.addCardToPack(str(i)+"TEST")


def selectPackScreenEventHandler(event):
    global scrollamount
    scrollspeed = 14
    if event.type == pygame.MOUSEWHEEL:
        scrollamount += event.y*scrollspeed
        if scrollamount > 0:
            scrollamount = 0
    if event.type == pygame.MOUSEBUTTONDOWN:
        for card in cardsInPack:
            if card.cardRect.collidepoint(event.pos):
                print("card clicked")
                card.select()
                return
        for card in cards:
            if card.cardRect.collidepoint(event.pos):
                print("card clicked")
                card.select()
                return

def updateSelectPackScreen(screen,deltaTime:float):
    global scrollamount
    if cardlayer == None:
        print("Couldn't initialize card layer")
        return
    if abs(scrollamount) > cardlayer.get_height()-height:
        scrollamount = -(cardlayer.get_height()-height)
    screen.blit(cardlayer,(0,scrollamount))

def startselectPackScreen(screen):
    global cardlayer
    margin = 10
    colcount:int = 10
    cardwidth:int = int(width/colcount-margin*2)
    cardheight = cardwidth*4//3
    if user == None:
        print("USER WASNT INITIALISED\n")
        return
    rows = len(user.selected)//colcount
    ypos = (cardheight+margin*2)*(rows + 1)



    if len(cardsInPack) == 0 and len(user.selected) != 0:
        colnum:int = 0
        for index in user.selected:
            card = user.cards[index]
            amountInRow = 0
            if len(user.selected) - (colnum // colcount)*colcount > colcount:
                amountInRow = colcount
            else:
                amountInRow = len(user.selected) - (colnum // colcount)*colcount
            x:float = (colnum%colcount)*(2*margin+cardwidth)+margin + width/2-(amountInRow)*(margin*2+cardwidth)/2
            y:float = margin+(margin*2+cardheight)*(colnum//colcount)
            cardsInPack.append(gameWrapper.CardSelectWrapper(cardwidth,cardheight,x,y,card))
            colnum += 1
    elif len(cardsInPack) > 0 and len(user.selected) == 0:
        cardsInPack.clear()

    if len(cards) == 0 and len(user.cards) != 0:
        colnum:int = 0
        for card in user.cards:
            amountInRow = 0
            if len(user.cards) - (colnum // colcount)*colcount > colcount:
                amountInRow = colcount
            else:
                amountInRow = len(user.cards) - (colnum // colcount)*colcount
            x:float = (colnum%colcount)*(2*margin+cardwidth)+margin + width/2-(amountInRow)*(margin*2+cardwidth)/2
            y:float = ypos+margin+(margin*2+cardheight)*(colnum//colcount)
            cards.append(gameWrapper.CardSelectWrapper(cardwidth,cardheight,x,y,card))
            colnum += 1
    elif len(cards) > 0 and len(user.cards) == 0:
        cardsInPack.clear()


    cardlayer = pygame.Surface((width,(rows+len(user.cards)//colcount)*(margin*2+cardheight)))
    cardlayer.fill((125,122,30))

    pygame.draw.line(cardlayer,(255,255,255),(0,ypos),(width,ypos))

    for card in cardsInPack:
        pygame.draw.rect(cardlayer,(0,125,125),card.cardRect,border_radius=3)
    for card in cards:
        pygame.draw.rect(cardlayer,(125,125,125),card.cardRect,border_radius=3)

    screen.blit(cardlayer,(0,0))



def UIMain():
    create()
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill((255, 255, 255))
    running = True
    clock:pygame.time.Clock = pygame.time.Clock()

    startselectPackScreen(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            selectPackScreenEventHandler(event)

        fps = clock.get_fps()
        if fps == 0:
            fps = 0.00001
        deltaTime:float = 1/fps
        updateSelectPackScreen(screen,deltaTime)
        pygame.display.flip()
        clock.tick(120)
    pygame.quit()
