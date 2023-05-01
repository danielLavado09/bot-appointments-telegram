import datetime
import random


def get_random_date():
    today = datetime.date.today()

    # Generamos las 5 fechas posteriores a la actual y las agregamos a la lista
    temp_dates = [today + datetime.timedelta(days=i + 1) for i in range(5)]

    temp_dates.sort()

    return temp_dates
