import mysql.connector
import matplotlib.pyplot as plt
STATES = {
"Alabama" : '1',
"Alaska" : '2' ,
"Arizona": '4' ,
"Arkansas": '5',
"California": '6',
"Colorado": '8',
"Connecticut": "9",
"Delaware": "10",
"Florida": "12",
"Georgia": "13",
"Hawaii": "15",
"Idaho": "16",
"Illinois": "17",
"Indiana": "18",
"Iowa": "19",
"Kansas": "20",
"Kentucky": "21",
"Louisiana": "22",
"Maine": "23",
"Maryland": "24",
"Massachusetts": "25",
"Michigan": "26",
"Minnesota": "27",
"Mississippi": "28",
"Missouri": "29",
"Montana": "30",
"Nebraska": "31",
"Nevada": "32",
"New Hampshire": "33",
"New Jersey": "34",
"New Mexico": "35",
"New York": "36",
"North Carolina": "37",
"North Dakota": "38",
"Ohio": "39",
"Oklahoma": "40",
"Oregon": "41",
"Pennsylvania": "42",
"Rhode Island": "44",
"South Carolina": "45",
"South Dakota": "46",
"Tennessee": "47",
"Texas": "48",
"Utah": "49",
"Vermont": "50",
"Virginia": "51",
"Washington": "53",
"West Virginia": "54",
"Wisconsin": "55",
"Wyoming": "56"
}
def opendb():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sootball11",
    database="covidproj"
    )

    mycursor = mydb.cursor()

    return mydb, mycursor

def getData():
    try:
        mydb, mycursor = opendb()
        mycursor.execute("SELECT ReportDate, Cases FROM counties WHERE State = %s and County = %s ORDER BY ReportDate", ("Maryland", "Harford County"))

        result = mycursor.fetchall()
        mydb.close()

        dates = []
        cases = []
        for i in range(len(result)):
            result[i] = list(result[i])
            dates.append(result[i][0])
            if result[i][1] == None:
                result[i][1] = 0
        
            cases.append(result[i][1])

        return dates, cases
    except:
        return None

def getDates():
    try:
        mydb, mycursor = opendb()
        mycursor.execute("SELECT ReportDate FROM counties WHERE state = %s and county = %sORDER BY ReportDate",("Maryland", "Harford County"))

        result = mycursor.fetchall()
        mydb.close()
        for i in range(len(result)):
            result[i] = str(list(result[i]))
        return result
    except:
        return None  
def createStateTable(mydb, mycursor):
    mycursor.execute("CREATE TABLE states (FIPS INT, State VARCHAR(255), ReportDate DATE, Cases FLOAT, IR FLOAT, Vaccinations INT, VR FLOAT)")
    mydb.commit()

def populateStates(mydb, mycursor, dates):
    for state in STATES:
        tmpState = state
        for currDate in dates:
            mycursor.execute("SELECT * FROM counties WHERE State = %s and ReportDate = DATE(%s)", (tmpState, currDate))
            result = mycursor.fetchall()

            totals = [[], [], [], []]
            for entry in result:
                if entry[4] != None:
                    totals[0].append(entry[4])
                if entry[5] != None:
                    totals[1].append(entry[5])
                if entry[6] != None:
                    totals[2].append(entry[6])
                if entry[7] != None:
                    totals[3].append(entry[7])

            if len(totals[0]) > 0:
                cases = sum(totals[0])
            else:
                cases = None
            if len(totals[1]) > 0:
                inf_rate = sum(totals[1]) / len(totals[1])
            else:
                inf_rate = None
            if len(totals[2]) > 0:
                vac_num = sum(totals[2])
            else:
                vac_num = None
            if len(totals[3]) > 0:
                vac_rate = sum(totals[3]) / len(totals[3])
            else:
                vac_rate = None

            sql = "INSERT INTO states (FIPS, State, ReportDate, Cases, IR, Vaccinations, VR) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (STATES[state], tmpState, currDate, cases, inf_rate, vac_num, vac_rate)
            mycursor.execute(sql, val)
            mydb.commit()

def createPlot(x, y, started):
    # if started:
    #     plt.clf()
    title = "Cases"
    x1 = x
    y1 = y

    plt.plot(x1, y1)
    plt.xlabel('Date')
    plt.xticks(rotation = 45)
    # naming the y axis
    plt.ylabel('Total number of new cases per 100k within last 7 days')
    # giving a title to my graph
    plt.title(title, fontname="Times New Roman", size=28, fontweight="bold")

    plt.grid()

    plt.savefig('./static/plot.png', bbox_inches = "tight")
    plt.clf()

def enterData():
    y = []
    x = []
    ui = input("Enter x num: or q for quit\n")
    while(ui != 'q'):
        y.append(int(ui))
        ui = input("Enter x num: or q for quit\n")

    for i in range(len(y)):
        x.append(i)

    return x, y

ui = input("Keep going or q")
i=0
while(ui != 'q'):
    x, y = enterData()
    if i == 0:
        createPlot(x,y,i)
        i+=1
    else:
        createPlot(x,y,i)
    ui = input("Keep going or q")

    
    

# dates = ["2021-08-22", "2021-08-29", "2021-09-01", "2021-09-08",
#          "2021-09-15", "2021-09-22", "2021-09-29", "2021-10-01", "2021-10-08",
#          "2021-10-15", "2021-10-22", "2021-10-29", "2021-11-01", "2021-11-08",
#          "2021-11-15", "2021-11-22", "2021-11-29", "2021-12-01"]
# mydb, mycursor = opendb()
# createStateTable(mydb, mycursor)
# populateStates(mydb, mycursor, dates)

#dates = [(datetime.date(2021, 8, 22),), (datetime.date(2021, 8, 29),), (datetime.date(2021, 9, 1),), (datetime.date(2021, 9, 8),), (datetime.date(2021, 9, 15),), (datetime.date(2021, 9, 22),), (datetime.date(2021, 9, 29),), (datetime.date(2021, 10, 1),), (datetime.date(2021, 10, 8),), (datetime.date(2021, 10, 15),), (datetime.date(2021, 10, 22),), (datetime.date(2021, 10, 29),), (datetime.date(2021, 11, 1),), (datetime.date(2021, 11, 8),), (datetime.date(2021, 11, 15),), (datetime.date(2021, 11, 22),), (datetime.date(2021, 11, 29),), (datetime.date(2021, 12, 1),)]
#print(dates)
# dates, cases= getData()
# # print(result)
# # print(len(result))

# x1 = dates
# y1 = cases

# plt.plot(x1, y1)

# plt.xlabel('Date')
# plt.xticks(rotation = 45)
# # naming the y axis
# plt.ylabel('Total number of new cases per 100k within last 7 days')
# # giving a title to my graph
# plt.title('Harford County Cases', fontname="Times New Roman", size=28, fontweight="bold")

# plt.grid()
 
# # function to show the plot
# #plt.show()
# plt.savefig('plot.png', bbox_inches = "tight")

# # x-coordinates of left sides of bars
# left = [1, 2, 3, 4, 5]
 
# # heights of bars
# height = [10, 24, 36, 40, 5]
 
# # labels for bars
# tick_label = ['one', 'two', 'three', 'four', 'five']
 
# # plotting a bar chart
# plt.bar(left, height, tick_label = tick_label,
#         width = 0.8, color = ['red', 'green'])
 
# # naming the x-axis
# plt.xlabel('x - axis')
# # naming the y-axis
# plt.ylabel('y - axis')
# # plot title
# plt.title('My bar chart!')
 
# # function to show the plot
# plt.show()

# def opendb():
#     mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Sootball11",
#     database="coviddata"
#     )

#     mycursor = mydb.cursor()

#     return mydb, mycursor

# def readcounties():
#     try:
#         mydb, mycursor = opendb()
#         mycursor.execute("SELECT FIPS_ID, `10/29/2021_Cases`, `10/29/2021_IR` FROM counties WHERE State_Name='Maryland';")
    
#         # # fetch all the matching rows
#         result = mycursor.fetchall()


#         mydb.close()

#         for i in range(len(result)):
#             result[i] = list(result[i])
        
#         return result
#     except:
#         return None

# print(readcounties())
