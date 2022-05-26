"""Crypto API."""

from typing import Dict, List

import requests

# API Documentation - https://www.coingecko.com/en/api#explore-api

def get_coins() -> List[Dict]:
    """
    This function will get the top 10 coins at the current time, sorted by market cap in desc order.
    Returns a list of tuples
    Item 0 -> Unix Timestamp
    Item 1 -> price
    """
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=3&page=1&sparkline=false')
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        logging.exception("NETWORK PROBLEM")
        raise SystemExit(1)
    except requests.exceptions.HTTPError:
        logging.exception("UNSUCCESSFUL STATUS CODE")
        raise SystemExit(1)
    except requests.exceptions.Timeout:
        logging.exception("REQUEST TIMED OUT")
        raise SystemExit(1)
    return response.json()

def get_coin_price_history(coin_id: str) -> List[Dict]:
    """
    Returns a list of tuples
    Item 0 -> Unix Timestamp
    Item 1 -> price
    """
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=10&interval=daily")
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        logging.exception("NETWORK PROBLEM")
        raise SystemExit(1)
    except requests.exceptions.HTTPError:
        logging.exception("UNSUCCESSFUL STATUS CODE")
        raise SystemExit(1)
    except requests.exceptions.Timeout:
        logging.exception("REQUEST TIMED OUT")
        raise SystemExit(1)
    return response.json()['prices']

# utilize this function when submitting an order
def submit_order(coin_id: str, quantity: int, bid: float):
    """
    Mock function to submit an order to an exchange. 
    
    Assume order went through successfully and the return value is the price the order was filled at.
    """
    return bid

def get_current_price(coin_id: str, currency='usd') -> float:
    """
    Gets the current price of one coin, based on the coin id
    Response returns a dict, and the price is retrieved from the coin_id and currency keys.
    {
      COIN_ID: {
        CURRENCY: VALUE
      }
    }
    """
    try:
        response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}")
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        logging.exception("NETWORK PROBLEM")
        raise SystemExit(1)
    except requests.exceptions.HTTPError:
        logging.exception("UNSUCCESSFUL STATUS CODE")
        raise SystemExit(1)
    except requests.exceptions.Timeout:
        logging.exception("REQUEST TIMED OUT")
        raise SystemExit(1)
    return response.json()[coin_id][currency]