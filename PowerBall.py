#!/us/bin/env python
#===========================================================================================================================
# Powerball Frequency  analyzer and quick pick
# basically a python re-write of https://github.com/toastyxen/Old_Perl_Projects/blob/master/lotto/pbhist00.pl
# with functionality of this https://github.com/toastyxen/Old_Perl_Projects/blob/master/lotto/powerballnew.pl
# Except powerball changed to 26 power ball numbers, as of April 2020 they used to do 35, while
# They increased the number of white balls from 59 to 69
# They also removed the winnums-text.txt and have a search fucntion, so we'll need to figure out how to get the history
# Author: Lloyd Turk Jr.
#===========================================================================================================================
# 

import random
import os
import urllib
import urllib.request as ur
import pandas as pd
import json
import time
from datetime import datetime
from collections import defaultdict

start_time = time.time()
system_random = random.SystemRandom
random.seed(system_random)

def get_drawing_history(): 
    url = "https://data.ny.gov/api/views/d6yy-54nr/rows.json" # It's on data.gov from NY
    response = ur.urlopen(url)
    json_data = json.loads(response.read())
    #print(json_data.keys())

    raw_data = json_data["data"]
    raw_list = [] #
    for x in raw_data:
        raw_list.extend((x[8], x[9]))
    
    chunked_data_list = []
    for x in range(0, len(raw_list), 2):
        chunk = raw_list[x:x + 2]
        chunked_data_list.append(chunk)
        
    final_data_list = []
    for x in chunked_data_list: # This works, it seems like it could still be more optimized though
        raw_date_time_str = x[0] # Raw date/time string from the json
        date_time_str = datetime.strptime(raw_date_time_str, "%Y-%m-%dT%H:%M:%S") # Cleaned up date/time string
        date_str = date_time_str.strftime("%Y-%m-%d") # Get rid of time part, we don't need it, I'm sure there is an easier/lighter way to do this, but this works for now
            
        final_data_list.append([date_str, x[1]])

    #print(final_data_list)
    return final_data_list
        
def white_balls(): # Get the 5 random numbers for the white balls
    nums = []
    count = 1
    while count <= 5: # we need 5 numbers
        pick = random.randint(1, 69) # From 1 to 69
        nums.append(pick) # Append them to the list
        count = count+1

    nums.sort() # Sort list for readability, and makes it easier when filling out the number slips 
    
    return nums # Return the list

# We also need the power ball
def power_ball(): # Get the random power ball "Red ball"
    pick = random.randint(1, 26)
    return pick

def frequency(): # There has to be a more effecient way to do this, this works for now though.
    data = get_drawing_history()
    
    #oldest_date = str(input("In put the oldest date in YYYY-MM-DD format: ")) # For custom date input
    oldest_date = "2020-04-08" # This is the latest rule change
    #oldest_date = "2010-02-03" # The oldest date the data set goes back to

    dates = pd.date_range(start=oldest_date, end=datetime.today()).to_pydatetime().tolist()
    
    date_list = []
    for dateTimeObj  in dates:
        date_str = dateTimeObj.strftime("%Y-%m-%d")
        date_list.append(date_str)

    ball_list = []
    for x in data:
        if x[0] in date_list:
            ball_list.append(x[1])

    split_list = []
    for x in ball_list:
        split = x.split()
        split_list.append(split)
    
    split_ball_list = []
    for i in split_list:
        for j in i:
            split_ball_list.append(j)
    
    pb_list = split_ball_list[5::6]

    del split_ball_list[5::6]

    white_ball_list = split_ball_list

    
    white_ball_list.sort()
    pb_list.sort()

    for i in range(0, len(white_ball_list)):
        white_ball_list[i] = int(white_ball_list[i])

    for i in range(0, len(pb_list)):
        pb_list[i] = int(pb_list[i])

    #unique_pb_list = list(set(pb_list))
    #unique_wb_list = list(set(white_ball_list))
    
    white_ball_dict = {i:white_ball_list.count(i) for i in white_ball_list}
    pb_dict = {i:pb_list.count(i) for i in pb_list}

    # Get powerball values and number of times they've been drawn
    #pb_all_values = pb_dict.values() # Get values from dict
    # Maximum value for PB
    pb_max_value = max(pb_dict.values()) # Find the most commonly drawn powerball number
    
    # Maximum secondary value for PB
    pb_max_secondary = 0
    for i in pb_dict.values(): # Find the second most commonly drawn powerball number
        if(i > pb_max_secondary and i < pb_max_value):
            pb_max_secondary = i

    print("========================================================================")
    print("All numbers drawn for PB with number of times drawn, in given date range")
    print("Number:Number of times drawn")
    print(pb_dict)
    #for key, value in pb_dict.items(): # Print all pb and number of times drawn
    #    print(str(key) + ":" + str(value))
    print("========================================================================")
    print("Most commonly drawn Powerball(s) since given date: ")
    print("Number:Number of times drawn")
    for key, value in pb_dict.items():
        if value == pb_max_value: # Print pb(s) with highest draw rate
            print(str(key) + ":" + str(value))
    print("========================================================================")
    print("Second most commonly drawn Powerball(s) since given date: ")
    print("Number:Number of times drawn")
    for key, value in pb_dict.items():
        if value == pb_max_secondary: # Print pb(s) with highest draw rate
            print(str(key) + ":" + str(value))
    print("========================================================================")

    # Get white ball values and number of times they've been drawn
    #wb_all_values = white_ball_dict.values()
    wb_max_value = max(white_ball_dict.values())
    # Maximum secondary value for PB
    wb_max_secondary = 0
    for i in white_ball_dict.values(): # Find the second most commonly drawn powerball number
        if(i > wb_max_secondary and i < wb_max_value):
            wb_max_secondary = i
    print("All numbers drawn with number of times drawn, in given date range")
    print("Number:Number of times drawn")
    print(white_ball_dict)
    #for key, value in white_ball_dict.items(): # Print all pb and number of times drawn
    #    print(str(key) + ":" + str(value))
    print("========================================================================")
    print("Most commonly drawn number(s) since given date: ")
    print("Number:Number of times drawn")
    for key, value in white_ball_dict.items():
        if value == wb_max_value: # Print wb(s) with highest draw rate
            print(str(key) + ":" + str(value))
    print("========================================================================")
    print("Second most commonly drawn number(s) since given date: ")
    print("Number:Number of times drawn")
    for key, value in white_ball_dict.items():
        if value == wb_max_secondary: # Print wb(s) with highest draw rate
            print(str(key) + ":" + str(value))
    print("========================================================================")
    


white_balls = white_balls()
power_ball = power_ball()
print("========================================================================")
print("Random quick pick numbers: " + str(white_balls) +" "+ str(power_ball))
#print("========================================================================")

frequency()

print('This program is just for frequency analysis and a "Quick Pick" random \nnumber generator making no pretense at predictive accuracy')

#print("--- %s seconds ---" % (time.time() - start_time)) # For debugging to make sure it didn't take an inexorpanant amount of time to run