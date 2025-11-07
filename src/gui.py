import pygame
import game

def select_kazamata(screen, mode):
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




def GAME():
    pass

def UIMain():
    mode = "BP"
    mainmode = "kazamata"
    game.newDungeon("Barlangi Portya", "Egyszerű kazamata", ["Nerun"], "sebzés")
    game.newDungeon("Osi Szentely", "Kis kazamata", ["Arin", "Emera", "Selia", "Lord Torak"], "életerő")
    game.newDungeon("A melyseg kiralynoje", "Nagy kazamata", ["Liora", "Arin", "Selia", "Nerun", "Torak", "Priestess Selia"], "")
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Játék mód")
    running = True
    if mainmode == "kazamata":
        select_kazamata(screen, mode)
    else:
        GAME()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEWHEEL and mainmode == "kazamata":
                if mode == "BP":
                    if event.y > 0:
                        mode = "OSZ"
                    else:
                        mode = "MK"
                    select_kazamata(screen, mode)
                elif mode == "OSZ":
                    if event.y > 0:
                        mode = "MK"
                    else:
                        mode = "BP"
                    select_kazamata(screen, mode)
                else:
                    if event.y > 0:
                        mode = "BP"
                    else:
                        mode = "OSZ"
                    select_kazamata(screen, mode)

        GAME()
        pygame.display.flip()
    pygame.quit()


UIMain()