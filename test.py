import unittest
from seencars import *
import pandas as pd

class unitTest(unittest.TestCase):

    def setUp(self):
        # crate dataframe from 'data/data.csv' with enough data
        self.df = pd.read_csv('data/data.csv', sep=' ', header=None)
        self.df.columns = ['time', 'counts']

        # crate dataframe from 'data/data1.csv' with only two rows of data
        self.df1 = pd.read_csv('data/data1.csv', sep=' ', header=None)
        self.df1.columns = ['time', 'counts']

        # crate dataframe from 'data/data2.csv' with least three counts are in two different days
        self.df2 = pd.read_csv('data/data2.csv', sep=' ', header=None)
        self.df2.columns = ['time', 'counts']


    def tearDown(self):
        # Executed after reach test
        pass

    # test the total number of cars seen from totalCount function
    def test_total_count(self):
        self.assertEqual(398, totalCount(self.df))
        self.assertEqual(17, totalCount(self.df1))

    # test the array result from dailyCount function
    def test_daily_count(self):
        self.assertEqual(4, len(dailyCount(self.df)))
        self.assertEqual("2021-12-01 179", dailyCount(self.df)[0])
        self.assertEqual("2021-12-05 81", dailyCount(self.df)[1])
        self.assertEqual("2021-12-08 134", dailyCount(self.df)[2])
        self.assertEqual("2021-12-09 4", dailyCount(self.df)[3])
        self.assertEqual(1, len(dailyCount(self.df1)))
        self.assertEqual("2021-12-01 17", dailyCount(self.df1)[0])

    # test the array result from topThreeCounts function
    def test_top_three_counts(self):
        self.assertEqual(46, topThreeCounts(self.df)[0][1])
        self.assertEqual(42, topThreeCounts(self.df)[1][1])
        self.assertEqual(33, topThreeCounts(self.df)[2][1])
        self.assertEqual(2, len(topThreeCounts(self.df1)))


    # test the array result from findLeastCarsInThreeHalfHour function
    def test_find_least_cars_in_three_half_hours(self):
        # three counts in the same day with df
        self.assertEqual(31, findLeastCarsInThreeHalfHour(self.df)[2])

        # no three counts founded with df1
        self.assertEqual('', findLeastCarsInThreeHalfHour(self.df1)[0])

        # three counts in two days with df2
        self.assertEqual('2021-12-08T23:00:00',
                         findLeastCarsInThreeHalfHour(self.df2)[0])
        self.assertEqual('2021-12-09T00:30:00',
                         findLeastCarsInThreeHalfHour(self.df2)[1])
        self.assertEqual(4, findLeastCarsInThreeHalfHour(self.df2)[2])
        

    
    # test the reading file error when executing countingCars function
    def test_read_file_error_counting_cars(self):
        # a file not exist
        error1 = seenCars('data/testing')
        # an empty file
        error2 = seenCars('data/empty.csv')

        self.assertEqual(True, error1)
        self.assertEqual(True, error2)

if __name__ == "__main__":
    # You can run this file using:  python test.py
    unittest.main()
