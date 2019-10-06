#!/usr/bin/env python
# coding: utf-8

# In[1]:

# manage.py

# In[2]:


import telepot
import time
import sys

import pickle
import _get_intent_4
# import pymysql


# In[3]:


InfoMsg = "WELCOME"
Answer = "SEE YOU AGAIN"


# In[4]:


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':
        if msg['text'].lower() in ['hi', 'hello', 'airscope', 'hey']:
            bot.sendMessage(chat_id, InfoMsg)

        elif msg['text'].lower() in ['bye', 'see you', 'thank you']:
            bot.sendMessage(chat_id, Answer)
        
        else:
            text_new = "".join(_get_intent_4.get_intent(msg['text']))
            bot.sendMessage(chat_id, text_new)


# In[5]:


token = "682502305:AAHgR74_gRqpboE9VYFVsAOtAjZ5Tk1qtaw"

bot = telepot.Bot(token)
# my_id = "864902416"

bot.message_loop(handle)
print('Listening...')


# In[ ]:


# Keep the program running

while (True):
    time.sleep(10)


# In[ ]:




