import requests
import logging
import json
import logging.config as config_logger
from fastapi import FastAPI, params

from typing import ItemsView, Optional

app = FastAPI()
s = requests.Session()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# TODO: Don't place API KEY here 
API_KEY = 'kq4h2f9oyu4g1zc3undgab6k'

MAIN_URL = 'https://openapi.etsy.com/'
PING_PATH = 'v3/application/openapi-ping'
FIND_SHOP_PATH = 'v3/application/shops'
GET_ITEMS_PATH = 'v3/application/shops/'
CHUNK_SIZE = 25


@app.get("/ping")
def ping(): 
    """"
    Tests connectivity with Etsy API using the provided API_KEY

    Args:

    Returns:
        Print success response and application_id
    """
    s.headers.update({'x-api-key':API_KEY})
    r = s.get(MAIN_URL+PING_PATH)
    if (r.status_code == requests.codes.ok):
        logger.info(f"Respuesta: {r.headers}")
        logger.info(f"Respuesta: {r.json()}")
        return([r.headers, r.json()])
    else:
        return('oops')


@app.get("/get_shops/")
def get_shops(shop_name: str="simon", limit: int = 10):
    """"
    Gets a list of up to 10 shops from a keyword in the shop's name

    Args:
        name: keyword to be search in shop's name, Default="simon"
        limit (optional) : Default=10
    Returns:
        shop_ids: List of selected Shop Ids
    """
    s.headers.update({'x-api-key':API_KEY})

    payload = {'shop_name': shop_name, 'limit': limit}
    r = s.get(MAIN_URL+FIND_SHOP_PATH, params=payload)
    logger.info(f"{r.url}")
    logger.info(f"{r.status_code}")
    shop_ids = []
    if (r.status_code == requests.codes.ok):
        for idx, shop in enumerate(r.json()['results']):
            logger.info(f"{idx}| {shop['shop_id']}  | {shop['shop_name']}")
            shop_ids.append(shop['shop_id'])
        return(shop_ids)
    else:
        return(f"Error, reason: {[r.json()]}")

@app.get("/get_items/")
def get_items(shop_id: int):
    """"
    Gets total items that are being sold on the shop given a shop_id

    Args:
        Shop_id (int)

    Returns:
        List containing the items (shop_id, listing_id, title, description)
    """
    #s = requests.Session()

    s.headers.update({'x-api-key':API_KEY})
    payload = {'limit': CHUNK_SIZE, 'offset': 0}
    r = s.get(MAIN_URL+GET_ITEMS_PATH+f"{shop_id}/listings/active", params=payload)
    items = []
    item = {}
    for idx in range(r.json()['count']): 
        if(idx%CHUNK_SIZE == 0 & idx>0):
            payload = {'limit': CHUNK_SIZE, 'offset': idx}
            r = s.get(MAIN_URL+GET_ITEMS_PATH+f"{shop_id}/listings/active", params=payload)
        #logger.info(f"{r.json()['results'][idx%CHUNK_SIZE]['listing_id']}")
        item = {
            "shop_id" : r.json()['results'][idx%CHUNK_SIZE]['shop_id'],
            "listing_id" : r.json()['results'][idx%CHUNK_SIZE]['listing_id'],
            "title" : r.json()['results'][idx%CHUNK_SIZE]['title'],
            "description" : r.json()['results'][idx%CHUNK_SIZE]['description']
        }
        items.append(item)    
    logger.info(f"Total Pulled items: {len(items)} for shop:{shop_id}")
    return(items)

@app.get("/get_items_for_shops/")
def get_items_for_shops(shop_name: str="simon", limit: int = 10):
    """"
    Gets all item for the shops listed in shops_list

    Args:
        name: keyword to be search in shop's name, Default="simon"
        limit (optional) : Default=10
    Returns:
        
    """
    logger.info(f"Input name: {shop_name}")
    shops = get_shops(shop_name, limit)
    all_items = []
    for idx, shop in enumerate(shops):
        logger.info(f"shop_id:{shop}")
        all_items.append(get_items(shop))
    return(all_items)
    """
    s.headers.update({'x-api-key':API_KEY})
    payload = {'shop_name': shop_name, 'limit': limit}
    r = s.get(MAIN_URL+FIND_SHOP_PATH, params=payload)
    logger.info(f"{r.url}")
    logger.info(f"{r.status_code}")
    shop_ids = []
    if (r.status_code == requests.codes.ok):
        for idx, shop in enumerate(r.json()['results']):
            logger.info(f"{idx}| {shop['shop_id']}  | {shop['shop_name']}")
            shop_ids.append(shop['shop_id'])
        return(shop_ids)
    else:
        return(f"Error, reason: {[r.json()]}")
    """