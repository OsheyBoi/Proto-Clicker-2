import pygame
import sys
import math
from Prices import *
from Prices import amount_sum


def amount_sum(amount):
    if amount < 1000:
        if amount >= 0:
            rounded_amount = round(amount, 2)
        if amount >= 10:
            rounded_amount = round(amount, 1)
        elif amount >= 100:
            rounded_amount = round(amount, 0)
        return str(rounded_amount)
    suffixes = ['','K','M','B','T','Qd','Qn','Sx','Sp','Oc',"No",'De','UDe','DDe',"TDe","QDe"]
    suffix_index = 0

    while amount >= 1000:
        amount /= 1000
        suffix_index += 1
    rounded_amount = 1
    if amount >= 0 and amount <= 9:
        rounded_amount = round(amount, 2)
    if amount >= 10 and amount <= 99:
        rounded_amount = round(amount, 1)
    if amount >= 100:
        rounded_amount = round(amount, 0)
    Summed_Amount = str(rounded_amount) + suffixes[suffix_index]
    return str(Summed_Amount)


class Upgrade:
    def __init__(self, menu_rect, current_level, max_level, cost_function):
        self.rect = menu_rect
        self.level = current_level
        self.max_level = max_level
        self.cost_fn = cost_function  # Passes the function used to calculate cost

    def try_buy(self, mouse_pos, current_menu, clicks):
        # 1. Check menu and click collision
        if current_menu != 1:
            return clicks, False  # Return original clicks, no purchase made

        if self.rect.collidepoint(mouse_pos):
            cost = self.cost_fn(self.level, "True Price")
            print(self.level)
            if clicks >= cost and self.level < self.max_level:
                clicks -= cost
                self.level += 1
                return clicks, True  # Return new clicks, purchase successful

        return clicks, False

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
Teir_menu = pygame.Rect(24, 427, 100, 100)
background = pygame.Rect(0, 0, 1300, 900)
Clicks_Amount_Box = pygame.Rect(250, 20, 350, 100)
Rebirth_Amount_Box = pygame.Rect(800, 20, 350, 100)
RebirthIcon = pygame.Rect(800, 20, 350, 100)
Button_center = (675, 400)
Button_radius = 200

RebirthIcon =  pygame.image.load("Rebirth.png")
Rebirthicon_Resize = pygame.transform.scale(RebirthIcon, (70, 60))
TierIcon =  pygame.image.load("Tier.png")
text1 = font.render("Shop", True, (0, 0, 0))

#Menu Stuff (Render place and size)
Menu_Box = pygame.Rect(20, 150, 1250, 710)
close_menu = pygame.Rect(1170, 200, 50, 50)
menu_ui_1 = pygame.Rect(1170, 200, 50, 50)
menu_ui_2 = pygame.Rect(1170, 200, 50, 50)
menu_ui_3 = pygame.Rect(1170, 200, 50, 50)
menu_ui_4 = pygame.Rect(1170, 200, 50, 50)
menu_ui_5 = pygame.Rect(1170, 200, 50, 50)
menu_ui_6 = pygame.Rect(1170, 200, 50, 50)
#Menu Text
menu_text1 = font.render("", True, (0, 0, 0))
menu_text2 = font.render("", True, (0, 0, 0))
menu_text3 = font.render("", True, (0, 0, 0))
menu_text4 = font.render("", True, (0, 0, 0))
menu_text5 = font.render("", True, (0, 0, 0))
menu_text6 = font.render("", True, (0, 0, 0))


running = True
CU1_multipler = (CU1 * CU1Mult)
CU2_multipler = (CU2 * CU2Mult)
CU3_multipler = (CU3Mult ** CU3)
CU4_multipler = (CU4Mult ** CU4)
CU5_multipler = (CU5Mult ** CU5)

#-----------------
upgrades = [
    Upgrade(menu_ui_1,  0, CU1M, CU1_CostAmount),
    Upgrade(menu_ui_2, 0, CU2M, CU2_CostAmount),
    Upgrade(menu_ui_3, 0, CU3M, CU3_CostAmount),
    Upgrade(menu_ui_4, 0, CU4M, CU4_CostAmount),
    Upgrade(menu_ui_5, 0, CU5M, CU5_CostAmount)
]
#----------------
while running:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    distance = math.hypot(mouse_pos[0] - Button_center[0], mouse_pos[1] - Button_center[1])

    Clicks_Shown = amount_sum(clicks)
    Clicks_AR = font.render("Clicks: " + str(Clicks_Shown), True, (0, 0, 0)) #AR - Amount Render
    Rebirth_AR = font.render("Rebirths: " + str(rebirths), True, (0, 0, 0))

    #Gain Amount
    CPC = (1 + CU1) * (CU2Mult ** CU2)  #Click per Click
    CPC_Show = amount_sum(CPC)   # Click per Click

    Rebirth_Gain = (clicks ** 0.2) * (CU4Mult ** CU4)
    Rebirth_Gain_Show = amount_sum(Rebirth_Gain)
    # Event Handling Loop
    # -----------------
    upgrades = [
        Upgrade(menu_ui_1, CU1, CU1M, CU1_CostAmount),
        Upgrade(menu_ui_2, CU2, CU2M, CU1_CostAmount),
        Upgrade(menu_ui_3, CU3, CU3M, CU3_CostAmount),
        Upgrade(menu_ui_4, CU4, CU4M, CU4_CostAmount),
        Upgrade(menu_ui_5, CU5, CU5M, CU5_CostAmount)
    ]
    # ----------------
    base_clicks = (1 + CU1)
    clicks_mult = (CU3 ** CU3_multipler)
    if clicks_mult == 0:
        clicks_mult = 1
    # ----------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click down
                print(mouse_pos)
                if Rebirth_menu.collidepoint(mouse_pos):
                    #Open Rebirth menu
                    if Menu == 0:
                        Menu = 11

                if Teir_menu.collidepoint(mouse_pos):
                    #Open Rebirth menu
                    if Menu == 0:
                        Menu = 12

                elif shop_menu.collidepoint(mouse_pos):
                    # Open Shop
                    if Menu == 0:
                        Menu = 1

                elif close_menu.collidepoint(mouse_pos):
                    if Menu >= 1:
                        # Close Menu Button
                        print("Shop")
                        Menu = 0

                elif Menu == 1:
                    upgrades[0].level = CU1
                    upgrades[1].level = CU2
                    upgrades[2].level = CU3
                    upgrades[3].level = CU4
                    upgrades[4].level = CU5
                    for up in upgrades:
                        clicks, bought = up.try_buy(mouse_pos, Menu, clicks)
                        if bought:
                            break # Stop checking other upgrades if one was clicked
                    CU1 = upgrades[0].level
                    CU2 = upgrades[1].level
                    CU3 = upgrades[2].level
                    CU4 = upgrades[3].level
                    CU5 = upgrades[4].level



                X1 = mouse_pos[1]
                Y1 = mouse_pos[0]




                if distance <= Button_radius:
                    clicks += CPC
    #Menu System (Functions)

        #Upgrade  Menu
        if 1 >= Menu <= 10:
            menu_ui_1 = pygame.Rect(110, 340, 420, 50)
            menu_ui_2 = pygame.Rect(110, 560, 420, 50)
            menu_ui_3 = pygame.Rect(110, 780, 420, 50)
            menu_ui_4 = pygame.Rect(710, 340, 420, 50)
            menu_ui_5 = pygame.Rect(710, 560, 420, 50)
            menu_ui_6 = pygame.Rect(710, 780, 420, 50)
        # Teir Menu
        if Menu == 12:
            menu_ui_1 = pygame.Rect(110, 700, 1100, 100)
            menu_ui_2 = pygame.Rect(110, 260, 1100, 400)
        # Rebirth Menu
        if Menu == 11:
            Tier_upgrade_box = pygame.Rect(710, 560, 420, 50)
            Tier_buy_button = pygame.Rect(710, 780, 420, 50)
    if Menu == 1:
        CU1_Cost_Show = CU1_CostAmount(CU1,"Suffix")
        CU2_Cost_Show = CU2_CostAmount(CU2, "Suffix")
        CU3_Cost_Show = CU3_CostAmount(CU3, "Suffix")
        CU4_Cost_Show = CU4_CostAmount(CU4, "Suffix")
        CU5_Cost_Show = CU5_CostAmount(CU5, "Suffix")

        CU1_multipler = (CU1 * CU1Mult)
        CU2_multipler = (CU2 * CU2Mult)
        CU3_multipler = (CU3Mult ** CU3)
        CU4_multipler = (CU4Mult ** CU4)
        CU5_multipler = (CU5Mult ** CU5)

        CU2_multipler_s = amount_sum(CU2_multipler)
        CU3_multipler_s = amount_sum(CU3_multipler)
        CU4_multipler_s = amount_sum(CU4_multipler)
        CU5_multipler_s = amount_sum(CU5_multipler)

        menu_text1 = font.render("Base Power: (" + str(CU1) + "/" + str(CU1M) + ") \n +" + str(CU1_multipler) + " \n  Cost: " + str(CU1_Cost_Show), True, (0, 0, 0))
        menu_text2 = font.render("Faster Clicks (" + str(CU2) + "/" + str(CU2M) + ")\n -" + str(CU2_multipler) + " Cd \n  Cost: " + str(CU2_Cost_Show), True, (0, 0, 0))
        menu_text3 = font.render("Power Clicks (" + str(CU3) + "/" + str(CU3M) + ")\n X" + str(CU3_multipler_s) + " \n  Cost: " + str(CU3_Cost_Show), True, (0, 0, 0))
        menu_text4 = font.render("More Rebirths ("  + str(CU4) + "/" + str(CU4M) + ")\n X" + str(CU4_multipler_s) + " \n   Cost: " + str(CU4_Cost_Show), True, (0, 0, 0))
        menu_text5 = font.render("More Xp (" + str(CU5) + "/" + str(CU5M) + ")\n X" + str(CU5_multipler_s) + " \n  Cost: " + str(CU5_Cost_Show), True, (0, 0, 0))
        menu_text6 = font.render("Coming Later", True, (0, 0, 0))

    if Menu == 12:
        menu_text1 = font.render("")
        menu_text2 = font.render("")

    # Drawing Systems
    pygame.draw.rect(screen, gray, background)

    pygame.draw.rect(screen, red, Rebirth_menu)
    pygame.draw.rect(screen, cyan, shop_menu)
    pygame.draw.rect(screen, yellow, Teir_menu)

    pygame.draw.rect(screen, black, Rebirth_menu,width=5)
    pygame.draw.rect(screen, black, shop_menu,width=5)
    pygame.draw.rect(screen, black, Teir_menu, width=5)

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
    screen.blit(TierIcon, (25, 427))
    screen.blit(Clicks_AR, CurrencyBox1)
    screen.blit(Rebirth_AR, CurrencyBox2)
    screen.blit(text1, Text1)

    # Menu System (Drawing)
    if Menu != 0:
        if Menu == 1:
            pygame.draw.rect(screen, green, Menu_Box, width=0, border_radius=50) #Menu Screen
        if Menu == 6:
            pygame.draw.rect(screen, red, Menu_Box, width=0, border_radius=50)
        if Menu == 11:
            pygame.draw.rect(screen, orange, Menu_Box, width=0, border_radius=50)
        if Menu == 12:
            pygame.draw.rect(screen, yellow, Menu_Box, width=0, border_radius=50)

        pygame.draw.rect(screen, black, Menu_Box, width=5, border_radius=50)

        pygame.draw.rect(screen, red, close_menu, width=0, border_radius=50) # Close Button
        pygame.draw.rect(screen, black, close_menu, width=5, border_radius=50)

        if Menu <= 9:
            pygame.draw.rect(screen, cyan, menu_ui_1, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, menu_ui_2, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, menu_ui_3, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, menu_ui_4, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, menu_ui_5, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, menu_ui_6, width=0, border_radius=50)
        if Menu ==  11:
           pygame.draw.rect(screen, cyan, menu_ui_1, width=0, border_radius=50)
           pygame.draw.rect(screen, cyan, menu_ui_2, width=0, border_radius=50)
        if Menu == 12:
            pygame.draw.rect(screen, cyan, menu_ui_1, width=0, border_radius=50)
            pygame.draw.rect(screen, cyan, menu_ui_2, width=0, border_radius=50)
            pygame.draw.rect(screen, black, menu_ui_2, width=7, border_radius=50)
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
