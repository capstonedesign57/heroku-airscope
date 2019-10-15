#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymysql


# In[4]:


def getdb():
    mydb = pymysql.connect(
    host = 'z1ntn1zv0f1qbh8u.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
    port = 3306,
    user = 'x3h6q2o87taceakh',
    passwd = 'eh2lx3rowe8pty87',
    db = 'xw6svbp8hrjpwvag',
    # charset = 'utf8',
    autocommit = True)
    
    cursor = db.cursor()

    cursor.execute("SELECT VERSION()")

    data = cursor.fetchone()

    print("Database version : %s " % data)

    db.close()

    return mydb
