import datetime

import calendar
import pprint
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout, \
    QPushButton, QAbstractItemView, QGridLayout, QGroupBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


import IOhandler
import client
import teammate

clientsData = []
teammatesData = []
sortedClients = []
displayTeammateIndex = 0

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'Weboptimizers Scheduler'
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 1000
        self.initUI()





    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createClientTable()
        self.createTeammateNameQlabal()
        self.createSummaryQlable()
        self.createTeammateTable()
        self.createOutputTable()
        self.createRelationshipTable()

        #start schedule button
        self.runButton = QPushButton('Start schedule', self)
        self.runButton.clicked.connect(self.clickToSchedule)
        self.runButton.resize(100, 32)
        self.runButton.move(500, 500)

        self.nextTeammateButton = QPushButton('Next Teammate', self)
        self.nextTeammateButton.clicked.connect(self.clickToNextTeammate)
        self.nextTeammateButton.resize(200, 60)
        self.nextTeammateButton.move(0,0)



        # Add grid layout, add table to grid layout
        self.createGridLayout()
        windowLayout = QVBoxLayout()

        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)



        # Show widget
        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()

        layout = QGridLayout()
        layout.setColumnStretch(0, 15)
        layout.setColumnStretch(1, 20)
        layout.setColumnStretch(2, 20)

        layout.setRowStretch(0, 10)
        layout.setRowStretch(1, 20)

        layout.addWidget(self.clientTableWidget, 0, 0)
        layout.addWidget(self.teammateTableWidget, 0, 1)
        layout.addWidget(self.outputtableWidget, 1,0,1,40)
        layout.addWidget(self.runButton, 2, 2)
        layout.addWidget(self.relationshipTableWidget,0,2)
        layout.addWidget(self.nextTeammateButton,2,1)
        layout.addWidget(self.teammateName, 2, 0)
        layout.addWidget(self.summary, 1, 3)
        self.horizontalGroupBox.setLayout(layout)

    def createTeammateNameQlabal(self):
        self.teammateName = QLabel('Displaying schedule: ')

    def createSummaryQlable(self):
        self.summary = QLabel('Result Summary')


    def createClientTable(self):
        client_list = client.getAllClients()
        # Create table
        self.clientTableWidget = QTableWidget()

        self.clientTableWidget.setRowCount(100)
        self.clientTableWidget.setColumnCount(2)
        self.clientTableWidget.setHorizontalHeaderLabels(['Client_Name','Client_Hour'])
        client_id = 0
        for c in client.clients:

            clientName = c.getName()
            clientHour = str(c.getInitHour())
            self.clientTableWidget.setItem(client_id, 0, QTableWidgetItem(clientName))
            self.clientTableWidget.setItem(client_id, 1, QTableWidgetItem(clientHour))
            client_id += 1
        self.clientTableWidget.move(0, 0)

        # table selection change
        self.clientTableWidget.doubleClicked.connect(self.on_click)


    def createRelationshipTable(self):

        self.relationshipTableWidget = QTableWidget()

        self.relationshipTableWidget.setRowCount(100)
        self.relationshipTableWidget.setColumnCount(2)
        self.relationshipTableWidget.setHorizontalHeaderLabels(['Client_Name','Responsible Teammate'])
        self.relationshipTableWidget.move(0, 0)
        self.relationshipTableWidget.horizontalHeader().setStretchLastSection(True)



    def createTeammateTable(self):
        # Create table
        self.teammateTableWidget = QTableWidget()
        self.teammateTableWidget.setRowCount(30)
        self.teammateTableWidget.setColumnCount(3)
        teammate_id = 0
        for t in teammate.teammates:
            teammateName = t.getName()
            teammateHour = str(t.getHour())
            teammateDay = str(t.getDay())
            self.teammateTableWidget.setHorizontalHeaderLabels(['Name', 'Hours', 'Days'])
            self.teammateTableWidget.setItem(teammate_id, 0, QTableWidgetItem(teammateName))
            self.teammateTableWidget.setItem(teammate_id, 1, QTableWidgetItem(teammateHour))
            self.teammateTableWidget.setItem(teammate_id, 2, QTableWidgetItem(teammateDay))
            teammate_id += 1

        self.teammateTableWidget.move(0, 0)

        # table selection change
        self.teammateTableWidget.doubleClicked.connect(self.on_click)



    def createOutputTable(self):
        # Create table
        weeks = 53
        weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday']


        self.outputtableWidget = QTableWidget()
        self.outputtableWidget.setRowCount(weeks)
        self.outputtableWidget.setColumnCount(len(weekdays))

        self.outputtableWidget.setHorizontalHeaderLabels(weekdays)
        self.outputtableWidget.move(0, 0)


    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.clientTableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

    def clickToNextTeammate(self):
        self.clearOutput()
        increaseDisplayIndex()
        self.teammateName.setText('Displaying schedule: ' + teammate.teammates[displayTeammateIndex].getName())
        self.scheduleTeammate(displayTeammateIndex)
        return




    def clickToSchedule(self):
        self.clearOutput()
        updateClients = self.updateClientData()
        updateTeammates = self.updateTeammateData()
        # pprint.pprint(updateClients)
        client.updateClientList(updateClients)

        # print('len of clientlist after update' + str(len(client.sortedClients)))
        # client.printSortedClients()

        teammate.updateTeammates(updateTeammates)

        cTotal = client.totalwork()
        tTotal = teammate.totalTeammatesHours()
        initialiseScaling(cTotal,tTotal)
        self.summary.setText('Result Summary: \n'
                             'Total hours required by clients: ' + str(cTotal) + '\n'
                             'Total hours avaialble by Teammates: ' + str(tTotal) + '\n'
                             'Appling scaling factor of: '+str(tTotal/cTotal))
        teammate.fillschedule(client.getSortedClients())


        # newteammatenames = []
        #
        # for t in teammate.teammates:
        #     newteammatenames.append(t.getName())
        #
        # self.outputtableWidget.setColumnCount(len(newteammatenames))
        # self.outputtableWidget.setHorizontalHeaderLabels(newteammatenames)


        #filling schedule in the output table (algorithm1)
        # days = calendar.nextMonthCalendar()
        # dayindex = 0
        # wordayindex = 0
        # for day in days:
        #
        #     if day.weekday() == 5 or day.weekday() == 6:
        #         dayindex += 1
        #         continue
        #
        #     teammateindex = 0
        #     print(str(dayindex))
        #     for t in teammate.teammates:
        #
        #         ouput = ''
        #         taskOnDay = t.getTasksbyDay(wordayindex+1)
        #         if len(taskOnDay) == 1:
        #             for task in taskOnDay:
        #                 ouput = ouput + task['client'] + ' ' + str(task['hour'])
        #         if len(taskOnDay) > 1:
        #             for task in taskOnDay:
        #                 ouput = ouput + '(' + task['client'] + ' ' + str(task['hour']) + ') '
        #
        #
        #
        #         self.outputtableWidget.setItem(dayindex, teammateindex, QTableWidgetItem(ouput))
        #         teammateindex += 1
        #     wordayindex += 1
        #     dayindex += 1



        # filling schedule in the output table (algorithm2)

        # days = calendar.nextMonthCalendar()
        #
        # teammateindex = 0
        # for t in teammate.teammates:
        #
        #     days = calendar.nextMonthCalendar()
        #     tasks = t.getSchedule()
        #     numWorkdays = t.getDay()
        #
        #     freedays = [5,6]
        #     while numWorkdays < 5:
        #         freedays.append(numWorkdays)
        #         numWorkdays+=1
        #
        #     dayindex = 0
        #     taskindex = 0
        #     for day in days:
        #
        #         #check is freeday or not first
        #
        #         if day.weekday() in freedays:
        #             self.outputtableWidget.setItem(dayindex, teammateindex, QTableWidgetItem(''))
        #             dayindex += 1
        #             continue
        #
        #
        #
                # ouput = ''
                # taskOnDay = t.getTasksbyDay(taskindex+1)
                # if len(taskOnDay) == 1:
                #     for task in taskOnDay:
                #         ouput = ouput + task['client'] + ' ' + str(task['hour'])
                # if len(taskOnDay) > 1:
                #     for task in taskOnDay:
                #         ouput = ouput + '(' + task['client'] + ' ' + str(task['hour']) + ') '
        #
        #         self.outputtableWidget.setItem(dayindex, teammateindex, QTableWidgetItem(ouput))
        #         dayindex +=1
        #         taskindex +=1
        #     teammateindex +=1
        #

        # filling schedule in the output table (algorithm3) for one teammate, row = weekdays, column = week number

        self.scheduleTeammate(displayTeammateIndex)
        self.teammateName.setText(
            'Displaying schedule: ' + teammate.teammates[displayTeammateIndex].getName())





        #filling the client-teammate relationship table
        client_id = 0
        for c in client.clients:
            clientName = c.getName()
            clientRelationship = ''
            for t in c.getRelatedTeammate():
                clientRelationship = clientRelationship + t + ' '

            self.relationshipTableWidget.setItem(client_id, 0, QTableWidgetItem(clientName))
            self.relationshipTableWidget.setItem(client_id, 1, QTableWidgetItem(clientRelationship))
            client_id += 1


        # teammate.printTasks()


    def updateClientData(self):
        updateClients =[]
        for i in range(100):
            try:
                clientName = self.clientTableWidget.item(i, 0).text()
                clientHour = self.clientTableWidget.item(i, 1).text()

                if clientName is not '':
                    updateClients.append([clientName,clientHour])
            except AttributeError:
                pass
        return updateClients

    def updateTeammateData(self):
        updateTeammates = []
        for i in range(30):
            try:
                teammateName = self.teammateTableWidget.item(i, 0).text()
                teammateHour = self.teammateTableWidget.item(i, 1).text()
                teammateDay = self.teammateTableWidget.item(i, 2).text()

                if teammateName is not '':
                    updateTeammates.append([teammateName, teammateHour, teammateDay])
            except AttributeError:
                pass
        return updateTeammates

    def clearOutput(self):
        for row in range(5):
            for column in range(53):
                self.outputtableWidget.setItem(column,row,QTableWidgetItem(''))

    def scheduleTeammate(self, teammateIndex):
        startingDate = calendar.getWorkDaysNextYear()[0]
        tasks = teammate.teammates[teammateIndex].getSchedule()
        tasks.sort(key=lambda x: x['day'])

        horizonIndex = 0
        verticalIndex = 0
        previousDay = startingDate
        for task in tasks:
            # print(str(task['day']) +task['client']+str(task['hour']))
            dayInterval = 0

            date = task['day']
            # print(date)
            # print(previousDay)
            dayInterval = (date - previousDay).days
            horizonIndex = horizonIndex + dayInterval
            if horizonIndex > 6:
                verticalIndex += horizonIndex // 7
                horizonIndex = horizonIndex % 7

            previousTask = self.outputtableWidget.item(verticalIndex, horizonIndex).text()
            output = ''
            output = previousTask + ' ' + output + task['client'] + ' ' + str(task['hour'])
            # print(task)
            # print(verticalIndex,horizonIndex)

            self.outputtableWidget.setItem(verticalIndex, horizonIndex, QTableWidgetItem(output))
            previousDay = date

def increaseDisplayIndex():
    global displayTeammateIndex
    indexrange = len(teammatesData)
    displayTeammateIndex += 1
    if displayTeammateIndex > indexrange-1:
        displayTeammateIndex = 0

def initialiseScaling(cHour,tHour):
    scaleFactor = tHour/cHour
    if scaleFactor < 1:
        for c in client.clients:
            initialClientHour = c.getHour()
            hourAfterScale = int(initialClientHour*scaleFactor)
            c.setHour(hourAfterScale)
            c.setScaledHourForYear(hourAfterScale)

if __name__ == '__main__':

    print(calendar.getNumWorkdaysPerMonth())

    clientsData = IOhandler.loadcsv('clients.csv')
    teammatesData = IOhandler.loadcsv('teammates.csv')

    client.initialiseClients(clientsData)


    totalClientHours = client.totalwork()

    teammate.initialiseTeammates(teammatesData)
    totalTeammateHours = teammate.totalTeammatesHours()

    initialiseScaling(totalClientHours,totalTeammateHours)
    client.sortClients()
    # for c in client.sortedClients:
    #     print(c.getHour())

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
