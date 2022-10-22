from logging import exception, raiseExceptions
import sys
import pandas as pd
from dateutil import parser
from datetime import timedelta
import filepath


FILE_PATH = filepath.FILE_PATH


def seenCars(file_path):
    # read data from csv file using pandas, check if file is valid(not empty) or exist
    try:
        df = pd.read_csv(file_path, sep=' ', header=None)
    except:
        error = True
        print(sys.exc_info()[1])
        return error

    # assign column names with time, and counts
    df.columns = ['time', 'counts']

    # call the totalCount function
    total_counts = totalCount(df)
    print(f'The number of cars seen in total is {total_counts}.')

    # call the dailyCount function, get an array containing daily counts data
    sequence_of_lines = dailyCount(df)
    printSequence(sequence_of_lines)

    # call topThreeCounts function, get the array of top three half hours with most cars
    three_most_cars = topThreeCounts(df)
    printTopThreeMostCars(three_most_cars)

    # call findLeastCarsInThreeHalfHour to get the least sums of cars in a continious 1.5 hours period
    start, end, least_sum = findLeastCarsInThreeHalfHour(df)
    printLeastCars(start, end, least_sum)
    
    return



# get the total counts
def totalCount(df: pd.DataFrame) -> int:
    total_counts = 0

    # iterate each count in the data
    for idx in df.index:
        current_counts = df['counts'][idx]
        total_counts += current_counts
    return total_counts



# get the array of daily counts
def dailyCount(df: pd.DataFrame) -> list:
    # use this variable to record the sum of counts during current day
    current_day_counts = 0
    # use this variable to determine if current day is the same day as previous
    previous_day = ''
    # store the (date, counts) in an array
    sequence_of_daily_counts = []

    for idx in df.index:
        # get the current day YYYY-MM-DD, 10 chs in total
        current_day = df['time'][idx][0:10]
        # get the current count
        current_counts = df['counts'][idx]

        # check if current day is the same as previous day
        # if previous day is not null, meaning previous day is not at start point of the data
        # or previous day is not the same as current day
        if previous_day != '' and previous_day != current_day:
            # reach the data of another day
            # firstly append the previous day data to the sequence
            sequence_of_daily_counts.append(
                previous_day + ' ' + str(current_day_counts))

            # re-assgin current_counts with current_day_counts
            current_day_counts = current_counts
        # if previous day is empty str or previous day is the same as current day
        else:
            # increase current_day_counts with current_counts
            current_day_counts += current_counts

        # update previous day with current day
        previous_day = current_day

    # the last day need to be added to the sequence array
    sequence_of_daily_counts.append(
        previous_day + ' ' + str(current_day_counts))

    return sequence_of_daily_counts


# print the sequence
def printSequence(sequence_of_lines: list):
    print('The sequence is:')
    for count in sequence_of_lines:
        print(count)
    return


# get top three counts in half hour
def topThreeCounts(df: pd.DataFrame) -> list:
    # get top three half hours wiht most cars according to counts in pandas dataframe
    top_three_df = df.nlargest(n=3, columns=['counts'])
    # convert the dataframe to array
    top_three_arr = top_three_df.to_numpy()
    return top_three_arr

# print top three most cars
def printTopThreeMostCars(three_most_cars: list):
    if len(three_most_cars) == 3:
        print('The top 3 half hours with most cars:')
        for count in three_most_cars:
            print(count[0], count[1])
    else:
        print('There are less than 3 sets of data in the file!')
    return


# find the least cars in a continuous one and half hours
def findLeastCarsInThreeHalfHour(df: pd.DataFrame) -> list:
    # using start and end to record the time period with least cars
    start = ''
    end = ''

    # initialize the least sum with the inf 
    least_sum = float('inf')

    # get the length of the df.index
    length = len(df.index)

    # using sliding window to find out the least sum of three
    # continious counts in one day
    left, right = 0, 0
    # using cur_sum to store the current counts sum (maxinum three sum)
    cur_sum = 0
    while right < length:
        # get current counts
        cur_counts = df['counts'][right]
        cur_sum += cur_counts

        # check if current data is the next half hour data of previous one
        previous_idx = max(left, right - 1)
        previous_time = df['time'][previous_idx]
        current_time = df['time'][right]
        # parse the string time into ISO 8601
        previous_time_formated = parser.parse(previous_time)
        current_time_formated = parser.parse(current_time)
        # get the time interval
        interval = current_time_formated - previous_time_formated

        # if interval.senconds larger than 1800, means current data is not continious with previous one
        if interval.seconds > 1800:
            cur_sum = cur_counts
            left = right
            right += 1

        #  if there are three elements in the window, compare cur_sum with least_sum
        elif right - left + 1 == 3:
            if least_sum > cur_sum:
                least_sum = cur_sum
                start = df['time'][left]

            # remove the left counts from cur_sum
            cur_sum -= df['counts'][left]
            # moving the window forward
            right += 1
            left += 1
        else:
            # if the window has not included three elements
            right += 1

    # if least_sum is not updated, meaning there is no continuous 1.5 hours in the given data
    if least_sum == float('inf'):
        least_sum = 0

    # if start is not a empty string, meaning that we find a valid least sum
    # then update the end time by adding 1.5 hours to the start
    if start != '':
        start_formated = parser.parse(start)
        end_formated = start_formated + timedelta(hours=1.5)
        end = end_formated.isoformat()

    return start, end, least_sum

# print least cars in continuous 1.5 hours
def printLeastCars(start: str, end: str, least_sum: int):
    if least_sum == 0:
        print(
            'The file does not contain any sets of data which are continuous for 1.5 hours!')
    else:
        print('The continuous 1.5 hours period with least cars:')
        print(
            f"From {start} to {end}, the least number of cars is {least_sum}.")
    return


if __name__ == '__main__':
    # You can run this file using:  python countingcars.py
    seenCars(FILE_PATH)