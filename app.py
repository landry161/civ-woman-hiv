from flask import Flask, flash, render_template,request,redirect,url_for,make_response
import csv
import mysql.connector
import pandas as pd
import pdb

#flask --app app.py --debug run

app = Flask(__name__)
mydb = mysql.connector.connect(host="localhost",user="root",password="",database="civdashboard")

@app.route("/")
def home():
	#return "<h1>Bienvenue sur notre page chers ami.es</h1>"
	#loadAndInsertIntoDB()
	years=getDistinctYear()
	country=getDistinctCountry()
	return render_template("index.html",years=years,countries=country)

def loadAndInsertIntoDB():
	print("Insert into DataBase")
	with open("couverture.csv","r") as file:
		fileReader=csv.reader(file,delimiter=",")
		header=next(fileReader)
		for row in fileReader:
			print(row[0])
			insertValue(row[0],row[1],row[2])
		pdb.set_trace()

	csvFile=pd.read_csv("couverture.csv")
	pdb.set_trace()

#Insertion dans la base de données
def insertValue(pays,annee,pourcentage):
	cursorDB=mydb.cursor()
	mySQL="""INSERT INTO civ(pays,annee,pourcentage) VALUES (%s,%s,%s)"""
	values=(pays,annee,pourcentage)
	cursorDB.execute(mySQL,values)
	mydb.commit()
	executeRows=cursorDB.rowcount

def getDistinctYear():
	cursorDB=mydb.cursor()
	finalArray=[]
	mySQL="""SELECT DISTINCT(annee) from civ order by annee ASC"""
	cursorDB.execute(mySQL)
	results=cursorDB.fetchall()
	for y in results:
		finalArray.append(y[0])
	return finalArray

def getDistinctCountry():
	cursorDB=mydb.cursor()
	finalCountry=[]
	mySQL="""SELECT DISTINCT(pays) from civ order by pays ASC"""
	cursorDB.execute(mySQL)
	results=cursorDB.fetchall()
	for y in results:
		finalCountry.append(y[0])
	return finalCountry

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)