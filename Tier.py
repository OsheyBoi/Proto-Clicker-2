def amount_sum(amount):
    if amount < 1000:
        if amount > 100:
            rounded_amount = round(amount, 1)
        else:
            rounded_amount = round(amount, 0)
        return str(rounded_amount)
    suffixes = ['','K','M','B','T','Qd','Qn','Sx','Sp','Oc',"No",'De','UDe','DDe',"TDe","QDe"]
    suffix_index = 0

    while amount >= 1000:
        amount /= 1000
        suffix_index += 1
        rounded_amount = 0.0
    if amount >= 1 and amount <= 9:
        rounded_amount = round(amount, 2)
    if amount >= 10 and amount <= 99:
        rounded_amount = round(amount, 1)
    if amount >= 100:
        rounded_amount = round(amount, 0)
    Summed_Amount = str(rounded_amount) + suffixes[suffix_index]
    return str(Summed_Amount)


def tier_info (Tier):
    if Tier == 0:
         text = " \n Tier 1: \n - Unlock Rebirths \n - Unlock Rebirth Upgrades \n  - 1.5x Clicks"
         return text
    elif Tier == 1:
         text = " \n Tier 2: \n - Unlock Click Upgrade 4 \n - 2x Clicks \n - 1.5x Rebirths \n - 1.5x Faster Button Cooldown"
         return text
    elif Tier == 2:
         text = " \n Tier 3: \n - Unlock Xp (1 / Click) (25% on Auto Click) \n - Auto Click (Base = 1 cps) \n  - 2x Clicks \n - 1.5x Rebirths "
         return text
    elif Tier == 3:
         text = " \n Tier 4: \n - Unlock Click Upgrade 5 \n - 3x Clicks \n  - 2x Rebirths \n - 1.25x Faster Button Cooldown"
         return text
    elif Tier == 4:
         text = " \n Tier 5: \n - Unlock Rebirth Upgrade 4 \n - Auto Rebirth (1% RPS) \n - 2x Clicks/Rebirths \n - Powerfull Clicks Power +0.05 and Max +10  \n Playtime Boost Clicks"
         return text
    elif Tier == 5:
         text = " \n You Have Reach Max Tier in V1.0 \n More Will Be add In V2.0 "
         return text

    else:
        text = "Error 1: \n Failed to load Tier Info"
        return  text



def tier_cost(tier, type):
    if tier == 0:
        Cost = 1000

    elif tier == 1:
        Cost = 50000

    elif tier == 2:
        Cost = 1000 ** 2

    elif tier == 3:
        Cost = 25000000

    elif tier == 4:
        Cost = 500000000


    elif tier == 5:
        Cost =  10000**10
        type = "Max Tier"

    if type == "Max Tier":
        return type

    if type != "Suffix":
        return Cost
    else:
        cost = amount_sum(Cost)
        return cost



