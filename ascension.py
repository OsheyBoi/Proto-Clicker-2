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


def ascension_cost(ascension, type):

    Base = (1000 ** 7)  * 100
    Cost = Base * (1000 ** ascension)

    if type == "Max ascension":
        return type

    if type != "Suffix":
        return Cost
    else:
        cost = amount_sum(Cost)
        return cost

