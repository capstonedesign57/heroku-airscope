#!/usr/bin/env python
# coding: utf-8

# In[4]:

from keras_contrib.layers import CRF
from keras_contrib.losses import crf_loss
from keras_contrib.metrics import crf_viterbi_accuracy
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing.sequence import pad_sequences

# To load the model
custom_objects={'CRF': CRF,'crf_loss':crf_loss,'crf_viterbi_accuracy':crf_viterbi_accuracy}
# To load a persisted model that uses the CRF layer 
BIO_TAGGER = load_model('_BIO_TAGGER.h5', custom_objects = custom_objects)
BIO_TAGGER._make_predict_function()

# In[5]:


from nltk import word_tokenize


# In[6]:


import pickle

with open('_word_to_index.pickle', 'rb') as f1:
    word_to_index = pickle.load(f1, encoding = 'latin1')
    
with open('_index_to_tag.pickle', 'rb') as f2:
    index_to_tag = pickle.load(f2, encoding = 'latin1')

with open('X_test.pickle', 'rb') as f3:
    X_test = pickle.load(f3, encoding = 'latin1')

with open('y_test.pickle', 'rb') as f4:
    y_test = pickle.load(f4, encoding = 'latin1')


# In[1]:


import numpy as np
import pandas as pd
from pandas import DataFrame as df
import re
from todatefomat import _date


# In[2]:


def todf(sent):
    
    tagged = pd.DataFrame(columns=("Word", "Prediction"))
    
    sent = sent.lower()
    sent = word_tokenize(sent)
    
    new_X = []
    for w in sent:
        try:
            new_X.append(word_to_index.get(w,1))
        except KeyError:
            new_X.append(word_to_index['OOV'])
            
    max_len = 70
    pad_new = pad_sequences([new_X], padding = "post", value = 0, maxlen = max_len)
    
    p = BIO_TAGGER.predict(np.array([pad_new[0]]))
    p = np.argmax(p, axis=-1)
    i =0
    for w, pred in zip(sent, p[0]):
        tagged.loc[i]=[w, index_to_tag[pred]]
        i += 1
    return tagged


# In[1]:


def get_element(user_input, intent, bot):  # for first input
    
    tagged = todf(user_input)
    
    loc = re.compile("airport|city|country|state")
    time = re.compile("date|time|day")

    fromloc=''
    stoploc=''
    toloc=''
    arrtime=''
    dpttime=''
    arl=''
    cheapest=0
    cost=''
    
    flag = False
    
    for w in tagged['Prediction']:
        if loc.search(w): # airport, city, country, state
            if "from" in w: #from
                fromloc = fromloc+' '+tagged[tagged['Prediction'].isin([w])].Word.tolist()[0]
                fromloc = fromloc.lstrip()
            elif "stop" in w: #stop
                stoploc = stoploc+' '+tagged[tagged['Prediction'].isin([w])].Word.tolist()[0]
                stoploc = stoploc.lstrip()
            else:  # default로 도착지
                toloc = toloc+' '+tagged[tagged['Prediction'].isin([w])].Word.tolist()[0]   
                toloc = toloc.lstrip()
        elif time.search(w): # date, time, day
            if flag == False:
                date=_date(tagged)
                if "arrive" in w or "return" in w: # arrive, return
                    arrtime = date
                else:  # default로 출발시간
                    dpttime = date
            else: 
                continue
        elif "airline" in w : # airline
            arl = arl+' '+tagged[tagged['Prediction'].isin([w])].Word.tolist()[0]
            arl = arl.lstrip()
        elif "cost" in w: # cost 
            cheapest = 1
        elif "fare" in w: # fare
            cost = cost+' '+tagged[tagged['Prediction'].isin([w])].Word.tolist()[0]
            cost = cost.lstrip()
        else: 
            continue
            
    result = df(data={'tag':['airline','fromloc','stoploc','toloc','dpttime','arrtime','cost','cheapest'],
                 'element':[arl,fromloc,stoploc,toloc,dpttime,arrtime,cost,cheapest]}, columns=['tag','element'])
    
    #의도는 있는데 요소가 없을 경우
#    if 'AskFlightWithAirline' in intent:
#        if result[result['tag'].isin(['airline'])].empty==None:
#            bot.sendMessage(chat_id, '{}'.format('Which airlilne would you like'))
#            #사용자에게 input을 받아온다
#            result.element[0]=input()
#    if 'AskFlightWithCost' in intent:
#        #print(result[result['tag'].isin(['cheapest'])].element.tolist()[0]==0 and result[result['tag'].isin(['cost'])].empty==False)
#        if result[result['tag'].isin(['cheapest'])].element.tolist()[0]==0 and result[result['tag'].isin(['cost'])].empty==False:
#            print("Do you want the cheapest flight or a ticket below a certain price?")
#            reply=input()
#            if "cheapest" in reply:
#                result.element[7]=1
#            else:
#                if reply.isdigit:
#                    result.element[6]='\''+re.findall('\d+', reply)[0]+'\''
#                else:
#                    print("Sorry, I didn't get that. Below how much?")
#                    reply=input()
#                    result.element[6]='\''+re.findall('\d+', reply)[0]+'\''
    
    return result


# In[2]:


def ellipsis(result, second_input, bot):
    
    df = todf(second_input)
    
    loc = re.compile("airport|city|country|state")
    time = re.compile("date|time|day")
    
    for w in df['Prediction']:
        if loc.search(w): # airport, city, country, state
            if "from" in w: #from
                result = result.replace(result.element[1], df[df['Prediction'].isin([w])].Word.tolist()[0])
            elif "stop" in w: #stop
                result = result.replace(result.element[2], df[df['Prediction'].isin([w])].Word.tolist()[0])
            elif "to" in w:  # default로 도착지
                result = result.replace(result.element[3], df[df['Prediction'].isin([w])].Word.tolist()[0])
            elif "from" in second_input: #from
                result = result.replace(result.element[1], df[df['Prediction'].isin([w])].Word.tolist()[0])
            elif "stop" in second_input: #stop
                result = result.replace(result.element[2], df[df['Prediction'].isin([w])].Word.tolist()[0])
            else:  # default로 도착지
                result = result.replace(result.element[3], df[df['Prediction'].isin([w])].Word.tolist()[0])    
        elif time.search(w): # date, time, day
            date=_date(df)
            if "arrive" in second_input or "return" in second_input: # arrive, return
                if date[:7]==result.element[5][:7]:
                    date=result.element[5][:7]+date[-3:]
                elif date[:3]==result.element[5][:3]:
                    date=result.element[5][:5]+date[-5:]
                else: 
                    continue
                result = result.replace(result.element[5], date)
            else:  # default로 출발시간
                if date[:7]==result.element[4][:7]:
                    date=result.element[4][:7]+date[-3:]
                elif date[:3]==result.element[4][:3]:
                    date=result.element[4][:5]+date[-5:]
                else: 
                    continue
                result = result.replace(result.element[4], date)
        elif "airline" in w : # airline
            arl = result.replace(result.element[0], df[df['Prediction'].isin([w])].Word.tolist()[0])
            arl = arl.lstrip()
        elif "cost" in w: # cost 
            result = result.replace(result.element[7], df[df['Prediction'].isin([w])].Word.tolist()[0])
        elif "fare" in w: # fare
            result = result.replace(result.element[6], df[df['Prediction'].isin([w])].Word.tolist()[0])
        else: # 우리가 필요한 성분은 없으므로 원래 데이터프레임 그대로
            continue
            
    return result

