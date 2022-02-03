import mysql.connector
from getpass import getpass
import csv

def getCred():
    while(True):
        print("Enter root password:")
        try:
            passWord = getpass()
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password = passWord,
                database = "coviddata"
            )
            #mydb.close()
            mycursor = mydb.cursor()
            return mydb, mycursor
        except:
            print("Invalid password")


def populateDatabase(mydb, mycursor):
    nullValues = [None, "0", "suppressed", ""]
    i = 0

    with open("County_Covid_Data.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            if i >= 0:
                line = row
                state_name = line[0]
                county_name = line[1]
                fips = line[2]
                report_date = line[3]
                cases = "".join(line[4].split(","))
                infection_rate = line[5]


                if cases in nullValues:
                    cases = None
                if infection_rate in nullValues:
                    infection_rate = None

                mycursor.execute("SELECT * FROM counties WHERE FIPS_ID = %s", (fips,))

                result = mycursor.fetchall()

                if len(result) > 0:
                    mycursor.execute("SHOW COLUMNS FROM counties LIKE %s", (report_date + "_Cases",))
                    subresult = mycursor.fetchall()

                    if len(subresult) == 0:
                        report_cases = "ALTER TABLE counties ADD `" + report_date + "_Cases` FLOAT"
                        report_ir = "ALTER TABLE counties ADD `" + report_date + "_IR` FLOAT"
                        mycursor.execute(report_cases)
                        mycursor.execute(report_ir)
                        mydb.commit()
                        sql = "UPDATE counties SET `" + report_date + "_Cases` = %s WHERE FIPS_ID = %s"
                        val = (cases, fips)
                        mycursor.execute(sql, val)

                        sql = "UPDATE counties SET `" + report_date + "_IR` = %s WHERE FIPS_ID = %s"
                        val = (infection_rate, fips)
                        mycursor.execute(sql, val)
                        


                        #sql = "INSERT INTO counties (FIPS_ID, State_Name, County_Name, `" + report_date + "_Cases`, `" + report_date + "_IR`) VALUES(%s, %s, %s, %s, %s)"
                        #val = (fips, state_name, county_name, cases, infection_rate)
                        #mycursor.execute(sql, val)
                    else:
                        sql = "UPDATE counties SET `" + report_date + "_Cases` = %s WHERE FIPS_ID = %s"
                        val = (cases, fips)
                        mycursor.execute(sql, val)

                        sql = "UPDATE counties SET `" + report_date + "_IR` = %s WHERE FIPS_ID = %s"
                        val = (infection_rate, fips)
                        mycursor.execute(sql, val)
                        #sql = "INSERT INTO counties (FIPS_ID, State_Name, County_Name, `" + report_date + "_Cases`, `" + report_date + "_IR`) VALUES(%s, %s, %s, %s, %s)"
                        #val = (fips, state_name, county_name, cases, infection_rate)
                        #mycursor.execute(sql, val)

                else:
                    mycursor.execute("SHOW COLUMNS FROM counties LIKE %s", (report_date + "_Cases",))
                    subresult = mycursor.fetchall()
                    print(subresult)
                    if len(subresult) == 0:
                        report_cases = "ALTER TABLE counties ADD `" + report_date + "_Cases` FLOAT"
                        report_ir = "ALTER TABLE counties ADD `" + report_date + "_IR` FLOAT"
                        print(report_cases)
                        mycursor.execute(report_cases)
                        mycursor.execute(report_ir)
                        mydb.commit()
                        sql = "INSERT INTO counties (FIPS_ID, State_Name, County_Name, `" + report_date + "_Cases`, `" + report_date + "_IR`) VALUES(%s, %s, %s, %s, %s)"
                        val = (fips, state_name, county_name, cases, infection_rate)
                        mycursor.execute(sql, val)
                    else:
                        sql = "INSERT INTO counties (FIPS_ID, State_Name, County_Name, `" + report_date + "_Cases`, `" + report_date + "_IR`) VALUES(%s, %s, %s, %s, %s)"
                        val = (fips, state_name, county_name, cases, infection_rate)
                        print(val)
                        mycursor.execute(sql, val)

                mydb.commit()
            i += 1


def readDatabase(mydb, mycursor):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM counties")

    result = mycursor.fetchall()

    for row in result:
        print(row)

    

if __name__ == '__main__':
    print("Initialize a database in mysql")
    mydb, mycursor = getCred()
    print("Successfully able to connect to localhost mysql")
    populateDatabase(mydb, mycursor)
    readDatabase(mydb, mycursor)
    mydb.close

