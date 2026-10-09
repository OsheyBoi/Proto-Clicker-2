from datetime import date
def event():
    today = date.today()
    month = today.month
    day = today.day
    if month == 10 and day >= 20:
        event = "spooky"
    elif month == 10 and day >= 20:
        event = "spooky"
    elif month == 12 and day <= 25:
        event = "festive"
    elif month == 12 and day >= 26 or month == 1 and day <= 3:
        event = "celebration"
    else:
        event = "base"
    return event
