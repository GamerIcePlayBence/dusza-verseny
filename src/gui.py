import pygame
from src import anim
from src import gameWrapper
from src import game

width, height = 1280, 720

#FO = főmenü
#KARTYA = kártya menü
#HARC =  harc event
MENU = "FO"

user = None

#fightEvent
projanim:anim.Projectileanim | None = None 
userCards:list[gameWrapper.CardSelectWrapper] = []
dungeonCards:list[gameWrapper.CardSelectWrapper] = []
turn=0
isPlayerMove=False
playerCardOut = 0
dungeonCardOut = 0
output:list[str] = []
swordanim = None
waittime = 0.5
fightclock = 0
endscreen = False
endfightclock = 1
playedDeadAnim = True
WONIMG = None
LOSTIMG = None

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
    path = "src/sound/"
    select_sound = pygame.mixer.Sound(path + "select_sound.wav")
    cbb_sound = pygame.mixer.Sound(path + "click_back_button_sound.wav")
    scroll_sound = pygame.mixer.Sound(path + "scroll.wav")
    fight_sound = pygame.mixer.Sound(path + "fight.wav")
    if typein == "select":
        select_sound.play()
    elif typein == "wood":
        cbb_sound.play()
    elif typein == "scroll":
        scroll_sound.set_volume(0.3)
        scroll_sound.play()
    elif typein == "fight":
        fight_sound.set_volume(0.2)
        fight_sound.play()

def fightEventEventhandler(event):
    global endscreen
    if endscreen:
        if event.type==pygame.MOUSEBUTTONDOWN:
            global turn
            global isPlayerMove
            global dungeonCardOut
            global playerCardOut
            global output
            global fightclock
            global endfightclock
            global MENU
            endscreen = False
            dungeonCards.clear()
            userCards.clear()
            turn=0
            isPlayerMove=False
            playerCardOut = 0
            dungeonCardOut = 0
            output.clear()
            fightclock = 0
            MENU = "FO"
            if swordanim != None:
                swordanim.done=False
                swordanim.innerclock = 0

def fightEvent(dungeon:game.Dungeon,user:game.User,background,screen,deltaTime:float):
    global WONIMG
    global LOSTIMG
    global turn
    global endscreen
    global isPlayerMove
    global dungeonCardOut
    global playerCardOut
    global output
    global fightclock
    global endfightclock
    global projanim
    global playedDeadAnim

    ymargins = 10
    margins = 10
    if len(output) == 0:
        output = game.fight(game.cardLookup[dungeon.name],user).split('\n')

    screen.blit(background,(0,0))

    percard = (margins*2+dungeonCharCardWidth)
    xpos = width/2 - len(user.selected)*percard/2
    dungeonxpos = width/2 - len(dungeon.cards)*percard/2

    if len(userCards) == 0:
        counter = 0
        for index in user.selected:
            card = user.cards[index]
            userCards.append(gameWrapper.CardSelectWrapper(dungeonCharCardWidth,dungeonCharCardHeight,xpos+percard*counter+margins,height-ymargins-dungeonCharCardHeight,card))
            counter+=1
    if len(dungeonCards) == 0:
        counter = 0
        for name in dungeon.cards:
            card = game.availableCards[game.cardLookup[name]]
            dungeonCards.append(gameWrapper.CardSelectWrapper(dungeonCharCardWidth,dungeonCharCardHeight,dungeonxpos+percard*counter+margins,ymargins,card))
            counter+=1

    if swordanim != None and not swordanim.done:
        screen.blit(background,(0,0))
        for card in userCards:
            card.update(deltaTime,1.5)
            card.draw(screen)
        for card in dungeonCards:
            card.update(deltaTime,1.5)
            card.draw(screen)
        swordanim.playAnim(deltaTime,screen)
        pygame.display.flip()
        return
    elif fightclock < waittime:
        screen.blit(background,(0,0))
        for card in userCards:
            card.update(deltaTime,1.5)
            card.draw(screen)
        for card in dungeonCards:
            card.update(deltaTime,1.5)
            card.draw(screen)
        fightclock+=deltaTime
        pygame.display.flip()
        return
    elif projanim != None and not projanim.done:
        screen.blit(background,(0,0))
        for card in userCards:
            card.update(deltaTime,1.5)
            card.draw(screen)
        for card in dungeonCards:
            card.update(deltaTime,1.5)
            card.draw(screen)
        projanim.playAnim(deltaTime,screen)
        pygame.display.flip()
        return


    #Check what to do
    currThing = output[turn].split(';')
    while len(output[turn]) == 0 or currThing[0]=="harc kezdodik":
        output.pop(turn)
        currThing = output[turn].split(';')

    if len(currThing)>=3 and currThing[2] == 'kijatszik':
        if currThing[0] == '1.kor':
            print(currThing)
            if isPlayerMove:
                userCards[0].destPos = (margins,height/2-dungeonCharCardHeight/2)
            else:
                dungeonCards[0].destPos = (width-dungeonCharCardWidth-margins,height/2-dungeonCharCardHeight/2)
            turn+=1
            isPlayerMove = not isPlayerMove
        else:
            if not playedDeadAnim:
                if isPlayerMove:
                    userCards[playerCardOut].destPos = (-20-dungeonCharCardWidth,height/2-dungeonCardHeight/2)
                else:
                    dungeonCards[dungeonCardOut].destPos = (width+20,height/2-dungeonCardHeight/2)
                playedDeadAnim = True
            if userCards[playerCardOut].destPos == (-1,-1) and dungeonCards[dungeonCardOut].destPos == (-1,-1):
                print(currThing)
                print(playerCardOut)
                print(dungeonCardOut)
                if isPlayerMove:
                    userCards[playerCardOut+1].destPos = (margins,height/2-dungeonCharCardHeight/2)
                    playerCardOut+=1
                else:
                    dungeonCards[dungeonCardOut+1].destPos = (width-dungeonCharCardWidth-margins,height/2-dungeonCharCardHeight/2)
                    dungeonCardOut+=1
                isPlayerMove = not isPlayerMove
                turn+=1
    elif len(currThing)>=3 and currThing[2] == 'tamad':
        if userCards[playerCardOut].destPos == (-1,-1) and dungeonCards[dungeonCardOut].destPos == (-1,-1):
            print(currThing)
            if isPlayerMove:
                if projanim != None:
                    projanim.done = False
                    projanim.y = height//2
                    projanim.startx = margins+dungeonCharCardWidth//2
                    projanim.distance = width-dungeonCharCardWidth//2-margins - projanim.startx
                    projanim.innerclock = 0
            else:
                if projanim != None:
                    projanim.done = False
                    projanim.y = height//2
                    projanim.startx = width+dungeonCharCardWidth//2+margins
                    projanim.distance = margins+dungeonCharCardWidth//2-projanim.startx
                    projanim.innerclock = 0
            if currThing[-1] == '0':
                playedDeadAnim = False
            isPlayerMove = not isPlayerMove
            turn+=1
    else:
        if waittime*2 < endfightclock:
            endscreen = True
            if currThing[0].split(' ')[1] == "nyert":
                if currThing[1] == "sebzes":
                    user.cards[user.cardNames[currThing[2]]].baseDmg = user.cards[user.cardNames[currThing[2]]].baseDmg + 1
                elif currThing[1] == "eletero":
                    user.cards[user.cardNames[currThing[2]]].baseHp = user.cards[user.cardNames[currThing[2]]].baseHp + 2
                else:
                    user.addCard(currThing[1])
                screen.blit(WONIMG, (0,0))
            else:
                screen.blit(LOSTIMG, (0,0))

        else:
            endfightclock+= deltaTime


    if not endscreen:
        for card in userCards:
            card.update(deltaTime,1.5)
            card.draw(screen)
        for card in dungeonCards:
            card.update(deltaTime,1.5)
            card.draw(screen)

    pygame.display.flip()

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
    selectedCards.clear()
    putinortakeoutCARD.clear()
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
    pygame.draw.rect(screen, (96, 69, 44), (1160, 0, 130, 120), border_radius=10)
    pygame.draw.rect(screen, (132, 101, 63), (1160, 0, 130, 120), width=4, border_radius=10)
    font_texture = pygame.image.load("src/img/cards.png").convert_alpha()
    font_texture_scaled = pygame.transform.scale(font_texture, (100, 100))
    screen.blit(font_texture_scaled, pygame.Rect(1170, 5, 200, 100).topleft)

def backtokartya():
    global MENU

    dungeons.clear()
    drawncards.clear()
    play_sound("wood")
    MENU = "KARTYA"

def kazamata_update(event):
    global mode
    global MENU
    if event.type == pygame.MOUSEWHEEL:
        mode -= event.y
        if mode > len(dungeons)-1:
            mode = len(dungeons)-1
        elif mode < 3 and mode > -1:
            play_sound("scroll")
        if mode < 0:
            mode = 0
        shiftFocus()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            if pygame.Rect(1160, 0, 130, 120).collidepoint(event.pos):
                backtokartya()
            for banner in dungeons:
                if banner.cardRect.collidepoint(event.pos):
                    pygame.display.set_caption("Harc")
                    MENU = "FIGHT"
                    play_sound("fight")


def create():
    game.newDungeon("Barlangi Portya", "Egyszerű kazamata", ["Nerun"], "sebzes")
    game.newDungeon("Osi Szentely", "Kis kazamata", ["Arin", "Emera", "Selia", "Lord Torak"], "eletero")
    game.newDungeon("A melyseg kiralynoje", "Nagy kazamata", ["Liora", "Arin", "Selia", "Nerun", "Torak", "Priestess Selia"], "")

    game.newCard("Arin", 2, 5, "fold")
    game.newCard("Liora", 2, 4, "levego")
    game.newCard("Selia", 2, 6, "viz")
    game.newCard("Nerun", 3, 3, "tuz")
    game.newCard("Torak", 3, 4, "fold")
    game.newCard("Emera", 2, 5, "levego")
    game.newCard("Kael", 3, 5, "tuz")
    game.newCard("Myra", 3, 6, "fold")
    game.newCard("Thalen", 3, 5, "levego")
    game.newCard("Isara", 2, 6, "viz")

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
    global MENU
    cards.clear()
    cardsInPack.clear()
    play_sound("wood")
    MENU="FO"

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
        card.update(deltaTime,-1)
        card.draw(cardlayer)
    for card in cards:
        card.update(deltaTime,-1)
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

    mydeck_font = pygame.font.Font("src/font/Minister Std Bold.otf", 50)
    mydeck_title = mydeck_font.render("Paklid", True, (255,255,255))
    gyujtemeny_title = mydeck_font.render("Kártyáid", True, (255,255,255))
    screen.blit(mydeck_title, (back_rect.x, back_rect.y+100))
    screen.blit(gyujtemeny_title, (back_rect.x, back_rect.y+200))


def drawCards(screen,background):
    global cardlayer
    global linepoint
    pygame.display.set_caption("Kártyáid")
    selectedCards.clear()
    putinortakeoutCARD.clear()
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
    global WONIMG
    global LOSTIMG

    create()
    if user == None:
        print("Couldnt initialize user")
        return
    pygame.init()
    background = pygame.image.load("./src/img/BG.jpg")
    background = pygame.transform.scale(background,(width,height))

    WONIMG = pygame.image.load("./src/img/WON.png")
    WONIMG = pygame.transform.scale_by(WONIMG,2)

    LOSTIMG = pygame.image.load("./src/img/LOST.png")
    LOSTIMG = pygame.transform.scale_by(LOSTIMG,2)

    pygame.mixer.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill((255, 255, 255))
    running = True
    clock:pygame.time.Clock = pygame.time.Clock()
    global swordanim
    swordanim = anim.SwordAnim(width,height)
    global projanim
    projanim = anim.Projectileanim(width,height)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if MENU == "FO":
                kazamata_update(event)
            elif MENU == "KARTYA":
                selectPackScreenEventHandler(event)
            else:
                fightEventEventhandler(event)

        fps = clock.get_fps()
        if fps == 0:
            fps = 0.00001
        deltaTime:float = 1/fps
        if MENU == "FO":
            select_kazamata(screen,background,deltaTime)
        elif MENU == "KARTYA":
            if len(cards) == 0 and len(cardsInPack) == 0:
                drawCards(screen,background)
            updateSelectPackScreen(screen,deltaTime,user,background)
        else:
            fightEvent(dungeons[mode].dungeon,user,background,screen,deltaTime)

        pygame.display.flip()
        clock.tick(120)
    pygame.quit()
