import psycopg2
import pdb
import json

connexion = psycopg2.connect("dbname=afwoman user=postgres host=localhost password=5432")

def countRecords():
	cursorDB=connexion.cursor()
	mySQL="""SELECT count(*) as total FROM civ;"""
	cursorDB.execute(mySQL)
	result=cursorDB.fetchone()
	cursorDB.close()
	return result[0]

def loadPieChart():
	cursorDB=connexion.cursor()
	pieChartYear=[]
	mySQL="""SELECT annee, SUM(pourcentage) as total FROM civ group by annee order by annee ASC"""
	cursorDB.execute(mySQL)
	res=cursorDB.fetchall()
	cursorDB.close()
	for j in res:
		pieChartYear.append({"name":j[0],"y":int(j[1])})
	return pieChartYear

def loadLineChart():
	cursorDB=connexion.cursor()
	arrayCountry=["Benin", "Burkina Faso","Cote d'Ivoire", "Gambia", "Ghana", "Guinea", "Guinea-Bissau", "Liberia", "Mali", "Niger", "Nigeria", "Senegal", "Sierra Leone", "Togo"]
	arraySeries=[]
	data=[]
	countrySQL="""SELECT id,pays,annee,pourcentage FROM civ ORDER BY annee ASC;"""
	cursorDB.execute(countrySQL)
	result=cursorDB.fetchall()
	cursorDB.close()
	
	for index in range(0,len(arrayCountry)):
		for r in result:
			if arrayCountry[index]==r[1]:
				data.append(r[3])
		arraySeries.append({"name":arrayCountry[index],"data":data})
		data=[]
	return json.dumps(arraySeries)

def getDistinctCountry():
	cursorDB=connexion.cursor()
	finalCountry=[]
	mySQL="""SELECT DISTINCT(pays) from civ order by pays ASC"""
	cursorDB.execute(mySQL)
	results=cursorDB.fetchall()
	cursorDB.close()
	for y in results:
		finalCountry.append(y[0])
	return finalCountry