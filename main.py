import client
import IOhandler
import teammate



def main():
    print('Welcome to Weboptimizers Workscheduler')
    print('-----------------------------------------------------------')
    print('reading client file....')

    clientsData = IOhandler.loadcsv('clients.csv')
    print(clientsData)
    client.initialiseClients(clientsData)

    client.totalWork = client.totalwork()


    # print(len(client.clients))
    print(client.totalwork())

    client.sortClients()

    print('reading teammate file...')
    teammatesData = IOhandler.loadcsv('teammates.csv')
    teammate.initialiseTeammates(teammatesData)


    #fill the teammate schedule with tasks!

    teammate.fillschedule(client.getSortedClients())
    teammate.printTasks()
    IOhandler.writeSchedule()



if __name__ == "__main__":
    main()