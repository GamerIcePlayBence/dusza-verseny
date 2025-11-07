import pygame
import game

def select_kazamata(screen, mode):
    screen.fill((255, 255, 255))
    BP_Color = (0, 255, 0)
    OSZ_Color = (255, 0, 0)
    MK_Color = (0, 0, 255)

    pygame.draw.line(screen, (0, 0, 0), (0, 450), (1280, 450), width=10)

    if mode == "BP":
        K_Rect = pygame.Rect(560, 500, 150, 200)
        BP_Rect = pygame.Rect(480, 40, 300, 400)
        OSZ_Rect = pygame.Rect(100, 140, 200, 300)
        MK_Rect = pygame.Rect(980, 140, 200, 300)
        pygame.draw.rect(screen, BP_Color, BP_Rect, border_radius=10)
        pygame.draw.rect(screen, OSZ_Color, OSZ_Rect, border_radius=10)
        pygame.draw.rect(screen, MK_Color, MK_Rect, border_radius=10)
        pygame.draw.rect(screen, BP_Color, K_Rect, border_radius=10)
    elif mode == "OSZ":
        BP_Rect = pygame.Rect(980, 140, 200, 300)
        OSZ_Rect = pygame.Rect(480, 40, 300, 400)
        MK_Rect = pygame.Rect(100, 140, 200, 300)
        pygame.draw.rect(screen, BP_Color, BP_Rect, border_radius=10)
        pygame.draw.rect(screen, OSZ_Color, OSZ_Rect, border_radius=10)
        pygame.draw.rect(screen, MK_Color, MK_Rect, border_radius=10)

        for i in range(4):
            K_POS_X = 760 - i*200
            K_Rect = pygame.Rect(K_POS_X, 500, 150, 200)
            pygame.draw.rect(screen, OSZ_Color, K_Rect, border_radius=10)
    elif mode == "MK":
        BP_Rect = pygame.Rect(100, 140, 200, 300)
        OSZ_Rect = pygame.Rect(980, 140, 200, 300)
        MK_Rect = pygame.Rect(480, 40, 300, 400)
        pygame.draw.rect(screen, BP_Color, BP_Rect, border_radius=10)
        pygame.draw.rect(screen, OSZ_Color, OSZ_Rect, border_radius=10)
        pygame.draw.rect(screen, MK_Color, MK_Rect, border_radius=10)

        for i in range(6):
            K_POS_X = 1050 - i*200
            K_Rect = pygame.Rect(K_POS_X, 500, 150, 200)
            pygame.draw.rect(screen, MK_Color, K_Rect, border_radius=10)




def GAME():
    pass

def UIMain():
    mode = "BP"
    mainmode = "kazamata"
    game.newDungeon("Barlangi Portya", "Egyszerű kazamata", ["Nerun"], "sebzés")
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Játék mód")
    running = True
    select_kazamata(screen, mode)
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