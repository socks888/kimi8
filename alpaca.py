import requests
import config
import time, json

"""
headers = {
    "APCA-API-KEY-ID": config.API_KEY,
    "APCA-API-SECRET-KEY": config.API_SECRET
}

trade_params = {
"symbol" : params["symbol"],
"quantity" : data["filled_qty"],
"average_fill_price" : data["filled_avg_price"],
"side" : params["side"]
}
"""

headers = {"APCA-API-KEY-ID":config.alpaca_key, "APCA-API-SECRET-KEY":config.alpaca_secret}
account_url = f"{config.BASE_URL}/v2/account"
positions_url = f"{config.BASE_URL}/v2/positions"
orders_url = f"{config.BASE_URL}/v2/orders"

#f"{config.BASE_URL}/v2/orders/{order_id}"

def submit_order(symbol, quantity, side, type, tif):
    trade_params = {
    "symbol" : symbol,
    "qty" : quantity,
    "side" : side,
    "type" : type,
    "time_in_force" : tif
    }
    order = requests.post(orders_url, json=trade_params, headers=headers)
    resp = order.json()

    order_id = resp["id"]
    time.sleep(1)
    new_order_status = f"{config.BASE_URL}/v2/orders/{order_id}"
    resp = requests.get(new_order_status, headers=headers)
    data = resp.json()
    print(data)
    return order

submit_order("BTCUSD", 0.01, "buy", "market", "day")
