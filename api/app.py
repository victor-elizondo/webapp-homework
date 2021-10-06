import requests
import logging
import json
import logging.config as config_logger
from fastapi import FastAPI

from typing import Optional

app = FastAPI()
s = requests.Session()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# TODO: Don't place API KEY here 
API_KEY = 'kq4h2f9oyu4g1zc3undgab6k'
MAIN_URL = 'https://openapi.etsy.com/'
PING_PATH = 'v3/application/openapi-ping'
FIND_SHOP_PATH = 'v3/application/shops'

@app.get("/ping")
def ping_api(): 
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
def get_shops(shop_name: str):
    """"
    Gets a list of the first 10 shops from a name

    Args:
        name: keyword to be search in shop's name

    Returns:
        Print success response
    """
    s.headers.update({'x-api-key':API_KEY})

    payload = {'shop_name': shop_name}
    r = s.get(MAIN_URL+FIND_SHOP_PATH, params=payload)
    logger.info(f"{r.url}")
    logger.info(f"{r.status_code}")
    if (r.status_code == requests.codes.ok):
        #logger.info(f"Respuesta: {r.headers}")
        #logger.info(f"Respuesta: {r.json()}")
        a = int(r.json()['count'])
        b = r.json()['results']
        print(type(r.json()['results']))
        for idx, shop in enumerate(r.json()['results']):
            print(f"{idx}| {shop['shop_id']}  | {shop['shop_name']}")
        #print(int(r.json()['count']))
        #print(len(b))



        return([r.json()])
    else:
        return(f"Error, reason: {[r.json()]}")