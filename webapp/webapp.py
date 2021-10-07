from numpy.lib.function_base import append
from pandas.core.frame import DataFrame
import streamlit as st
import numpy as np 
import pandas as pd
import requests
import logging
import json
import logging.config as config_logger
from sklearn.feature_extraction.text import CountVectorizer

API_URL = 'http://localhost:8000'
API_PATH = '/get_items_for_shops/'

s = requests.Session()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

st.header('Simon Data Home Work')
st.write('This WebApp is for display the results for the Challenge')

## 1st Part : retreiving the data

def get_data():
    shop_name = "bar"
    limit = 10

    payload = {'shop_name': shop_name, 'limit': limit}
    r = s.get(API_URL+API_PATH, params=payload)
    df = pd.DataFrame()
    shops = []
    for shop in r.json():
        shops.append(pd.DataFrame(shop))
    return(shops)


## 2nd Part : Process the data
def get_relevant_terms(shop: DataFrame, limit: int=5):
 
    # create a count vectorizer
    count_vec = CountVectorizer(stop_words='english')
    #transformmm
    
    count_data = count_vec.fit_transform(shop['description'])
    
    #print(count_vec.get_feature_names_out())
    #print(count_data.toarray().sum(axis=0))
    freqs = zip(count_vec.get_feature_names_out(), count_data.toarray().sum(axis=0))
    
    words = pd.DataFrame(freqs, columns=['relevant terms','frequency'])
    words.sort_values(by='frequency', ascending=False, inplace=True, ignore_index=True)
    return(words.head(limit))

    #print sorted(freqs, key=lambda x: -x[1])
    #create dataframe
    #cv_dataframe=pd.DataFrame(count_data.toarray(),columns=count_vec.get_feature_names_out())
    #print(cv_dataframe)

def process_data(shops):
    processed_shops = []
    shop_info = {}
    for shop in shops:
        shop_info = {
            "shop_id" : shop['shop_id'][0],
            "top_terms" : get_relevant_terms(shop, limit=10)
        }
        processed_shops.append(shop_info)

    return(processed_shops)
      

        

#matrix = count_vect.fit_transform(doc_list)

# sort from largest to smallest
#print sorted(freqs, key=lambda x: -x[1])



df = get_data()
#st.dataframe(df.head(10))
#print(type(data[0]))
#print(type(data[0][0]))
#print(data[0][0])
#df = pd.DataFrame(data[0])
#print(df.info())
proc_shops = process_data(df)
for shop in proc_shops:
    st.title(shop['shop_id'])
    st.table(shop['top_terms'])
#get_relevant_terms(df)