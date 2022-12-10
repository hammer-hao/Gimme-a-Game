import celery
from datetime import datetime
from SC2 import sc2
import mysql.connector
import os
from dotenv import load_dotenv

app = celery.Celery(
    'tasks',
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

load_dotenv()
hostname=os.getenv('HOSTNAME')
dbname=os.getenv('DBNAME')
username=os.getenv('DBUSERNAME')
pwd=os.getenv('PASSWORD')

conn = mysql.connector.connect(user=username, password=pwd,
                                 host=hostname,
                                 database=dbname)


@app.task

def updatemmr():
    ladderid_list= {'eu':sc2.formladderlist(sc2.update1v1ladder("eu", 52), "eu"),
                    'us':sc2.formladderlist(sc2.update1v1ladder("us", 52), "us"),
                    'kr':sc2.formladderlist(sc2.update1v1ladder("kr", 52), "kr")}
    