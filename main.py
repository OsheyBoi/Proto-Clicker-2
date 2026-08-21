import pygame
import sys
import math
import json
import threading
global WINDOWED_WIDTH_CACHE, WINDOWED_HEIGHT_CACHE, is_fullscreen, WINDOW_WIDTH, WINDOW_HEIGHT, screen, scale, offset_x, offset_y

# Debugging and other things
import os
import sys
import importlib

try:
    import debugger

    debugger_active = 0
    debug_file = 1
    DEBUGGER_AVAILABLE = False
except ImportError:
    debugger_active = 0
    debugger = None
    debug_file = 0
    DEBUGGER_AVAILABLE = None
try:
    import game_console
    CONSOLE_AVAILABLE = True
    game_console.start() # Fire up the background thread immediately
except ImportError:
    game_console = None
    CONSOLE_AVAILABLE = False

from Prices import *
from Tier import *
from ascension  import *
from Prices import amount_sum
from Tier import tier_cost


# Save File
save_dir = pygame.system.get_pref_path("Oshey Studios", "Proto Clicker 2")
save_path = os.path.join(save_dir, "save_Data.json")
save_path_backup = os.path.join(save_dir, "save_data_Backup.json")

#Old Local File Saves
SAVE_FILE = "save_data.json"
SAVE_FILE_BACKUP = "save_data_backup.json"


# Image Locations
base_dir = os.path.dirname(__file__)
img_dir = os.path.join(base_dir, 'images')

def amount_sum(amount):
    if amount < 1000:
        if amount <= 9:
            rounded_amount = round(amount, 2)
        elif amount <= 99:
            rounded_amount = round(amount, 1)
        elif amount <= 999:
            rounded_amount = round(amount, 0)
        else:
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
            cost = self.cost_fn(self.level, current_tier, "True Price")
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
            return rebirths, False  # Return original clicks, no purchase made
        if self.rect.collidepoint(mouse_pos):
            cost = self.cost_fn(self.level, current_tier, "True Price")
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

GAME_WIDTH, GAME_HEIGHT = 1300, 900
canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
# 1300 x 900
WINDOW_WIDTH, WINDOW_HEIGHT = 1300, 900
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Auto-Scaled Window")
Size_changer = "1300 x 900"
Old_Size = 0

Visual_Effect_Switch = "On"
is_fullscreen = False

def calculate_scale(win_w, win_h):
    scale_x = win_w / GAME_WIDTH
    scale_y = win_h / GAME_HEIGHT
    scale = min(scale_x, scale_y)
    offset_x = (win_w - (GAME_WIDTH * scale)) / 2
    offset_y = (win_h - (GAME_HEIGHT * scale)) / 2
    return scale, offset_x, offset_y

##########################
#   Display Set up
##########################

Set_size  = 0
dev_mult = 1
scale, offset_x, offset_y = calculate_scale(WINDOW_WIDTH, WINDOW_HEIGHT)
clock = pygame.time.Clock()
size = 1
Change_size = 1
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

font1 = pygame.font.SysFont("Arial", 30) #(Smaller)
font2 = pygame.font.SysFont("Arial", 40) #(Small)
font3 = pygame.font.SysFont("Arial", 50) #(Normal)
font4 = pygame.font.SysFont("Arial", 60) #(Big)
font5 = pygame.font.SysFont("Arial", 80) #(Huge)
pygame.display.set_caption('Proto Clicker 2')

##########################
#   Veriable Setup
##########################
# V1.0
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
dev_mult = 1.0
Last_Speed = 1


# V3.0
current_ascension = 0
ascension_tokens = 0
ascension_stage = 0
ascension_stage_2 = 0
Keep_Click_Upgrades = 1
Keep_Rebirth_Upgrades = 1
ascension_Auto_Click_Speed = 1

default_game_state = {
    # V1.0
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
    "RU3": RU3,
    # V3.0
    "current_ascension"  : current_ascension,
    "ascension_tokens" : ascension_tokens,
    "ascension_stage" : ascension_stage,
    "ascension_stage_2": ascension_stage_2
}

current_state = {
    # V1.0
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
    "RU3": RU3,
    # V3.0
    "current_ascension": current_ascension,
    "ascension_tokens": ascension_tokens,
    "ascension_stage": ascension_stage,
    "ascension_stage_2": ascension_stage_2
}


def save_game(game_state):
    """Writes the current game state dictionary to a JSON file."""
    try:
        with open(save_path, "w") as f:
            json.dump(game_state, f, indent=4)
        print(f"[SYSTEM] Game saved successfully!")
    except IOError:
        print(f"[SYSTEM] Error: Could not write save file.")

def save_game_backup(game_state):
    """Writes the current game state dictionary to a JSON file."""
    try:
        with open(save_path_backup, "w") as f:
            json.dump(game_state, f, indent=4)
        print(f"[SYSTEM] Game saved successfully!")
    except IOError:
        print(f"[SYSTEM] Error: Could not write save file.")

menu_base_1 = [11,12,13]


################################################################################
#    Upgrades
################################################################################
# Notes:
#  (y) U(x) = (Currency) Upgrade (x = Number) - Current Amount of the upgrade you have
#  (y)U(x)M = (Currency) Upgrade (Number) Max Amount
#  (y)U(x)Mult = CU(x) = (Currency) (Number) Multipler
# Y = Currency  (C = Clicks) (R = Rebirths)

#   Clicks

CU1M = 25
CU1Mult = 1
CU1_Cost = 1

CU2M = 10
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

RU1M = 15
RU1Mult = 1.6
RU1_Cost = 1

RU2M = 15
RU2Mult = 1.25
RU2_Cost = 1

RU3M = 25
RU3Mult = 1.1
RU3_Cost = 1

ascension_stage = 0

################################################################################
#    Ui / Text Set up
################################################################################
shop_menu = pygame.Rect(420, 720, 440, 140)
Rebirth_menu = pygame.Rect(24, 230, 120, 120)
Tier_menu = pygame.Rect(24, 400, 120, 120)
ascension_menu = pygame.Rect(24, 570, 120, 120)
settings_menu = pygame.Rect(10, 10, 80, 80)

Clicks_Amount_Box = pygame.Rect(100, 20, 350, 100)
Rebirth_Amount_Box = pygame.Rect(500, 20, 350, 100)
Xp_Amount_Box = pygame.Rect(900, 20, 350, 100)
Button_center = (675, 400)
Button_radius = 200

Show_Button_1_hitbox = pygame.Rect(0, 0, 0, 0)
Show_Button_2_hitbox = pygame.Rect(0, 0, 0, 0)
Show_Button_3_hitbox = pygame.Rect(0, 0, 0, 0)
Show_Button_4_hitbox = pygame.Rect(0, 0, 0, 0)
Show_Button_5_hitbox = pygame.Rect(0, 0, 0, 0)
Show_Button_6_hitbox = pygame.Rect(0, 0, 0, 0)
Show_Button_7_hitbox = pygame.Rect(0, 0, 0, 0)

Show_Button_1 = pygame.Surface((0, 0))
Show_Button_2 = pygame.Surface((0, 0))
Show_Button_3 = pygame.Surface((0, 0))
Show_Button_4 = pygame.Surface((0, 0))
Show_Button_5 = pygame.Surface((0, 0))
Show_Button_6 = pygame.Surface((0, 0))
Show_Button_7 = pygame.Surface((0, 0))

background =  pygame.image.load(os.path.join(img_dir, 'Other', 'Background.png'))
Rebirth_Menu_Button = pygame.image.load(os.path.join(img_dir, 'Button', "Rebirth_Button.png"))
Tier_Menu_Button =  pygame.image.load(os.path.join(img_dir, 'Button', "Tier_Button.png"))
Shop_Menu_Button = pygame.image.load(os.path.join(img_dir, 'Button', "Shop_Button.png"))
Click_Button = pygame.image.load(os.path.join(img_dir, 'Click_Button', "Click_Button_clicked.png"))
settings_Button = pygame.image.load(os.path.join(img_dir, 'Button', "Setting_Button.png"))
ascension_Button = pygame.image.load(os.path.join(img_dir, 'Button', "Ascension_Button.png"))

Shown_Menu = pygame.image.load(os.path.join(img_dir,'Menu',"Click_Upgrades.png"))
Locked_Image = pygame.image.load(os.path.join(img_dir,'Menu',"Locked.png"))

click_amount = pygame.image.load(os.path.join(img_dir, 'Amount_Shown', "click_amount.png"))
rebirth_amount = pygame.image.load(os.path.join(img_dir, 'Amount_Shown', "rebirth_amount.png"))
xp_amount = pygame.image.load(os.path.join(img_dir, 'Amount_Shown', "xp_amount.png"))

#Menu Stuff (Render place and size)
Menu_Box = pygame.Rect(20, 150, 1250, 710)
close_menu = pygame.Rect(1170, 200, 50, 50)
menu_ui_1 = pygame.Rect(1170, 200, 50, 50)
menu_ui_2 = pygame.Rect(1170, 200, 50, 50)
menu_ui_3 = pygame.Rect(1170, 200, 50, 50)
menu_ui_4 = pygame.Rect(1170, 200, 50, 50)
menu_ui_5 = pygame.Rect(1170, 200, 50, 50)
menu_ui_6 = pygame.Rect(660, 780, 190, 80)
menu_ui_7 = pygame.Rect(860, 780, 220, 80)
#Menu Text
menu_text1 = font2.render("", True, (0, 0, 0))
menu_text2 = font2.render("", True, (0, 0, 0))
menu_text3 = font2.render("", True, (0, 0, 0))
menu_text4 = font2.render("", True, (0, 0, 0))
menu_text5 = font2.render("", True, (0, 0, 0))
menu_text6 = font2.render("", True, (0, 0, 0))

################################################################################
#    Loading System
################################################################################

running = True

game_vars = {
    "clicks": 0,
    "rebirths": 0,
    "current_tier" : 0,
    "current_ascension" : 0,
    "ascension_tokens": 0,

}

try:
    with open(save_path, "r") as f:
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

        # V3.0 Ascensions
        current_ascension = loaded_data.get("current_ascension", 0)
        ascension_tokens = loaded_data.get("ascension_tokens", 0)
        ascension_stage = loaded_data.get("ascension_stage", 0)
        ascension_stage_2 = loaded_data.get("ascension_stage", 0)


except (FileNotFoundError, json.JSONDecodeError):
    try:
        with open(save_path_backup, "r") as f:
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

            # V3.0 Ascensions
            current_ascension = loaded_data.get("current_ascension", 0)
            ascension_tokens = loaded_data.get("ascension_tokens", 0)
            ascension_stage = loaded_data.get("ascension_stage", 0)
            ascension_stage_2 = loaded_data.get("ascension_stage", 0)

    except (FileNotFoundError, json.JSONDecodeError):
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

                # V3.0 Ascensions
                current_ascension = loaded_data.get("current_ascension", 0)
                ascension_tokens = loaded_data.get("ascension_tokens", 0)
                ascension_stage = loaded_data.get("ascension_stage", 0)
                ascension_stage_2 = loaded_data.get("ascension_stage", 0)

        except (FileNotFoundError, json.JSONDecodeError):
            # Default variables if no save file exists
            clicks = 0
            rebirths = 0
            current_tier = 0
            xp = 0
            total_time_played = 0

            CU1 = 0
            CU2 = 0
            CU3 = 0
            CU4 = 0
            CU5 = 0

            RU1 = 0
            RU2 = 0
            RU3 = 0

            # V3.0 Ascensions
            current_ascension = 0
            ascension_tokens = 0
            ascension_stage = 0
            ascension_stage_2 = 0

##########################
#   Multipler Setup
##########################


CU1_multipler = (CU1 * CU1Mult)
CU2_multipler = (CU2 * CU2Mult)
CU3_multipler = (CU3Mult ** CU3)
CU4_multipler = (CU4Mult ** CU4)
CU5_multipler = (CU5Mult ** CU5)

#-----------------
##########################
#   Upgrade Shop set up
##########################
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
##########################
#   Auto Events (Save, Clicks, Rebirths)
##########################

AUTOSAVE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(AUTOSAVE_EVENT, 10000)

AUTOSAVE_EVENT2 = pygame.USEREVENT + 1
pygame.time.set_timer(AUTOSAVE_EVENT, 60000)


AUTOClick_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(AUTOClick_EVENT, 1000)

AUTORebirth_EVENT = pygame.USEREVENT + 3
pygame.time.set_timer(AUTORebirth_EVENT, 1000)


if len(sys.argv) > 2:
  Menu = int(sys.argv[1])
  DEBUGGER_AVAILABLE = sys.argv[2] == "True"
  print(f"[SYSTEM] Restored -> Menu: {Menu}, Debugger Active: {DEBUGGER_AVAILABLE}")

################################################################################
#    Start Application
################################################################################
while running:

##########################
#   For Debuger
##########################
    physical_mouse_pos = pygame.mouse.get_pos()
    mouse_x = int((physical_mouse_pos[0] - offset_x) / scale)
    mouse_y = int((physical_mouse_pos[1] - offset_y) / scale)
    mouse_pos = (
        max(0, min(mouse_x, GAME_WIDTH - 1)),
        max(0, min(mouse_y, GAME_HEIGHT - 1))
    )

    distance = math.hypot(mouse_pos[0] - Button_center[0], mouse_pos[1] - Button_center[1])

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
        "RU3": RU3,
        "current_ascension": current_ascension,
        "ascension_tokens": ascension_tokens,
        "ascension_stage": ascension_stage,
        "ascension_stage_2": ascension_stage_2
    }
##########################
#   Currency Being shown
##########################
    Clicks_Shown = amount_sum(clicks)
    Rebirths_Shown = amount_sum(rebirths)
    Clicks_AR = font2.render(str(Clicks_Shown), True, (0, 0, 0)) #AR - Amount Render
    if current_tier >= 1:
        Rebirth_AR = font2.render(str(Rebirths_Shown), True, (0, 0, 0))
    else:
        Rebirth_AR = font2.render("Unlock at T1", True, (0, 0, 0))

################################################################################
#    Xp system
################################################################################
    Xp_needed =  int(15* (1.4 ** levels ))
    Xp_needed_sum = amount_sum(Xp_needed)

    total_xp_for_past_levels = 0
    for lvl in range(1, levels):
        total_xp_for_past_levels += int(15 * (1.4 ** lvl) + 3)

    Xp_Current_Level = Xp - total_xp_for_past_levels
    Xp_Current_Level_sum = amount_sum(Xp_Current_Level)
    if Xp_Current_Level >= Xp_needed:
        levels += 1
        Xp_Current_Level = 0
    if current_tier >= 3:
        Click_Xp_Mult = 1.1 ** levels
        Xp_AR = font1.render("Level " + str(levels) + "\n(" +str(Xp_Current_Level_sum) + "/" + str(Xp_needed_sum) + ")", True, (0, 0, 0))
    if current_tier <= 2:
        Xp_AR = font2.render("Unlock At T3",True, (0, 0, 0))

################################################################################
#    Tier Upgrade Multiplers
################################################################################
    if current_tier ==  0:          #    Tier Base Upgrades
        Tier_Xp = 1                 #    Xp Mult
        Tier_Cm = 1                 #    Clicks Multipler
        Tier_Cp = 1                 #    CLicks Power
        Tier_Rm = 1                 #    Rebirth Mult
        Auto_Click_Speed = 0
        Tier_Click_Speed = 1        #    Tier Click Speed Mult
    if current_tier ==  1:
        Tier_Xp = 1
        Tier_Cm = 2  # x2
        Tier_Cp = 1
        Tier_Rm = 1
        Auto_Click_Speed = 0
        Tier_Click_Speed = 1

    if current_tier == 2:
        Tier_Xp = 1
        Tier_Cm = 4       #  x2
        Tier_Cp = 1
        Tier_Rm = 1.5     # x1.5
        Auto_Click_Speed = 0
        Tier_Click_Speed = 1.5 # x1.5

    if current_tier ==  3:
        Tier_Xp = 1
        Tier_Cm = 8    #  x2
        Tier_Cp = 1
        Tier_Rm = 2.25  # x1.5
        Auto_Click_Speed = 1
        Tier_Click_Speed = 1.5

    if current_tier ==  4:
        Tier_Xp = 1
        Tier_Cm = 24    # x3
        Tier_Cp = 1
        Tier_Rm = 4.5  # x2
        Auto_Click_Speed = 1
        Tier_Click_Speed = 1.875  # x1.25

    if current_tier == 5 or current_tier == 6:
        Tier_Xp = 1
        Tier_Cm = 48 # x2
        Tier_Cp = 1
        Tier_Rm = 9 # x2
        Auto_Click_Speed = 1
        Tier_Click_Speed = 1.875
        Auto_Rebirth_Speed = 1

    if current_tier == 7:
        Tier_Xp = 1
        Tier_Cm = 48
        Tier_Cp = 1
        Tier_Rm = 9
        Auto_Click_Speed = 1
        Tier_Click_Speed = 2.35 # x1.25
        Auto_Rebirth_Speed = 1

    if current_tier == 8:
        Tier_Xp = 4
        Tier_Cm = 48
        Tier_Cp = 1.01  # +0.01
        Tier_Rm = 9
        Auto_Click_Speed = 2 # x2
        Tier_Click_Speed = 2.35
        Auto_Rebirth_Speed = 1

    if current_tier == 9:
        Tier_Xp = 4
        Tier_Cm = 48
        Tier_Cp = 1.02 # +0.01
        Tier_Rm = 9
        Auto_Click_Speed = 2
        Tier_Click_Speed = 2.35
        Auto_Rebirth_Speed = 1

    if current_tier == 10:
        Tier_Xp = 4
        Tier_Cm = 48
        Tier_Cp = 1.03 # +0.01
        Tier_Rm = 9
        Auto_Click_Speed = 2
        Tier_Click_Speed = 2.35
        Auto_Rebirth_Speed = 1

    if current_tier == 11:
        Tier_Xp = 4
        Tier_Cm = 480 # x10
        Tier_Cp = 1.04 # +0.01
        Tier_Rm = 45 # x5
        Auto_Click_Speed = 2
        Tier_Click_Speed = 2.35
        Auto_Rebirth_Speed = 1

    if current_tier == 12:
        Tier_Xp = 4
        Tier_Cm = 480
        Tier_Cp = 1.05 # +0.01
        Tier_Rm = 45
        Auto_Click_Speed = 2
        Tier_Click_Speed = 2.35
        Auto_Rebirth_Speed = 1


################################################################################
#    Ascension Upgrade Tree
################################################################################
# Main PATH PART 1
    if ascension_stage == 0:
        Extra_Tiers = 0
        Ascension_QOL_Clicks = 1


    if ascension_stage_2 <= 1:
        Ascension_Click_Mult = 1
        Ascension_XP_Mult = 1
        Ascension_Rebirth_Mult = 1


    if ascension_stage == 1:
        Extra_Tiers = 2
        Ascension_QOL_Clicks = 1

# QOL PATH PART 1

    if ascension_stage == 2:
        Extra_Tiers = 2
        Keep_Click_Upgrades = 1
        Ascension_QOL_Clicks = 2.5

    if ascension_stage == 3:
        Extra_Tiers = 2
        Keep_Click_Upgrades = 1
        Keep_Rebirth_Upgrades = 1
        ascension_Auto_Click_Speed = 1
        Ascension_QOL_Clicks = 6.25


# Boost PATH PART 1
    if ascension_stage_2 == 2:
        Ascension_Click_Mult = 10
        Ascension_Rebirth_Mult = 5
        Ascension_XP_Mult = 2

    if ascension_stage_2 == 3:
        Ascension_Click_Mult = 50
        Ascension_Rebirth_Mult = 15
        Ascension_XP_Mult = 6

# Main Path Part 2

    if ascension_stage == 4:
        Extra_Tiers = 5
        Keep_Click_Upgrades = 1
        Keep_Rebirth_Upgrades = 1
        ascension_Auto_Click_Speed = 1
        Ascension_QOL_Clicks = 6.25

    if ascension_stage_2 == 4:
        Ascension_Click_Mult = 100
        Ascension_Rebirth_Mult = 30
        Ascension_XP_Mult = 12
################################################################################
#   Gain Amount
################################################################################
    current_time = pygame.time.get_ticks()
    time_passed = current_time - last_time_check
    total_time_played += time_passed / 1000.0
    last_time_check = current_time

    if current_tier >= 5:
        total_time_played_Click = total_time_played ** 0.1
    else:
        total_time_played_Click = 1


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
################################################################################
#    Currency Amount Gain
#################################################################################

    base_clicks = (1 + CU1)
    if current_tier <= 5:
        Rebirth_x_clicks = 1
        rebirth_x_self = 1
    if current_tier >= 6:
        Rebirth_x_clicks = 1 + (rebirths ** 0.085)
        rebirth_x_self = 1 + (rebirths ** 0.065)

    CM_Upgrades = (CU3Mult ** CU3) * (RU1Mult ** RU1)
    CM_Tiers = Tier_Cm * Click_Xp_Mult
    CM_Ascension = Ascension_QOL_Clicks * Ascension_Click_Mult
    CM_Other = total_time_played_Click * Rebirth_x_clicks

    Total_clicks_mult =  CM_Upgrades * CM_Tiers * CM_Ascension * CM_Other * dev_mult
    if Total_clicks_mult == 0:
        Total_clicks_mult = 1
    # ----------------

######################
#   Auto CLick Speed
#####################

    if Auto_Click_Speed == 2:
        if ascension_Auto_Click_Speed == 1 and Last_Speed != 3:
            pygame.time.set_timer(AUTOClick_EVENT, 200)
            Last_Speed = 3
        elif ascension_Auto_Click_Speed == 0 and Last_Speed != 2:
            pygame.time.set_timer(AUTOClick_EVENT,500)
            Last_Speed = 2
    elif Auto_Click_Speed == 1 and Last_Speed != 1:
        pygame.time.set_timer(AUTOClick_EVENT, 1000)
        Last_Speed = 1

#####################
#   Gain Amount
#####################
    CPC = base_clicks * Total_clicks_mult  #Click per Click
    CPC_Show = amount_sum(CPC)   # Click per Click

    CooldownLength = 1000 - ((CU2Mult * CU2) * 1000) / Tier_Click_Speed


    Xp_Gain = 1 * (1.1 ** CU5) * (1.1 ** RU3) * Ascension_XP_Mult * Tier_Xp

    if clicks >= 1000:
        Rebirth_Gain = int(((clicks / 500) ** 0.32) * (CU4Mult ** CU4) * (RU2Mult ** RU2) * Tier_Rm * rebirth_x_self * Ascension_Rebirth_Mult)
        Rebirth_Gain_Show = amount_sum(Rebirth_Gain)
    else:
        Rebirth_Gain = 0
        Rebirth_Gain_Show = str(0)


################################################################################
#    Upgrade Changes
################################################################################
    #Click  upgrade 1
    if current_tier >= 9:
        if current_tier >= 12:
            CU1M = 1000
            CU1Mult = 5
    else:
        CU1M = 100
        U1Mult = 2

    #CLick upgrade 3
    if current_tier >= 5:
        if current_tier >= 7:
            if current_tier >= 10:
                CU3M = 25
                CU3Mult = 1.75
            else:
                CU3M = 20
                CU3Mult = 1.5
        else:
            CU3M = 15
            CU3Mult = 1.3

    #Rebirth upgrade 1
    if current_tier >= 6:
            RU1M = 20
            RU1Mult = 1.5


    for event in pygame.event.get():

##########################################
#    Full Screen Mode
###########################################

        if event.type == pygame.VIDEORESIZE:
            if not is_fullscreen:
                WINDOW_WIDTH, WINDOW_HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
                scale, offset_x, offset_y = calculate_scale(WINDOW_WIDTH, WINDOW_HEIGHT)

####################################
#   Auto Events (+ pygame.quit)
####################################

        if event.type == AUTORebirth_EVENT:
            if current_tier >= 5:
                rebirths += Rebirth_Gain / 100

        if event.type == AUTOClick_EVENT:
            if current_tier >= 3:
                    clicks += CPC
                    Xp += 0.25

        if event.type == pygame.QUIT:
            running = False
            save_game(current_state)
            pygame.quit()
            sys.exit()

        # 3. Catch the 10-second timer event here
        if event.type == AUTOSAVE_EVENT:
            save_game(current_state)
            print(f"[SYSTEM] Autosaved for Main ")

        if event.type == AUTOSAVE_EVENT2:
            save_game(current_state)
            print(f"[SYSTEM] Autosaved for backup!")
################################################################################
#    Extra Debug Tools (Only For Development)
#################################################################################
        if event.type == pygame.KEYDOWN:
            if debug_file == 1:
                if event.key == pygame.K_p:
                    debugger_active = not debugger_active
                    print(f"[SYSTEM] Debugger toggled: {debugger_active}")

                elif event.key == pygame.K_o:
                    if debugger_active:
                        print("[SYSTEM] Restarting game script and saving state...")
                        save_game(current_state)
                        pygame.quit()
                        os.execl(sys.executable, sys.executable, __file__, str(Menu), str(debugger_active))
                elif event.key == pygame.K_i:
                    print ("[SYSTEM] Debug variable Checker:")
                    print("[SYSTEM] Currencies:")
                    print("Clicks: " + str(clicks))
                    print("Rebirths: " + str(rebirths))
                    print("Xp: " + str(Xp))
                    print("Tokens: " + str(ascension_tokens))
                    print("Menu: " + str(Menu))
                    print("[SYSTEM] Click Multiplers:")
                    print("Upgrades: " + str(CM_Upgrades))
                    print("Tier: " + str(CM_Tiers))
                    print("Ascension: " + str(CM_Ascension))
                    print("Other: " + str(CM_Other))

##############################
# Button Clicked with mouse
##############################

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click down
                if Rebirth_menu.collidepoint(mouse_pos):
                    #Open Rebirth menu
                    if Menu == 0:
                        if current_tier >= 1:
                            Menu = 11

                if ascension_menu.collidepoint(mouse_pos):
                    if Menu == 0:
                        if current_tier >= 10 or current_ascension >= 1:
                            Menu = 13

                if Tier_menu.collidepoint(mouse_pos):
                    #Open Rebirth menu
                    if Menu == 0:
                        Menu = 12

                if settings_menu.collidepoint(mouse_pos):
                    if Menu == 0:
                        Menu = 52

                if menu_ui_6.collidepoint(mouse_pos)  and Menu <= 9:
                    if Menu == 6:
                        Menu = 1
                    elif Menu == 1:
                        Menu = 6
                if shop_menu.collidepoint(mouse_pos):

                    if Menu == 0:
                        Menu = 1

                if close_menu.collidepoint(mouse_pos):
                    if Menu >= 1:
                        # Close Menu Button
                        Menu = 0

                if menu_ui_1.collidepoint(mouse_pos) and Menu == 12:
                    Tier_cost = tier_cost(current_tier, "None")
                    Tier_cost_Shown = tier_cost(current_tier, "Suffix")
                    if current_tier <= 11:
                        if clicks >= Tier_cost:
                            clicks = 0
                            rebirths = 0
                            if ascension_stage <= 1:
                                CU1 = 0
                                CU2 = 0
                                CU3 = 0
                                CU4 = 0
                            if ascension_stage <= 2:
                                RU1 = 0
                                RU2 = 0
                                RU3 = 0
                            current_tier += 1





                if menu_ui_7.collidepoint(mouse_pos) and Menu <= 9:
                    if 9 <=Menu >= 1:
                        if current_ascension >= 1:
                            Menu = 14



                if Show_Button_1_hitbox.collidepoint(mouse_pos) and Menu == 14:
                    if ascension_stage == 0:
                        ascension_stage = 1
                        ascension_stage_2 = 1

                if Show_Button_2_hitbox.collidepoint(mouse_pos) and Menu == 14:
                    if ascension_stage_2 == 1:
                        if ascension_tokens >= 1:
                            ascension_stage_2 = 2
                            ascension_tokens -= 1

                if Show_Button_3_hitbox.collidepoint(mouse_pos) and Menu == 14:
                    if ascension_stage_2 == 2:
                        if ascension_tokens >= 1:
                            ascension_stage_2 = 3
                            ascension_tokens -= 1

                if Show_Button_4_hitbox.collidepoint(mouse_pos) and Menu == 14:
                    if ascension_stage == 1:
                        if ascension_tokens >= 1:
                            ascension_stage = 2
                            ascension_tokens -= 1

                if Show_Button_5_hitbox.collidepoint(mouse_pos) and Menu == 14:
                    if ascension_stage == 2:
                        if ascension_tokens >= 1:
                            ascension_stage = 3
                            ascension_tokens -= 1

                if Show_Button_6_hitbox.collidepoint(mouse_pos) and Menu == 14:
                    if ascension_stage == 3:
                        if ascension_tokens >= 1:
                            ascension_stage = 4
                            ascension_tokens -= 1



                if menu_ui_1.collidepoint(mouse_pos)  and Menu == 11:
                        if Menu == 11:
                            if clicks >= 1000:
                                clicks = 0
                                if ascension_stage <= 1:
                                    CU1 = 0
                                    CU2 = 0
                                    CU3 = 0
                                    CU4 = 0
                                rebirths += Rebirth_Gain

                if menu_ui_1.collidepoint(mouse_pos)  and Menu == 13:
                        if clicks >= ascension_cost(current_ascension, "NA"):
                            clicks = 0
                            CU1 = 0
                            CU2 = 0
                            CU3 = 0
                            CU4 = 0
                            RU1 = 0
                            RU2 = 0
                            RU3 = 0
                            rebirths = 0
                            current_tier = 0



################################################################################
#    Upgrade Menu stuff
################################################################################

                if Menu == 1:
                    upgrades[0].level = CU1
                    upgrades[1].level = CU2
                    upgrades[2].level = CU3
                    upgrades[3].level = CU4
                    upgrades[4].level = CU5
                    for up in upgrades:
                        clicks, bought = up.try_buy(mouse_pos, Menu, clicks)
                        if bought:
                            break
                    CU1 = upgrades[0].level
                    CU2 = upgrades[1].level
                    CU3 = upgrades[2].level
                    CU4 = upgrades[3].level
                    CU5 = upgrades[4].level

                if Menu == 6:
                    upgrades2[0].level = RU1
                    upgrades2[1].level = RU2
                    upgrades2[2].level = RU3

                    for up in upgrades2:
                        rebirths, bought = up.try_buy(mouse_pos, Menu, rebirths)
                        if bought:
                            break #
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
                            Xp += Xp_Gain
#########
# Settings Buttons
###########
                if Menu == 52:
                    if menu_ui_4.collidepoint(mouse_pos):
                        if Change_size == 2:
                            Change_size = 1
                            Size_changer = "1300 x 900"
                        elif Change_size == 1:
                            Change_size = 2
                            Size_changer = "Full Screen"

                    if menu_ui_5.collidepoint(mouse_pos):
                        size = Change_size
                        Set_size = 1

                    if menu_ui_6.collidepoint(mouse_pos):
                        running = False
                        save_game(current_state)
                        pygame.quit()
                        sys.exit()
                else:
                    Change_size = size
 ################################################################################
#    Console/Debug
################################################################################

        if CONSOLE_AVAILABLE:
            if CONSOLE_AVAILABLE:
                temp_state = {
                    "clicks": clicks,
                    "rebirths": rebirths,
                    "current_tier": current_tier,
                    "dev_mult": dev_mult,
                    "current_ascension": current_ascension,
                    "ascension_tokens": ascension_tokens
                }

                temp_state = game_console.check_commands(temp_state)

                clicks = temp_state["clicks"]
                rebirths = temp_state["rebirths"]
                current_tier = temp_state["current_tier"]
                dev_mult = temp_state["dev_mult"]
                current_ascension = temp_state["current_ascension"]
                ascension_tokens = temp_state["ascension_tokens"]
        # ========================================================
        # ========================================================

        # ========================================================

################################################################################
#    Drawing Ui Elements
################################################################################
        #Upgrade  Menu

        if current_Cooldown <= current_time:
            Click_Button = pygame.image.load(os.path.join(img_dir,'Click_Button', "Click_Button_unclicked.png"))
        else:
            Click_Button = pygame.image.load(os.path.join(img_dir,'Click_Button',"Click_Button_clicked.png"))

        if Menu <= 10:
            menu_ui_1 = pygame.Rect(110, 340, 425, 55)
            menu_ui_2 = pygame.Rect(110, 560, 425, 55)
            menu_ui_3 = pygame.Rect(110, 780, 425, 55)
            menu_ui_4 = pygame.Rect(710, 340, 425, 55)
            menu_ui_5 = pygame.Rect(710, 560, 425, 55)
            menu_ui_6 = pygame.Rect(660, 780, 200, 80)
            menu_ui_7 = pygame.Rect(860, 780, 220, 80)

            #menu_ui_6 = pygame.Rect(620, 760, 270, 120)

        # Tier, rebirth and ascension  Menu
        if Menu in menu_base_1:
            menu_ui_1 = pygame.Rect(200, 720, 870, 100)
            menu_ui_2 = pygame.Rect(110, 250, 1100, 400)
        if Menu == 1:
            CU1_Cost_Show = CU1_CostAmount(CU1, current_tier,"Suffix")
            CU2_Cost_Show = CU2_CostAmount(CU2, current_tier, "Suffix")
            CU3_Cost_Show = CU3_CostAmount(CU3, current_tier, "Suffix")
            CU4_Cost_Show = CU4_CostAmount(CU4, current_tier, "Suffix")
            CU5_Cost_Show = CU5_CostAmount(CU5, current_tier,"Suffix")

            CU1_multipler = (CU1 * CU1Mult)
            CU2_multipler = (CU2 * CU2Mult)
            CU3_multipler = (CU3Mult ** CU3)
            CU4_multipler = (CU4Mult ** CU4)
            CU5_multipler = (CU5Mult ** CU5)

            CU2_multipler_s = amount_sum(CU2_multipler)
            CU3_multipler_s = amount_sum(CU3_multipler)
            CU4_multipler_s = amount_sum(CU4_multipler)
            CU5_multipler_s = amount_sum(CU5_multipler)

            menu_text1 = font2.render("Base Power: (" + str(CU1) + "/" + str(CU1M) + ") \n +" + str(CU1_multipler) + " \n  Cost: " + str(CU1_Cost_Show), True, (0, 0, 0))
            menu_text2 = font2.render("Faster Clicks (" + str(CU2) + "/" + str(CU2M) + ")\n -" + str(CU2_multipler_s) + " Cd \n  Cost: " + str(CU2_Cost_Show), True, (0, 0, 0))
            menu_text3 = font2.render("Power Clicks (" + str(CU3) + "/" + str(CU3M) + ")\n X" + str(CU3_multipler_s) + " \n  Cost: " + str(CU3_Cost_Show), True, (0, 0, 0))

            if current_tier >= 2:
                menu_text4 = font2.render("More Rebirths ("  + str(CU4) + "/" + str(CU4M) + ")\n X" + str(CU4_multipler_s) + " \n   Cost: " + str(CU4_Cost_Show), True, (0, 0, 0))
            else:
                menu_text4 = font2.render("Unlock At Tier 2 ", True, (0, 0, 0))
            if current_tier >= 4:
                menu_text5 = font2.render("More Xp (" + str(CU5) + "/" + str(CU5M) + ")\n X" + str(CU5_multipler_s) + " \n  Cost: " + str(CU5_Cost_Show), True, (0, 0, 0))
            else:
                menu_text5 = font2.render("Unlock At Tier 4 ", True, (0, 0, 0))

            menu_text6 = font2.render("", True, (0, 0, 0))

        if Menu == 6:
            RU1_Cost_Show = RU1_CostAmount(RU1, current_tier, "Suffix")
            RU2_Cost_Show = RU2_CostAmount(RU2, current_tier, "Suffix")
            RU3_Cost_Show = RU3_CostAmount(RU3, current_tier, "Suffix")

            RU1_multipler = (RU1Mult ** RU1)
            RU2_multipler = (RU2Mult ** RU2)
            RU3_multipler = (RU3Mult ** RU3)

            RU1_multipler_s = amount_sum(RU1_multipler)
            RU2_multipler_s = amount_sum(RU2_multipler)
            RU3_multipler_s = amount_sum(RU3_multipler)


            menu_text1 = font2.render("Clicks Power 2: (" + str(RU1) + "/" + str(RU1M) + ") \n x" + str(RU1_multipler_s) + " \n  Cost: " + str(RU1_Cost_Show), True, (0, 0, 0))
            menu_text2 = font2.render("Rebirth Power (" + str(RU2) + "/" + str(RU2M) + ")\n x" + str(RU2_multipler_s) + " \n  Cost: " + str(RU2_Cost_Show), True, (0, 0, 0))
            menu_text3 = font2.render("Extra Xp (" + str(RU3) + "/" + str(RU3M) + ")\n X" + str(RU3_multipler_s) + " \n  Cost: " + str(RU3_Cost_Show), True, (0, 0, 0))
            menu_text4 = font2.render("Coming Later", True, (0, 0, 0))
            menu_text5 = font2.render("Coming Later ", True, (0, 0, 0))
            menu_text6 = font2.render("", True, (0, 0, 0))


        if Menu == 13:
            ascensiontext = ascension_cost(current_ascension,"Suffix")
            menu_text1 = font5.render("To Ascend get:\n  " + str(ascensiontext) +" Clicks", True, (0, 0, 0))
        if Menu == 12:
            Tiertext = tier_cost(current_tier,"Suffix")
            menu_text1 = font3.render((tier_info(current_tier)), True,  (0, 0, 0))
            menu_text2 = font2.render("Cost: " + str(Tiertext) , True, (0, 0, 0))
        if Menu == 11:
            menu_text1 = font5.render(("If you rebirth you gain: \n \n     " + Rebirth_Gain_Show) + " Rebirths", True,  (0, 0, 0))
        # Drawing Systems
        canvas.blit(background, (0, 0))
        if Menu == 0:
            canvas.blit(Shop_Menu_Button, (420, 720))

    pygame.draw.rect(canvas, green, Clicks_Amount_Box, width=0, border_radius=30)
    pygame.draw.rect(canvas, red, Rebirth_Amount_Box, width=0, border_radius=30)
    pygame.draw.rect(canvas, yellow, Xp_Amount_Box, width=0, border_radius=30)

    pygame.draw.rect(canvas, black, Clicks_Amount_Box, width=5, border_radius=30)
    pygame.draw.rect(canvas, black, Rebirth_Amount_Box, width=5, border_radius=30)
    pygame.draw.rect(canvas, black, Xp_Amount_Box, width=5, border_radius=30)

    canvas.blit(Click_Button, (440, 190))

    canvas.blit(click_amount, (95, 15))
    canvas.blit(rebirth_amount, (495, 15))
    canvas.blit(xp_amount, (895, 15))

    CurrencyBox1 = Clicks_AR.get_rect()
    CurrencyBox2 = Rebirth_AR.get_rect()
    CurrencyBox3 = Xp_AR.get_rect()
    if Menu != 14:
        close_menu = pygame.Rect(1170, 200, 50, 50)
    if Menu == 14:
        close_menu = pygame.Rect(1170, 100, 50, 50)

    Menu_text1 = menu_text1.get_rect()
    Menu_text2 = menu_text2.get_rect()
    Menu_text3 = menu_text3.get_rect()
    Menu_text4 = menu_text4.get_rect()
    Menu_text5 = menu_text5.get_rect()
    Menu_text6 = menu_text6.get_rect()

    CurrencyBox1.center = (250, 75)

    if current_tier <= 1:
        CurrencyBox2.center = (720, 75)
    if current_tier >= 2:
        CurrencyBox2.center = (660, 75)

    CurrencyBox3.center = (1130, 70)

    if current_tier >= 1:
        canvas.blit(Rebirth_Menu_Button, (25, 230))
    canvas.blit(Tier_Menu_Button, (25, 400))
    canvas.blit(settings_Button, (-10, -10))
    if current_tier >= 10 or current_ascension >= 1:
        canvas.blit(ascension_Button, (25, 570))
    canvas.blit(Clicks_AR, CurrencyBox1)
    canvas.blit(Rebirth_AR, CurrencyBox2)
    canvas.blit(Xp_AR, CurrencyBox3)


    # Menu System (Drawing)
    if Menu != 0:
        if Menu == 1:
            Shown_Menu = pygame.image.load(os.path.join(img_dir,'Menu',"Click_Upgrades.png"))
            canvas.blit(Shown_Menu, (0, 0))
        if Menu == 6:
            Shown_Menu = pygame.image.load(os.path.join(img_dir,'Menu',"Rebirth_Upgrades.png"))
            canvas.blit(Shown_Menu, (0, 0))
        if Menu == 11:
            Shown_Menu = pygame.image.load(os.path.join(img_dir,'Menu',"Rebirth_Menu.png"))
            canvas.blit(Shown_Menu, (0, 0))
        if Menu == 12:
            Shown_Menu = pygame.image.load(os.path.join(img_dir,'Menu',"Tier_Menu.png"))
            canvas.blit(Shown_Menu, (0, 0))
        if Menu == 13:
            Shown_Menu = pygame.image.load(os.path.join(img_dir,'Menu',"Ascension_Menu.png"))
            canvas.blit(Shown_Menu, (0, 0))
        if Menu == 14:
            Shown_Menu = pygame.image.load(os.path.join(img_dir,'Menu',"Tree_Background.png"))
            canvas.blit(Shown_Menu, (0, 0))
        if Menu == 52:
            Shown_Menu = pygame.image.load(os.path.join(img_dir,'Menu',"Settings_Menu.png"))
            canvas.blit(Shown_Menu, (0, 0))

        if 1 <= Menu <= 9 :
            if current_ascension == 0:
                Locked_Image = pygame.image.load(os.path.join(img_dir, 'Menu', "Locked.png"))
                canvas.blit(Locked_Image, (0, -1))

            Menu_text1.center = (300, 320)
            Menu_text2.center = (300, 540)
            Menu_text3.center = (300, 760)
            Menu_text4.center = (880, 320)
            Menu_text5.center = (860, 540)
            Menu_text6.center = (860, 760)
            canvas.blit(menu_text1, Menu_text1)
            canvas.blit(menu_text2, Menu_text2)
            canvas.blit(menu_text3, Menu_text3)
            canvas.blit(menu_text4, Menu_text4)
            canvas.blit(menu_text5, Menu_text5)
            canvas.blit(menu_text6, Menu_text6)


#####
# Hide Ui element when not on the menu
######
        if Menu == 0 :
            Menu_text1.center = (3000, 320)
            Menu_text2.center = (3000, 540)
            Menu_text3.center = (3000, 760)
            Menu_text4.center = (8800, 320)
            Menu_text5.center = (8600, 540)
            Menu_text6.center = (8600, 760)
            canvas.blit(Shown_Menu, (1000, 1000))

######
# Tiers Menu Text line up
######
        if Menu == 12:
            if current_tier == 0:
                Menu_text1.center = (440, 380)
            elif current_tier == 1:
                Menu_text1.center = (470, 410)
            elif current_tier == 2:
                Menu_text1.center = (610, 410)
            elif current_tier == 3:
                Menu_text1.center = (550, 420)
            elif current_tier == 4:
                Menu_text1.center = (610, 430)
            elif current_tier == 5:
                Menu_text1.center = (400, 510)
            elif current_tier == 6:
                Menu_text1.center = (570, 370)
            elif current_tier == 7:
                Menu_text1.center = (400, 370)
            elif current_tier == 8:
                Menu_text1.center = (600, 370)
            elif current_tier == 9:
                Menu_text1.center = (570, 370)
            elif current_tier == 10:
                Menu_text1.center = (435, 370)
            elif current_tier == 11:
                Menu_text1.center = (470, 370)
            elif current_tier == 12:
                Menu_text1.center = (570, 370)
            elif current_tier == 13:
                Menu_text1.center = (570, 370)

            canvas.blit(menu_text1, Menu_text1)


        if Menu == 11:
            Menu_text1.center = (650, 462)
            canvas.blit(menu_text1, Menu_text1)

        if Menu == 13:

            Menu_text1.center = (600, 462)
            canvas.blit(menu_text1, Menu_text1)



        if Menu == 14:
            if ascension_stage == 0:
                Show_Button_1 = pygame.image.load(os.path.join(img_dir,'Tree_Buttons',"#1_V1.png"))


            if ascension_stage_2 == 1:
                Show_Button_2 = pygame.image.load(os.path.join(img_dir,'Tree_Buttons',"#2_V1.png"))


            if ascension_stage_2 == 2:
                Show_Button_3 = pygame.image.load(os.path.join(img_dir,'Tree_Buttons',"#3_V1.png"))

            if ascension_stage == 1:
                Show_Button_4 = pygame.image.load(os.path.join(img_dir,'Tree_Buttons',"#4_V1.png"))

            if ascension_stage == 2:
                Show_Button_5 = pygame.image.load(os.path.join(img_dir,'Tree_Buttons',"#5_V1.png"))

            if ascension_stage == 3:
                Show_Button_6 = pygame.image.load(os.path.join(img_dir,'Tree_Buttons',"#6_V1.png"))

            if ascension_stage ==  4:
                Show_Button_7 = pygame.image.load(os.path.join(img_dir,'Tree_Buttons',"#7_V1.png"))



            Show_Button_1 = pygame.image.load(os.path.join(img_dir, 'Tree_Buttons', "#1_V2.png")) if ascension_stage >= 1 else Show_Button_1
            Show_Button_4 = pygame.image.load(os.path.join(img_dir, 'Tree_Buttons', "#4_V2.png")) if ascension_stage >= 2 else Show_Button_4
            Show_Button_5 = pygame.image.load(os.path.join(img_dir, 'Tree_Buttons', "#5_V2.png")) if ascension_stage >= 3 else Show_Button_5
            Show_Button_6 = pygame.image.load(os.path.join(img_dir, 'Tree_Buttons', "#6_V2.png")) if ascension_stage >= 4 else Show_Button_6

            Show_Button_2 = pygame.image.load(os.path.join(img_dir, 'Tree_Buttons', "#2_V2.png")) if ascension_stage_2 >= 2 else Show_Button_2
            Show_Button_3 = pygame.image.load(os.path.join(img_dir, 'Tree_Buttons', "#3_V2.png")) if ascension_stage_2 >= 3 else Show_Button_3

#------------------------
# Start of Showwing buttons
 # -------------------------
# (X = +\- 420 |||| Y = - 235

            ascension_tokens = 10
            if ascension_stage >= 0:
                canvas.blit(Show_Button_1, (450, 630))
                Show_Button_1_hitbox = Show_Button_1.get_rect(topleft=(450, 630))


            if ascension_stage_2 >= 1:
                canvas.blit(Show_Button_2, (30, 450))
                Show_Button_2_hitbox = Show_Button_2.get_rect(topleft=(50, 425))

            if ascension_stage_2 >= 2:
                canvas.blit(Show_Button_3, (30, 185))
                Show_Button_3_hitbox = Show_Button_3.get_rect(topleft=(50, 220))

            if ascension_stage >= 1:
                canvas.blit(Show_Button_4, (870, 450))
                Show_Button_4_hitbox = Show_Button_4.get_rect(topleft=(850, 425))

            if ascension_stage >= 2:
                canvas.blit(Show_Button_5, (870, 185))
                Show_Button_5_hitbox = Show_Button_5.get_rect(topleft=(850, 220))

            if ascension_stage >= 3:
                canvas.blit(Show_Button_6, (450, 15))
                Show_Button_6_hitbox = Show_Button_6.get_rect(topleft=(450, 15))

            if ascension_stage >= 10:
                canvas.blit(Show_Button_7, (0, 0))
                Show_Button_7_hitbox = Show_Button_7.get_rect()

################
## Settings
################
        if Menu == 52:
            menu_ui_1 = pygame.Rect(145, 370, 440, 105)
            menu_ui_2 = pygame.Rect(145, 510, 440, 105)
            menu_ui_3 = pygame.Rect(145, 680, 435, 110)
            menu_ui_4 = pygame.Rect(700, 405, 440, 101)
            menu_ui_5 = pygame.Rect(750, 520, 330, 90)
            menu_ui_6 = pygame.Rect(690, 660, 440, 105)
            Menu_text4.center = (920, 460)
            menu_text4 = font2.render(Size_changer, True, (0, 0, 0))
            canvas.blit(menu_text4, Menu_text4)

        if Set_size == 1:
            if size == 1:
                if Old_Size == 2:
                    is_fullscreen = not is_fullscreen
                WINDOW_WIDTH, WINDOW_HEIGHT = 1300, 900
                Size_changer = "1300 x 900"
                Set_size = 0
                Old_Size = 1
            if size == 2:
                is_fullscreen = not is_fullscreen
                Size_changer = "Full Screen"
                Set_size = 0
                Old_Size = 2

                if is_fullscreen:
                    # Cache the size right before we go into fullscreen mode
                    info_before = pygame.display.Info()
                    if info_before.current_w > 0:
                        WINDOWED_WIDTH_CACHE = info_before.current_w
                        WINDOWED_HEIGHT_CACHE = info_before.current_h

                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    info = pygame.display.Info()
                    WINDOW_WIDTH, WINDOW_HEIGHT = info.current_w, info.current_h
                else:
                    WINDOW_WIDTH = WINDOWED_WIDTH_CACHE
                    WINDOW_HEIGHT = WINDOWED_HEIGHT_CACHE
                    # FIXED: Ensure the resizable flag is applied when returning to windowed mode
                    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

                # Recalculate your math variables instantly so mouse coordinates don't break
                scale, offset_x, offset_y = calculate_scale(WINDOW_WIDTH, WINDOW_HEIGHT)


##################################
# Debugger -> Note: The Debugger is made by ai but is only used for testing)
###################################
    if debugger_active:
        debugger.draw_hud(canvas, globals(), mouse_pos, clock)

###################################
 #   End of Script
###################################

    screen.fill((0, 0, 0))
    new_size = (int(GAME_WIDTH * scale), int(GAME_HEIGHT * scale))
    scaled_canvas = pygame.transform.scale(canvas, new_size)
    screen.blit(scaled_canvas, (offset_x, offset_y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
