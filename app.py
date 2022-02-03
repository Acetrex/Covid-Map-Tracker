from flask import Flask
from flask import render_template, request, redirect, url_for, flash
import mysql.connector
import os
import matplotlib.pyplot as plt
STATES = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]

STATEFIPS = {
"Alabama" : ['1', [32.3182, -86.9023], 6],
"Alaska" : ['2', [64.2008, -149.4937], 4] ,
"Arizona": ['4', [34.0489, -111.0937], 6],
"Arkansas": ['5', [35.2010, -91.8318], 7],
"California": ['6', [36.7783, -119.4179], 5],
"Colorado": ['8', [39.5501, -105.7821], 6],
"Connecticut": ["9", [41.6032, -73.0877], 8],
"Delaware": ["10", [38.9108, -75.5277], 8],
"Florida": ["12", [27.6648, -81.5158], 6],
"Georgia": ["13", [32.1656, -82.9001], 6],
"Hawaii": ["15", [19.8968, -155.5828], 6],
"Idaho": ["16", [44.0682, -114.7420], 5],
"Illinois": ["17", [40.6331, -89.3985], 6],
"Indiana": ["18", [40.2672, -86.1349], 6],
"Iowa": ["19", [41.8780, -93.0977], 6],
"Kansas": ["20", [39.0119, -98.4842], 6], 
"Kentucky": ["21", [37.8393, -84.2700], 6],
"Louisiana": ["22", [30.9843, -91.9623], 6], 
"Maine": ["23", [45.2538, -69.4455], 6],
"Maryland": ["24", [39.0458, -76.6413], 7], 
"Massachusetts": ["25", [42.4072, -71.3824], 7],
"Michigan": ["26", [44.3148, -85.6024], 6],
"Minnesota": ["27", [46.7296, -94.6859], 6], 
"Mississippi": ["28", [32.3547, -89.3985], 6],
"Missouri": ["29", [37.9643, -91.8318], 6],
"Montana": ["30", [46.8797, -110.3626], 6],
"Nebraska": ["31", [41.4925, -99.9018], 6],
"Nevada": ["32", [38.8026, -116.4194], 6],
"New Hampshire": ["33", [43.1939, -71.5724], 7],
"New Jersey": ["34", [40.0583, -74.4057], 7],
"New Mexico": ["35", [34.5199, -105.8701], 6],
"New York": ["36", [40.7128, -74.0060], 6],
"North Carolina": ["37", [35.7596, -79.0193], 6],
"North Dakota": ["38", [47.5515, -101.0020], 6],
"Ohio": ["39", [40.4173, -82.9071], 7], 
"Oklahoma": ["40", [35.0078, -97.0929], 6],
"Oregon": ["41", [43.8041, -120.5542], 6],
"Pennsylvania": ["42", [41.2033, -77.1945], 7],
"Rhode Island": ["44", [41.5801, -71.4774], 8],
"South Carolina": ["45", [33.8361, -81.1637], 6],
"South Dakota": ["46", [43.9695, -99.9018], 6],
"Tennessee": ["47", [35.5175, -86.5804], 6],
"Texas": ["48", [31.9686, -99.9018], 5],
"Utah": ["49", [39.3210, -111.0937], 6],
"Vermont": ["50", [44.5588, -72.5778], 7],
"Virginia": ["51", [37.4316, -78.6569], 6],
"Washington": ["53", [47.7511, -120.7401], 6],
"West Virginia": ["54", [38.5976, -80.4549], 7],
"Wisconsin": ["55", [43.7844, -88.7879], 6],
"Wyoming": ["56", [43.0760, -107.2903], 6]
}

DATES = ["2021-08-22", "2021-08-29", "2021-09-01", "2021-09-08",
         "2021-09-15", "2021-09-22", "2021-09-29", "2021-10-01", "2021-10-08",
         "2021-10-15", "2021-10-22", "2021-10-29", "2021-11-01", "2021-11-08",
         "2021-11-15", "2021-11-22", "2021-11-29", "2021-12-01"]
MAPDATA = []
SELECTEDSTATE = ""
BOOLSTATE = False
USCASES = ""
USIR = ""
USVAC = ""
USVR = ""
USDATA = []
ALLUSDATA = []

MAPUSE = "map"
CURRCASES = ""
CURRIR = ""
CURRVR = ""
REGIONS = STATES
CURRREGION = "USA"
CURRSTATE = ""
STARTED = False

COUNTIESDICT = {}


app = Flask(__name__)
def opendb():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="covidproj"
    )

    mycursor = mydb.cursor()

    return mydb, mycursor

def readcounties():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="coviddata"
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT FIPS_ID, `10/29/2021_Cases`, `10/29/2021_IR` FROM counties WHERE State_Name='Maryland';")
    
        # # fetch all the matching rows
        result = mycursor.fetchall()


        mydb.close()
        print(result)
        for i in range(len(result)):
            result[i] = list(result[i])
        print(result)
        return result
    except:
        return None

def getStateStats(state):
    try:
        mydb, mycursor = opendb()
        mycursor.execute("SELECT * FROM states WHERE State = %s and ReportDate = DATE(%s)", (state, "2021-12-01"))

        result = mycursor.fetchall()
        mydb.close()
        return result
    except:
        return None

def getCountyStats(county):
    try:
        mydb, mycursor = opendb()
        mycursor.execute("SELECT * FROM counties WHERE County = %s and ReportDate = DATE(%s)", (county, "2021-12-01"))

        result = mycursor.fetchall()
        mydb.close()
        return result
    except:
        return None

def getStateCounties(state):
    print("entered function")
    try:
        global COUNTIESDICT
        mydb, mycursor = opendb()
        query = "SELECT County FROM counties WHERE State = \'" + str(state) + "\'"
        #mycursor.execute("SELECT County FROM counties WHERE State = %s", state)
        mycursor.execute(query)

        result = mycursor.fetchall()
        result = set(result)
        counties = []
        countiesDict = {}
        for i in result:
            #print(str(i[0]))
            tmp = "".join(i[0].split("\'"))
            tmp2 = " and ".join(tmp.split("&"))

            counties.append(tmp2)
            countiesDict[tmp2] = i[0]
    
        mydb.close()
        COUNTIESDICT = countiesDict
        #print(result)
        return counties
    except:
        return None

def getRegionData(state):
    try:
        mydb, mycursor = opendb()
        mycursor.execute("SELECT FIPS, Cases, IR, Vaccinations, VR FROM counties WHERE State = %s and ReportDate = DATE(%s)", (state, "2021-12-01"))

        result = mycursor.fetchall()
        mydb.close()

        for i in range(len(result)):
            result[i] = list(result[i])
            if result[i][1] == None:
                result[i][1] = 0
            if result[i][2] == None:
                result[i][2] = 0
            if result[i][3] == None:
                result[i][3] = 0
            if result[i][4] == None:
                result[i][4] = 0

        return result
    except:
        return None

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

def createPlot(dates, cases):
    title = CURRREGION + " Cases"
    x1 = dates
    y1 = cases

    plt.plot(x1, y1)
    plt.xlabel('Date')
    plt.xticks(rotation = 80)
    # naming the y axis
    plt.ylabel('Total number of new cases per 100k within last 7 days')
    # giving a title to my graph
    plt.title(title, fontname="Times New Roman", size=28, fontweight="bold")

    plt.grid()
    
    plt.savefig('./static/plot.png', bbox_inches = "tight")
    plt.close()

def getStatePlotData(state):
    try:
        mydb, mycursor = opendb()
        mycursor.execute("SELECT ReportDate, Cases FROM states WHERE State = %s ORDER BY ReportDate", (state,))

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
        return None, None

def getCountyPlotData(state, county):
    try:
        mydb, mycursor = opendb()
        mycursor.execute("SELECT ReportDate, Cases FROM counties WHERE State = %s and County = %s ORDER BY ReportDate", (state, county))

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
        return None, None

def getUSPlotData():
    try:
        mydb, mycursor = opendb()
        cases = []
        for date in DATES:
            mycursor.execute("SELECT Cases FROM states WHERE ReportDate = DATE(%s)", (date,))

            result = mycursor.fetchall()

            tmp = 0
            for i in range(len(result)):
                result[i] = list(result[i])
                if result[i][0] == None:
                    result[i][0] = 0
                tmp += result[i][0]
            cases.append(tmp)
        mydb.close()
        return cases

    except:
        return None





@app.route('/', methods=['GET', 'POST'])
def home_page():
    global MAPUSE, CURRCASES, CURRIR, CURRVR, REGIONS, CURRREGION, STARTED
    if request.method == "POST":
        print("test")
        if request.form.get("Submit") == "Submit":
            print("entered")
            id = request.form["selection"]
            if id in STATES:
                global MAPUSE, CURRREGION, CURRSTATE

                STARTED = True

                stats = getStateStats(id)[0]
                regions = getStateCounties(id)
                regions.sort()
                

                MAPUSE = "states"
                CURRCASES = str(stats[3])
                CURRIR = str(stats[4])
                CURRVR = str(stats[6])
                REGIONS = regions
                CURRREGION = id
                CURRSTATE = id
                dates, cases = getStatePlotData(id)
                print("------------------TESTING---------------------")
                print(dates)
                print(cases)
                createPlot(DATES, cases)
                
                print(type(regions))
                #print(stats[1])
                global MAPDATA, SELECTEDSTATE
                SELECTEDSTATE = []
                SELECTEDSTATE = STATEFIPS[id]
                if id not in SELECTEDSTATE:
                    SELECTEDSTATE.append(id)
                #print("Reading counties function:\n", readcounties())
                MAPDATA = getRegionData(id)
                return render_template('index.html', state = "states", cases = str(stats[3]), ir=str(stats[4]), vr = str(stats[6]), regions = regions, regionSelected = id) 

            elif id in REGIONS:
                STARTED = True
                print("COUnty selected")
                tmp = COUNTIESDICT[id]
                stats = getCountyStats(tmp)[0]
                print(stats)

                MAPUSE = "states"
                CURRCASES = str(stats[4])
                CURRIR = str(stats[5])
                CURRVR = str(stats[7])
                CURRREGION = id

                dates, cases = getCountyPlotData(CURRSTATE, tmp)
                createPlot(DATES, cases)

                return render_template('index.html', state = MAPUSE, cases = CURRCASES, ir = CURRIR, vr = CURRVR, regions = REGIONS, regionSelected = CURRREGION)

        elif request.form.get("Home") == "Home":
            print("***********************Home button pressed")
            MAPUSE = "map"
            CURRCASES = str(USCASES)
            CURRIR = str(USIR)
            CURRVR = str(USVR)
            REGIONS = STATES
            CURRREGION = "USA"
            STARTED = True
            print("CHeching if going through createPlot")
            createPlot(DATES, ALLUSDATA)
            print("Passed create plot")

            return render_template('index.html', state = 'map', cases = str(USCASES), ir=str(USIR), vr = str(USVR), regions = STATES, regionSelected = "USA")

    return render_template('index.html', state = MAPUSE, cases = CURRCASES, ir=CURRIR, vr = CURRVR, regions = REGIONS, regionSelected = CURRREGION)

@app.route('/map')
def map():

    return render_template('map.html', datacounties = USDATA)


@app.route('/states')
def states():
    # print("Get Region Data function:\n", MAPDATA)
    print("------------------------------------------")
    print('-------------------------------------------')
    print('-----------------------------------------------')
    print(SELECTEDSTATE)
    selection = SELECTEDSTATE[0]
    view = SELECTEDSTATE[1]
    zoom = SELECTEDSTATE[2]
    jsonFile = "/static/" + str("".join(str(SELECTEDSTATE[3]).split(" "))) + "Counties.js"
    #jsonFile = "/static/Counties.js"
    return render_template('states.html', datacounties = MAPDATA, selectedState = selection, jsonFile = jsonFile, view = view, zoom = zoom)

@app.route('/404')
def error_Page():

    return render_template('404.html')

@app.errorhandler(404)
def page_not_found(e):

    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/FAQ')
def FAQ_Page():

    return render_template('FAQ.html')
def setConst():
    try:
        mydb, mycursor = opendb()
        mycursor.execute("SELECT FIPS, Cases, IR, Vaccinations, VR FROM states WHERE ReportDate = DATE(\'2021-12-01\')")

        result = mycursor.fetchall()
        mydb.close()

        #print(result)
        global USCASES, USIR, USVAC, USVR, CURRCASES, CURRIR, CURRVR
        cases = 0
        ir = 0
        vac = 0
        vr = 0
        for i in range(len(result)):
            result[i] = list(result[i])
            if result[i][1] == None:
                result[i][1] = 0
            else:
                cases += result[i][1]
            if result[i][2] == None:
                result[i][2] = 0
            else:
                ir += result[i][2]
            if result[i][3] == None:
                result[i][3] = 0
            else:
                vac += result[i][3]
            if result[i][4] == None:
                result[i][4] = 0
            else:
                vr += result[i][4]
        
        USCASES = cases
        USIR = int(ir / 50)
        USVAC = vac
        USVR = int(vr / 50)
        CURRCASES = str(USCASES)
        CURRIR = str(USIR)
        CURRVR = str(USVR)

        return result
    except:
        return None

if __name__ == '__main__':
    print(os.getcwd())
    USDATA = setConst()
    ALLUSDATA = getUSPlotData()
    createPlot(DATES, ALLUSDATA)
    print(USDATA)
    print(USCASES)
    print(USIR)
    print(USVAC)
    print(USVR)
    app.run(debug=True, host='0.0.0.0')
