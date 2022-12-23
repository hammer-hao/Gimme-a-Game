from flask import Flask, render_template, redirect, url_for, request, redirect, g
import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
hostname=os.getenv('HOSTNAME')
dbname=os.getenv('DBNAME')
username=os.getenv('DBUSERNAME')
pwd=os.getenv('PASSWORD')

def connect_db():
    conn = mysql.connector.connect(user=username, password=pwd,
                                    host=hostname,
                                    database=dbname)
    return conn

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

app = Flask(__name__)

@app.teardown_appcontext
def close_db(_):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/', methods=['POST', 'GET'])
def index():
    mycursor = get_db().cursor(buffered=True)
    if request.method=="POST":
        if len(request.form['name'])==0:
            return render_template('index.html', playerlist='empty')
        else:
            query = "SELECT * FROM players_s52 WHERE name LIKE '%" + request.form['name'] + "%'" + " ORDER BY mmr DESC"
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
    mycursor = get_db().cursor(buffered=True)
    query = "SELECT * FROM players_s52 WHERE playerid = " + str(playerid)
    mycursor.execute(query)
    thisplayer=mycursor.fetchall()
    try:
        tplayer=thisplayer[0]
        return render_template('details.html', player=tplayer)
    except IndexError:
        return render_template('details.html', player='notfound')
    

@app.route('/details/<int:playerid>/matchhistory')
def getmatchhistory(playerid):
    mycursor = get_db().cursor(buffered=True)
    query = 'SELECT * FROM pairedmatches WHERE playerid=' + str(playerid) + " ORDER BY date DESC"
    mycursor.execute(query)
    thisplayer=mycursor.fetchall()
    return render_template('matchhistory.html', matches=thisplayer)

@app.route('/details/<int:playerid>/<int:server>/mmrhistory')
def getmmrhistory(playerid, server):
    server_dict={
        1:'us',
        2:'eu'
    }
    servername=server_dict[server]
    mycursor = get_db().cursor(buffered=True)
    datequery = 'SELECT lastupdated from lastupdate'+servername
    mycursor.execute(datequery)
    thisdate = mycursor.fetchall()
    print(thisdate)
    lastupdated=thisdate[0][0]
    mmrquery = 'SELECT * FROM mmrlive' + str(lastupdated) + servername + ' WHERE playerid='+ str(playerid)
    mmrcursor = get_db().cursor(dictionary=True)
    mmrcursor.execute(mmrquery)
    mmr=mmrcursor.fetchall()
    datesraw=list(mmr[0].keys())[2:]
    date = [datetime.utcfromtimestamp(int(thistime)).strftime('%Y-%m-%d') for thistime in datesraw]
    values=list(mmr[0].values())[2:]
    return render_template('mmr.html', labels=date, ratings=values)

@app.route('/privacypolicy')
def privacy():
    return render_template('privacypolicy.html')