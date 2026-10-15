from datetime import date


# Years: 2026 to 2050
easter_months = [3, 4, 4, 4, 4, 3, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 3, 4, 4, 4, 4]
easter_days   = [28, 16, 1, 21, 13, 28, 17, 9, 25, 13, 5, 25, 10, 1, 21, 6, 29, 17, 9, 25, 14, 5, 18, 10]

def event():
    today = date.today()
    month = today.month
    day = today.day
    if month == 10 and day >= 20:
        event = "spooky" # Lasts From October 20th -> October 31st
    elif month == 12 and day <= 25:
        event = "festive" # Lasts From December 1st -> December 25th
    elif month == 12 and day >= 26 or month == 1 and day <= 2:
        event = "celebration" # Lasts From December 26th -> January 2nd

    elif month == 3 or month == 4: # Easter
        year = today.year
        year = year - 2026
        easter_day = (easter_days)[year]
        easter_month = (easter_months)[year]
        if easter_day <= 5:
            split_start = 36 - easter_day
            if month == 3 and split_start <= 31 or month == 4 and easter_day >= day:
                event = "egg"  # Goes to 2050
        elif easter_day >= 6:
            easter_start = easter_day - 5
            if month == easter_month and easter_day >= easter_start:
                event = "egg" # Goes to 2050
        else:
            event = "base"
    else:
        event = "base"


########
# Override
########
    a = 0
    if a == 1:
        event = "base"
    if a == 2:
        event = "spooky"
    if a == 3:
        event = "festive"
    if a == 4:
        event = "celebration"
    if a == 5:
        event = "egg"
    return event



##############################
# To Add:
# Anniversary -> Jun 18
# St Partrics Day -> 14 Feb
##############################
