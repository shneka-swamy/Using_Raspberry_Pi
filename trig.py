import math

def PolarToCartesian(radius, degrees):
    x = radius * math.cos(degrees)
    y = radius * math.sin(degrees)
    return (x, y)

def CartesianToPolar(x, y):
    radius = math.sqrt(pow(x,2)+pow(y,2))
    degrees = math.atan(y,x)
    return (radius, degrees)