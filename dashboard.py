from flask import Flask, render_template, redirect, url_for, request, redirect
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
hostname=os.getenv('HOSTNAME')
dbname=os.getenv('DBNAME')
username=os.getenv('DBUSERNAME')
pwd=os.getenv('PASSWORD')

conn = mysql.connector.connect(user=username, password=pwd,
                                 host=hostname,
                                 database=dbname)
mycursor = conn.cursor()

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method=="POST":
        if len(request.form['name'])==0:
            return render_template('index.html', playerlist='empty')
        else:
            query = "SELECT * FROM players_s52 WHERE name LIKE '%" + request.form['name'] + "%'"
            mycursor.execute(query)
            thisresult=mycursor.fetchall()
            if len(thisresult)>0:
                return render_template('index.html', playerlist=thisresult)
            else:
                return render_template('index.html', playerlist='notfound')
    else:
        return render_template('index.html', playerlist=[])

@app.route("/details/<int:playerid>/<int:server>")
def getdetails(playerid, server):
    query = "SELECT * FROM players_s52 WHERE playerid = " + str(playerid) + " AND region =" + str(server)
    mycursor.execute(query)
    thisplayer=mycursor.fetchall()
    return render_template('details.html', player=thisplayer[0])

@app.route('/details/<int:playerid>/matchhistory')
def getmatchhistory(playerid):
    query = 'SELECT * FROM matches WHERE playerid=' + str(playerid)
    mycursor.execute(query)
    thisplayer=mycursor.fetchall()
    return render_template('matchhistory.html', matches=thisplayer)

@app.route('/privacypolicy')
def privacy():
    return render_template('privacypolicy.html')