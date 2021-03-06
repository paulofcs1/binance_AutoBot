from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from datetime import datetime
from decimal import *
from decimal import Decimal
from flask import Flask
from flask_cors import CORS
from multiprocessing import Process, Value
import math
import time
import sys, os
import logging
from bot import Bot

app = Flask(__name__)
cors = CORS(app, resource={r"/*":{"origins": "*"}})

key = os.environ.get('API_KEY')
secret = os.environ.get('API_SECRET')
coin = os.environ.get('COIN')
minimalQtd = os.environ.get('MINIMAL_COIN_BUY')
minimalProfit = os.environ.get('MINIMAL_PROFIT_USD')
leverage = os.environ.get('COIN_LEVERAGE')

# --------------------------- Tesnet API Keys -------------------------------------------

# g_api_key = '9ed2810f070aa3c9378af0a828cdc46c6a20a347f9c80004e37a26f5d373e3b5'
# g_secret_key = 'c2340bebf086e113b6e3bd52f5bd17ccb201649a8f2b82804dec531a7fb16b0f'
# coin = 'BTCUSDT'
# minimalQtd = 0.001
# minimalProfit = 0.35
# leverage = 100
# --------------------------- Init Client -------------------------------------------
try:
    # request_client = RequestClient(api_key=key, secret_key=secret, url='https://testnet.binancefuture.com/')
    request_client = RequestClient(api_key=key, secret_key=secret,  url='https://fapi.binance.com')
    #  request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key, url='https://testnet.binancefuture.com/')
except Exception as e:
    print("ERROR: Connecting to client")
else:
    print("INFO: Connected to client")

# coin = 'BTCUSDT'
# minimalQtd = 0.001
# minimalProfit = 0.5
# leverage = 100

backtest = Bot(request_client, coin, float(minimalQtd), float(minimalProfit), float(leverage))

# try:
#
#     close = numpy.random.random(100)
#     print(close)
#     moving_average = talib.RSI(close)
#
#     print(moving_average)
# except Exception as e:
#     print("EROOR")

# This function provides utility functions to work with Strings
# 1. reverse(s): returns the reverse of the input string
# 2. print(s): prints the string representation of the input object
def record_loop():
    global request_client

    backtest.init_strategy()

    current = 0
    while (True):
        try:
            dataNow = datetime.now().minute
            # check the server connection
            if dataNow != current:
                if (dataNow % 5) == 0:
                    result = backtest.get_servertime()

                    if result != 0:
                        current = dataNow

                        backtest.positionSize = 0
                        backtest.get_open_positions(backtest.coin)
                        if backtest.positionSize == 0:
                            backtest.buyStatus = 0
                        backtest.process_Price()
                        print("INFO: Bot -> ON ")

                    else:
                        try:
                            request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key,
                                                       url='https://testnet.binancefuture.com/')
                        except Exception as e:
                            print(e)
                            print("ERROR: restarting client")
                        else:
                            print("INFO: Cient restarted")

        except Exception as e:
            print(e)

    # This function provides utility functions to work with Strings
    # 1. reverse(s): returns the reverse of the input string
    # 2. print(s): prints the string representation of the input object

@app.route("/", methods=['GET'])
def index():
    return "<h1>Hello World!</h1>"

    # This function provides utility functions to work with Strings
    # 1. reverse(s): returns the reverse of the input string
    # 2. print(s): prints the string representation of the input object
def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

    # This function provides utility functions to work with Strings
    # 1. reverse(s): returns the reverse of the input string
    # 2. print(s): prints the string representation of the input object
if __name__ == '__main__':
    p = Process(target=record_loop)
    p.start()
    main()
    p.join()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
