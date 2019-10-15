#!/usr/bin/env python
# coding: utf-8

# # Manage

# In[2]:


import telepot
import pickle
import sys
import time
import re

import pymysql


# In[3]:


# Import User Libraries
from _get_intent_4 import get_intent
from _spelling_corrector import _correction
from _get_tag import get_element, todf
# from mydb import getdb
from _get_view import getroute
from todatefomat import _date

def getdb():
    mydb = pymysql.connect(
    host = 'z1ntn1zv0f1qbh8u.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
    port = 3306,
    user = 'x3h6q2o87taceakh',
    passwd = 'eh2lx3rowe8pty87',
    db = 'xw6svbp8hrjpwvag',
    # charset = 'utf8',
    autocommit = True)
    return mydb

# In[4]:


token = "682502305:AAHgR74_gRqpboE9VYFVsAOtAjZ5Tk1qtaw"
# my_id = "729092704"

bot = telepot.Bot(token)
status = True

InfoMsg = "WELCOME"
Answer = "SEE YOU AGAIN"

state = 0
flag = 9


# In[5]:


intent = None
tagged = None

def handle(msg):
    global flag
    global intent
    global tagged
    
    content_type, chat_type, chat_id = telepot.glance(msg)

    if msg['text'].lower() in ['hi', 'hello', 'airscope', 'hey']:
        flag = 9
        
    if flag == 9:
        if content_type == 'text':
            if msg['text'].lower() in ['hi', 'hello', 'airscope', 'hey']:
                bot.sendMessage(chat_id, InfoMsg)
            elif msg['text'].lower() in ['bye', 'see you', 'thank you']:
                bot.sendMessage(chat_id, Answer)
            else:
                user_input = _correction(msg['text'])
                # bot.sendMessage(chat_id, user_input)
                intent = get_intent(user_input)
                intent = ''.join(intent)
                # bot.sendMessage(chat_id, intent)
                tagged = get_element(user_input, intent, bot)
                flag = 0
        

    if flag == 1:
        tagged.element[1] = msg['text']
        flag = 0
    elif flag == 2:
        tagged.element[3] = msg['text']
        flag = 0
    elif flag == 3:
        date = _date(todf(msg['text']))
        tagged.element[4] = date
        flag = 0
    elif flag == 4:
        tagged.element[0]=msg['text']
        flag = 0
    elif flag == 5:
        reply = msg['text'].lower()
        if "cheapest" in reply:
            tagged.element[7] = 1
            flag = 0
        else:
            if reply.isdigit:
                tagged.element[6] = '\'' + re.findall('\d+', reply)[0] + '\''
                flag = 0
            else:
                bot.sendMessage(chat_id,'{}'.format("Sorry, I didn't get that. Below how much?"))
                reply = msg['text']
                tagged.element[6] = '\''+re.findall('\d+', reply)[0] + '\''
                flag = 0
    else:
        flag = flag
    
    if flag == 0 :
        # if null값 있으면 flag=1, 모두 있으면 flag=2
        if tagged[tagged['tag'].isin(['fromloc'])].element.tolist()[0] == '':
            bot.sendMessage(chat_id,'{}'.format("Where would you like to depart?"))
            flag = 1
        elif tagged[tagged['tag'].isin(['toloc'])].element.tolist()[0] == '':
            bot.sendMessage(chat_id,'{}'.format("Where would you want to arrive?"))
            flag = 2
        elif tagged[tagged['tag'].isin(['dpttime'])].element.tolist()[0] == '' and tagged[tagged['tag'].isin(['arrtime'])].element.tolist()[0]=='':
            bot.sendMessage(chat_id,'{}'.format("When would you like to depart?"))
            flag = 3  
        elif 'AskFlightWithAirline' in intent and tagged[tagged['tag'].isin(['airline'])].element.tolist()[0] == '':
                bot.sendMessage(chat_id, '{}'.format('Which airline would you like'))
                flag = 4
        elif 'AskFlightWithCost' in intent and tagged[tagged['tag'].isin(['cheapest'])].element.tolist()[0] == 0 and tagged[tagged['tag'].isin(['cost'])].element.tolist()[0]=='':
                bot.sendMessage(chat_id, '{}'.format("Do you want the cheapest flight or a ticket below a certain price?"))
                flag = 5
        else: 
            flag = 6

    if flag == 6:
        mydb = getdb()
        route = getroute(intent, tagged, mydb)
        route = route.iloc[0]
        bot.sendMessage(chat_id, '\n{}\n'.format("here are your results:"))
        bot.sendMessage(chat_id, ' airline: {}({})\n depart: {} ({},{})\n arrive: {} ({},{})\n stops: {}\n departure time: {}\n arrival time: {}\n cost: {}\n\n'.format(route[1],route[0],route[2],route[3],route[4],route[5],route[6],route[7],route[8],route[9],route[10],route[11]))
        flag = 9
        
bot.message_loop(handle)

while status == True:
    time.sleep(10)

