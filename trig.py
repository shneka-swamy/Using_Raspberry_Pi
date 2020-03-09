import math

def PolarToCartesian(radius, degrees):
    rad = (math.pi / 180) * degrees
    x = radius * math.cos(rad)
    y = radius * math.sin(rad)
    return (x, y)

def CartesianToPolar(x, y):
    radius = math.sqrt(pow(x,2)+pow(y,2))
    rad = math.atan(y,x)
    degrees = (180 / math.pi) * rad
    return (radius, degrees)