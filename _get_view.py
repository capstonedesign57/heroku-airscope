#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pymysql
import pandas as pd

# In[2]:


def get_airport(loc, db):
    curs = db.cursor()
    sql = "SELECT iata FROM airports WHERE name=\'"+loc+"\' or city=\'"+loc+"\' or country=\'"+loc+"\' or iata=\'"+loc+"\'"
    curs.execute(sql)
    result = curs.fetchall()
    return result

def get_airline(airline, db):
    curs = db.cursor()
    sql = "SELECT iata FROM airlines WHERE iata=\'"+airline+"\' or name LIKE \'%"+airline+"%\'"
    curs.execute(sql)
    result = curs.fetchall()
    for (a,) in result:
        return a

def getroute(intent, tagged, db, bot, chat_id):
    curs = db.cursor()
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # from, to, date 등 필요한 요소들 받아오기
    fromloc = 'src_airport='
    for (a,) in get_airport(tagged[tagged['tag'].isin(['fromloc'])].element.tolist()[0],db):
        fromloc=fromloc+'\''+a+'\''+' or src_airport='
    #fromloc='('+fromloc[:-16]+')'
    fromloc = fromloc[:-16]

    toloc = 'dst_airport='
    for (a,) in get_airport(tagged[tagged['tag'].isin(['toloc'])].element.tolist()[0],db):
        toloc=toloc+'\''+a+'\''+' or dst_airport='
    #toloc='('+toloc[:-16]+')'
    toloc = toloc[:-16]
    
    # stop이 있는 경우
    flag = 0
    if tagged[tagged['tag'].isin(['stoploc'])].empty!=None:
        stoploc = 'stop_airport='
        for (a,) in get_airport(tagged[tagged['tag'].isin(['stoploc'])].element.tolist()[0],db):
            stoploc=stoploc+'\''+a+'\''+' or stop_airport='      
        stoploc='('+stoploc[:-17]+')'
        flag = 1

    #get date
    dpt_date = "\'"+tagged[tagged['tag'].isin(['dpttime'])].element.tolist()[0]+"\'"
    arr_date = "\'"+tagged[tagged['tag'].isin(['arrtime'])].element.tolist()[0]+"\'"

    
    # create selectedRoute
    sql="CREATE OR REPLACE VIEW selectedRoute AS \
        SELECT route_id, airline, airline_id, src_airport, src_name, src_city, src_country, dst_airport, dst_name, dst_city, dst_country, stops, dpt_time, \
        DATE_ADD(dpt_time, INTERVAL TIME_TO_SEC(est_time) SECOND) as arr_time \
        FROM joinedRoute\
        WHERE " + toloc + " AND DATE(dpt_time)=" + dpt_date
        # WHERE " + fromloc + " AND " + toloc + " AND DATE(dpt_time)=" + dpt_date
        # WHERE "+fromloc+" AND "+toloc+" AND DATE(dpt_time)="+dpt_date
    curs.execute(sql)

    #selectedRoute에 airline_name, cost JOIN
    sql2="CREATE OR REPLACE VIEW Route AS \
        SELECT s.*, a.name as airline_name, c.cost \
        FROM selectedRoute as s, airlines as a, cost as c \
        WHERE s.airline_id=a.airline_id AND s.route_id=c.route_id"
    curs.execute(sql2)
    
    
    #의도별 항공권 검색 수행
    if "AskFlightWithAirline" in intent and "AskFlightWithCost" in intent:
        airline = get_airline(tagged[tagged['tag'].isin(['airline'])].element.tolist()[0],db)
        if tagged[tagged['tag'].isin(['cheapest'])].element.tolist()[0]==1:
            sql3 = "SELECT * FROM Route WHERE airline=\'"+airline+"\' or airline_name=\'"+airline+"\' ORDER BY cost ASC"
        else:
            cost=tagged[tagged['tag'].isin(['cost'])].element.tolist()[0]
            sql3="SELECT * FROM Route WHERE airline=\'"+airline+"\' or airline_name=\'"+airline+"\' and cost<="+cost
        cursor.execute(sql3)
    
    elif "AskFlightWithAirline" in intent:
        airline = get_airline(tagged[tagged['tag'].isin(['airline'])].element.tolist()[0],db)
        sql3 = "SELECT * FROM Route WHERE airline=\'"+airline+"\' or airline_name=\'"+airline+"\'"
        cursor.execute(sql3)
        
    elif "AskFlightWithCost" in intent:
        if tagged[tagged['tag'].isin(['cheapest'])].element.tolist()[0]==1:
            sql3="SELECT * FROM Route ORDER BY cost ASC"
        else:
            cost=tagged[tagged['tag'].isin(['cost'])].element.tolist()[0]
            sql3="SELECT * FROM Route WHERE cost<="+cost
        cursor.execute(sql3)
    
    else:
        cursor.execute("SELECT * FROM Route")
        
    #검색결과 Route을 df로 읽어오기
    bot.sendMessage(chat_id, '\n{}\n'.format("here are your results:"))
    count = 0
    while True :
        result = cursor.fetchone()
        if result == None:
            if count == 0:
                bot.sendMessage(chat_id, '{}'.format("Oops! The flight you are looking for does not exist."))
            break
        count = count+1
        df = pd.DataFrame(result, index = [0])
        route_id = df.iloc[0]["route_id"]
        df = df[["airline","airline_name","src_name","src_city","src_country","dst_name","dst_city","dst_country","stops","dpt_time","arr_time","cost"]]
        bot.sendMessage(chat_id, ' airline: {}({})\ndepart: {} ({},{})\narrive: {} ({},{})\nstops: {}\ndeparture time: {}\narrival time: {}\ncost: {}\n\n'.format(df.iloc[0][1],df.iloc[0][0],df.iloc[0][2], df.iloc[0][3],df.iloc[0][4],df.iloc[0][5], df.iloc[0][6],df.iloc[0][7],df.iloc[0][8], df.iloc[0][9],df.iloc[0][10],df.iloc[0][11]))

        #### 경유지가 있는 경우는???
        if flag == 1:
            bot.sendMessage(chat_id, '{}\n'.format("stop info:"))
            cursor2 = db.cursor(pymysql.cursors.DictCursor)
            stopsql = "SELECT name, city, country, stop_order FROM stopview WHERE route_id = "+str(route_id)
            cursor2.execute(stopsql)
            for i in range(df.iloc[0]["stops"]):
                stop_result = cursor2.fetchone()
                stop = pd.DataFrame(stop_result, index = [0])
                bot.sendMessage(chat_id, '{} {}   {} {}'.format(stop.iloc[0]["stop_order"], stop.iloc[0]["name"], 
                                                                stop.iloc[0]["city"], stop.iloc[0]["country"]))
