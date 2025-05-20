from pybit.unified_trading import HTTP
import pandas as pd
from ta.momentum import RSIIndicator
import math
from decimal import Decimal, ROUND_DOWN, ROUND_FLOOR
import time

# Configuración del cliente API
api_key = "8haYfkWVTkoIjyvaGM"
api_secret = "7jD6Q1VJVzkCRlaajGnhkLjJl27EUjILncqN"
symbol = "BTCUSDT"
timeframe = "1"  # Intervalo de tiempo 1,3,5,15,30,60,120,240,360,720,D,M,W
rsi_periodo = 14
usdt = 10  # Cantidad en dolares que se va a operar

tp_percent = 0.2  # Take profit porcentaje
sl_percent = 0.4  # Stop loss porcentaje

client = HTTP(api_key=api_key, api_secret=api_secret, testnet=True)

# Datos de la moneda
step = client.get_instruments_info(category="linear", symbol=symbol)
ticksize = float(step['result']['list'][0]['priceFilter']['tickSize'])
scala_precio = int(step['result']['list'][0]['priceScale'])
precision_step = float(step["result"]["list"][0]["lotSizeFilter"]["qtyStep"])


def obtener_datos_historicos(symbol, interval):
    """Obtiene datos históricos de velas."""
    response = client.get_kline(category="linear", symbol=symbol, interval=interval, limit=200)
    # print(response['result']['list'][0])
    if "result" in response:
        df = pd.DataFrame(response['result']['list']).astype(float)
        return df[4]
    else:
        raise Exception("Error al obtener datos históricos: " + str(response))


def obtener_rsi(data, periodo):
    # Calcular el RSI
    rsi = RSIIndicator(close=data, window=periodo).rsi()
    smoothed_rsi = rsi.rolling(window=periodo).mean()
    return smoothed_rsi.iloc[-1]


def qty_precision(qty, precision):
    qty = math.floor(qty / precision) * precision
    return qty


def qty_step(price):
    precision = Decimal(f"{10 ** scala_precio}")
    tickdec = Decimal(f"{ticksize}")
    precio_final = (Decimal(f"{price}") * precision) / precision
    precide = precio_final.quantize(Decimal(f"{1 / precision}"), rounding=ROUND_FLOOR)
    operaciondec = (precide / tickdec).quantize(Decimal('1'), rounding=ROUND_FLOOR) * tickdec
    result = float(operaciondec)

    return result


def crear_orden(symbol, side, order_type, qty):
    response = client.place_order(
        category="linear",  # Linear para futuros USDT
        symbol=symbol,
        side=side,
        orderType=order_type,
        qty=qty,  # Cantidad calculada y ajustada
        timeInForce="GoodTillCancel"  # Validez de la orden
    )
    print("Orden creada con éxito:", response)


def establecer_stop_loss(symbol, sl):
    sl = qty_step(sl)

    # PONER ORDEN STOP LOSS
    order = client.set_trading_stop(
        category="linear",
        symbol=symbol,
        stopLoss=sl,
        slTriggerB="LastPrice",
        positionIdx=0,
    )

    return order

def establecer_take_profit(symbol, tp, side, qty):
    price = qty_step(tp)

    # PONER ORDEN TAKE PROFIT
    order = client.place_order(
        category="linear",
        symbol=symbol,
        side=side,
        orderType="Limit",
        reduceOnly=True,
        qty=qty,
        price=price,
    )

    return order


stop = False
tipo = ""
qty = 0
while True:
    try:
        posiciones = client.get_positions(category="linear", symbol=symbol)
        if float(posiciones['result']['list'][0]['size']) != 0:
            print("Hay una posicion abierta en " + symbol)
            if not stop:
                precio_de_entrada = float(posiciones['result']['list'][0]['avgPrice'])
                if posiciones['result']['list'][0]['side'] == 'Buy':
                    stop_loss_price = precio_de_entrada * (1 - sl_percent / 100)
                    take_profit_price = precio_de_entrada * (1 + tp_percent / 100)
                    establecer_stop_loss(symbol, stop_loss_price)
                    establecer_take_profit(symbol, take_profit_price, "Sell", qty)
                    print("Stop loss y Take profit activados")
                    stop = True
                else:
                    stop_loss_price = precio_de_entrada * (1 + sl_percent / 100)
                    take_profit_price = precio_de_entrada * (1 - tp_percent / 100)
                    establecer_stop_loss(symbol, stop_loss_price)
                    establecer_take_profit(symbol, take_profit_price, "Buy", qty)
                    print("Stop loss y Take profit activados")
                    stop = True
        else:
            stop = False
            qty = 0
            # Obtener datos historicos
            data = obtener_datos_historicos(symbol, timeframe)
            # Obtener RSI
            rsi = obtener_rsi(data, rsi_periodo)
            print(round(rsi, 2))

            if rsi >= 70: # Valor del RSI para iniciar un SHORT
                precio = client.get_tickers(category='linear', symbol=symbol)
                precio = float(precio['result']['list'][0]['lastPrice'])
                precision = precision_step
                qty = usdt / precio
                qty = qty_precision(qty, precision)
                if qty.is_integer():
                    qty = int(qty)  # Convertir a entero si no tiene decimales
                print("Cantidad de monedas: " + str(qty))
                if tipo == "long" or tipo == "":
                    crear_orden(symbol, "Sell", "Market", qty)
                    tipo = "short"

            if rsi <= 30: # Valor del RSI para iniciar un LONG
                precio = client.get_tickers(category='linear', symbol=symbol)
                precio = float(precio['result']['list'][0]['lastPrice'])
                precision = precision_step
                qty = usdt / precio
                qty = qty_precision(qty, precision)
                if qty.is_integer():
                    qty = int(qty)  # Convertir a entero si no tiene decimales
                print("Cantidad de monedas: " + str(qty))
                if tipo == "short" or tipo == "":
                    crear_orden(symbol, "Buy", "Market", qty)
                    tipo = "long"

            print("")
        time.sleep(1)

    except Exception as e:
        print(f"Error en el bot: {e}")
        time.sleep(60)
