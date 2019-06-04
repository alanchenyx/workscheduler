#read system current datetime and return all days next month in a list
import datetime

def nextMonthCalendar():
    date = datetime.datetime.now()
    currentMonth = date.month
    calendar = []

    while date.month < currentMonth + 2:
        date += datetime.timedelta(days=1)
        if date.month == currentMonth + 1:
            calendar.append(date)

    return calendar

def getWeekday(date):
    weekday = date.weekday()
    if weekday == 0:
        return 'Monday'
    if weekday == 1:
        return 'Tuesday'
    if weekday == 2:
        return 'Wednesday'
    if weekday == 3:
        return 'Thursday'
    if weekday == 4:
        return 'Friday'
    if weekday == 5:
        return 'Saturday'
    if weekday == 6:
        return 'Sunday'


def getWorkdayNum(dateList):
    count = 0
    for date in dateList:
        count += 1
        if date.weekday == 5 or date.weekday == 6:
            pass

    return count