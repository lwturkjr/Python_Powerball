#!/us/bin/env python
#===========================================================================================================================
# Powerball Frequency  analyzer and quick pick
# I will also see if we can also analyze hot/cold numbers
# basically a python re-write of https://github.com/toastyxen/Old_Perl_Projects/blob/master/lotto/pbhist00.pl
# with functionality of this https://github.com/toastyxen/Old_Perl_Projects/blob/master/lotto/powerballnew.pl
# Except powerball changed to 26 power ball numbers, as of April 2020 they used to do 35, while
# They increased the number of white balls from 59 to 69 (lol nice)
# They also removed the winnums-text.txt and have a search fucntion, so we'll need to figure out how to get the history
# Author: Lloyd Turk Jr.
#===========================================================================================================================
# 

import random
import os
import urllib
import urllib.request as ur
import json
from datetime import datetime


system_random = random.SystemRandom
random.seed(system_random)

def get_drawing_history(): 
    url = "https://data.ny.gov/api/views/d6yy-54nr/rows.json"
    response = ur.urlopen(url)
    data = json.loads(response.read())
    return data

get_drawing_history()

def white_balls(): # Get the 5 random numbers for the white balls
    nums = []
    count = 1
    while count <= 5: # we need 5 numbers
        pick = random.randint(1, 69) # From 1 to 69
        nums.append(pick) # Append them to the list
        count = count+1

    nums.sort()
    
    return nums # Return the list

# We also need the power ball

def power_ball(): # Get the random power ball "Red ball"
    pick = random.randint(1, 26)
    return pick

#white_balls = white_balls()
#power_ball = power_ball()

#print("Quick pick numbers: " + str(white_balls) +" "+ str(power_ball))


