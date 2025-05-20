### RSI Bot de trading para futuros de Bybit

Este bot fue desarrollado para abrir y cerrar operaciones con el indicador RSI.

**Como usar el script**
- Descargar python [Aqui](https://www.python.org/ "Aqui")
- Descargar y modificar el Archivo script.py, el archivo lo puedes modificar con sublime text o algun otro editor de codigo como pycharm.
- Recuerda agregar las apis de Bybit, las apis las puedes encontrar [Aqui](https://partner.bybit.com/b/GafasTrading "Aqui")
- Ahora busca las siguientes lineas y modificalas a tu gusto.
```python
# Configuración del cliente API
api_key = ""
api_secret = ""
symbol = "BTCUSDT"
timeframe = "5"  # Intervalo de tiempo 1,3,5,15,30,60,120,240,360,720,D,M,W
rsi_periodo = 14
usdt = 10  # Cantidad en dolares que se va a operar

tp_percent = 0.2  # Take profit porcentaje
sl_percent = 0.4  # Stop loss porcentaje

if rsi >= 70: # Valor del RSI para iniciar un SHORT
if rsi <= 30: # Valor del RSI para iniciar un LONG
```
- Una vez guardado el archivo debes ejecutarlo desde una terminal de windows o de tu sistema operativo que uses con el siguiente comando.
`python script.py`

#### Contact
- Twitter: [https://twitter.com/ElGafasTrading](https://twitter.com/ElGafasTrading "https://twitter.com/ElGafasTrading")
- Instagram: [https://www.instagram.com/elgafastrading/](https://www.instagram.com/elgafastrading/ "https://www.instagram.com/elgafastrading/")
- Youtube: [https://www.youtube.com/@ElGafasTrading](https://www.youtube.com/@ElGafasTrading "https://www.youtube.com/@ElGafasTrading")
