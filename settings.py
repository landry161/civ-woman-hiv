import csv
import psycopg2
import pandas as pd
import requests
import pdb
import os.path
from psycopg2 import OperationalError, errorcodes, errors

connexion = psycopg2.connect("dbname=afwoman user=postgres host=localhost password=5432")

#On vérifie l'existence du fichier csv
def checkIfFileExists(fileName):
    checkFile=os.path.isfile(fileName)

    if checkFile==False:
        #Téléchargement du fichier CSV depuis le site
        downloadFile()
        renameCSVDowloaded()
        createTable()
        insertPDIntoDB()
        runServerFunction()
    else:
        #Fichier exixte, donc démarrage du serveur
        print(" Démarrage du serveur ")
        runServerFunction()

def renameCSVDowloaded():
    myDataFrame=pd.read_csv("cover.csv",delimiter=",",encoding="ISO-8859-1")
    myDataFrame=myDataFrame.rename(columns={myDataFrame.columns[0]: 'pays',myDataFrame.columns[1]: "annee",myDataFrame.columns[2]: "pourcentage"})
    myDataFrame.to_csv("cover.csv",index=False)
    print(" Fichier CSV mis à jour avec succès ")

#Méthode de création des tables
def createTable():
    try:
        cursor = connexion.cursor()
        query="""CREATE TABLE civ(id serial PRIMARY KEY,pays VARCHAR(30),annee INT,pourcentage INT)"""
        cursor.execute(query)
        connexion.commit()
        print("Table créée avec succès")
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)
        print(" Impossible de créer cette table. Cette base de données existe probalement déjà")
    cursor.close()

#Insertion
def insertPDIntoDB():
    print("Chargement dans la base ...")
    cursor = connexion.cursor()
    dataFrame=pd.read_csv("cover.csv")
    myQuery=f"""insert into civ(pays,annee,pourcentage) VALUES(%s,%s,%s)"""
    cursor.executemany(myQuery,dataFrame.values)
    connexion.commit()
    cursor.close()

#Méthode de démarrage de notre application Flask
def runServerFunction():
    os.system("flask --app app.py run --debug")

#Télchargement du fichier
def downloadFile():
    defaultUrl="https://data.gouv.ci/data-fair/api/v1/datasets/couverture-des-femmes-enceintes-sous-traitement-anti-retroviraux/data-files/couverture-des-femmes-enceintes-sous-traitement-anti-retroviraux_pays_CEDEAO.csv"
    myUrl=requests.get(defaultUrl)
    fileName="cover.csv"
    file=open(fileName,"w")
    file.write(myUrl.content.decode("utf-8"))
    print("Fichier téléchargé avec succès")

#Démarrage
checkIfFileExists("couverture-des-femmes-enceintes-sous-traitement-anti-retroviraux_pays_CEDEAO.csv")