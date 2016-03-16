import random
import geoproc as elevation




def getElevation(coords):
    ll = coords.split(",")
    return '{},{}'.format(coords, elevation.elevation_data(ll)[0][0]) ##call the geoproc class and get the value


def getInitTemp(s):
    if s == 'Sunny':
     return +39.5
    elif s == 'Rain':
     return 26.4
    else:
     return -4.9

def getTemperature(s):
    ##This is not how its done. This is terrible hack.
    if s == 'Snow':
       return '{}'.format(round(random.uniform(-1.0, -25.0), 2))
    elif s == 'Rain':
       return '+{}'.format(round(random.uniform(10.0, 30.0), 2))
    else:
        return '+{}'.format(round(random.uniform(25.0, 50.0), 2))

def getHumidity(s):
        if s == 'Snow':
           return '{}'.format(random.randrange(20, 55, 1))
        elif s == 'Rain':
           return '{}'.format(random.randrange(60, 90, 1))
        else:
            return '{}'.format(random.randrange(10, 30), 2)

def getPressure(s):
        if s == 'Snow':
           return '{}'.format(round(random.uniform(600.0, 1000.0), 2))
        elif s == 'Rain':
           return '{}'.format(round(random.uniform(1000.0, 1200.0), 2))
        else:
            return '{}'.format(round(random.uniform(1200.0, 1300.0), 2))
