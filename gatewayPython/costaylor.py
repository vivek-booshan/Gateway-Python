from math import dist
from random import random as rand
import numpy as np

n = int(input("Enter a # of trials n: "))
x, y = rand(), rand()
print(x, y)

def distance(x, y):
    dist = np.linalg.norm(x - y)
    return dist

print(distance(x, y))