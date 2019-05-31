class Client:

    def __init__(self, name, hour):
        self.name = name
        self.hour = hour
        self.done = False


    def getName(self):
        return self.name

    def getHour(self):
        return self.hour

    def setHour(self, hour):
        self.hour = hour

    def setDone(self):
        self.done = True

    def getDoneStatus(self):
        return self.done


clients = []
sortedClients = []
totalWork = 0

def initialiseClients(clientsData):
    #clientsData = [['google', ' 120'], ['apple', ' 170'], ['facebook', ' 50'], ['microsoft', ' 70']]
    for c in clientsData:
        clients.append(Client(c[0],int(c[1])))


def totalwork():
    sum = 0
    for client in clients:
        sum = sum + client.getHour()
    return sum

def printAllClients():
    for client in clients:
        print(client.getName(), client.getHour())


def sortClients():
    for client in reversed(sorted(clients, key=lambda x: x.hour)):
        sortedClients.append(client)


    # for client in sortedClients:
    #     print(client.getName())
    #     print(client.getHour())

def getSortedClients():
    return sortedClients

def getAllClients():
    return clients