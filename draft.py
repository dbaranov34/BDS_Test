import os
import csv
import datetime
import collections
from deal_window import DealWindow

if __name__ == '__main__':
    # getting file path
    csvPath = os.path.join(os.path.dirname(__file__), 'testExamples', 'TRD2.csv')

    deals = DealWindow()
    with open(csvPath) as csvFile:
        deals.analyze(csv.DictReader(csvFile))  # analyze what we read
        out_strings = DealWindow.format_answer(deals)

    for string in out_strings:
        print(out_strings[string])
