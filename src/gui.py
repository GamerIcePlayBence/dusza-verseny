import pygame
from src import gameWrapper
from src import game

width, height = 1280, 720

#FO = főmenü
#KARTYA = kártya menü
MENU = "FO"

user = None

#dungeon selection menu
mode = 0
centered = 0
dungeons:list[gameWrapper.DungeonSelectWrapper] = []
drawncards:list[gameWrapper.CardSelectWrapper] = []

dungeonCardWidth = 250
dungeonCardHeight = 300
onscreen = 3
margins = (width/onscreen - dungeonCardWidth)/2
spaceperdungeon = (dungeonCardWidth+margins*2)
dungeonYpos = 300

dungeonCharCardHeight = 144
dungeonCharCardWidth = 108
dungeonCharMargin = 10
dungeonCharYpos = 625           #the center of the card

#card selection menu
#első, az hogy melyik listában van (0=pack;1=gyüjtemény) második, hogy hanyadik
selectedCards:list[tuple[int,int]] = []
cardlayer = None
scrollamount = 0
linepoint = 0
cardsInPack:list[gameWrapper.CardSelectWrapper] = []
cards:list[gameWrapper.CardSelectWrapper] = []
putinortakeoutCARD = []

def play_sound(typein):
    select_sound = pygame.mixer.Sound("src/sound/select_sound.wav")
    cbb_sound = pygame.mixer.Sound("src/sound/click_back_button_sound.wav")
    if typein == "select":
        select_sound.play()
    elif typein == "wood":
        cbb_sound.play()

def shiftFocus():
    global centered
    for i in range(len(dungeons)):
        if mode != centered:
            dungeons[i].destPos = (i-(centered-1))*spaceperdungeon+margins-(mode-centered)*spaceperdungeon
        dungeons[i].selected = mode==i
    centered = mode

    drawncards.clear()
    counter = 0
    xpos = width/2 - len(dungeons[mode].dungeon.cards)*(dungeonCharMargin*2+dungeonCharCardWidth)/2
    percard = (dungeonCharMargin*2+dungeonCharCardWidth)
    for card in dungeons[mode].dungeon.cards:
        drawncards.append(gameWrapper.CardSelectWrapper(dungeonCharCardWidth,dungeonCharCardHeight,xpos+counter*percard+dungeonCharMargin,dungeonCharYpos-dungeonCharCardHeight//2,game.availableCards[game.cardLookup[card]]))
        counter+=1

def select_kazamata(screen,background,deltaTime):
    if len(dungeons) == 0:
        counter = 1
        for dungeon in game.availableDungeons:
            dungeons.append(gameWrapper.DungeonSelectWrapper(dungeonCardWidth,dungeonCardHeight,spaceperdungeon*counter+margins,dungeonYpos-dungeonCardHeight//2,dungeon))
            counter += 1
        shiftFocus()

    pygame.display.set_caption("Kazamata választás")
    screen.blit(background,(0,0))


    for dungeon in dungeons:
        dungeon.update(deltaTime)
        dungeon.draw(screen)

    for card in drawncards:
        card.draw(screen)

    pygame.draw.line(screen, (0, 0, 0), (0, 500), (1280, 500), width=10)

        #for i in range(len(game.availableDungeons[2].cards)):
        #    K_POS_X = 1050 - i*200
        #    K_Rect = pygame.Rect(K_POS_X, 500, 150, 200)
        #    pygame.draw.rect(screen, MK_Color, K_Rect, border_radius=10)
        #    pygame.draw.rect(screen, (0, 0, 0), K_Rect, width=4, border_radius=10)
    #Borders


def kazamata_update(event):
    global mode
    if event.type == pygame.MOUSEWHEEL:
        mode -= event.y
        if mode > len(dungeons)-1:
            mode = len(dungeons)-1
        if mode < 0:
            mode = 0
        shiftFocus()


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

    game.newLeader("Torak","Lord Torak","sebzes")
    game.newLeader("Selia","Priestess Selia","eletero")


    global user
    user = game.User()

    user.addCard("Arin")
    user.addCard("Liora")
    user.addCard("Selia")
    user.addCard("Nerun")
    user.addCard("Torak")


    user.addCardToPack("Arin")
    user.addCardToPack("Liora")
    user.addCardToPack("Selia")

def backtodungeon():
    play_sound("wood")

def checkForCollision(scrollamount:int,rect:pygame.Rect, point:tuple)->bool:
    #check if it isn't in the same column:
    if point[0] <= rect.x or rect.x+rect.w <= point[0]:
        return False
    #check if it isn't in the same row:
    if point[1] <= rect.y+scrollamount or rect.y+rect.h+scrollamount <= point[1]:
        return False
    return True

def selectPackScreenEventHandler(event):
    global scrollamount
    scrollspeed = 14
    if event.type == pygame.MOUSEWHEEL:
        scrollamount += event.y*scrollspeed
        if scrollamount > 0:
            scrollamount = 0
    elif event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:
            counter = 0
            for card in cardsInPack:
                if checkForCollision(scrollamount,card.cardRect,event.pos):
                    play_sound("select")
                    putinortakeoutCARD.append(card)
                    return
                counter+=1

            counter = 0
            for card in cards:
                if checkForCollision(scrollamount,card.cardRect,event.pos):
                    play_sound("select")
                    putinortakeoutCARD.append(card)
                    return
                counter+=1
        if event.button == 1:
            counter = 0
            for card in cardsInPack:
                if checkForCollision(scrollamount,card.cardRect,event.pos):
                    play_sound("select")
                    card.selected = not card.selected
                    if card.selected:
                        selectedCards.append((0,counter))
                    else:
                        countertwo = 0
                        for pair in selectedCards:
                            if pair[0] == 0 and pair[1] == counter:
                                selectedCards.pop(countertwo)
                                break
                            countertwo+=1
                    return
                counter+=1

            counter = 0
            for card in cards:
                if checkForCollision(scrollamount,card.cardRect,event.pos):
                    play_sound("select")
                    card.selected = not card.selected
                    if card.selected:
                        selectedCards.append((1,counter))
                    else:
                        countertwo = 0
                        for pair in selectedCards:
                            if pair[1] == 0 and pair[1] == counter:
                                selectedCards.pop(countertwo)
                                break
                            countertwo+=1
                    return
                counter+=1

            back_rect = pygame.Rect(0, 0, 120, 60)    
            if back_rect.collidepoint(event.pos):
                backtodungeon()

def updateSelectPackScreen(screen,deltaTime:float,user,background):
    global scrollamount
    if cardlayer == None:
        print("Couldn't initialize card layer")
        return
    if abs(scrollamount) > cardlayer.get_height()-height:
        scrollamount = -(cardlayer.get_height()-height)

    cardlayer.fill((0,0,0,0))
    pygame.draw.line(cardlayer,(255,255,255),(0,linepoint),(width,linepoint))

    if len(putinortakeoutCARD) > 0:
        if (len(cardsInPack) == 1 and not putinortakeoutCARD[0] in cardsInPack) or \
                (len(cardsInPack) > 1):
            gameWrapper.putInORtakeOut(putinortakeoutCARD[0],user)
            cardsInPack.clear()
            cards.clear()
            drawCards(screen,background)
        putinortakeoutCARD.clear()


    if len(selectedCards)>=2:
        if selectedCards[0][0] == 0:
            if selectedCards[1][0] == 0:
                gameWrapper.swapCards(cardsInPack[selectedCards[0][1]],cardsInPack[selectedCards[1][1]],user)
            if selectedCards[1][0] == 1:
                gameWrapper.swapCards(cardsInPack[selectedCards[0][1]],cards[selectedCards[1][1]],user)
        if selectedCards[0][0] == 1:
            if selectedCards[1][0] == 0:
                gameWrapper.swapCards(cards[selectedCards[0][1]],cardsInPack[selectedCards[1][1]],user)
            if selectedCards[1][0] == 1:
                gameWrapper.swapCards(cards[selectedCards[0][1]],cards[selectedCards[1][1]],user)
        selectedCards.clear()

    for card in cardsInPack:
        card.update(deltaTime)
        card.draw(cardlayer)
    for card in cards:
        card.update(deltaTime)
        card.draw(cardlayer)

    if background == None:
        screen.fill((0,0,0))
    else:
        screen.blit(background,(0,scrollamount))
    screen.blit(cardlayer,(0,scrollamount))

    back_texture = pygame.image.load("src/img/Backarrow.png").convert_alpha()
    back_rect = pygame.Rect(0, 0, 120, 60)
    scaled_texture = pygame.transform.scale(back_texture, (back_rect.width, back_rect.height))
    screen.blit(scaled_texture, back_rect.topleft)


def drawCards(screen,background):
    global cardlayer
    global linepoint
    margin = 10
    colcount:int = 10
    cardwidth:int = int(width/colcount-margin*2)
    cardheight = cardwidth*4//3
    if user == None:
        print("USER WASNT INITIALISED\n")
        return
    rows = len(user.selected)//colcount
    ypos = (cardheight+margin*2)*(rows + 1)

    linepoint = ypos


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

    colnum:int = 0
    counter:int = 0
    for card in user.cards:
        if counter in user.selected:
            counter += 1
            continue
        amountInRow = 0
        if len(user.cards)-len(user.selected) - (colnum // colcount)*colcount > colcount:
            amountInRow = colcount
        else:
            amountInRow = len(user.cards)-len(user.selected) - (colnum // colcount)*colcount
        x:float = (colnum%colcount)*(2*margin+cardwidth)+margin + width/2-(amountInRow)*(margin*2+cardwidth)/2
        y:float = ypos+margin+(margin*2+cardheight)*(colnum//colcount)
        cards.append(gameWrapper.CardSelectWrapper(cardwidth,cardheight,x,y,card))
        colnum += 1
        counter += 1


    if cardlayer == None:
        cardlayerheight = (rows+len(user.cards)//colcount)*(margin*2+cardheight)
        if cardlayerheight < height:
            cardlayerheight = height
        cardlayer = pygame.Surface((width,cardlayerheight),pygame.SRCALPHA)

    cardlayer.fill((0,0,0,0))
    pygame.draw.line(cardlayer,(255,255,255),(0,ypos),(width,ypos))

    for card in cardsInPack:
        card.draw(cardlayer)
    for card in cards:
        card.draw(cardlayer)

    screen.blit(background,(0,0))
    screen.blit(cardlayer,(0,0))



def UIMain():
    create()
    pygame.init()
    background = pygame.image.load("./src/img/BG.jpg")
    background = pygame.transform.scale(background,(width,height))

    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill((255, 255, 255))
    running = True
    clock:pygame.time.Clock = pygame.time.Clock()

    if MENU=="KARTYA":
        drawCards(screen,background)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if MENU == "FO":
                kazamata_update(event)
            else:
                selectPackScreenEventHandler(event)

        fps = clock.get_fps()
        if fps == 0:
            fps = 0.00001
        deltaTime:float = 1/fps
        if MENU == "FO":
            select_kazamata(screen,background,deltaTime)
        else:
            updateSelectPackScreen(screen,deltaTime,user,background)

        pygame.display.flip()
        clock.tick(120)
    pygame.quit()
