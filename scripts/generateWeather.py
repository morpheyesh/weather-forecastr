#Markov implemetation to generate weather data

import numpy as np
import datetime
import time
import scipy.stats as st
import random as rm
from numpy import linalg as LA
import mockdata as md

#Define states (3 state spaces)
states = ['Sunny', 'Rain', 'Snow']
rang = ['High', 'Med', 'Low']

STARTDATE = "10-10-2011T12:00Z"

#define transition matrix
tMax = [[0.65, 0.28, 0.07],
        [0.15, 0.67, 0.18],
        [0.12, 0.36, 0.52]]

#observation matrix for temperature
oTMax = [[0.4, 0.5, 0.1],
        [0.5, 0.2, 0.3],
        [0.7, 0.1, 0.2]]

i = 0

#Need a initial state vector to do calculcations with tMax
sVec = [0.0, 0.9, 0.1]
stateVectors = {'Sunny': [0.55, 0.34, 0.11], 'Rain': [0.32, 0.49, 0.19], 'Snow': [0.09, 0.29, 0.62]}

LatlongMap = {'SYD': '-33.86,151.21', 'MAA':'13.08,80.27', 'ADL': '-34.92,138.62', 'MEL': '-37.83,144.98', 'SFO': '37.77,-122.41', 'NYC' : '40.71,-74.00',
              'PER':'-9.18,-75.01', 'TOR': '43.65,-79.38', 'BOM' : '19.07,72.87' , 'DEL' : '28.61,77.20' }
## With TPM and OB -> use single vector state -> use markov chain to get data.

'''
getElevation will return the elevation for a latitude and longitude
'''


def writeToFile(k, e, time, itState, t, h, p, target):
    singleLine = '{}|{}|{}|{}|{}|{}|{}\n'.format(k,e,time, itState, t, h, p)
    target.write(singleLine)

def primeInitData():
     start_date = STARTDATE
     initial_data = []
     for k in LatlongMap:
        #print k
        e = md.getElevation(LatlongMap[k])
        itState = rm.choice(states)
        t = md.getInitTemp(itState)
        h = md.getHumidity(itState)
        p = md.getPressure(itState)
        initial_data.append({'station': k, 'coordinates': e, 'date': start_date, 'state': itState, 'temperature': t, 'humidity': h, 'pressure': p})
     return initial_data

###
# For a given time period(days) - each station will generate weather data. A stochastic process
# Sample - SYD|-33.86,151.21,39|2015-12-23T05:02:12Z|Rain|+12.5|1004.3|97
####

def dateSeq(d, i):
     date_1 = datetime.datetime.strptime(d, "%m-%d-%YT%I:%MZ")
     end_date = date_1 + datetime.timedelta(days=i)
     return end_date.strftime("%m-%d-%YT%I:%MZ")

'''
This is the main function which generates the weather data
'''

def markovChain(stateVectors, tMax):
 init = primeInitData()
 target = open("weatherdata.txt", "w")

 for i in init:
  mx = np.matrix(stateVectors[i['state']]) #day0
  my = np.matrix(tMax)
  oy = np.matrix(oTMax)

  for j in range(10):
    tVal = mx * oy
    date = dateSeq(i['date'], j)
    day1 = states[np.argmax(mx)]
    mx = mx * my
    #print rang[np.argmax(tVal)]
    #temp = getTemp(rang[np.argmax(tVal)])
    temp = md.getTemperature(day1)
    humidity = md.getHumidity(day1)
    pressure = md.getPressure(day1)

    writeToFile(i['station'], i['coordinates'], date, day1, temp, pressure, humidity, target )
 target.close()

markovChain(stateVectors, tMax)


###Design approach: (Note: update after deadline of 6 hours - two evenings)####
#
#  Essentially we need to build a system that generates valid data. Valid data can be generated with satellite image
# to get the initial readings and using markov, we can get a chain of next state(s).
##
# 1. Get the satellite image of the earth
# 2. Split it into multiple grids each having one weather station(to keep things simple for now)
# 3. When new coordinates are given, it is converted into pixel and line with that determine the grid number and hence
# the weather station too.
# 4. With the pixel, line data, the elevation can be calculated from the image.
# 5. Using the satellite image reading of the temperature and relative humidity, pressure can be found(Fourier transformation? Need to figure how its done)
# 6. Now, with a given coords, the weather station that reads the data can be found, along with elevation and approx. t, h and p values
#   with a random state(depending on the temperature - it can't be sunny in antartica with 35C.(http://geog.uoregon.edu/envchange/clim_animations/flash/tmp2m.html) )
#
#
# Problem:  After n iterations, the state vector repeats. Use inhomogeneous markov chain, transition matrix varies?
# (http://mathoverflow.net/questions/168398/time-inhomogeneous-markov-chains)
#
#
