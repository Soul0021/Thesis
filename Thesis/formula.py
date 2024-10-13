import math

def getEFactorCalculation(prevEF, q):
    return prevEF + 0.1 - (1 - q) * (0.08 + (1 - q) * 0.02)

def getIntervalCalculation(prevInterval, currEF):
    return prevInterval * currEF 

def getHalfLifeCalculation(currInterval, forgettingCurve, prevBase):
    return forgettingCurve + (prevBase * (currInterval - forgettingCurve))

def getTimeIntervalCalculation(currBase, probability):
    timeInterval = -currBase * math.log(probability)
    decimalPart, integerPart = math.modf(timeInterval)
    return {"newTimeInterval": timeInterval, "hour": integerPart, "minute": decimalPart * 60}

def systemArchitecture(q, prevEF, prevInterval, forgettingCurve, prevBase, probability):
    EFactor = getEFactorCalculation(prevEF=prevEF, q=q)
    interval = getIntervalCalculation(prevInterval=prevInterval, currEF=EFactor)
    halfLife = getHalfLifeCalculation(currInterval=interval, forgettingCurve=forgettingCurve, prevBase=prevBase)
    timeInterval = getTimeIntervalCalculation(currBase=halfLife, probability=probability)
    return {"newEFactor": EFactor, "newInterval": interval, "newHalfLife": halfLife, "newTimeInterval": timeInterval["newTimeInterval"], "hour": timeInterval["hour"], "minute": timeInterval["minute"]}

test = systemArchitecture(q=1, prevEF=0.5, prevInterval=1, forgettingCurve=2, prevBase=0.1, probability=0.8)

print(test)