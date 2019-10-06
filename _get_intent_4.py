#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle

def get_intent(sent):
    # Flight/NoFlight
    filename = 'MNB_model_1.sav'
    MNB_model_load = pickle.load(open(filename, 'rb'), encoding='latin1')
    dtmvector = pickle.load(open('dtmvector_1', 'rb'), encoding='latin1')
    tfidf_transformer = pickle.load(open('tfidf_transformer_1', 'rb'), encoding='latin1')
    
    # 4_Intents (Only Flight/Cost/Airline)
    filename_2 = 'MNB_model_2.sav'
    MNB_model_load_2 = pickle.load(open(filename_2, 'rb'), encoding='latin1')
    dtmvector_2 = pickle.load(open('dtmvector_2', 'rb'), encoding='latin1')
    tfidf_transformer_2 = pickle.load(open('tfidf_transformer_2', 'rb'), encoding='latin1')
    
    test = []
    test.append(sent)
    test_dtm = dtmvector.transform(test)
    tfidfv_test = tfidf_transformer.transform(test_dtm)
    predict = MNB_model_load.predict(tfidfv_test)
    
    # 항공권 검색 질의인 경우
    if predict == "Flight" : # 의도가 Flight일 때 세부 의도 파악하는 부분
        test_dtm = dtmvector_2.transform(test)
        tfidf_test = tfidf_transformer_2.transform(test_dtm)
        predict = MNB_model_load_2.predict(tfidf_test)
        return(predict)
    
    else :
        return('NOT MY JOB')

