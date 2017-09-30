import os
import csv
import datetime
import collections

def csvExchangeLogAnalyzer(path):
    dealLog = {}
    with open(path) as csvFile:
        reader = csv.DictReader(csvFile)  # engage csv-reader
        maxDeals = {}  # prepare counters for deals during or interval
        topTimestamp = {}  # prepare storages for found timestamps

        for row in reader:
            (timestamp, exchange) = parserow(row)  # parse new row
            if not (exchange in dealLog):  # If met new echange
                dealLog[exchange] = collections.deque()  # create new list in exchange list
                maxDeals[exchange] = 0  # create new counter for each exchange
                topTimestamp[exchange] = 0  # create new timestamp for each exchange

            step(dealLog[exchange], timestamp)  # put timestamp in the corresponding list and do the maths

            if len(dealLog[exchange]) > maxDeals[exchange]:  # check if we have more deals in the interval than before
                maxDeals[exchange] = len(dealLog[exchange])  # upd counteer
                topTimestamp[exchange] = timestamp  # upd timestamp

    return (dealLog,topTimestamp,maxDeals)

def printAnswer(dealLog,topTimestamp, maxDeals):
    for exchange in dealLog:
        endOfWindow = getTimeWithMs(topTimestamp[exchange]/1000)    #get back to readable format
        beginningOfWindow = getTimeWithMs((topTimestamp[exchange]-1000)/1000+0.001)     #get the beginning of the current second

        print ("Maximum deals during one-second window was registered at exchange {} between {} and {}. {} deals were performed at that second".format(exchange, beginningOfWindow, endOfWindow, maxDeals[exchange]))

        # TODO: ask, how do they prefer to define the interval? By the median, left or right border.


def getTimeWithMs(time):                        #formatting shortcut
    return (datetime.datetime.fromtimestamp(time).strftime('%H:%M:%S.%f')[:-3])


def step(window, timestamp, interval = 1000):   #main algorythm
    window.append(timestamp)                    #append timestamp to theend of list
    left = window.popleft()                     #look at the beginning of the list
    while timestamp - left > interval:          #While the list contains the timestamps outside the interval
        if window:                              #if not empty
            left = window.popleft()             #pop another timestamp until we done
    window.appendleft(left)                     #revert the last popped left element back when it valid

    return window                               #return window


def parserow(row):                                      #row parser
    time = datetime.datetime.strptime(row['Time'], '%H:%M:%S.%f').time()  ##convert terrible string to a nice timestamp
    time = datetime.datetime.combine(defaultDate, time)  #append a fictious date to avoid negative timestamps
    timestamp = time.timestamp() * 1000                  #store miliseconds

    return (timestamp,row['EXCHANGE'])          #return timestamp and exchange name


#getting file path
csvPath = os.path.join(os.path.dirname(__file__),'testExamples','TRD2.csv')
defaultDate = datetime.datetime.today()

(dealLog, topTimestamp, maxDeals) =csvExchangeLogAnalyzer(csvPath)
printAnswer(dealLog, topTimestamp, maxDeals)