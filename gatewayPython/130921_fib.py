sum = 0
for i in range(1000):
    if i%3 == 0 or i%5 == 0:
        sum += i
print(sum)

n1, n2 = 1, 1
fib = [1, 1]
n = int(input("Enter n: "))
dec = input("Would you like all terms or even terms (all/even)? ")

if dec == 'all':
    for i in range(1, n-1):
        n3 = n1 + n2
        fib.append(n3)
        n1, n2 = n2, n3
    print(fib)
elif dec == 'even':
    while len(fib) < n:
        n3 = n1 + n2
        n1, n2 = n2, n3
        if n3%2 != 0: continue
        else: fib.append(n3)
    print(fib)
