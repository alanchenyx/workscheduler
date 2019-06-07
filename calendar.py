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



#return a list of days for next year starting from input "date"
def getNextYear():
    date = datetime.datetime(2019, 7, 1)

    datesOfYear = []

    count = 0
    while count < 365:

        datesOfYear.append(date)
        date += datetime.timedelta(days=1)
        count += 1


    return datesOfYear

def getWorkDaysNextYear():
    fullYear = getNextYear()
    fullYearR = fullYear[:]
    for day in fullYear:
        if day.weekday() == 5 or day.weekday() == 6:
            fullYearR.remove(day)
    return fullYearR

def getNumWorkdaysPerMonth():
    monthDays = []
    for monthIndex in range(1,13):
        monthDays.append(len(getWorkdaysByMonth(monthIndex)))
    return monthDays

def getWorkdaysByMonth(monthnum):
    allWorkDays = getWorkDaysNextYear()

    monthStartIndex = allWorkDays[0].month

    monthIndex = monthStartIndex + (monthnum - 1)
    yearIndex = allWorkDays[0].year
    if monthIndex > 12:
        monthIndex = monthIndex % 12
        yearIndex = yearIndex + 1

    monthWorkDay = []
    for day in allWorkDays:
        if day.month == monthIndex and day.year == yearIndex:
            monthWorkDay.append(day)

    return monthWorkDay