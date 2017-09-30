import unittest
import os
import csv
from deal_window import DealWindow


class MyTestCase(unittest.TestCase):
    def test_init(self):
        window = DealWindow()
        self.assertEqual(len(window.dealLog), 0)
        self.assertEqual(len(window.maxDeals), 0)
        self.assertEqual(len(window.topTimestamp), 0)

    def test_add_exchange(self):
        window = DealWindow()
        window.add_exchange("nam")
        self.assertEqual(len(window.dealLog), 1)
        self.assertEqual(len(window.maxDeals), 1)
        self.assertEqual(len(window.topTimestamp), 1)

    def test_empty_printer(self):
        window = DealWindow()
        window.format_answer()
        self.assertEqual(window.format_answer(), {})

    def test_one_deal(self):
        csvPath = os.path.join(os.path.dirname(__file__), 'testExamples', 'oneExch_oneDeal.csv')
        deals = DealWindow()
        with open(csvPath) as csvFile:
            DealWindow.analyze(deals, csv.DictReader(csvFile))
        self.assertEqual(deals.dealLog.keys(), {'Q'})
        self.assertEqual(deals.maxDeals, {'Q': 1})
        self.assertEqual(deals.format_answer(), {
            'Q': 'Maximum deals during one-second window was registered at exchange Q between 10:01:59.783 and 10:02:00.782. 1 deals were performed at that second'})

    def test_ten_deals(self):
        csvPath = os.path.join(os.path.dirname(__file__), 'testExamples', 'oneExch_tenDeals_psec.csv')
        deals = DealWindow()
        with open(csvPath) as csvFile:
            DealWindow.analyze(deals, csv.DictReader(csvFile))
        self.assertEqual(deals.dealLog.keys(), {'Q'})
        self.assertEqual(deals.maxDeals, {'Q': 10})
        self.assertEqual(deals.format_answer()['Q'],
                         'Maximum deals during one-second window was registered at exchange Q between 10:01:59.775 and 10:02:00.774. 10 deals were performed at that second')

    def test_ten_deals_4spec(self):
        csvPath = os.path.join(os.path.dirname(__file__), 'testExamples', 'oneExch_tenDeals_4psec.csv')
        deals = DealWindow()
        with open(csvPath) as csvFile:
            DealWindow.analyze(deals, csv.DictReader(csvFile))
        self.assertEqual(deals.dealLog.keys(), {'Q'})
        self.assertEqual(deals.maxDeals, {'Q': 4})
        self.assertEqual(deals.format_answer()['Q'],
                         'Maximum deals during one-second window was registered at exchange Q between 10:01:59.743 and 10:02:00.742. 4 deals were performed at that second')

    def test_ten_deals_4spec2(self):
        csvPath = os.path.join(os.path.dirname(__file__), 'testExamples', 'oneExch_tenDeals_4psec2.csv')
        deals = DealWindow()
        with open(csvPath) as csvFile:
            DealWindow.analyze(deals, csv.DictReader(csvFile))
        self.assertEqual(deals.dealLog.keys(), {'Q'})
        self.assertEqual(deals.maxDeals, {'Q': 4})
        self.assertEqual(deals.format_answer()['Q'],
                         'Maximum deals during one-second window was registered at exchange Q between 10:02:02.763 and 10:02:03.762. 4 deals were performed at that second')

    def test_twoExch_tenDeals_3psec(self):
        csvPath = os.path.join(os.path.dirname(__file__), 'testExamples', 'twoExch_tenDeals_3psec.csv')
        deals = DealWindow()
        with open(csvPath) as csvFile:
            DealWindow.analyze(deals, csv.DictReader(csvFile))
        self.assertEqual(deals.dealLog.keys(), {'Q', 'z'})
        self.assertEqual(deals.maxDeals, {'Q': 3, 'z': 2})
        self.assertEqual(deals.format_answer()['Q'],
                         'Maximum deals during one-second window was registered at exchange Q between 10:01:59.753 and 10:02:00.752. 3 deals were performed at that second')
        self.assertEqual(deals.format_answer()['z'],
                         'Maximum deals during one-second window was registered at exchange z between 10:01:59.743 and 10:02:00.742. 2 deals were performed at that second')

    def test_twoExch_twoDeals(self):
        csvPath = os.path.join(os.path.dirname(__file__), 'testExamples', 'twoExch_twoDeals.csv')
        deals = DealWindow()
        with open(csvPath) as csvFile:
            DealWindow.analyze(deals, csv.DictReader(csvFile))
        self.assertEqual(deals.dealLog.keys(), {'Q', 'z'})
        self.assertEqual(deals.maxDeals, {'Q': 1, 'z': 1})
        self.assertEqual(deals.format_answer()['Q'],
                         'Maximum deals during one-second window was registered at exchange Q between 10:01:59.713 and 10:02:00.712. 1 deals were performed at that second')
        self.assertEqual(deals.format_answer()['z'],
                         'Maximum deals during one-second window was registered at exchange z between 10:01:59.723 and 10:02:00.722. 1 deals were performed at that second')


if __name__ == '__main__':
    unittest.main()
