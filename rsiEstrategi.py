//@version=4
//study(title="Divergence Indicator", format=format.price)
//GOOGL setting  5 , close, 3 , 1  profitLevel at 75 shows win rate  87.21 %  profit factor 7.059
//GOOGL setting  8 , close, 3 , 1  profitLevel at 80 shows win rate  86.57 %  profit factor 18.96 
//SPY setting    5, close , 3, 3  profitLevel at 70  , shows win rate 80.34%  profit factor 2.348
strategy(title="RSI Divergence Indicator", overlay=false,pyramiding=2, default_qty_value=2,   default_qty_type=strategy.fixed, initial_capital=10000, currency=currency.USD)

len = input(title="RSI Period", minval=1, defval=9)
src = input(title="RSI Source", defval=close)
lbR = input(title="Pivot Lookback Right", defval=3)
lbL = input(title="Pivot Lookback Left", defval=1)
takeProfitRSILevel = input(title="Take Profit at RSI Level", minval=70, defval=80)

rangeUpper = input(title="Max of Lookback Range", defval=60)
rangeLower = input(title="Min of Lookback Range", defval=5)
plotBull = input(title="Plot Bullish", defval=true)
plotHiddenBull = input(title="Plot Hidden Bullish", defval=true)
plotBear = input(title="Plot Bearish", defval=true)
plotHiddenBear = input(title="Plot Hidden Bearish", defval=false)

//useTrailStopLoss = input(false, title="Use Trailing Stop Loss")

sl_type = input("NONE", title="Trailing StopLoss Type", options=['ATR','PERC', 'NONE'])

stopLoss = input(title="Stop Loss%", defval=5, minval=1)

atrLength=input(14, title="ATR Length (for Trailing stop loss)")
atrMultiplier=input(3.5, title="ATR Multiplier (for Trailing stop loss)")


bearColor = color.purple
bullColor = color.green
hiddenBullColor = color.new(color.green, 80)
hiddenBearColor = color.new(color.red, 80)
textColor = color.white
noneColor = color.new(color.white, 100)

osc = rsi(src, len)

plot(osc, title="RSI", linewidth=2, color=#8D1699)
hline(50, title="Middle Line", linestyle=hline.style_dotted)
obLevel = hline(70, title="Overbought", linestyle=hline.style_dotted)
osLevel = hline(30, title="Oversold", linestyle=hline.style_dotted)
fill(obLevel, osLevel, title="Background", color=#9915FF, transp=90)

plFound = na(pivotlow(osc, lbL, lbR)) ? false : true
phFound = na(pivothigh(osc, lbL, lbR)) ? false : true

_inRange(cond) =>
    bars = barssince(cond == true)
    rangeLower <= bars and bars <= rangeUpper

//------------------------------------------------------------------------------
// Regular Bullish

// Osc: Higher Low
oscHL = osc[lbR] > valuewhen(plFound, osc[lbR], 1) and _inRange(plFound[1])

// Price: Lower Low
priceLL = low[lbR] < valuewhen(plFound, low[lbR], 1)

bullCond = plotBull and priceLL and oscHL and plFound

plot(
	 plFound ? osc[lbR] : na,
	 offset=-lbR,
	 title="Regular Bullish",
	 linewidth=2,
	 color=(bullCond ? bullColor : noneColor),
	 transp=0
	 )


plotshape(
	 bullCond ? osc[lbR] : na,
	 offset=-lbR,
	 title="Regular Bullish Label",
	 text=" Bull ",
	 style=shape.labelup,
	 location=location.absolute,
	 color=bullColor,
	 textcolor=textColor,
	 transp=0
	 )

//------------------------------------------------------------------------------
// Hidden Bullish

// Osc: Lower Low
oscLL = osc[lbR] < valuewhen(plFound, osc[lbR], 1) and _inRange(plFound[1])

// Price: Higher Low
priceHL = low[lbR] > valuewhen(plFound, low[lbR], 1)

hiddenBullCond = plotHiddenBull and priceHL and oscLL and plFound

plot(
	 plFound ? osc[lbR] : na,
	 offset=-lbR,
	 title="Hidden Bullish",
	 linewidth=2,
	 color=(hiddenBullCond ? hiddenBullColor : noneColor),
	 transp=0
	 )

plotshape(
	 hiddenBullCond ? osc[lbR] : na,
	 offset=-lbR,
	 title="Hidden Bullish Label",
	 text=" H Bull ",
	 style=shape.labelup,
	 location=location.absolute,
	 color=bullColor,
	 textcolor=textColor,
	 transp=0
	 )

longCondition=bullCond or hiddenBullCond
//? osc[lbR] : na  
//hiddenBullCond
strategy.entry(id="RSIDivLE", long=true,  when=longCondition)


//Trailing StopLoss
////// Calculate trailing SL
/////////////////////////////////////////////////////
sl_val = sl_type == "ATR"      ? stopLoss * atr(atrLength) : 
         sl_type == "PERC" ? close * stopLoss / 100 : 0.00

trailing_sl = 0.0
trailing_sl :=   strategy.position_size>=1 ?  max(low  - sl_val, nz(trailing_sl[1])) :  na

//draw initil stop loss
//plot(strategy.position_size>=1 ? trailing_sl : na, color = color.blue , style=plot.style_linebr,  linewidth = 2, title = "stop loss")
//plot(trailing_sl, title="ATR Trailing Stop Loss", style=plot.style_linebr, linewidth=1, color=color.purple, transp=30)
//Trailing StopLoss
////// Calculate trailing SL
/////////////////////////////////////////////////////


//------------------------------------------------------------------------------
// Regular Bearish

// Osc: Lower High
oscLH = osc[lbR] < valuewhen(phFound, osc[lbR], 1) and _inRange(phFound[1])

// Price: Higher High
priceHH = high[lbR] > valuewhen(phFound, high[lbR], 1)

bearCond = plotBear and priceHH and oscLH and phFound

plot(
	 phFound ? osc[lbR] : na,
	 offset=-lbR,
	 title="Regular Bearish",
	 linewidth=2,
	 color=(bearCond ? bearColor : noneColor),
	 transp=0
	 )

plotshape(
	 bearCond ? osc[lbR] : na,
	 offset=-lbR,
	 title="Regular Bearish Label",
	 text=" Bear ",
	 style=shape.labeldown,
	 location=location.absolute,
	 color=bearColor,
	 textcolor=textColor,
	 transp=0
	 )

//------------------------------------------------------------------------------
// Hidden Bearish

// Osc: Higher High
oscHH = osc[lbR] > valuewhen(phFound, osc[lbR], 1) and _inRange(phFound[1])

// Price: Lower High
priceLH = high[lbR] < valuewhen(phFound, high[lbR], 1)

hiddenBearCond = plotHiddenBear and priceLH and oscHH and phFound

plot(
	 phFound ? osc[lbR] : na,
	 offset=-lbR,
	 title="Hidden Bearish",
	 linewidth=2,
	 color=(hiddenBearCond ? hiddenBearColor : noneColor),
	 transp=0
	 )

plotshape(
	 hiddenBearCond ? osc[lbR] : na,
	 offset=-lbR,
	 title="Hidden Bearish Label",
	 text=" H Bear ",
	 style=shape.labeldown,
	 location=location.absolute,
	 color=bearColor,
	 textcolor=textColor,
	 transp=0
	 )
longCloseCondition=crossover(osc,takeProfitRSILevel) or bearCond
strategy.close(id="RSIDivLE", comment="Close All="+tostring(close - strategy.position_avg_price, "####.##"), when= abs(strategy.position_size)>=1  and  sl_type == "NONE" and longCloseCondition)

//close all on stop loss
strategy.close(id="RSIDivLE", comment="TSL="+tostring(close - strategy.position_avg_price, "####.##"),  when=abs(strategy.position_size)>=1 and (sl_type == "PERC"   or sl_type == "ATR" ) and crossunder(close, trailing_sl)  )  //close<ema55 and rsi5Val<20 //ema34<ema55  //close<ema89
