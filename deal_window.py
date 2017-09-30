import collections
import csv
from datetime import datetime

defaultDate = datetime.today()


def getTimeWithMs(time):                        #formatting shortcut
    return (datetime.fromtimestamp(time).strftime('%H:%M:%S.%f')[:-3])

def parserow(row):                                      #row parser
    time = datetime.strptime(row['Time'], '%H:%M:%S.%f').time()  ##convert terrible string to a nice timestamp
    time = datetime.combine(defaultDate, time)  #append a fictious date to avoid negative timestamps
    timestamp = time.timestamp() * 1000                  #store miliseconds
    return (timestamp,row['EXCHANGE'])          #return timestamp and exchange name

def step(window, timestamp, interval = 1000):   #main algorithm
    window.append(timestamp)                    #append timestamp to theend of list
    left = window.popleft()                     #look at the beginning of the list
    while timestamp - left > interval:          #While the list contains the timestamps outside the interval
        if window:                              #if not empty
            left = window.popleft()             #pop another timestamp until we done

    if timestamp - left <= interval:
        window.appendleft(left)                     #revert the last popped left element back when it valid


class DealWindow:
    dealLog = {}
    maxDeals={}
    topTimestamp={}

    def __init__(self):
        self.dealLog = {}
        self.maxDeals = {}
        self.topTimestamp = {}

    def add_exchange(self, name):
        self.dealLog[name] = collections.deque()
        self.maxDeals[name] = 0
        self.topTimestamp[name] = 0


    def update_deal_counter(self, exchange, timestamp):
        if len(self.dealLog[exchange]) > self.maxDeals[exchange]:   # check if we have more deals in the interval than before
            self.maxDeals[exchange] = len(self.dealLog[exchange])   # upd counter
            self.topTimestamp[exchange] = timestamp                 # upd timestamp


    def analyze(self,reader):
        for row in reader:
            (timestamp, exchange) = parserow(row)  # parse row
            if not (exchange in self.dealLog): # If met new exchange name
                DealWindow.add_exchange(self,exchange)
            step(self.dealLog[exchange], timestamp)  # put timestamp in the corresponding list and do the maths
            DealWindow.update_deal_counter(self, exchange, timestamp)


    def format_answer(self):
        out_strings = {}
        for exchange in self.dealLog:
            endOfWindow = getTimeWithMs(self.topTimestamp[exchange]/1000)    #get back to readable format
            beginningOfWindow = getTimeWithMs((self.topTimestamp[exchange]-1000)/1000+0.001)     #get the beginning of the current second
            out_strings[exchange] = "Maximum deals during one-second window was registered at exchange {} between {} and {}. {} deals were performed at that second".format(exchange, beginningOfWindow, endOfWindow, self.maxDeals[exchange])
            # TODO: ask, how do they prefer to define the interval? By the median, left or right border.
        return out_strings





