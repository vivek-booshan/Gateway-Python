from math import dist
from random import random as rand
import numpy as np

n = int(input("Enter a # of trials n: "))

n_circle = 0

def distance(x, y):
    distx = np.linalg.norm([x, y])
    return distx

for i in range(n):
    x, y = rand(), rand()
    if distance(x, y) <= 1: 
        n_circle += 1
    else: continue

estimate_pi = (4 * n_circle) / n
print(estimate_pi)