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
        self.createTeammateTable()
        self.createOutputTable()
        self.createRelationshipTable()

        self.runbutton = QPushButton('Start schedule', self)
        self.runbutton.clicked.connect(self.clickMethod)
        self.runbutton.resize(100, 32)
        self.runbutton.move(500, 500)

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
        layout.setColumnStretch(0, 10)
        layout.setColumnStretch(1, 15)
        layout.setColumnStretch(2, 20)

        layout.setRowStretch(0, 10)
        layout.setRowStretch(1, 20)

        layout.addWidget(self.clientTableWidget, 0, 0, )
        layout.addWidget(self.teammateTableWidget, 0, 1)
        layout.addWidget(self.outputtableWidget, 1,0,1,40)
        layout.addWidget(self.runbutton, 2, 1)
        layout.addWidget(self.relationshipTableWidget,0,2)

        self.horizontalGroupBox.setLayout(layout)

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
            clientHour = str(c.getinitHour())
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
        days = calendar.nextMonthCalendar()



        self.outputtableWidget = QTableWidget()
        self.outputtableWidget.setRowCount(len(days))

        teammateNum = len(teammate.teammates)
        self.outputtableWidget.setColumnCount(teammateNum)


        teammateNames = teammate.teammateList()
        self.outputtableWidget.setHorizontalHeaderLabels(
            teammateNames)

        weekdays = []
        for day in days:
            label = str(day.day) + '/' + str(day.month) + '/' + str(day.year) + ' ' + calendar.getWeekday(day)
            weekdays.append(label)

        self.outputtableWidget.setVerticalHeaderLabels(weekdays)

        self.outputtableWidget.move(0, 0)


    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.clientTableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())




    def clickMethod(self):

        updateClients = self.updateClientData()
        updateTeammates = self.updateTeammateData()
        # pprint.pprint(updateClients)
        client.updateClientList(updateClients)

        # print('len of clientlist after update' + str(len(client.sortedClients)))
        # client.printSortedClients()

        teammate.updateTeammates(updateTeammates)
        teammate.fillschedule(client.getSortedClients())

        newteammatenames = []

        for t in teammate.teammates:
            newteammatenames.append(t.getName())

        self.outputtableWidget.setColumnCount(len(newteammatenames))
        self.outputtableWidget.setHorizontalHeaderLabels(newteammatenames)


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

        days = calendar.nextMonthCalendar()

        teammateindex = 0
        for t in teammate.teammates:

            days = calendar.nextMonthCalendar()
            tasks = t.getSchedule()
            numWorkdays = t.getDay()

            freedays = [5,6]
            while numWorkdays < 5:
                freedays.append(numWorkdays)
                numWorkdays+=1

            dayindex = 0
            taskindex = 0
            for day in days:

                #check is freeday or not first

                if day.weekday() in freedays:
                    self.outputtableWidget.setItem(dayindex, teammateindex, QTableWidgetItem(''))
                    dayindex += 1
                    continue



                ouput = ''
                taskOnDay = t.getTasksbyDay(taskindex+1)
                if len(taskOnDay) == 1:
                    for task in taskOnDay:
                        ouput = ouput + task['client'] + ' ' + str(task['hour'])
                if len(taskOnDay) > 1:
                    for task in taskOnDay:
                        ouput = ouput + '(' + task['client'] + ' ' + str(task['hour']) + ') '

                self.outputtableWidget.setItem(dayindex, teammateindex, QTableWidgetItem(ouput))
                dayindex +=1
                taskindex +=1
            teammateindex +=1








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


        teammate.printTasks()



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

if __name__ == '__main__':

    clientsData = IOhandler.loadcsv('clients.csv')
    teammatesData = IOhandler.loadcsv('teammates.csv')

    client.initialiseClients(clientsData)
    client.totalWork = client.totalwork()
    client.sortClients()


    teammate.initialiseTeammates(teammatesData)


    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

