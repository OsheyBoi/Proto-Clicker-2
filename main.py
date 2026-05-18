import pygame
import sys
import math


pygame.init()
screen = pygame.display.set_mode((1300, 900))
clock = pygame.time.Clock()

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
cyan = (0, 255, 255)
white = (255, 255, 255)
light_gray = (200, 200, 200)
gray = (128, 128, 128)
dark_gray = (64, 64, 64)
black = (0, 0, 0)
orange = (255, 165, 0)
purple = (128, 0, 128)

font = pygame.font.SysFont("Arial", 50)
pygame.display.set_caption('Proto Clicker 2')

#Base Veriables
clicks = 0
rebirths = 0

shop_menu = pygame.Rect(460, 720, 440, 140)
Rebirth_menu = pygame.Rect(24, 227, 100, 100)
background = pygame.Rect(0, 0, 1300, 900)
Clicks_Amount_Box = pygame.Rect(250, 20, 350, 100)
Rebirth_Amount_Box = pygame.Rect(800, 20, 350, 100)
RebirthIcon = pygame.Rect(800, 20, 350, 100)
Button_center = (675, 400)  # Centered exactly where your 100x100 box was
Button_radius = 200

RebirthIcon =  pygame.image.load("Rebirth.png")
Rebirthicon_Resize = pygame.transform.scale(RebirthIcon, (70, 60))
text1 = font.render("Shop", True, (0, 0, 0))


running = True
while running:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    distance = math.hypot(mouse_pos[0] - Button_center[0], mouse_pos[1] - Button_center[1])
    Clicks_AR = font.render("Clicks: " + str(clicks), True, (0, 0, 0)) #AR - Amount Render
    Rebirth_AR = font.render("Rebirths: " + str(rebirths), True, (0, 0, 0))
    # Event Handling Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click down
                print(mouse_pos)
                if Rebirth_menu.collidepoint(mouse_pos):
                    print("Rebirth")
                if shop_menu.collidepoint(mouse_pos):
                    print("Shop")

                if distance <= Button_radius:
                    clicks += 1
                    print(clicks)




    #Menu System

    # Drawing Systems
    pygame.draw.rect(screen, gray, background)

    pygame.draw.rect(screen, red, Rebirth_menu)
    pygame.draw.rect(screen, cyan, shop_menu)

    pygame.draw.rect(screen, black, Rebirth_menu,width=5)
    pygame.draw.rect(screen, black, shop_menu,width=5)

    pygame.draw.rect(screen, green, Clicks_Amount_Box, width=0, border_radius=30)
    pygame.draw.rect(screen, red, Rebirth_Amount_Box, width=0, border_radius=30)

    pygame.draw.rect(screen, black, Clicks_Amount_Box, width=5, border_radius=30)
    pygame.draw.rect(screen, black, Rebirth_Amount_Box, width=5, border_radius=30)

    pygame.draw.circle(screen, blue, Button_center, Button_radius)
    pygame.draw.circle(screen, black, Button_center, Button_radius, width=5)

    CurrencyBox1 = Clicks_AR.get_rect()
    CurrencyBox2 = Rebirth_AR.get_rect()
    Text1 = text1.get_rect() #"Shop" Text

    CurrencyBox1.center = (380, 75)
    CurrencyBox2.center = (950, 75)
    Text1.center = (651, 794)

    screen.blit(Rebirthicon_Resize, (40, 247))
    screen.blit(Clicks_AR, CurrencyBox1)
    screen.blit(Rebirth_AR, CurrencyBox2)
    screen.blit(text1, Text1)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
