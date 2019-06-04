#load clients.csv and teammates csv
import client
import teammate


def loadcsv(filename):
    data = []
    with open('./input/'+filename, 'r') as f:
        # create a list of rows in the CSV file
        rows = f.readlines()

        # strip white-space and newlines
        rows = list(map(lambda x: x.strip(), rows))

        for row in rows:
            # further split each row into columns assuming delimiter is comma
            row = row.split(',')

            # append to data-frame our new row-object with columns
            data.append(row)
    return data

def writeSchedule():
    #write a report to txt
    report = open("./output/monthly_report.txt", "w")
    workLeft = client.totalwork()

    report.write(
        'The total number of hours required by clients are: ' + str(client.totalWork) + '\n'
        'The number of hours left is: ' + str(workLeft) + '\n'
    )

    if workLeft == 0:
        report.write('congrats! all work can be done on time this month!')

    else:
        remainClients = client.getSortedClients()
        todoStatement = ''
        for rc in remainClients:
            if rc.getHour() > 0:
                todoStatement = todoStatement + rc.getName() + ' ' + str(rc.getHour()) +'\n'

        report.write('below is the works not finished, displayed in client name and hours left' + '\n' +todoStatement)

    report.close()









    f = open('./output/teammate_schedule.csv', 'w')

    teammateList = teammate.teammates
    outputNames = ''

    for t in teammateList:
        outputNames = outputNames + t.getName() + ', '


    f.write('workDay\Teammate, ' + outputNames + '\n')  # Give your csv text here.
    ## Python will convert \n to os.linesep




    for workDay in range(1, 21):
        outputWork = str(workDay) + ', '
        for t in teammateList:
            taskOnDay = t.getTasksbyDay(workDay)
            taskOut = ''


            if len(taskOnDay) == 1:
                for task in taskOnDay:
                    taskOut = taskOut + task['client'] + ' ' +str(task['hour']) + ', '
                outputWork = outputWork + taskOut

            if len(taskOnDay) > 1:
                for task in taskOnDay:
                    taskOut = taskOut + '(' +task['client'] + ' ' + str(task['hour']) + ') '

                outputWork = outputWork + taskOut + ', '


            if len(taskOnDay) == 0:
                outputWork = outputWork + ', '



        f.write(outputWork + '\n')
    f.close()



