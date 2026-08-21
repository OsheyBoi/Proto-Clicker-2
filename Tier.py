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
         text = " \n Tier 1: Cost: (" + tier_cost(Tier,"Suffix") + ")\n - Unlock Rebirths \n - Unlock Rebirth Upgrades \n  - 1.5x Clicks"
         return text
    elif Tier == 1:
         text = " \n Tier 2: Cost: (" + tier_cost(Tier,"Suffix") + ")\n - Unlock Click Upgrade 4 \n - 2x Clicks \n - 1.5x Rebirths \n - 1.5x Faster Button Cooldown"
         return text
    elif Tier == 2:
         text = " \n Tier 3: Cost: (" + tier_cost(Tier,"Suffix") + ") \n - Unlock Xp (1 / Click) (25% on Auto Click) \n - Auto Click (Base = 1 cps) \n - 2x Clicks \n - 1.5x Rebirths "
         return text
    elif Tier == 3:
         text = " \n Tier 4: Cost: (" + tier_cost(Tier,"Suffix") + ") \n - Unlock Click Upgrade 5 \n - 3x Clicks \n - 2x Rebirths \n - 1.25x Faster Button Cooldown"
         return text
    elif Tier == 4:
         text = " \n Tier 5: Cost: (" + tier_cost(Tier,"Suffix") + ") \n - Unlock Rebirth Upgrade 3 \n - Auto Rebirth (1% RPS) \n - 2x Clicks/Rebirths \n - Powerful Clicks Effect: +0.05 / Cap: +5  \n - Playtime Boost Clicks (Permanent)"
         return text
    elif Tier == 5:
         text = " \n Tier 6: Cost: (" + tier_cost(Tier,"Suffix") + ") \n Rebirths Boost Clicks \n Rebirths Boost themself \n Clicks Power 2 +10 Max / +0.05x \n (+ Price Increase) "
         return text
    elif Tier == 6:
         text = " \n Tier 7: Cost: (" + tier_cost(Tier,"Suffix") + ") \n - Powerful Clicks Effect: +0.2x / Cap: +5 \n (+ Price Increase) \n - x1.25 Faster Button Cooldown"
         return text
    elif Tier == 7:
         text = " \n Tier 8: Cost: (" + tier_cost(Tier,"Suffix") + ") \n - 4x Xp \n - 1.01^ Clicks \n - 2x Faster Autoclicker. "
         return text
    elif Tier == 8:
         text = " \n Tier 9: Cost: (" + tier_cost(Tier,"Suffix") + ") \n - Base Power Effect: +1 -> +2 / Cap: +80  \n (+ Price Increase) \n - 1.01^ - 1.02^ Clicks"
         return text
    elif Tier == 9:
         text = " \n Tier 10: Cost: (" + tier_cost(Tier,"Suffix") + ") \n - Powerful Clicks Effect: +0.25x  \n 1.02^ - 1.03^ Clicks \n Unlock Ascension (V3)"
         return text
    elif Tier == 10:
         text = " \n Tier 11: Cost: (" + tier_cost(Tier,"Suffix") + ")\n - 10x Click \n - 5x Rebirths \n - Clicks Power 1.03 -> 1.04"
         return text
    elif Tier == 11:
         text = " \n Tier 12: Cost: (" + tier_cost(Tier,"Suffix") + ") \n - Base Power Effect: +2 -> +5 \n - Base Power Cap: +900 \n - Clicks Power 1.04 -> 1.05 "
         return text
    elif Tier == 12:
         text = " \n You Have Reach Max Tier in V4.0 \n Tiers 13 - 15 are Coming Soon "
         return text

    else:
        text = "Error 1: \n Failed to load Tier Info"
        return  text



def tier_cost(tier, type):
    if tier == 0:
        # 1 Thousand
        Cost = 1000

    elif tier == 1:
        #150 Thousand
        Cost = 150000

    elif tier == 2:
        #5 Million
        Cost = (1000 ** 2) *5

    elif tier == 3:
        #100 Million
        Cost = 100000000

    elif tier == 4:
        # 5B Billion
        Cost = (1000 ** 3) * 5

    elif tier == 5:
        # 5 Billion
        Cost = (1000 ** 3) * 100

    elif tier == 6:
        # 5 trillion
        Cost = (1000 ** 4) * 5

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
        Cost =  (1000 ** 8) * 250

    elif tier == 11:
        Cost =  (1000 ** 10) * 10

    elif tier == 12:
        Cost =  100000**10
        type = "Max Tier"

    if type == "Max Tier":
        return type

    if type != "Suffix":
        return Cost
    else:
        cost = amount_sum(Cost)
        return cost



