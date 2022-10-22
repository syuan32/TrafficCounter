# Automatic Traffic Counter Data Management App

An automated traffic counter sits by a road and counts the number of cars that go past. Every half-hour the counter outputs the number of cars seen and resets the counter to zero. This program is to read a file generated from the automatic counter, where each line contains a timestamp (in yyyy-mm- ddThh:mm:ss format, i.e. ISO 8601) for the beginning of a half-hour and the number of cars seen that half hour. Then, it will output four parts of information:
1. The number of cars seen in total
2. A sequence of lines where each line contains a date (in yyyy-mm-dd format) and the
number of cars seen on that day (eg. 2016-11-23 289) for all days listed in the input file.
3. The top 3 half hours with most cars, in the same format as the input file
4. The 1.5 hour period with least cars (i.e. 3 contiguous half hour records)

## Getting Started
You will need Python 3.9 (recommended) or older.

## Running
The default file path is store in filepath.py, and feel free to change it when using.

From the app home directory, to run the program, execute:
```
python3 seencars.py
```
You should see something like:
```
The number of cars seen in total is 398.
The sequence is:
2021-12-01 179
2021-12-05 81
2021-12-08 134
2021-12-09 4
The top 3 half hours with most cars:
2021-12-01T07:30:00 46
2021-12-01T08:00:00 42
2021-12-08T18:00:00 33
The continuous 1.5 hours period with least cars:
From 2021-12-01T05:00:00 to 2021-12-01T06:30:00, the least number of cars is 31.
```

## Test
Run the `unittest` unit tests with:
```
python3 test.py
```
You should see something like:
```
..[Errno 2] No such file or directory: 'data/testing'
No columns to parse from file
...
----------------------------------------------------------------------
Ran 5 tests in 0.010s

OK
```






# TrafficCounter
