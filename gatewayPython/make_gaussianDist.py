import math as m
x = int(input("Enter parameter x: "))
mu = int(input("Enter parameter mu: "))
sigma = int(input("Enter parameter sigma: "))

def gauss(x, mu=0, sigma=1):
    coeff = 1 / (sigma * m.sqrt(2 * m.pi))
    exp = (-1/2) * ((x - mu) / sigma)**2
    dist = coeff * m.exp(exp)
    return dist

print(gauss(x, mu, sigma))