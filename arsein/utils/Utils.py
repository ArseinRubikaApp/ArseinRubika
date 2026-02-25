import time


def auto_delete_time(Time):
    now = int(time.time() * 1000)
    Time = Time.strip()

    days = ["1 روز", "2 روز", "3 روز", "4 روز", "5 روز", "6 روز"]
    weeks = ["1 هفته", "2 هفته", "3 هفته"]
    months = ["1 ماه", "2 ماه", "3 ماه", "4 ماه", "5 ماه", "6 ماه"]
    years = ["یکسال", "1 سال"]

    if Time in days:
        get_time = int(Time.split()[0])
        return now + get_time * 86400000

    if Time in weeks:
        get_time = int(Time.split()[0])
        return now + get_time * 7 * 86400000

    if Time in months:
        get_time = int(Time.split()[0])
        return now + get_time * 30 * 86400000

    if Time in years:
        return now + 365 * 86400000

    return None
