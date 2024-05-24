from flask import Flask, flash, render_template,request,redirect,url_for,make_response
import csv
import mysql.connector
import json
import pandas as pd
import pdb
import numpy as np
from decimal import *
from db import *

#flask --app app.py --debug run
app = Flask(__name__)

@app.route("/")
def home():
	#loadAndInsertIntoDB()
	#years=getDistinctYear()
	country=getDistinctCountry()
	records=countRecords()
	#queriesSeries=selectQueryLineChart()
	return render_template("index.html",records=records,countArray=len(country),countries=country)

@app.route("/charts",methods=["POST"])
def loadChartsWithData():
	tags=request.form.get("tags")
	year=request.form.get("year")
	print(year)
	print(tags)
	pdb.set_trace()
	return render_template("charts.html")

@app.route("/stathome",methods=["POST"])
def getStatHomeByYear():
	countries = request.form.get("tags")
	year= request.form.get("year")
	ok=[]
	print(countries)
	print(year)
	res=getQueryByTags(countries)
	#queryPieChart=pieChartByYear()
	#ok.append({"res":res})
	return res

#Diagramme circulaire par An
@app.route("/pie-chart",methods=["GET"])
def pieChartByYear():
	pieChartYear=loadPieChart()
	return pieChartYear
	'''
	cursorDB=mydb.cursor()
	pieChartYear=[]
	mySQL="""SELECT annee, SUM(pourcentage) as total FROM civ group by annee order by annee ASC"""
	cursorDB.execute(mySQL)
	res=cursorDB.fetchall()
	for j in res:
		pieChartYear.append({"name":j[0],"y":int(j[1])})
	
	return pieChartYear
	'''

#Liste des pays
@app.route("/line-query-chart",methods=["GET"])
def selectQueryLineChart():
	arraySeries=loadLineChart()
	return arraySeries

#Insertion dans la base de données

def getDistinctYear():
	'''
    cursorDB=mydb.cursor()
	finalArray=[]
	mySQL="""SELECT DISTINCT(annee) from civ order by annee ASC"""
	cursorDB.execute(mySQL)
	results=cursorDB.fetchall()
	for y in results:
		finalArray.append(y[0])
	return finalArray
	'''

"""
def countRecords():
	cursorDB=mydb.cursor()
	finalCountry=[]
	mySQL=SELECT count(*) as total FROM civ;
	cursorDB.execute(mySQL)
	result=cursorDB.fetchone()	
	return result[0]
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)