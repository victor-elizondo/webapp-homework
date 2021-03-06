import streamlit as st
import numpy as np 
import pandas as pd
import requests
import logging
import logging.config as config_logger
from sklearn.feature_extraction.text import CountVectorizer

### API URL Definition, choose one of them depending the case:
# This works for running stand alone -->
#API_URL = 'http://localhost:8000'      
# This work for containerized running -->
API_URL = 'http://host.docker.internal:8000'   

API_PATH = '/get_items_for_shops/'

s = requests.Session()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

st.header('Simon Data Home Work')
st.write('This WebApp is for display the results for the Challenge')
st.write('Developed by Victor Elizondo (victor.elizondo.v [@] gmail.com')

## 1st Part : retreiving the data

def get_data(shop_name: str="simon", limit: int=10):
    """"
    Connect to the API and pull all items for the number of shops given by limit, searching shops by the keyword shop_name

    Args:
    shop_name: Keyword to search shops for
    limit: number of shops to grab
    """
    if(len(shop_name) == 0):
        shop_name = "simon"

    payload = {'shop_name': shop_name, 'limit': limit}
    r = s.get(API_URL+API_PATH, params=payload)
    logger.info(r.url)
    df = pd.DataFrame()
    shops = []
    for idx, shop in enumerate(r.json()):
        shops.append(pd.DataFrame(shop))
        logger.info(f"{shops[idx].shape[0]} Items pulled from current shop")
    logger.info(f"Data pulled from {len(shops)} shops")
    return(shops)


## 2nd Part : Process the data
def get_relevant_terms(shop: pd.DataFrame, top: int=5):
    """
    Extracts the most relevant words from all text in titles and descriptions from items 
    belonging to a given shop. The importance of a given term is determined by the frequency
    the word is repeated across all text. Step-words are taken out from the analysis.
    
    Args:
        shop: DataFrame containing the titles an descriptions from all items belonging to de shop,
        also contain shop's name and id.
        top: Number of top terms to be extracted
    Returns:
        words: DataFrame containing the top words and its frequencies for the given shop's data.    
    """
 
    # create a count vectorizer to extract and count differents tokens (words)
    count_vec = CountVectorizer(stop_words='english')
    #transform all the text from the items descriptions and items titles
    count_data = count_vec.fit_transform(shop['description'].append(shop['title']))
    # Adding counting across all items
    freqs = zip(count_vec.get_feature_names_out(), count_data.toarray().sum(axis=0))
    
    # sorting
    words = pd.DataFrame(freqs, columns=['relevant terms','frequency'])
    words.sort_values(by='frequency', ascending=False, inplace=True, ignore_index=True)
    return(words.head(top))


def process_data(shops, top: int=5):
    """
    Extract all Top most relevant terms for all given shops, return a List of Dicts
    containing shop_id, shop_name and a DataFrame that contains the Relevant terms and its frequencies.

    Args:
        shops: List of shop's data
        top: top: Number of top terms to be extracted for each shop
    Returns:
        processed_shops: List of Dicts containing shop_id, shop_name and a DataFrame that contains the Relevant terms and its frequencies.
    """

    processed_shops = []
    shop_info = {}
    for shop in shops:
        if(not shop.empty):       
            shop_info = {
                "shop_id" : shop['shop_id'][0],
                "shop_name" : shop['shop_name'][0],
                "top_terms" : get_relevant_terms(shop, top)
            }
            processed_shops.append(shop_info)

    return(processed_shops)
      

## 3rd Part : Displaying the interactive widgets and the results

with st.form('Form1'):
    number_input = st.number_input('Insert the number of shops to pull', min_value=1, max_value=20, value=10, step=1)
    top_number = st.number_input('Insert the number relevant terms to extract', min_value=1, max_value=10, value=5, step=1)
    text_input = st.text_input(label='Enter some keyword (by default "simon" wil be used)',)
    submitted = st.form_submit_button('Pull & Process data')

if submitted:
    if(len(text_input) == 0):
        text_input = "simon"
    st.subheader(f'Pulling data using keyword: {text_input} for {number_input} shops and extracting {top_number} most relevant terms for each shop.')
    df = get_data(text_input, limit=number_input)
    proc_shops = process_data(df, top=top_number)
    st.header(f"Results:")
    for shop in proc_shops:
        st.subheader(shop['shop_name'])
        st.subheader(f"shop_id:{shop['shop_id']}")
        st.table(shop['top_terms'])