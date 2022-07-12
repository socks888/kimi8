import yfinance as yf
import vectorbt as vbt
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 1) download from YF
# 2) check df for sorting order last entry (0 or -1?) === YF is LAST entry, TWELVE is FIRST entry
# 3) get average of window closes
# 4) loop through 5 different tas and insert into DB
# 5) optimize and insert into DB
# 6) show summary with react (check rapid api tutorial on this on Twitter), but FIRST STREAMLIT

# start = '2022-01-01 UTC' crypto is in UTC
start = '2022-01-01'  # crypto is in UTC
end = '2022-07-01'

stocks = ['CRWD', 'ZS']
for symbol in stocks:
    stock_price = vbt.YFData.download(symbol, start=start, end=end).get('Close')

    fast_ma = vbt.MA.run(stock_price, 2, short_name='fast')
    slow_ma = vbt.MA.run(stock_price, 5, short_name='slow')

    entries = fast_ma.ma_crossed_above(slow_ma)
    exits = fast_ma.ma_crossed_below(slow_ma)
    #pf_return = pf.total_return()
    pf = vbt.Portfolio.from_signals(stock_price, entries=entries, exits=exits)
    #print(f"{symbol}:", pf_return )
    print(pf.stats())

def log_trade(trade_params):
    symbol =  trade_params["symbol"]
    quantity = trade_params["quantity"]
    average_fill_price = trade_params["average_fill_price"]
    side = trade_params["side"]
    timestamp = datetime.datetime.now()
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    time = now.strftime("%H-%M-%S")
    if not os.path.isdir("trades"):
        os.mkdir("trades")
    if not os.path.isfile(f"trades/{today}.csv"):
        with open(f"trades/trades_{today}.csv", "w") as trade_file:
            trade_file.write(
                "symbol, quantity, price, side, date\n"
            )
    else:
        with open(f"trades/trades_{today}.csv", "a+") as trade_file:
            trade_file.write(
                f"{symbol}, {quantity}, {average_fill_price}, {side}, {timestamp}\n"
                )
    log(f"{side} {quantity} {symbol} at {average_fill_price} on {timestamp}")
    return trade_params

def log(msg):
    print(f"Log: {msg}")
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    time = now.strftime("%H-%M-%S")
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    if not os.path.isfile(f"logs/logs_{today}.csv"):
        with open(f"logs/logs_{today}.txt", "a+") as log_file:
            log_file.write(f"{time} : {msg}\n")
    else:
        with open(f"logs/logs_{today}.txt", "a+") as log_file:
            log_file.write(f"{time} : {msg}\n")

    return msg

def submit_order(account, params):

    if params["side"] == "buy":
        account["is_buying"] = False
        print("we just bought")
    else:
        account["is_buying"] = True
        print("we just sold")
    with open("bot_account.json", "w") as f:
        f.write(json.dumps(account))

    order = requests.post(orders_url, json=params, headers=headers)
    resp = order.json()
    order_id = resp["id"]
    time.sleep(1)
    new_order_status = f"{config.BASE_URL}/v2/orders/{order_id}"
    resp = requests.get(new_order_status, headers=headers)
    data = resp.json()
    trade_params = {
    "symbol" : params["symbol"],
    "quantity" : data["filled_qty"],
    "average_fill_price" : data["filled_avg_price"],
    "side" : params["side"]
    }
    log_trade(trade_params)

    return order
