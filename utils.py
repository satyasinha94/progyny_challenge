import crypto_api
import pandas
import logging
from decimal import Decimal
"""
This is where helper functions go.
"""


def calculate_gain_loss(coin, values):
    values_df = pandas.DataFrame(values).round(2)
    values_df_pct = values_df.pct_change().values[-1][0]
    logging.info(f"{coin} GAIN/LOSS: {round(100 * values_df_pct, 2)} %")
    return

def calculate_moving_avg(coin_id):
    price_history = crypto_api.get_coin_price_history(coin_id)
    prices = pandas.DataFrame({'Moving Avg': [x[1] for x in price_history]})
    return prices.rolling(10).mean().values[-1]

def convert_float_to_decimal(float_val):
    return Decimal(float_val).quantize(Decimal('1.00'))
