import mysql.connector
from getpass import getpass
import csv
import os
from datetime import datetime


DATES_YEAR = '2021'
DATES_MONTH = '08'
DATES_DAYS = ['01', '08', '15', '22', '29']
STATES = {
    'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut',
    'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'MA': 'Massachusetts',
    'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota', 'MO': 'Missouri', 'MS': 'Mississippi',
    'MT': 'Montana', 'NC': 'North Carolina', 'ND': 'North Dakota', 'NE': 'Nebraska', 'NH': 'New Hampshire', 
    'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VT': 'Vermont',
    'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'
}

def getCred():
    while(True):
        print("Enter root password:")
        try:
            passWord = getpass()
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password = passWord,
            )
            #mydb.close()
            mycursor = mydb.cursor()
            mycursor.execute("CREATE DATABASE covidProj")
            mydb.close()
            return passWord
        except:
            print("Invalid password")

def connect(myPassword):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password = myPassword,
        database = "covidProj"
    )

    mycursor = mydb.cursor()

    return mydb, mycursor

def createTables(mydb, mycursor):
    mycursor.execute("CREATE TABLE counties (FIPS INT, State VARCHAR(255), County VARCHAR(255), ReportDate DATE, Cases FLOAT, IR FLOAT, Vaccinations INT, VR FLOAT)")
    mycursor.execute("CREATE TABLE states (FIPS INT, State VARCHAR(255), ReportDate DATE, Cases FLOAT, IR FLOAT, Vaccinations INT, VR FLOAT)")
    mydb.commit()

def populateCountiesCases(mydb, mycursor):
    dates = []
    #countyCasesFile = input("What is the path of the file?\n")
    #while (not os.path.isfile(countyCasesFile)):
    #    print("Invalid file")
    #    countyCasesFile = input("What is the path of the file?\n")
    countyCasesFile = r'C:\Users\mrome\OneDrive\Documents\FA 2021\CMSC447\covid_proj\venv\Cases_Filtered.csv'
    print(countyCasesFile)

    nullValues = [None, "0", "suppressed", ""]

    with open(countyCasesFile, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            line = row
            state_name = line[0]
            county_name = line[1]
            fips = line[2]
            report_date = line[0].split("/")
            #YYYY-MM-DD
            tmp_date = line[3].split("/")
            #print(type(report_date))
            #report_date = report_date[2] + "-" + report_date[0] + "-" + report_date[1]
            cases = "".join(line[4].split(","))
            infection_rate = line[5]

            if len(tmp_date[0]) == 1:
                tmp_date[0] = "0" + tmp_date[0]
            if len(tmp_date[1]) == 1:
                tmp_date[1] = "0" + tmp_date[1]
            report_date = tmp_date[2] + "-" + tmp_date[0] + "-" + tmp_date[1]

            if cases in nullValues:
                    cases = None
            if infection_rate in nullValues:
                infection_rate = None

            #checking year
            #print(tmp_date)
            if tmp_date[2] >= DATES_YEAR:
                if tmp_date[0] >= DATES_MONTH:
                    if tmp_date[1] in DATES_DAYS:
                        #print(state_name)
                        if state_name in STATES.values():
                            #print("entered")
                            sql = "INSERT INTO counties (FIPS, State, County, ReportDate, Cases, IR, Vaccinations, VR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                            val = (fips, state_name, county_name, report_date, cases, infection_rate, None, None)
                            mycursor.execute(sql, val)
                            mydb.commit()
                            if report_date not in dates:
                                dates.append(report_date)

    return dates

def populateCountiesVac(mydb, mycursor, dates):
    dates = []
    #countyVacFile = input("What is the path of the file?\n")
    #while (not os.path.isfile(countyVacFile)):
        #print("Invalid file")
        #countyVacFile = input("What is the path of the file?\n")

    countyVacFile = r'C:\Users\mrome\OneDrive\Documents\FA 2021\CMSC447\covid_proj\venv\Vaccines_Filtered.csv'
    nullValues = [None, "0", "suppressed", "", "UNK", "Unknown"]

    with open(countyVacFile, 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            line = row
            report_date = line[0].split("/")
            fips = line[1]
            county_name = line[2]
            state_name = line[3]
            vac_num = line[5]
            vac_rate = line[4]
            tmp_date = report_date
            if fips not in nullValues and county_name not in nullValues and state_name not in nullValues:
                if len(tmp_date[0]) == 1:
                    tmp_date[0] = "0" + tmp_date[0]
                if len(tmp_date[1]) == 1:
                    tmp_date[1] = "0" + tmp_date[1]
                report_date = tmp_date[2] + "-" + tmp_date[0] + "-" + tmp_date[1]
                

                if vac_num in nullValues:
                    vac_num = None
                if vac_rate in nullValues:
                    vac_rate = None
                
                if tmp_date[2] >= DATES_YEAR:
                    if tmp_date[0] >= DATES_MONTH:
                        if tmp_date[1] in DATES_DAYS:
                            if state_name in STATES:
                                state_name = STATES[state_name]

                                mycursor.execute("SELECT * FROM counties WHERE FIPS = %s and ReportDate = DATE(%s)", (fips, report_date))

                                result = mycursor.fetchall()

                                if len(result) > 0:
                                    sql = "UPDATE counties SET Vaccinations = %s WHERE FIPS = %s and ReportDate = DATE(%s)"
                                    val = (vac_num, fips, report_date)
                                    mycursor.execute(sql, val)

                                    sql = "UPDATE counties SET VR = %s WHERE FIPS = %s and ReportDate = DATE(%s)"
                                    val = (vac_rate, fips, report_date)
                                    mycursor.execute(sql, val)

                                else:
                                    sql = "INSERT INTO counties (FIPS, State, County, ReportDate, Cases, IR, Vaccinations, VR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                                    val = (fips, state_name, county_name, report_date, None, None, vac_num, vac_rate)
                                    mycursor.execute(sql, val)

                                mydb.commit()

                                if report_date not in dates:
                                    dates.append(report_date)
                        

    return dates


def populateStates(mydb, mycursor, dates):
    i = 1
    for state in STATES:
        tmpState = STATES[state]
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
            val = (i, tmpState, currDate, cases, inf_rate, vac_num, vac_rate)
            mycursor.execute(sql, val)
            mydb.commit()

        i += 1






if __name__ == "__main__":
    passWord = getCred()
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    mydb, mycursor = connect(passWord)

    createTables(mydb, mycursor)
    dates = populateCountiesCases(mydb, mycursor)
    dates = populateCountiesVac(mydb, mycursor, dates)
    populateStates(mydb, mycursor, dates)
    print(dates)
    end = datetime.now()
    current_time = end.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    diff = end - now
    print("Difference", diff)

    #print("Maryland" in STATES.values())



    #mycursor.execute("SELECT ReportDate FROM counties")
    #result = list(set(mycursor.fetchall()))
    #for i in range(len(result)):
    #    result[i] = str(result[i][0])
    #print(result)

    #countyVacFile = r'C:\Users\mrome\OneDrive\Documents\FA 2021\CMSC447\covid_proj\venv\Cases_Filtered.csv'
    #print(os.path.isfile(countyVacFile))
    #mycursor.execute("CREATE TABLE states (FIPS INT, State VARCHAR(255), ReportDate DATE, Cases FLOAT, IR FLOAT, Vaccinations INT, VR FLOAT)")
    #mydb.commit()
    #populateStates(mydb, mycursor, result)
    #createTables(mydb, mycursor)
    #dates = populateCountiesCases(mydb, mycursor)
    #dates = populateCountiesVac(mydb, mycursor, [])
    #print(dates)
    #tmp = "24005"
    #sql = "SELECT * from counties where reportdate = STR_TO_DATE('22, 08, 2021', '%d, %m, %Y') and fips = 24005"
    #sql = "select * from counties where reportdate = STR_TO_DATE('22, 08, 2021', '%d, %m, %Y')"
    #sql = "show columns from counties"
    #sql = "select * from counties where reportdate = DATE('2021-08-22')"
    #val = (tmp)
    #fips = "24005"
    #report_date = "2021-08-22"
    #mycursor.execute("SELECT * FROM counties WHERE FIPS = %s and ReportDate = DATE(%s)", (fips, report_date))

    #print(mycursor.fetchall())
    mydb.close()