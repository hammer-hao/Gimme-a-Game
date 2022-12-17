import pandas as pd
from celery import Celery
import time
from SC2 import sc2, APIkey
import mysql.connector
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

app = Celery(
    'tasks',
    broker="amqps://jifohjzo:l3252HkgK65PYczCTGZ7U6H5o1WxfA5A@whale.rmq.cloudamqp.com/jifohjzo",
)

load_dotenv()
hostname=os.getenv('HOSTNAME')
dbname=os.getenv('DBNAME')
username=os.getenv('DBUSERNAME')
pwd=os.getenv('PASSWORD')

conn = mysql.connector.connect(user=username, password=pwd,
                                 host=hostname,
                                 database=dbname)
mycursor = conn.cursor(buffered=True,dictionary=True)

engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
				.format(host=hostname, db=dbname, user=username, pw=pwd))

@app.task
def updatemmr():
    for i in range(2):
        region_code=APIkey.region_idr[i+1]
        ladderid_list= sc2.formladderlist(sc2.update1v1ladder(region_code, 53), region_code)
        region_player_full_data = sc2.update_playerstats(ladderid_list)
        allplayers=sc2.fullplayerlist(region_player_full_data)
        region_player_mmr_data = [[player[0], player[8], player[4]] for player in region_player_full_data]
        date = int(time.time())
        mmr_df=pd.DataFrame(region_player_mmr_data, columns=['playerid', 'race', ('mmr'+str(date))])
        mmr_df.to_sql(('mmrhistorytemp'+region_code), conn, if_exists='replace', index=False)

#Getting players mmr data
region_code='eu'
ladderid_list= sc2.formladderlist(sc2.update1v1ladder(region_code, 53), region_code)
region_player_full_data = sc2.update_playerstats(ladderid_list)
region_player_mmr_data = [[int(player[0]), player[8], player[4]] for player in region_player_full_data]

#getting current time
date = int(time.time())
mmr_df=pd.DataFrame(region_player_mmr_data, columns=['playerid', 'race', (str(date))])

#writing into a temporary SQL table
mmr_df.to_sql(('mmrhistorytemp'+region_code), engine, if_exists='replace', index=False)

#merging
query=('SELECT * FROM lastupdate'+'eu')
mycursor.execute(query)
response=mycursor.fetchall()
last_updated=response[0]['lastupdated']
merging=('CREATE TABLE IF NOT EXISTS mmrlive'+str(date)+' AS'+ 
        ' (SELECT * FROM mmrlive'+str(last_updated)+' LEFT OUTER JOIN mmrhistorytemp'+'eu'+' USING (playerid, race)'+
        ' UNION SELECT * FROM mmrlive'+str(last_updated)+' RIGHT OUTER JOIN mmrhistorytemp'+'eu'+' USING (playerid, race))')
mycursor.execute(merging)
conn.commit()

#drop the tmporary tables
drop=('DROP TABLE mmrlive'+str(last_updated))
mycursor.execute(drop)
conn.commit()
drop2=('DROP TABLE mmrhistorytemp'+'eu')
mycursor.execute(drop2)
conn.commit()

#Saving the last updated date at the database
date_df=pd.DataFrame({'lastupdated':date}, index=[0])
date_df.to_sql(('lastupdate'+region_code), engine, if_exists='replace', index=False)