import pygame
from src import game

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


def GAME(screen):
    pygame.display.set_caption("Játék")
    #Pakli
    pygame.draw.rect(screen, (255, 201, 14), pygame.Rect(20, 20, 1230, 200), border_radius=10)
    pygame.draw.rect(screen, (255, 127, 39), pygame.Rect(20, 20, 1230, 200), width=4, border_radius=10)

    #Összes kártya
    pygame.draw.rect(screen, (255, 201, 14), pygame.Rect(20, 250, 1230, 450), border_radius=10)
    pygame.draw.rect(screen, (255, 127, 39), pygame.Rect(20, 250, 1230, 450), width=4, border_radius=10)

    #for pakli
    maxpaklikartya = int
    if len(game.availableCards) % 2 == 0:
        maxpaklikartya = len(game.availableCards) / 2
    else:
        maxpaklikartya = len(game.availableCards) + 1
    
    user = game.User()
    for i in range(len(user.selected)):
        if i >= 8:
            i = i-8
            K_POS_X = 30 + (i*150)
            K_POS_Y = 120
        else:
            K_POS_X = 30 + (i*150)
            K_POS_Y = 30
        
        if i <= maxpaklikartya:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(K_POS_X, K_POS_Y, 100, 80), border_radius=10)

    #for gyűjtemény
    for i in range(len(game.availableCards)):
        if i >= 8:
            i = i-8
            K_POS_X = 30 + (i*150)
            K_POS_Y = 350
        else:
            K_POS_X = 30 + (i*150)
            K_POS_Y = 260
    
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(K_POS_X, K_POS_Y, 100, 80), border_radius=10)
    
    

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

def UIMain():
    mode = "BP"
    mainmode = "Game"
    create()
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill((255, 255, 255))
    running = True
    if mainmode == "Kazamata választás":
        select_kazamata(screen, mode)
    else:
        GAME(screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL and mainmode == "Kazamata választás":
                if mode == "BP":
                    if event.y < 0:
                        mode = "OSZ"
                    else:
                        mode = "MK"
                    select_kazamata(screen, mode)
                elif mode == "OSZ":
                    if event.y < 0:
                        mode = "MK"
                    else:
                        mode = "BP"
                    select_kazamata(screen, mode)
                else:
                    if event.y < 0:
                        mode = "BP"
                    else:
                        mode = "OSZ"
                    select_kazamata(screen, mode)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if mainmode == "Kazamata választás":
                        mouse_x, mouse_y = event.pos
                        if mode == "BP":
                            if mouse_x >= 980 and mouse_x <= 1169 and mouse_y >= 147 and mouse_y <= 432:
                                mode = "MK"
                                select_kazamata(screen, mode)
                            elif mouse_x >= 103 and mouse_x <= 292 and mouse_y >= 147 and mouse_y <= 432:
                                mode = "OSZ"
                                select_kazamata(screen, mode)
                        elif mode == "MK":
                            if mouse_x >= 980 and mouse_x <= 1169 and mouse_y >= 147 and mouse_y <= 432:
                                mode = "OSZ"
                                select_kazamata(screen, mode)
                            elif mouse_x >= 103 and mouse_x <= 292 and mouse_y >= 147 and mouse_y <= 432:
                                mode = "BP"
                                select_kazamata(screen, mode)
                        elif mode == "OSZ":
                            if mouse_x >= 980 and mouse_x <= 1169 and mouse_y >= 147 and mouse_y <= 432:
                                mode = "BP"
                                select_kazamata(screen, mode)
                            elif mouse_x >= 103 and mouse_x <= 292 and mouse_y >= 147 and mouse_y <= 432:
                                mode = "MK"
                                select_kazamata(screen, mode)

        pygame.display.flip()
    pygame.quit()