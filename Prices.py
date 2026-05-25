def amount_sum(amount):
    if amount < 1000:
        if amount > 100:
            rounded_amount = round(amount, 1)
        else:
            rounded_amount = round(amount, 0)
        return str(rounded_amount)
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

def CU1_CostAmount(upgrade):
    if upgrade == 0:
        cost = 10
    else:
        cost = (10 + int(upgrade * 3)) ** 1.03
        cost = amount_sum(cost)
    return cost

def CU2_CostAmount(upgrade):
    if upgrade == 0:
        cost = 50
    else:
        cost = (50 + int(upgrade * 10)) ** 1.1
        cost = amount_sum(cost)
    return cost

def CU3_CostAmount(upgrade):
    if upgrade == 0:
        cost = 100
    else:
        cost = (100 + int(upgrade * 10)) ** 1.05
        cost = amount_sum(cost)
    return cost

def CU4_CostAmount(upgrade):
    if upgrade == 0:
        cost = 1000
    else:
        cost = (1000 + int(upgrade * 100)) ** 1.05
        cost = amount_sum(cost)
    return cost
def CU5_CostAmount(upgrade):
    if upgrade == 0:
        cost = 1000
    else:
        cost = (1000 ** 3 + int(1000 ** 3 * 5))
        cost = amount_sum(cost)
    return cost