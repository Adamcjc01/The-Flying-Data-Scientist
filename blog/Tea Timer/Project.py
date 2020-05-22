import threading
import datetime
import math
import os

def DrinkRdy():
    #print place holder for optimum temp
    print("Tea is at optimum temp")
    os.system('spd-say "your tea is now at the optimal drinking temperature"')

def DrinkHot():
    #print place holder for optimum temp upper limit
    print("Tea is at the hottest drinkable temp")
    os.system('spd-say "Alert, Alert, your tea is now a drinkable temperature"')


def DrinkCold():
    #print place holder for optimum temp lower limit
    print("Tea is at the coldest drinkable temp")
    os.system('spd-say "crisis, crisis, tea is getting too cold"')

def CoolingCalc(T_initial, T_calc, T_ambient,a,h):
    c = 4184 #heat capacity
    k = h * a/c
    t = abs(math.log((T_calc - T_ambient)/(T_initial - T_ambient))/k)
    return t

def CoolingTimer(t,Lim):
    if Lim == 1: timer = threading.Timer(t, DrinkHot)
    elif Lim == 2: timer = threading.Timer(t, DrinkCold)
    else: timer = threading.Timer(t, DrinkRdy)
    timer.start()
    now = datetime.datetime.now()
    if Lim == 1: print("Your drink will be a drinkable temperature at time:")
    elif Lim == 2: print("Your drink will be cold at time:")
    else: print("Your drink will be a optimal temperature at time:")
    b = now + datetime.timedelta(0,t)
    print (b.strftime("%H:%M:%S"))

#initialise the inputs from the user
print("Starting")
print("What is the room temp?:")
T_ambient = int(input())

print("Are you making (1) Tea with milk (2) Black Coffee or (3) Green tea?")
typeOfTea = int(input())
if typeOfTea == 1:
    T_initial = 90
elif typeOfTea == 2:
    T_initial = 95
else:
    T_initial = 80

print("Do you like your drink (1) Hot or (2) Extra hot?")
Hotness = int(input())
if Hotness == 1:
    T_upper = 60
    T_lower = 45
else:
    T_upper = 65
    T_lower = 50

print("Are you using (1) mug, (2) paper cup or (3) flask?")
cupType = int(input())

if cupType == 1:
    a = 0.3
    h = 15
elif cupType == 2:
    a = 0.3
    h = 20
else:
    a= 0.4
    h=10

t1 = CoolingCalc(T_initial, T_upper, T_ambient, a,h)
t2 = CoolingCalc(T_initial, T_lower, T_ambient, a,h)
t3 = CoolingCalc(T_initial, ((T_upper-T_lower)/2 + T_lower), T_ambient, a,h)

CoolingTimer(t1,1)
CoolingTimer(t2,2)
CoolingTimer(t3,3)
