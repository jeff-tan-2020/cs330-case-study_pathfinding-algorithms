import math
import datetime
import random
def cooperative(x):
    return 1 - (1/(1+(10/x)**4))

def exponential(x, k):
    return 1-math.exp(-.693*x/k)



def geometric(p):
    #Based on the geometric probability distribution
    #P(X>10)=1−P(X<=10)=0.5
    #P(X=k)=(1−p)^k−1 * p
    #For the average number of rides each driver gives to be 10
    #The probability that a driver leaves is 0.0747997
    #Rounded to 7.5% chance
    return 1/p
    
def calculate(r, t, p):
    #bayesian algorithm that returns probability
    #based on number of rides given r. Higher r, then lower P(X)
    #current profit p. Low p, then higher P(x)
    #and total time on app t of driver. Higher t, then lower P(X)
    hrs = random.randint(9, 11)
    rds = random.randint(15, 20)
    pr = random.randint(4, 6)
    P_rides = exponential(r, rds)
    P_time = exponential(t, datetime.timedelta(hours=hrs))
    P_profit = exponential(t, datetime.timedelta(minutes=pr))
    if P_rides * P_time * P_profit  > random.uniform(0.15, 0.25):
        #if enough rides and or time, then driver leaves
        return 0
    else:
        return 1