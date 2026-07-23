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
         text = " \n Tier 5: \n - Unlock Rebirth Upgrade 3 \n - Auto Rebirth (1% RPS) \n - 2x Clicks/Rebirths \n - Powerful Clicks Power +0.05 and Max +5  \n Playtime Boost Clicks"
         return text
    elif Tier == 5:
         text = " \n Tier 6: \n Rebirths Boost Clicks \n Rebirths Boost themself \n Clicks Power 2 +10 Max / +0.05x \n (+ Price Increase) "
         return text
    elif Tier == 6:
         text = " \n  Tier 7: \n Powerful Clicks +0.2x / + 5 Max \n (+ Price Increase) \n x1.25 Faster Button Cooldown"
         return text
    elif Tier == 7:
         text = " \n  Tier 8: \n 4x Xp \n 1.01^ Clicks \n 2x Faster Autoclicker. "
         return text
    elif Tier == 8:
         text = " \n  Tier 9: Base Power +1 -> +2 / 4x Cap \n (+ Price Increase) \n 1.01^ - 1.02^ Clicks"
         return text
    elif Tier == 9:
         text = " \n  Tier 10: Powerful Clicks +0.25x Mult \n 1.02^ - 1.03^ Clicks \n Unlock Ascension (V3)"
         return text
    elif Tier == 10:
         text = " \n You Have Reach Max Tier in V2.0 \n More Will Be added Soon "
         return text

    else:
        text = "Error 1: \n Failed to load Tier Info"
        return  text



def tier_cost(tier, type):
    if tier == 0:
        # 1 Thousand
        Cost = 1000

    elif tier == 1:
        #50 Thousand
        Cost = 50000

    elif tier == 2:
        #1 Million
        Cost = 1000 ** 2

    elif tier == 3:
        #25 Million
        Cost = 25000000

    elif tier == 4:
        # 500 Million
        Cost = 500000000

    elif tier == 5:
        # 5 Billion
        Cost = (1000 ** 3) * 5

    elif tier == 6:
        # 500  Billion
        Cost = (1000 ** 3) * 500

    elif tier == 7:
        # 100 trillion
        Cost = (1000 ** 4) * 100

    elif tier == 8:
        # 750 quadrillion
        Cost = (1000 ** 5) * 750

    elif tier == 9:
        # 1 sextillion
        Cost = (1000 ** 7)

    elif tier == 10:
        Cost =  10000**10
        type = "Max Tier"

    if type == "Max Tier":
        return type

    if type != "Suffix":
        return Cost
    else:
        cost = amount_sum(Cost)
        return cost



