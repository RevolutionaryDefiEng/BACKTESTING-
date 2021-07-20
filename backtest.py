import backtrader as bt
import datetime


class RSIStrategy(bt.Strategy):
    global success
    success = 0
    global fail 
    fail = 0
    global lastEntered
    lastEntered = 0


    def notify_order(self, order):
        if not order.status == order.Completed:
            return  # discard any other notification
        if not order.alive():
            self.order = None  # indicate no order is pending
            
        global lastEntered
        global success
        global fail 

        if not self.position:  # we left the market
            # print('LEFT MARKWT @price: {:.2f}'.format(order.executed.price))
            if lastEntered < order.executed.price:
                success = success + 1
                # print("Success trade (long)")
            else:
                fail = fail + 1
                # print("Failed long trade")
            return

        if self.position:
            # We have entered the market
            # print('ENTERED MARKET @price: {:.2f}'.format(order.executed.price))
            lastEntered = order.executed.price

    def __init__(self):
        
        self.rsi = bt.talib.RSI(self.data, period=14)      

    def next(self):
        if self.rsi < 35 and not self.position:
            current = self.data.close[0]
            toBuy = cerebro.broker.getvalue() / current
            self.buy(size= toBuy)
        
        if self.rsi > 69 and self.position:
            self.close()


cerebro = bt.Cerebro()

fromdate = datetime.datetime.strptime('2017-01-01', '%Y-%m-%d')
todate = datetime.datetime.strptime('2020-07-12', '%Y-%m-%d')

data = bt.feeds.GenericCSVData(dataname='daily_2020.csv', dtformat=2, compression=15, timeframe=bt.TimeFrame.Minutes, fromdate=fromdate, todate=todate)

cerebro.adddata(data)

cerebro.addstrategy(RSIStrategy)

cerebro.run()
print("success = ", success, " Fails = ", fail)
cerebro.plot()

print("success = ", success, " Fails = ", fail)

#cerebro.run(runcone=not args.use_next, stdstats=False)



