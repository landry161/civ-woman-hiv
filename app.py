from flask import Flask, flash, render_template,request,redirect,url_for,make_response
import csv
import mysql.connector
import json
import pandas as pd
import pdb
import numpy as np
from decimal import *

#flask --app app.py --debug run

app = Flask(__name__)
mydb = mysql.connector.connect(host="localhost",user="root",password="",database="civdashboard")

@app.route("/")
def home():
	#return "<h1>Bienvenue sur notre page chers ami.es</h1>"
	#loadAndInsertIntoDB()
	years=getDistinctYear()
	country=getDistinctCountry()
	records=countRecords()
	return render_template("index.html",years=years,records=records,countArray=len(country),countries=country)

@app.route("/stathome",methods=["POST"])
def getStatHomeByYear():
	countries = request.form.get("tags")
	
	res=getQueryByTags(countries)
	#pdb.set_trace()
	return res
	'''
	for r in res:
		print("---Non---")
		print(r)
		print(res)
		print("Oui")
	print(countries)
	'''
	#pdb.set_trace()
	'''
	mySQL="""SELECT annee,sum(pourcentage) as total FROM civ group by annee;"""
	finalStat=[]
	mySQL="""SELECT count(*) as total FROM civ;"""
	cursorDB.execute(mySQL)
	results=cursorDB.fetchall()
	for val in results:
		finalStat.append({"year":val[0],"pourcentage":val[1]})
	return finalStat
	'''

#Méthode pour la récupération selon les tags
def getQueryByTags(tagsValue):
	cursorDB=mydb.cursor()
	arrayVal=tagsValue.split(",")
	finalStat=[]
	for val in range(0,len(arrayVal)):
		if len(arrayVal[val])>1:
			mySQL="""SELECT pays, sum(pourcentage) as total FROM civ WHERE pays=%s group by pays;"""
			value=(arrayVal[val],)
			cursorDB.execute(mySQL,value)
			results=cursorDB.fetchall()

			for val in results:
				finalStat.append({"annee":val[0],"pourcentage":int(val[1])})
	'''
	mySQL="""SELECT pays, sum(pourcentage) as total FROM civ WHERE pays=%s group by pays;"""
	value=(tagsValue,)
	finalStat=[]
	cursorDB.execute(mySQL,value)
	results=cursorDB.fetchall()

	for val in results:
		finalStat.append({"annee":val[0],"pourcentage":int(val[1])})
	'''
	return finalStat

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

def countRecords():
	cursorDB=mydb.cursor()
	finalCountry=[]
	mySQL="""SELECT count(*) as total FROM civ;"""
	cursorDB.execute(mySQL)
	result=cursorDB.fetchone()	
	return result[0]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)