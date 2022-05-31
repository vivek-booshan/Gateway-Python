import math

def isprime(n):
        if n%2 == 0: return False
        val = True
        for i in range(2, round(math.sqrt(n))+1):
            if i != 2 and i%2 == 0: continue
            elif n%i == 0: val = False
            elif n%i != 0: continue
        if val == False: print("not prime")
        else: print("prime")
n = int(input("Enter a value n: "))
print(isprime(n))