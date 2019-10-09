#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import pandas as pd
import re


# In[1]:


def _date(tagged):
    now = datetime.datetime.now()
    
    #year
    if tagged[tagged['Prediction'].str.contains("year")].empty:
        year=now.timetuple().tm_year
    else :
        year=tagged[tagged['Prediction'].str.contains("year")].Word.iloc[0]
        
    #month
    if tagged[tagged['Prediction'].str.contains("month")].empty:
        month=now.timetuple().tm_mon
    else :
        month=tagged[tagged['Prediction'].str.contains("month")].Word.iloc[0]
        
    if month in ["january","jan"]:
        _mon=1
    elif month in ["february","feb"]:
        _mon=2
    elif month in ["march","mar"]:
        _mon=3
    elif month in ["april","apr"]:
        _mon=4
    elif month in ["may"]:
        _mon=5
    elif month in ["june","jun"]:
        _mon=6
    elif month in ["july","jul"]:
        _mon=7
    elif month in ["august","aug"]:
        _mon=8
    elif month in ["september","sep","sept"]:
        _mon=9
    elif month in ["october","oct"]:
        _mon=10
    elif month in ["november","nov"]:
        _mon=11
    elif month in ["december","dec"]:
        _mon=12
    else:
        _mon=now.timetuple().tm_mon
        
    #day
    flag=False
    days=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    #날짜가 들어왔을 때
    if tagged[tagged['Prediction'].str.contains("day_number")].empty==False:
        i=0 
        day=''
        for w in tagged['Prediction'].str.contains("day_number"):
            if w:
                day+=tagged['Word'][i]
            i+=1
    #요일이 들어왔을 때
    elif tagged[tagged['Prediction'].str.contains("day_name")].empty==False:
        flag=True
        day = tagged[tagged['Prediction'].str.contains("day_name")].Word.iloc[0]
        dif=days.index((day))-now.weekday()
        if tagged[tagged['Prediction'].str.contains("date_relative")].empty==False:
            dif+=7
    else :
        day=now.timetuple().tm_mday
        
    #날짜 숫자로 변환    
    if flag:   #요일이 들어왔을때 
        if dif < 0:
            dif+=7
        enddate = now+datetime.timedelta(days=dif)
        year=enddate.timetuple().tm_year
        _mon=enddate.timetuple().tm_mon
        _day=enddate.timetuple().tm_mday
    elif day.isdigit():
        _day=day
    elif re.findall('\d+', day):
        _day=int(re.findall('\d+', day)[0])
    else:
        if "first" in day or "one" in day:
            if "twenty" in day:
                _day=21
            elif "thirty" in day:
                _day=31
            else:
                _day=1
        elif "second" in day or "two" in day:
            if "twenty" in day:
                _day=22
            else:
                _day=2
        elif "third" in day or "three" in day:
            if "twenty" in day:
                _day=23
            else:
                _day=3
        elif "four" in day:
            if "teenth" in day:
                _day=14
            elif "twenty" in day:
                _day=24
            else:
                _day=4
        elif "five" in day or "fif" in day:
            if "teenth" in day:
                _day=15
            elif "twenty" in day:
                _day=25
            else:
                _day=5
        elif "six" in day:
            if "teenth" in day:
                _day=16
            elif "twenty" in day:
                _day=26
            else:
                _day=6
        elif "seven" in day:
            if "teenth" in day:
                _day=17
            elif "twenty" in day:
                _day=27
            else:
                _day=7
        elif "eight" in day:
            if "teenth" in day:
                _day=18
            elif "twenty" in day:
                _day=28
            else:
                _day=8
        elif "ninth" in day or "nine" in day:
            if "teenth" in day:
                _day=19
            elif "twenty" in day:
                _day=29
            else:
                _day=9
        elif "ten" in day:
            _day=10
        elif "eleven" in day:
            _day=11
        elif "twelfth" in day or "twelve" in day:
            _day=12
        elif "thirteen" in day:
            _day=13
        elif "twenty" in day or "twentieth" in day:
            _day=20
        else:
            _day=30    
    
    d=datetime.date(int(year),_mon,_day)
    d=d.strftime('%Y-%m-%d')
    return d


# In[ ]:




