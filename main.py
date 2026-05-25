import pygame
import sys
import math
from Prices import *
def amount_sum(amount):
    if amount < 1000:
        return str(amount)
    suffixes = ['','K','M','B','T','Qd','Qn','Sx','Sp','Oc',"No"]
    suffix_index = 0

    while amount >= 1000:
        amount /= 1000
        suffix_index += 1
    if amount >= 1 and amount <= 9:
        rounded_amount = round(amount, 2)
    if amount >= 10 and amount <= 99:
        rounded_amount = round(amount, 1)
    if amount >= 100:
        rounded_amount = round(amount, 0)
    Summed_Amount = str(rounded_amount) + suffixes[suffix_index]
    return str(Summed_Amount)

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

font = pygame.font.SysFont("Arial", 40)
pygame.display.set_caption('Proto Clicker 2')

#Base Veriables
clicks = 0
rebirths = 0
Menu = 0


#Clicks Upgrade
# Notes:
#  (y) U(x) = (Currency) Upgrade (x = Number) - Current Amount of the upgrade you have
#  (y)U(x)M = (Currency) Upgrade (Number) Max Amount
#  (y)U(x)Mult = CU(x) = (Currency) (Number) Multipler
# Y = Currency  (C = Clicks) (R = Rebirths

CU1 = 0
CU1M = 25
CU1Mult = 1
CU1_Cost = 1
CU2 = 0
CU2M = 10
CU2Mult = 0.1
CU2_Cost = 1
CU3 = 0
CU3M = 5
CU3Mult = 1.25
CU3_Cost = 1
CU4 = 0
CU4M = 10
CU4Mult = 1.3
CU4_Cost = 1
CU5 = 0
CU5M = 25
CU5Mult = 1.1
CU5_Cost = 1

shop_menu = pygame.Rect(460, 720, 440, 140)
Rebirth_menu = pygame.Rect(24, 227, 100, 100)
background = pygame.Rect(0, 0, 1300, 900)
Clicks_Amount_Box = pygame.Rect(250, 20, 350, 100)
Rebirth_Amount_Box = pygame.Rect(800, 20, 350, 100)
RebirthIcon = pygame.Rect(800, 20, 350, 100)
Button_center = (675, 400)
Button_radius = 200

RebirthIcon =  pygame.image.load("Rebirth.png")
Rebirthicon_Resize = pygame.transform.scale(RebirthIcon, (70, 60))
text1 = font.render("Shop", True, (0, 0, 0))

#Menu Stuff (Render place and size)
Menu_Box = pygame.Rect(20, 150, 1250, 710)
close_menu = pygame.Rect(1170, 200, 50, 50)
Upgrade1_menu = pygame.Rect(1170, 200, 50, 50)
Upgrade2_menu = pygame.Rect(1170, 200, 50, 50)
Upgrade3_menu = pygame.Rect(1170, 200, 50, 50)
Upgrade4_menu = pygame.Rect(1170, 200, 50, 50)
Upgrade5_menu = pygame.Rect(1170, 200, 50, 50)
Upgrade6_menu = pygame.Rect(1170, 200, 50, 50)
#Menu Text
menu_text1 = font.render("", True, (0, 0, 0))
menu_text2 = font.render("", True, (0, 0, 0))
menu_text3 = font.render("", True, (0, 0, 0))
menu_text4 = font.render("", True, (0, 0, 0))
menu_text5 = font.render("", True, (0, 0, 0))
menu_text6 = font.render("", True, (0, 0, 0))


running = True
while running:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    distance = math.hypot(mouse_pos[0] - Button_center[0], mouse_pos[1] - Button_center[1])

    Clicks_Shown = amount_sum(clicks)
    Clicks_AR = font.render("Clicks: " + str(Clicks_Shown), True, (0, 0, 0)) #AR - Amount Render
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
                    if Menu == 0:
                        print("Shop")
                        Menu = 1
                if close_menu.collidepoint(mouse_pos):
                    if Menu >= 1:
                        print("Shop")
                        Menu = 0

                X1 = mouse_pos[1]
                Y1 = mouse_pos[0]




                if distance <= Button_radius:
                    clicks += 1

    #Menu System (Functions)

        Upgrade1_menu = pygame.Rect(110, 340, 420, 50)
        Upgrade2_menu = pygame.Rect(110, 560, 420, 50)
        Upgrade3_menu = pygame.Rect(110, 780, 420, 50)
        Upgrade4_menu = pygame.Rect(710, 340, 420, 50)
        Upgrade5_menu = pygame.Rect(710, 560, 420, 50)
        Upgrade6_menu = pygame.Rect(710, 780, 420, 50)

    if Menu == 1:
        CU1_Cost = CU1_CostAmount(CU1)
        CU2_Cost = CU2_CostAmount(CU2)
        CU3_Cost = CU3_CostAmount(CU3)
        CU4_Cost = CU4_CostAmount(CU4)
        CU5_Cost = CU5_CostAmount(CU5)

        CU1_multipler = CU1 * CU1Mult
        CU2_multipler = CU2 * CU2Mult
        CU3_multipler = CU3 * CU3Mult
        CU4_multipler = CU4 * CU4Mult
        CU5_multipler = CU5 * CU5Mult

        menu_text1 = font.render("Base Power: (" + str(CU1) + "/" + str(CU1M) + ") \n +" + str(CU1_multipler) + " \n  Cost: " + str(CU1_Cost), True, (0, 0, 0))
        menu_text2 = font.render("Faster Clicks (" + str(CU2) + "/" + str(CU2M) + ")\n X" + str(CU2_multipler) + " \n  Cost: " + str(CU2_Cost), True, (0, 0, 0))
        menu_text3 = font.render("Power Clicks (" + str(CU3) + "/" + str(CU3M) + ")\n X" + str(CU3_multipler) + " \n  Cost: " + str(CU3_Cost), True, (0, 0, 0))
        menu_text4 = font.render("More Rebirths (" + str(CU4) + "/" + str(CU4M) + ")\n X" + str(CU4_multipler) + " \n  Cost: " + str(CU4_Cost), True, (0, 0, 0))
        menu_text5 = font.render("More Xp (" + str(CU5) + "/" + str(CU5M) + ")\n X" + str(CU5_multipler) + " \n  Cost: " + str(CU5_Cost), True, (0, 0, 0))
        menu_text6 = font.render("Coming Later", True, (0, 0, 0))


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

    CurrencyBox1 = Clicks_AR.get_rect()

    Menu_text1 = menu_text1.get_rect()
    Menu_text2 = menu_text2.get_rect()
    Menu_text3 = menu_text3.get_rect()
    Menu_text4 = menu_text4.get_rect()
    Menu_text5 = menu_text5.get_rect()
    Menu_text6 = menu_text6.get_rect()

    CurrencyBox1.center = (380, 75)
    CurrencyBox2.center = (950, 75)
    Text1.center = (651, 794)


    screen.blit(Rebirthicon_Resize, (40, 247))
    screen.blit(Clicks_AR, CurrencyBox1)
    screen.blit(Rebirth_AR, CurrencyBox2)
    screen.blit(text1, Text1)

    # Menu System (Drawing)
    if Menu != 0:
        pygame.draw.rect(screen, green, Menu_Box, width=0, border_radius=50) #Menu Screen
        pygame.draw.rect(screen, black, Menu_Box, width=5, border_radius=50)

        pygame.draw.rect(screen, red, close_menu, width=0, border_radius=50) # Close Button
        pygame.draw.rect(screen, black, close_menu, width=5, border_radius=50)

        if Menu <= 9:
            pygame.draw.rect(screen, cyan, Upgrade1_menu, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, Upgrade2_menu, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, Upgrade3_menu, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, Upgrade4_menu, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, Upgrade5_menu, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, Upgrade6_menu, width=0, border_radius=50)
    if Menu >= 1:
        if Menu <= 9:
            Menu_text1.center = (300, 320)
            Menu_text2.center = (300, 540)
            Menu_text3.center = (300, 760)
            Menu_text4.center = (880, 320)
            Menu_text5.center = (860, 540)
            Menu_text6.center = (860, 760)
            screen.blit(menu_text1, Menu_text1)
            screen.blit(menu_text2, Menu_text2)
            screen.blit(menu_text3, Menu_text3)
            screen.blit(menu_text4, Menu_text4)
            screen.blit(menu_text5, Menu_text5)
            screen.blit(menu_text6, Menu_text6)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
