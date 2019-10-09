#!/usr/bin/env python
# coding: utf-8

# In[3]:


import setuptools


# In[4]:


setuptools.setup(
    name = "heroku",
    install_requires = [
        "keras>=2.1.4", 
        "keras_contrib"
    ],
    dependency_links = ["https://github.com/keras-team/keras-contrib/tarball/master#egg=keras_contrib"],
)

