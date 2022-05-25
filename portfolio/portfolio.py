import crypto_api
from datetime import datetime
from decimal import Decimal
import logging
from tables.position import Position
from tables.trade import Trade
from utils.utils import *

"""
All the logic related specifically to portfolios goes here
"""

def get_positions(db_session):
    return db_session.query(Position.coin_id, Position.cost_basis, Position.quantity).all()


def should_we_build_portfolio(db_session):
    if len(get_positions(db_session)) == 0:
        logging.info("Building initial portfolio")
        build_portfolio(db_session)
    else:
        logging.info("Portfolio already initialized")


def build_portfolio(db_session):
    coins = crypto_api.get_coins()
    for coin in coins:
        db_session.add(Position(coin_id=coin['id'],
                                name=coin['name'],
                                symbol=coin['symbol'],
                                cost_basis=coin['current_price'],
                                quantity=1.00))
    db_session.commit()
    db_session.close()


def should_we_buy(db_session):
    positions = get_positions(db_session)
    moving_avg_dict = {}
    curr_prices = {}
    for position in positions:
        name = position[0]
        curr_prices[name] = crypto_api.get_current_price(name)
    for k in curr_prices:
        moving_avg_dict[k] = calculate_moving_avg(k)[0]
    logging.info(f"MOVING AVERAGES: {moving_avg_dict}")
    logging.info(f"CURRENT PRICES: {curr_prices}")
    for k in curr_prices:
        if curr_prices[k] < moving_avg_dict[k]:
            make_trade(k, 1, db_session, curr_prices[k])


def make_trade(coin_id, quantity, db_session, curr_price):
    crypto_api.submit_order(coin_id=coin_id, quantity=quantity, bid=curr_price)
    db_session.add(Trade(coin_id=coin_id, quantity=1, price=curr_price, trade_datetime = datetime.now()))
    decimal_curr_price = convert_float_to_decimal(curr_price)
    query = db_session.query(Position).filter(Position.coin_id == coin_id)
    position = query.all()[0]
    new_value = position.quantity * decimal_curr_price
    old_and_new_value = [position.cost_basis, new_value]
    query.update({"cost_basis": old_and_new_value[0] + decimal_curr_price, "quantity": position.quantity + 1})
    db_session.commit()
    position = query.all()[0]
    logging.info(f"PURCHASED {quantity} {coin_id} AT {decimal_curr_price}")
    logging.info(f"CURRENT {coin_id} QUANTITY: {position.quantity}")
    logging.info(f"CURRENT USD VALUE OF {coin_id} HOLDINGS: {new_value}")
    db_session.close()
    calculate_gain_loss(coin_id, old_and_new_value)


def log_total_portfolio_gain_loss(db_session):
    positions = get_positions(db_session)
    logging.info(f"PORTFOLIO GAIN/LOSS FOR ALL HOLDINGS:")
    for position in positions:
        name, cost_basis, quantity = position[0], position[1], position[2]
        new_val = convert_float_to_decimal(crypto_api.get_current_price(name)) * quantity
        logging.info(calculate_gain_loss(name, [cost_basis, new_val]))
        logging.info(f"TOTAL VALUE OF {name}: {new_val}")