import mysql.connector
from getpass import getpass
import csv
import os
from datetime import datetime

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

def opendb(passWord):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password= passWord ,
    database="covidProj"
    )

    mycursor = mydb.cursor()

    return mydb, mycursor

def createTables(mydb, mycursor):
    mycursor.execute("CREATE TABLE counties (FIPS INT, State VARCHAR(255), County VARCHAR(255), ReportDate DATE, Cases FLOAT, IR FLOAT, Vaccinations INT, VR FLOAT)")
    mycursor.execute("CREATE TABLE states (FIPS INT, State VARCHAR(255), ReportDate DATE, Cases FLOAT, IR FLOAT, Vaccinations INT, VR FLOAT)")
    mydb.commit()

def populateCounties(passWord):
    mydb, mycursor = opendb(passWord)
    with open('./Counties.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            line = row
            fips = row[0]
            state = row[1]
            county = row[2]
            reportdate = row[3]
            cases = row[4]
            ir = row[5]
            vac = row[6]
            vr = row[7]

            if cases == "NULL":
                cases = None
            if ir == "NULL":
                ir = None
            if vac == "NULL":
                vac = None
            if vr == "NULL":
                vr = None
            print(line)
            sql = "INSERT INTO counties (FIPS, State, County, ReportDate, Cases, IR, Vaccinations, VR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            val = (fips, state, county, reportdate, cases, ir, vac, vr)
            mycursor.execute(sql, val)
            mydb.commit()

    print("Finished populating counties")
    mydb.close()

def populateStates(passWord):
    mydb, mycursor = opendb(passWord)
    with open('./States.csv', 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            line = row
            fips = row[0]
            state = row[1]
            reportdate = row[2]
            cases = row[3]
            ir = row[4]
            vac = row[5]
            vr = row[6]

            if cases == "NULL":
                cases = None
            if ir == "NULL":
                ir = None
            if vac == "NULL":
                vac = None
            if vr == "NULL":
                vr = None
            
            sql = "INSERT INTO states (FIPS, State, ReportDate, Cases, IR, Vaccinations, VR) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (fips, state, reportdate, cases, ir, vac, vr)
            mycursor.execute(sql, val)
            mydb.commit()

    print("Finished populating states")
    mydb.close()        


if __name__ == '__main__':
    print("Initialize a database in mysql")
    passWord = getCred()
    mydb, mycursor = opendb(passWord)
    createTables(mydb, mycursor)
    mydb.close()

    print("Successfully able to connect to localhost mysql")
    populateCounties(passWord)
    populateStates(passWord)