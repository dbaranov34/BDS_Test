
import os
import csv
import datetime
import collections





csvPath = os.path.join(os.path.dirname(__file__),'testExamples','TRD2.csv')


## getting date will be added
## for now we just take today date


defaultDate=datetime.datetime.today()

window = collections.deque()

with open(csvPath) as csvFile:
    reader = csv.DictReader(csvFile)
    ## prepare counters and storage
    maxtrades = 0
    lasttimestap =datetime.datetime.today()
    for row in reader:
        ## prepare counters and storage

        time = datetime.datetime.strptime(row['Time'],'%H:%M:%S.%f').time()
        time = datetime.datetime.combine(defaultDate, time) ##convert terrible string to a nice timestamp
        timestamp=time.timestamp()*1000

        ##for the beginning we will ignore exchange name and just will define a maxIntercal for all of the exchanges
        if True: #row['EXCHANGE']=='V':
            window.append(timestamp)
            left = window.popleft()
            while timestamp-left>1000:
                if window:
                    left = window.popleft()
            window.appendleft(left)
            #print (window)
            if maxtrades<len(window):
                maxtrades=len(window)
                endTimestamp=timestamp

                print(maxtrades,endTimestamp)