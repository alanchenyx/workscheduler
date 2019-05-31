import pprint
from operator import attrgetter
import client


class Teammate:

    def __init__(self, name, hour, day):
        self.name = name
        self.hour = hour
        self.day = day
        self.availableHourLeft = 4*day*hour
        self.schedule = []

    def getName(self):
        return self.name

    def getHour(self):
        return self.hour

    def getDay(self):
        return self.day

    def addTask(self, dayNum, workHour, client):
        self.schedule.append({'day': dayNum, 'hour': workHour, 'client': client})

    def getSchedule(self):
        return self.schedule

    def getAvailableHourLeft(self):
        return self.availableHourLeft

    def setAvailableHourLeft(self, hour):
        self.availableHourLeft = hour

    def checkNextAvailableDay(self):
        sortSchedule = sorted(self.schedule, key=lambda k: k['day'])

        for dayIndex in range(1, self.getDay()*4 + 1):
            hourLeft = self.getHour()
            for day in self.schedule:
                if day['day'] == dayIndex:
                    hourLeft = hourLeft - day['hour']

            # print('hours left for day' + str(dayIndex) + ' is:' + str(hourLeft))

            if hourLeft > 0:
                return [dayIndex, hourLeft]

    def getTasksbyDay(self, day):
        tasksOnDay = []
        for task in self.schedule:
            if task['day'] == day:
                tasksOnDay.append(task)
        return tasksOnDay


    # def printTaskByName(self):
    #     print(self.schedule)


teammates = []

#return True if there is any teammate has available hour >0
def checkAvaiblable():
    for teammate in teammates:
        if teammate.getAvailableHourLeft() > 0:
            return True
    return False


def printTasks():
    for teammate in teammates:
        print('========== I AM '+teammate.getName() +'=========')
        tasks = teammate.getSchedule()
        for task in tasks:
            pprint.pprint(task)


def initialiseTeammates(teammatesData):
    for t in teammatesData:
        teammates.append(Teammate(t[0],int(t[1]),int(t[2])))

def printTeammates():
    for teammate in teammates:
        print(teammate.getName())



def fillschedule(clients):
    #algorithm1, let one teammate deal with one client if not possible, give the work to second teammate

    #for each client in the client list distribute the client's hours to teammates
    #A teammate's total avaible hours is his hour*day


    # for client in clients:
    #     cHour = client.getHour()
    #
    #     print('=======================================================================================')
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


    for client in clients:
        cHour = client.getHour()
        for teammate in teammates:
            tHourLeft = teammate.getAvailableHourLeft()
            if tHourLeft > cHour:
                while cHour > 0:
                    [nextAvailableDay, availableHour] = teammate.checkNextAvailableDay()
                    if cHour > availableHour:
                        workHour = availableHour
                    if cHour < availableHour:
                        workHour = cHour
                    teammate.addTask(nextAvailableDay, workHour, client.getName())

                    print('adding task: {day: ' + str(nextAvailableDay) + ' workHour: ' + str(
                        workHour) + ' client: ' + client.getName() + '}')

                    teammate.setAvailableHourLeft(tHourLeft - workHour)
                    cHour = cHour - workHour
                    tHourLeft = tHourLeft - workHour
                    client.setHour(cHour)
                    print('client ' + client.getName() + ' has ' + str(client.getHour()) + ' hours left')

        teammates.sort(key=attrgetter('availableHourLeft'), reverse=True)
        while cHour > 0:
            if not checkAvaiblable():
                break

            for teammate in teammates:
                tHourLeft = teammate.getAvailableHourLeft()
                while tHourLeft > 0 and cHour > 0:
                    [nextAvailableDay, availableHour] = teammate.checkNextAvailableDay()

                    if cHour > availableHour:
                        workHour = availableHour
                    if cHour < availableHour:
                        workHour = cHour

                    teammate.addTask(nextAvailableDay, workHour, client.getName())

                    print('adding task: {day: ' + str(nextAvailableDay) + ' workHour: ' + str(
                        workHour) + ' client: ' + client.getName() + '}')

                    teammate.setAvailableHourLeft(tHourLeft - workHour)
                    cHour = cHour - workHour
                    tHourLeft = tHourLeft - workHour
                    client.setHour(cHour)
                    print('client ' + client.getName() + ' has ' + str(client.getHour()) + ' hours left')





