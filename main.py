import pandas as pd
from datetime import datetime, timedelta

""" Note: this is the format of the dates.txt file that I am cleaning in the following lines
   ;ID;DATE
1  ;01  ;20220104              
2  ;02  ;20220105              
3  ;03  ;20220106              
4  ;04  ;20220107              
5  ;05  ;20220110   
"""

# This takes the data from file, puts it into dictionaries with column names as keys
with open("dates.txt", "r") as f:
    lines = f.read().splitlines()
new_lines = []
for line in range(len(lines)):
    split_text = lines[line].split(";")
    new_lines.append(split_text)
# creates key names
key_1 = new_lines[0][1]
key_2 = new_lines[0][2]
lines_as_dicts = []
# puts values into a list of dictionaries and strips out trailing spaces
for line in range(1, len(new_lines)):
    value_1 = new_lines[line][1].strip()
    value_2 = datetime.strptime(new_lines[line][2].strip(), "%Y%m%d")
    new_dict = {key_1: value_1, key_2: value_2}
    lines_as_dicts.append(new_dict)
# takes the dictionaries and creates a dataframe
data = pd.DataFrame(lines_as_dicts)

# Creates a list of business holidays to be used in new date calculations
business_holidays_2022_string = ['2022-01-03', '2022-01-17', '2022-04-15', '2022-05-30', '2022-07-04', '2022-09-05',
                                 '2022-11-24', '2022-11-25', '2022-12-23', '2022-12-26']
business_holidays_2022_datetime = [datetime.strptime(date, '%Y-%m-%d') for date in business_holidays_2022_string]


# weekday() indexes: Monday = 0, Tuesday = 1, Wednesday = 2, Thursday = 3, Friday = 4, Saturday = 5, Sunday = 6
def calculate_new_date(old_date):
    """Calculates the new date using the old date as an input
    (new date is expected to be three business days after old date, so holidays and weekends must be skipped)"""
    if old_date.weekday() == 4:  # ensures if old date falls on a Friday, new date is the following Wednesday
        new_date = old_date + timedelta(days=5)
    else:
        new_date = old_date + timedelta(days=3)  # adds the standard 3 days to the old date to get the new date
    while new_date in business_holidays_2022_datetime:  # adds 1 day to the new date while new date falls on holiday
        new_date += timedelta(days=1)
    if new_date.weekday() == 5:  # moves new date from Saturday to the following Monday
        new_date += timedelta(days=2)
    elif new_date.weekday() == 6:  # moves new date from Sunday to the following Tuesday
        new_date += timedelta(days=2)
    return new_date


# calculates the new date for each old date in the dataframe
new_dates = [calculate_new_date(value) for index, value in data[key_2].items()]
new_dates_series = pd.Series(new_dates)
# adds the new date to the dataframe
data['NEW_DATE'] = new_dates_series
# print(data)

# save dataframe as csv
# data.to_csv("dates_and_new_dates.csv")

""" This is how the dates_and_new_dates.csv looks:
,ID,DATE,NEW_DATE
0,01,2022-01-04,2022-01-07
1,02,2022-01-05,2022-01-10
2,03,2022-01-06,2022-01-11
3,04,2022-01-07,2022-01-12
4,05,2022-01-10,2022-01-13
"""
