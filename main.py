import pygame
import sys
import math
import json
import os

from Prices import *
from Tier import *
from Prices import amount_sum
from Tier import tier_cost

SAVE_FILE = "save_data.json"


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
class Upgrade2:
    def __init__(self, menu_rect, current_level, max_level, cost_function):
        self.rect = menu_rect
        self.level = current_level
        self.max_level = max_level
        self.cost_fn = cost_function  # Passes the function used to calculate cost

    def try_buy(self, mouse_pos, current_menu, rebirths):
        # 1. Check menu and click collision
        if current_menu != 6:
            print("h")
            return rebirths, False  # Return original clicks, no purchase made
        print("try buy pass menu 6 check")
        if self.rect.collidepoint(mouse_pos):
            cost = self.cost_fn(self.level, "True Price")
            print(self.level)
            if rebirths >= cost and self.level < self.max_level:
                rebirths -= cost
                self.level += 1
                return rebirths, True  # Return new clicks, purchase successful

        return rebirths, False

################################################################################
#    Set up
################################################################################

pygame.init()
screen = pygame.display.set_mode((1300, 900))
clock = pygame.time.Clock()

red = (255, 50, 50)
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

font = pygame.font.SysFont("Arial", 40) #(Small)
font2 = pygame.font.SysFont("Arial", 80) #(Big)
pygame.display.set_caption('Proto Clicker 2')

#Base Veriables
clicks = 0
rebirths = 0
current_tier = 0
Menu = 0
total_time_played = 0
Xp = 0
CU1 = 0
CU2 = 0
CU3 = 0
CU4 = 0
CU5 = 0
RU1 = 0
RU2 = 0
CPS = 0
Tier_Cm = 1
Tier_Rm = 1
RU3 = 0
levels = 1
Xp_Current_Level = 0
Xp_needed = 0
current_Cooldown = 0
time_passed_Since_Last_Click = 0
total_time_played_Click = 1
last_time_check_for_Auto_click = 0
Click_Xp_Mult = 1
CooldownLength = 0
Tier_Click_Speed = 1
last_time_check = 0

default_game_state = {
    "clicks": clicks,
    "rebirths": rebirths,
    "current_tier": current_tier,
    "total_time_played": total_time_played,
    "xp": Xp,
    "CU1": CU1,
    "CU2": CU2,
    "CU3": CU3,
    "CU4": CU4,
    "CU5": CU5,
    "RU1": RU1,
    "RU2": RU2,
    "RU3": RU3
}


current_state = {
    "clicks": clicks,
    "rebirths": rebirths,
    "current_tier": current_tier,
    "total_time_played": total_time_played,
    "xp": Xp,
    "CU1": CU1,
    "CU2": CU2,
    "CU3": CU3,
    "CU4": CU4,
    "CU5": CU5,
    "RU1": RU1,
    "RU2": RU2,
    "RU3": RU3
}


def save_game(game_state):
    """Writes the current game state dictionary to a JSON file."""
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(game_state, f, indent=4)
        print("Game saved successfully!")
    except IOError:
        print("Error: Could not write save file.")





################################################################################
#    Upgrades
################################################################################
# Notes:
#  (y) U(x) = (Currency) Upgrade (x = Number) - Current Amount of the upgrade you have
#  (y)U(x)M = (Currency) Upgrade (Number) Max Amount
#  (y)U(x)Mult = CU(x) = (Currency) (Number) Multipler
# Y = Currency  (C = Clicks) (R = Rebirths

#Clicks

CU1M = 25
CU1Mult = 1
CU1_Cost = 1

CU2M = 7
CU2Mult = 0.1
CU2_Cost = 1

CU3M = 5
CU3Mult = 1.25
CU3_Cost = 1

CU4M = 10
CU4Mult = 1.3
CU4_Cost = 1

CU5M = 25
CU5Mult = 1.1
CU5_Cost = 1

#Rebirths

RU1M = 20
RU1Mult = 1.5
RU1_Cost = 1

RU2M = 15
RU2Mult = 1.25
RU2_Cost = 1

RU3M = 25
RU3Mult = 1.1
RU3_Cost = 1

################################################################################
#    Ui Set up
################################################################################
shop_menu = pygame.Rect(460, 720, 440, 140)
Rebirth_menu = pygame.Rect(24, 227, 100, 100)
Teir_menu = pygame.Rect(24, 427, 100, 100)
background = pygame.Rect(0, 0, 1300, 900)
Clicks_Amount_Box = pygame.Rect(100, 20, 350, 100)
Rebirth_Amount_Box = pygame.Rect(500, 20, 350, 100)
Xp_Amount_Box = pygame.Rect(900, 20, 350, 100)
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

################################################################################
#    Multipler and Upgrade Set up
################################################################################

running = True

try:
    with open(SAVE_FILE, "r") as f:
        loaded_data = json.load(f)

        # Core game progress variables
        clicks = loaded_data.get("clicks", 0)
        rebirths = loaded_data.get("rebirths", 0)
        current_tier = loaded_data.get("current_tier", 0)
        Xp = loaded_data.get("xp", 0)
        total_time_played = loaded_data.get("total_time_played", 0)

        # Click Upgrades
        CU1 = loaded_data.get("CU1", 0)
        CU2 = loaded_data.get("CU2", 0)
        CU3 = loaded_data.get("CU3", 0)
        CU4 = loaded_data.get("CU4", 0)
        CU5 = loaded_data.get("CU5", 0)

        # Rebirth Upgrades
        RU1 = loaded_data.get("RU1", 0)
        RU2 = loaded_data.get("RU2", 0)
        RU3 = loaded_data.get("RU3", 0)

except (FileNotFoundError, json.JSONDecodeError):
    # Default variables if no save file exists
    clicks = 0
    rebirths = 0
    current_tier = 0
    total_time_played = 0

    CU1 = 0
    CU2 = 0
    CU3 = 0
    CU4 = 0
    CU5 = 0

    RU1 = 0
    RU2 = 0
    RU3 = 0


CU1_multipler = (CU1 * CU1Mult)
CU2_multipler = (CU2 * CU2Mult)
CU3_multipler = (CU3Mult ** CU3)
CU4_multipler = (CU4Mult ** CU4)
CU5_multipler = (CU5Mult ** CU5)

#-----------------
upgrades = [
    Upgrade(menu_ui_1, 0, CU1M, CU1_CostAmount),
    Upgrade(menu_ui_2, 0, CU2M, CU2_CostAmount),
    Upgrade(menu_ui_3, 0, CU3M, CU3_CostAmount),
    Upgrade(menu_ui_4, 0, CU4M, CU4_CostAmount),
    Upgrade(menu_ui_5, 0, CU5M, CU5_CostAmount),

]

upgrades2 = [
    Upgrade2(menu_ui_1, 0, RU2M, RU1_CostAmount),
    Upgrade2(menu_ui_2, 0, RU2M, RU2_CostAmount),
    Upgrade2(menu_ui_3, 0, RU3M, RU3_CostAmount)


]
#----------------
AUTOSAVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(AUTOSAVE_EVENT, 10000)


AUTOClick_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(AUTOClick_EVENT, 1000)

AUTORebirth_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(AUTORebirth_EVENT, 1000)

################################################################################
#    Start Application
################################################################################
while running:
    screen.fill((0, 0, 0))
    mouse_pos = pygame.mouse.get_pos()
    distance = math.hypot(mouse_pos[0] - Button_center[0], mouse_pos[1] - Button_center[1])

    Clicks_Shown = amount_sum(clicks)
    Rebirths_Shown = amount_sum(rebirths)
    Clicks_AR = font.render("Clicks: " + str(Clicks_Shown), True, (0, 0, 0)) #AR - Amount Render
    if current_tier >= 1:
        Rebirth_AR = font.render("Rebirths: " + str(Rebirths_Shown), True, (0, 0, 0))
    else:
        Rebirth_AR = font.render("Unlock at T1", True, (0, 0, 0))

################################################################################
#    Xp system
################################################################################

    Xp_needed =  int(15* (1.4 ** levels ))

    total_xp_for_past_levels = 0
    for lvl in range(1, levels):
        total_xp_for_past_levels += int(15 * (1.4 ** lvl) + 3)

    Xp_Current_Level = Xp - total_xp_for_past_levels
    if Xp_Current_Level >= Xp_needed:
        print("test")
        levels += 1
        Xp_Current_Level = 0
    if current_tier >= 3:
        Xp_AR = font.render("Level: " + str(levels) + " (" +str(Xp_Current_Level) + "/" + str(Xp_needed) + ")", True, (0, 0, 0))
    if current_tier <= 2:
        Xp_AR = font.render("Unlock At T3",True, (0, 0, 0))
    if current_tier >= 3:
        Click_Xp_Mult = 1.2 ** levels
################################################################################
#    Tier Upgrade Multiplers
################################################################################
    if current_tier ==  1:
        Tier_Cm = 2
        Tier_Rm = 1
    if current_tier == 2:
        Tier_Cm = 4
        Tier_Rm = 1.5
        Tier_Click_Speed = 1.5
    if current_tier ==  3:
        Tier_Cm = 8
        Tier_Rm = 2.25
        Auto_Click_Speed = 1
    if current_tier ==  4:
        Tier_Cm = 24
        Tier_Rm = 4.5
        Tier_Click_Speed = 1.875
    if current_tier == 5:
        Tier_Cm = 48
        Tier_Rm = 9
        Auto_Rebirth_Speed = 1
################################################################################
#Gain Amount
################################################################################
    current_time = pygame.time.get_ticks()
    time_passed = current_time - last_time_check
    total_time_played += time_passed / 1000.0
    last_time_check = current_time

    if current_tier >= 5:
        total_time_played_Click = total_time_played ** 0.1
    else:
        total_time_played_Click = 1



    # -----------------
    upgrades = [
        Upgrade(menu_ui_1, 0, CU1M, CU1_CostAmount),
        Upgrade(menu_ui_2, 0, CU2M, CU2_CostAmount),
        Upgrade(menu_ui_3, 0, CU3M, CU3_CostAmount),
        Upgrade(menu_ui_4, 0, CU4M, CU4_CostAmount),
        Upgrade(menu_ui_5, 0, CU5M, CU5_CostAmount),

    ]

    upgrades2 = [
        Upgrade2(menu_ui_1, 0, RU2M, RU1_CostAmount),
        Upgrade2(menu_ui_2, 0, RU2M, RU2_CostAmount),
        Upgrade2(menu_ui_3, 0, RU3M, RU3_CostAmount)

    ]
    # ----------------
    ################################################################################
    #    Currency Amount Gain
    ################################################################################
    # ----------------
    base_clicks = (1 + CU1)
    clicks_mult = (CU3Mult ** CU3) * (RU1Mult ** RU1) * Tier_Cm * total_time_played_Click * Click_Xp_Mult
    if clicks_mult == 0:
        clicks_mult = 1
    # ----------------

    #Gain Amount
    CPC = base_clicks * clicks_mult  #Click per Click
    CPC_Show = amount_sum(CPC)   # Click per Click

    CooldownLength = 1000 - ((CU2Mult * CU2) * 1000) / Tier_Click_Speed

    if clicks >= 1000:
        Rebirth_Gain = int(((clicks - 999) ** 0.25) * (CU4Mult ** CU4) * (RU2Mult ** RU2) * Tier_Rm)
        Rebirth_Gain_Show = amount_sum(Rebirth_Gain)
    else:
        Rebirth_Gain = 0
        Rebirth_Gain_Show = str(0)


    ################################################################################
    #    Upgrade Changes
    ################################################################################

    if current_tier >= 5:
        CU3M = 15
        CU3Mult = 1.3


    ################################################################################
    #    Pygame Mouse  collidepoint checker
    ################################################################################
    for event in pygame.event.get():

        if event.type == AUTOClick_EVENT:
            if current_tier == 3:
                clicks += CPC
                Xp += 0.25

        if event.type == AUTOClick_EVENT:
            if current_tier == 5:
                rebirths += Rebirth_Gain / 100


        if event.type == pygame.QUIT:
            running = False
            current_state = {
                "clicks": clicks,
                "rebirths": rebirths,
                "current_tier": current_tier,
                "total_time_played": total_time_played,
                "xp": Xp,
                "CU1": CU1,
                "CU2": CU2,
                "CU3": CU3,
                "CU4": CU4,
                "CU5": CU5,
                "RU1": RU1,
                "RU2": RU2,
                "RU3": RU3
            }
            save_game(current_state)
            pygame.quit()
            sys.exit()

        # 3. Catch the 10-second timer event here
        if event.type == AUTOSAVE_EVENT:
            current_state = {
                "clicks": clicks,
                "rebirths": rebirths,
                "current_tier": current_tier,
                "total_time_played": total_time_played,
                "xp": Xp,
                "CU1": CU1,
                "CU2": CU2,
                "CU3": CU3,
                "CU4": CU4,
                "CU5": CU5,
                "RU1": RU1,
                "RU2": RU2,
                "RU3": RU3
            }
            save_game(current_state)
            print("Autosaved at 10-second interval!")


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click down
                print(mouse_pos)
                print(Menu)
                if Rebirth_menu.collidepoint(mouse_pos):
                    #Open Rebirth menu
                    if Menu == 0:
                        if current_tier >= 1:
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

                elif menu_ui_1.collidepoint(mouse_pos) and Menu == 12:
                        Tier_cost = tier_cost(current_tier, "None")
                        Tier_cost_Shown = tier_cost(current_tier, "Suffix")
                        if clicks >= Tier_cost:
                            clicks = 0
                            CU1 = 0
                            CU2 = 0
                            CU3 = 0
                            CU4 = 0
                            RU1 = 0
                            RU2 = 0
                            RU3 = 0
                            current_tier += 1
                            print("Tier up")
                        else:
                            print("no")
                elif menu_ui_6.collidepoint(mouse_pos):
                    if Menu == 1:
                        Menu = 6

                elif menu_ui_1.collidepoint(mouse_pos)  and Menu == 11:
                        if Menu == 11:
                            if clicks >= 1000:
                                clicks = 0
                                CU1 = 0
                                CU2 = 0
                                CU3 = 0
                                CU4 = 0
                                rebirths += Rebirth_Gain


################################################################################
#    Upgrade Menu stuff
################################################################################

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

                elif Menu == 6:
                    upgrades2[0].level = RU1
                    upgrades2[1].level = RU2
                    upgrades2[2].level = RU3

                    for up in upgrades2:
                        rebirths, bought = up.try_buy(mouse_pos, Menu, rebirths)
                        if bought:
                            break # Stop checking other upgrades if one was clicked
                    RU1 = upgrades2[0].level
                    RU2 = upgrades2[1].level
                    RU3 = upgrades2[2].level


                X1 = mouse_pos[1]
                Y1 = mouse_pos[0]


                if distance <= Button_radius and Menu == 0:
                    if current_Cooldown <= current_time:
                        clicks += CPC
                        current_Cooldown = current_time + CooldownLength
                        if current_tier >= 3:
                            Xp += 1

################################################################################
#    Drawing Ui Elements
################################################################################
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
            menu_ui_1 = pygame.Rect(110, 700, 1100, 100)
            menu_ui_2 = pygame.Rect(110, 260, 1100, 400)
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
        menu_text2 = font.render("Faster Clicks (" + str(CU2) + "/" + str(CU2M) + ")\n -" + str(CU2_multipler_s) + " Cd \n  Cost: " + str(CU2_Cost_Show), True, (0, 0, 0))
        menu_text3 = font.render("Power Clicks (" + str(CU3) + "/" + str(CU3M) + ")\n X" + str(CU3_multipler_s) + " \n  Cost: " + str(CU3_Cost_Show), True, (0, 0, 0))

        if current_tier >= 2:
            menu_text4 = font.render("More Rebirths ("  + str(CU4) + "/" + str(CU4M) + ")\n X" + str(CU4_multipler_s) + " \n   Cost: " + str(CU4_Cost_Show), True, (0, 0, 0))
        else:
            menu_text4 = font.render("Unlock At Tier 2 ", True, (0, 0, 0))
        if current_tier >= 4:
            menu_text5 = font.render("More Xp (" + str(CU5) + "/" + str(CU5M) + ")\n X" + str(CU5_multipler_s) + " \n  Cost: " + str(CU5_Cost_Show), True, (0, 0, 0))
        else:
            menu_text5 = font.render("Unlock At Tier 4 ", True, (0, 0, 0))

        menu_text6 = font.render("Rebirth Upgrades", True, (0, 0, 0))

    if Menu == 6:
        RU1_Cost_Show = RU1_CostAmount(RU1, "Suffix")
        RU2_Cost_Show = RU2_CostAmount(RU2, "Suffix")
        RU3_Cost_Show = RU3_CostAmount(RU3, "Suffix")

        RU1_multipler = (RU1Mult ** RU1)
        RU2_multipler = (RU2Mult ** RU2)
        RU3_multipler = (RU3Mult ** RU3)

        RU1_multipler_s = amount_sum(RU1_multipler)
        RU2_multipler_s = amount_sum(RU2_multipler)
        RU3_multipler_s = amount_sum(RU3_multipler)


        menu_text1 = font.render("Clicks Power 2: (" + str(RU1) + "/" + str(RU1M) + ") \n x" + str(RU1_multipler_s) + " \n  Cost: " + str(RU1_Cost_Show), True, (0, 0, 0))
        menu_text2 = font.render("Rebirth Power (" + str(RU2) + "/" + str(RU2M) + ")\n x" + str(RU2_multipler_s) + " \n  Cost: " + str(RU2_Cost_Show), True, (0, 0, 0))
        menu_text3 = font.render("Extra Xp (" + str(RU3) + "/" + str(RU3M) + ")\n X" + str(RU3_multipler_s) + " \n  Cost: " + str(RU3_Cost_Show), True, (0, 0, 0))
        menu_text4 = font.render("Coming Later", True, (0, 0, 0))
        menu_text5 = font.render("Coming Later ", True, (0, 0, 0))
        menu_text6 = font.render("Coming Later", True, (0, 0, 0))


    if Menu == 12:
        test = tier_cost(current_tier,"Suffix")
        menu_text1 = font.render((tier_info(current_tier)), True,  (0, 0, 0))
        menu_text2 = font.render("Buy (Cost - " + str(test) + ")", True, (0, 0, 0))
    if Menu == 11:
        menu_text1 = font2.render(("If you rebirth you gain: \n \n     " + Rebirth_Gain_Show) + " Rebirths", True,  (0, 0, 0))
        menu_text2 = font.render("Rebirth", True, (0, 0, 0))
    # Drawing Systems
    pygame.draw.rect(screen, gray, background)
    if Menu == 0:
        pygame.draw.rect(screen, cyan, shop_menu)
        pygame.draw.rect(screen, yellow, Teir_menu)
        pygame.draw.rect(screen, black, shop_menu,width=5)
        pygame.draw.rect(screen, black, Teir_menu, width=5)

        if current_tier >= 1:
            pygame.draw.rect(screen, red, Rebirth_menu)
            pygame.draw.rect(screen, black, Rebirth_menu,width=5)



    pygame.draw.rect(screen, green, Clicks_Amount_Box, width=0, border_radius=30)
    pygame.draw.rect(screen, red, Rebirth_Amount_Box, width=0, border_radius=30)
    pygame.draw.rect(screen, yellow, Xp_Amount_Box, width=0, border_radius=30)

    pygame.draw.rect(screen, black, Clicks_Amount_Box, width=5, border_radius=30)
    pygame.draw.rect(screen, black, Rebirth_Amount_Box, width=5, border_radius=30)
    pygame.draw.rect(screen, black, Xp_Amount_Box, width=5, border_radius=30)

    pygame.draw.circle(screen, blue, Button_center, Button_radius)
    pygame.draw.circle(screen, black, Button_center, Button_radius, width=5)

    CurrencyBox1 = Clicks_AR.get_rect()
    CurrencyBox2 = Rebirth_AR.get_rect()
    CurrencyBox3 = Clicks_AR.get_rect()
    Text1 = text1.get_rect() #"Shop" Text


    Menu_text1 = menu_text1.get_rect()
    Menu_text2 = menu_text2.get_rect()
    Menu_text3 = menu_text3.get_rect()
    Menu_text4 = menu_text4.get_rect()
    Menu_text5 = menu_text5.get_rect()
    Menu_text6 = menu_text6.get_rect()

    CurrencyBox1.center = (230, 75)
    CurrencyBox2.center = (630, 75)
    CurrencyBox3.center = (1030, 75)
    Text1.center = (651, 794)

    if current_tier >= 1:
        screen.blit(Rebirthicon_Resize, (40, 247))
    screen.blit(TierIcon, (25, 427))
    screen.blit(Clicks_AR, CurrencyBox1)
    screen.blit(Rebirth_AR, CurrencyBox2)
    screen.blit(Xp_AR, CurrencyBox3)
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
           pygame.draw.rect(screen, red, menu_ui_1, width=0, border_radius=50)
           pygame.draw.rect(screen, red, menu_ui_2, width=0, border_radius=50)
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
        if Menu == 12:
            Menu_text2.center = (600, 752)
            Menu_text1.center = (630, 382)
            screen.blit(menu_text1, Menu_text1)
            screen.blit(menu_text2, Menu_text2)

        if Menu == 11:
            Menu_text2.center = (600, 752)
            Menu_text1.center = (650, 452)
            screen.blit(menu_text1, Menu_text1)
            screen.blit(menu_text2, Menu_text2)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
