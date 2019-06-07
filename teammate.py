import datetime

import calendar
import pprint
from operator import attrgetter

#assumption: the maximum working hour for each teammate everymonth = hour*day
class Teammate:

    def __init__(self, name, hour, day):

        self.name = name
        self.hour = hour
        self.day = day


        self.availableHourLeft = []
        #schedule = [{datetime Object, hour, clientName}...]
        self.schedule = []

    def getName(self):
        return self.name

    def getHour(self):
        return self.hour

    def getDay(self):
        return self.day

    def addTask(self, date, workHour, client):
        self.schedule.append({'day': date, 'hour': workHour, 'client': client.getName()})
        tList = client.getRelatedTeammate()
        if self.getName() not in tList:
            client.addRelatedTeammate(self.getName())


    def clearTask(self):
        self.schedule.clear()

    def getSchedule(self):
        return self.schedule

    def getHourList(self):
        return self.availableHourLeft


    def getAvailableHourLeft(self,month):
        return self.availableHourLeft[month -1]

    def setAvailableHourLeft(self,month, hour):
        self.availableHourLeft[month-1] = hour

    def checkNextAvailableDay(self, month):
        #old method
        sortSchedule = sorted(self.schedule, key=lambda k: k['day'])

        for dayIndex in range(1, self.getDay()*4 + 1):
            hourLeft = self.getHour()
            for day in self.schedule:
                if day['day'] == dayIndex:
                    hourLeft = hourLeft - day['hour']

            # print('hours left for day' + str(dayIndex) + ' is:' + str(hourLeft))

            if hourLeft > 0:
                return [dayIndex, hourLeft]

        #todo find new way to colloectdays & addtasks

    #this method get next avaialbe day by month
    def nextAvailableDay(self,month):
        sortSchedule = sorted(self.schedule, key=lambda k: k['day'])
        workDaysInMonth = calendar.getWorkdaysByMonth(month)
        # print('month index is :' + str(month) + ' workdays in this month is: ' )
        # print(workDaysInMonth)

        copy = workDaysInMonth[:]

        # if datetime.datetime(2019, 8, 30, 0, 0) in workDaysInMonth:
        #     print('yes')
        for workday in copy:
            # print(workday)
            hourLeft = self.getHour()
            for task in self.getSchedule():
                if task['day'].date() == workday.date():
                    hourLeft = hourLeft - task['hour']
            # try:
            #
            # except TypeError:
            #     pass

            if hourLeft > 0:
                return [workday, hourLeft]



    def getTasksbyDay(self, day):
        tasksOnDay = []
        for task in self.schedule:
            if task['day'] == day:
                tasksOnDay.append(task)
        return tasksOnDay


    def printTaskByName(self):
        print(self.schedule)




teammates = []

#return True if there is any teammate has available hour >0
def checkAvaiblable(month):
    for teammate in teammates:
        if teammate.getAvailableHourLeft(month) > 0:
            return True
    return False


def printTasks():
    for teammate in teammates:
        print('========== I AM '+teammate.getName() +'=========')
        tasks = teammate.getSchedule()
        for task in tasks:
            pprint.pprint(task)



def initialiseTeammates(teammatesData):
    #teammateDate = [[name,hour,day]...]
    monthWorkday = calendar.getNumWorkdaysPerMonth()
    for tData in teammatesData:
        teammates.append(Teammate(tData[0],int(tData[1]),int(tData[2])))
    for teammate in teammates:
        # set up available hours for 12 month
        count = 1
        while count < 13:
            teammate.availableHourLeft.append(teammate.getHour()*monthWorkday[count-1])
            count += 1
        # set up calendar



def printTeammates():
    for teammate in teammates:
        print(teammate.getName())

def teammateList():
    result = []
    for teammate in teammates:
        result.append(teammate.getName())
    return result

def clearAllTasks():
    for teammate in teammates:
        teammate.clearTask()

def updateTeammates(newlist):
    teammates.clear()
    initialiseTeammates(newlist)

def totalTeammatesHours():
    result = 0
    for t in teammates:
        result += sum(t.getHourList())
    return result

def fillschedule(clients):
    #algorithm1, let one teammate deal with one client if not possible, give the work to second teammate

    #for each client in the client list distribute the client's hours to teammates
    #A teammate's total avaible hours is his hour*day


    # for client in clients:
    #     cHour = client.getHour()
    #
    #     print('=====================================================================indexte==================')
    #     print('dealing with client: ' + client.getName())
    #     while cHour > 0:
    #
    #
            # for teammate in teammates:
            #     tHour = teammate.getHour()
            #     tHourLeft = teammate.getAvailableHourLeft()
            #
            #     while tHourLeft > 0 and cHour > 0:
            #         [nextAvailableDay, availableHour] = teammate.checkNextAvailableDay()
            #
            #         #if client work hour requrired left > teammate's available hour left one that day, work as much as he can:
            #         if cHour > availableHour:
            #             workHour = availableHour
            #         # if client work hour requrired left < teammate's available hour left one that day, work amount left:
            #         if cHour < availableHour:
            #             workHour = cHour
            #
            #         teammate.addTask(nextAvailableDay, workHour, client.getName())
            #
            #         print('adding task: {day: ' + str(nextAvailableDay) + ' workHour: ' +str(workHour) +' client: ' + client.getName()+'}')
            #
            #         teammate.setAvailableHourLeft(tHourLeft - workHour)
            #         cHour = cHour - workHour
            #         tHourLeft = tHourLeft -workHour
            #         client.setHour(cHour)
            #         print('client ' + client.getName() + ' has ' + str(client.getHour()) + ' hours left')


    #algorithm 2: * do clients with hightest hours first
    #             * least number of teammates for one client ideally 1-1
    #             * even the workload among all teammates


    #todo change fillschdule addtask
    for client in clients:

        for month in range(1,13):

            cHour = client.getYearHours()[month-1]
            bindings = client.getRelatedTeammate()
            Done = False
            print(cHour)

            for teammate in teammates:
                tHourLeft = teammate.getAvailableHourLeft(month)
                if tHourLeft > cHour and (teammate.getName() in bindings):
                    while cHour > 0:
                        [day, availableHour] = teammate.nextAvailableDay(month)

                        if cHour > availableHour:
                            workHour = availableHour
                        if cHour < availableHour:
                            workHour = cHour
                        teammate.addTask(day, workHour, client)
                        # print('adding task: ' + str(day) + str(workHour) + ' ' + client.getName())
                        # print('adding task: {day: ' + str(nextAvailableDay) + ' workHour: ' + str(
                        #     workHour) + ' client: ' + client.getName() + '}')

                        teammate.setAvailableHourLeft(month, tHourLeft - workHour)
                        cHour = cHour - workHour
                        tHourLeft = tHourLeft - workHour
                        client.setYearHours(month, cHour)
                        # print('client ' + client.getName() + ' has ' + str(client.getHour()) + ' hours left')
                    Done = True

            if not Done:
                for teammate in teammates:
                    tHourLeft = teammate.getAvailableHourLeft(month)
                    if tHourLeft > cHour:
                        while cHour > 0:
                            [day, availableHour] = teammate.nextAvailableDay(month)

                            if cHour > availableHour:
                                workHour = availableHour
                            if cHour < availableHour:
                                workHour = cHour
                            teammate.addTask(day, workHour, client)
                            # print('adding task: ' + str(day) + str(workHour) + ' ' + client.getName())
                            # print('adding task: {day: ' + str(nextAvailableDay) + ' workHour: ' + str(
                            #     workHour) + ' client: ' + client.getName() + '}')


                            teammate.setAvailableHourLeft(month, tHourLeft - workHour)
                            cHour = cHour - workHour
                            tHourLeft = tHourLeft - workHour
                            client.setYearHours(month, cHour)
                            # print('client ' + client.getName() + ' has ' + str(client.getHour()) + ' hours left')

            # todo make sort the teammates by their avaiable hours left this month
            # teammates.sort(key=attrgetter('availableHourLeft')[month-1], reverse=True)
            teammates.sort(key=lambda x: x.getAvailableHourLeft(month) , reverse=True)


            #when tHourLeft<cHour
            while cHour > 0:
                if not checkAvaiblable(month):
                    break

                for teammate in teammates:

                    # print('==========this is teammate: ' + teammate.getName() +'================')

                    tHourLeft = teammate.getAvailableHourLeft(month)
                    while tHourLeft > 0 and cHour > 0:
                        try:
                            [day, availableHour] = teammate.nextAvailableDay(month)
                            if cHour > availableHour:
                                workHour = availableHour
                            if cHour < availableHour:
                                workHour = cHour

                            teammate.addTask(day, workHour, client)
                            # print('adding task: ' + str(day) + ' ' + str(8) + 'hours ' + client.getName())
                            # print('adding task: {day: ' + str(day) + ' workHour: ' + str(
                            #     workHour) + ' client: ' + client.getName() + '}')

                            teammate.setAvailableHourLeft(month, tHourLeft - workHour)
                            cHour = cHour - workHour
                            tHourLeft = tHourLeft - workHour
                            # print('hour left: ' + str(cHour) + '  '+ str(tHourLeft))
                            # print(teammate.printTaskByName())
                            client.setYearHours(month, cHour)
                            # print('client ' + client.getName() + ' has ' + str(client.getHour()) + ' hours left')
                        except TypeError:
                            print('fatal error when scheduling workload')
                            exit()









