#!/usr/bin/env python
# coding: utf-8

# # 출처: http://norvig.com/spell-correct.html

# In[1]:


import re
from collections import Counter
from nltk import word_tokenize


# In[2]:


def words(text):
    return re.findall(r'\w+', text.lower())


# In[3]:


WORDS = Counter(words(open('_corpus.txt', encoding="utf-8").read()))


# In[4]:


def P(word, N=sum(WORDS.values())):
    "Probability of `word`."
    return WORDS[word] / N


# In[5]:


def correction(word):
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)


# In[6]:


def candidates(word):
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])


# In[7]:


def known(words):
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)


# In[8]:


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)


# In[9]:


def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# In[17]:


def _correction(user_sent):
    user_input=''
    sent = user_sent.lower()
    sent2 = word_tokenize(sent)
    for word in sent2:
        user_input = user_input+' '+(correction(word))
    user_input = user_input.lstrip()
    return user_input


# In[ ]:




