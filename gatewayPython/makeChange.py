while True:
    cash = float(input("Enter value in $: "))
    coins = cash*100
    type_coin = [25, 10, 5, 1]
    num_coin = []

    for i in type_coin:
        num_coin.append(coins // i)
        coins = coins%i
    print(num_coin[0], "quarters,", num_coin[1], "dimes,", num_coin[2], "nickels", num_coin[3], "pennies")
