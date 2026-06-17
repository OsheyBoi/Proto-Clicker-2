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

def CU1_CostAmount(upgrade,Type):
    if upgrade == 0:
        cost = 10
    else:
        cost = (10 + int(upgrade * 4)) ** 1.05
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    return cost
def CU2_CostAmount(upgrade,Type):
    if upgrade == 0:
        cost = 25
    else:
        cost = (25 + int(upgrade * 30)) ** 1.35
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    return cost
def CU3_CostAmount(upgrade,Type):
    if upgrade == 0:
        cost = 100
    else:
        cost = (100 * 2 ** upgrade)
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    return cost
def CU4_CostAmount(upgrade,Type):
    if upgrade == 0:
        cost = 1000
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    else:
        cost = (1000 + int(upgrade * 100)) ** 1.05
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    return cost
def CU5_CostAmount(upgrade,Type):

    if upgrade == 0:
        cost = 1000 ** 3
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    else:
        cost = (1000 ** 3 * (upgrade ** 5))
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    return cost

def RU1_CostAmount(upgrade,Type):

    if upgrade == 0:
        cost = 1
    else:
        cost = (1 + (upgrade * 2) ** 1.1)
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    return cost

def RU2_CostAmount(upgrade,Type):

    if upgrade == 0:
        cost = 5
    else:
        cost = (5 + (upgrade * 5) ** 1.25)
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    return cost

def RU3_CostAmount(upgrade,Type):

    if upgrade == 0:
        cost = 1000
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    else:
        cost = (1000 * (upgrade ** 5))
        if Type != "Suffix":
            return cost
        else:
            cost = amount_sum(cost)
    return cost