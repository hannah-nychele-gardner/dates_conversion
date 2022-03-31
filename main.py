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
    """Calculates the new date using the old date as an input. New date is expected to be three business days after 
    old date."""
    new_date = old_date  # dates start out as matching
    biz_days_elapsed = 0  # number of business days that have elapsed since old date
    while biz_days_elapsed != 3:  # for every business day that passes, biz_days_elapsed will increase until it is 3
        if new_date.weekday() >= 5 or new_date in business_holidays_2022_datetime:  # new date is not a business day
            new_date += timedelta(days=1)
        else:  # new date is a business day
            if biz_days_elapsed == 2 and new_date.weekday() == 4:  # ensures Wed old date has new date on Mon
                new_date += timedelta(days=3)
            else:
                new_date += timedelta(days=1)
            biz_days_elapsed += 1
    while new_date in business_holidays_2022_datetime:  # catches cases when old date + 3 business days is a holiday
        if new_date.weekday() == 4:  # moves Fri new date to the following Mon
            new_date += timedelta(days=3)
        else:  # moves new date to following business day
            new_date += timedelta(days=1)
    return new_date


# calculates the new date for each old date in the dataframe
new_dates = [calculate_new_date(value) for index, value in data[key_2].items()]
new_dates_series = pd.Series(new_dates)
# adds the new date to the dataframe
data['NEW_DATE'] = new_dates_series
# print(data)

# save dataframe as csv
# data.to_csv("dates_and_new_dates.csv", index=False)

""" This is how the dates_and_new_dates.csv looks:
ID,DATE,NEW_DATE
01,2022-01-04,2022-01-07
02,2022-01-05,2022-01-10
03,2022-01-06,2022-01-11
04,2022-01-07,2022-01-12
05,2022-01-10,2022-01-13
"""
